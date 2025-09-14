"""Run experiments and generate report."""
import argparse
import json
import logging
import random
import statistics
from pathlib import Path
from typing import Any, Dict, List, Optional

from .llm_client import GroqClientWrapper
from .prompts import zero_shot_prompt, few_shot_prompt, cot_prompt
from .grader import grade_score
from .config import DEFAULT_MODEL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

random.seed(0)  # reproducible few-shot choices


def load_dataset(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _extract_content(resp_msg: Any) -> str:
    """
    Unified extractor for the wrapper response object/dict.
    Returns a string (strips whitespace) or JSON-stringified content for non-strings.
    """
    content = None
    # Groq wrapper returns an object with .content in our helper
    if hasattr(resp_msg, "content"):
        content = resp_msg.content
    elif isinstance(resp_msg, dict):
        # maybe {'content': ...}
        content = resp_msg.get("content", resp_msg)
    else:
        content = resp_msg

    if content is None:
        return ""
    if isinstance(content, str):
        return content.strip()
    # if content is structured (dict/list), stringify it so it's JSON-safe in results
    try:
        return json.dumps(content, ensure_ascii=False)
    except Exception:
        return str(content)


def run_experiment(
    dataset_path: Path,
    outdir: Path,
    model: str = DEFAULT_MODEL,
    max_items: Optional[int] = None,
    save_every: int = 10,
):
    outdir.mkdir(parents=True, exist_ok=True)
    dataset = load_dataset(dataset_path)
    client = GroqClientWrapper(model=model)

    results: List[Dict[str, Any]] = []
    scores: List[Dict[str, Any]] = []

    items = dataset if max_items is None else dataset[:max_items]

    for idx, item in enumerate(items, start=1):
        puzzle = item.get("puzzle", "")
        expected = item.get("expected_answer", "")

        logger.info(f"[{idx}/{len(items)}] Running puzzle id={item.get('id', idx)}")

        try:
            # zero-shot
            zs_prompt = zero_shot_prompt(puzzle)
            zs_msg = [{"role": "user", "content": zs_prompt}]
            zs_resp_msg = client.chat(messages=zs_msg, temperature=0.0, max_tokens=200)
            zs_output = _extract_content(zs_resp_msg)

            # few-shot
            fs_prompt = few_shot_prompt(puzzle, dataset, num_examples=2)
            fs_msg = [{"role": "user", "content": fs_prompt}]
            fs_resp_msg = client.chat(messages=fs_msg, temperature=0.0, max_tokens=300)
            fs_output = _extract_content(fs_resp_msg)

            # CoT
            cot_prompt_txt = cot_prompt(puzzle)
            cot_msg = [{"role": "user", "content": cot_prompt_txt}]
            cot_resp_msg = client.chat(messages=cot_msg, temperature=0.0, max_tokens=400)
            cot_output = _extract_content(cot_resp_msg)

            results.append(
                {
                    "id": item.get("id", idx),
                    "puzzle": puzzle,
                    "expected": expected,
                    "prompts": {
                        "zero_shot": zs_prompt,
                        "few_shot": fs_prompt,
                        "cot": cot_prompt_txt,
                    },
                    "outputs": {
                        "zero_shot": zs_output,
                        "few_shot": fs_output,
                        "cot": cot_output,
                    },
                }
            )

            # grading (with safe model_dump/dict fallback)
            try:
                zs_grade = grade_score(client, puzzle, expected, zs_output)
                zs_grade_dict = zs_grade.model_dump()  # pydantic v2
            except AttributeError:
                zs_grade_dict = zs_grade.dict()

            try:
                fs_grade = grade_score(client, puzzle, expected, fs_output)
                fs_grade_dict = fs_grade.model_dump()
            except AttributeError:
                fs_grade_dict = fs_grade.dict()

            try:
                cot_grade = grade_score(client, puzzle, expected, cot_output)
                cot_grade_dict = cot_grade.model_dump()
            except AttributeError:
                cot_grade_dict = cot_grade.dict()

            scores.append(
                {
                    "id": item.get("id", idx),
                    "correct": expected,
                    "zero_shot_grade": zs_grade_dict,
                    "few_shot_grade": fs_grade_dict,
                    "cot_grade": cot_grade_dict,
                }
            )

        except Exception as e:
            logger.exception(f"Error processing item id={item.get('id', idx)}: {e}")
            # append a placeholder so indices remain consistent
            results.append(
                {
                    "id": item.get("id", idx),
                    "puzzle": puzzle,
                    "expected": expected,
                    "prompts": {},
                    "outputs": {"zero_shot": "", "few_shot": "", "cot": ""},
                    "error": str(e),
                }
            )
            scores.append(
                {
                    "id": item.get("id", idx),
                    "correct": expected,
                    "zero_shot_grade": None,
                    "few_shot_grade": None,
                    "cot_grade": None,
                }
            )

        # periodic save
        if idx % save_every == 0:
            with open(outdir / "results.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            with open(outdir / "scores.json", "w", encoding="utf-8") as f:
                json.dump(scores, f, indent=2, ensure_ascii=False)

    # final save
    with open(outdir / "results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    with open(outdir / "scores.json", "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2, ensure_ascii=False)

    # generate a comparative report
    generate_report(results, scores, outdir)
    logger.info("Experiment finished.")


def generate_report(results: List[Dict[str, Any]], scores: List[Dict[str, Any]], outdir: Path):
    # compute averages per metric and per strategy
    metrics = ["correctness", "clarity", "completeness", "conciseness"]
    strat_keys = ["zero_shot_grade", "few_shot_grade", "cot_grade"]

    def mean_for(metric_name: str, strat_key: str) -> Optional[float]:
        vals = []
        for s in scores:
            strat = s.get(strat_key)
            if strat and isinstance(strat, dict):
                v = strat.get(metric_name)
                if isinstance(v, (int, float)):
                    vals.append(v)
        if not vals:
            return None
        return round(statistics.mean(vals), 3)

    lines = ["# Experiment Report", ""]
    lines.append("## Summary metrics")
    for m in metrics:
        mvals = {k: mean_for(m, k) for k in strat_keys}
        lines.append(f"- **{m}**: zero_shot={mvals['zero_shot_grade']}, few_shot={mvals['few_shot_grade']}, cot={mvals['cot_grade']}")

    # best strategy by mean correctness
    mean_corrects = {k: mean_for("correctness", k) or 0.0 for k in strat_keys}
    best_strat_key = max(mean_corrects.items(), key=lambda x: x[1])[0]
    best_name = {"zero_shot_grade": "Zero-shot", "few_shot_grade": "Few-shot", "cot_grade": "CoT"}[best_strat_key]
    lines.append("")
    lines.append(f"## Comparative insights")
    lines.append(f"Overall best strategy by mean correctness: **{best_name}** (score {mean_corrects[best_strat_key]:.3f})")

    # per-item table (first 50)
    lines.append("")
    lines.append("## Per-item results (first 50 shown)")
    lines.append("| id | puzzle | expected | zero_shot | few_shot | cot |")
    lines.append("|---|---|---|---|---|---|")
    for r in results[:50]:
        puzzle_short = (r.get("puzzle") or "")[:60].replace("|", " ")
        expected = r.get("expected", "")
        zs = (r.get("outputs", {}).get("zero_shot") or "")[:40].replace("|", " ")
        fs = (r.get("outputs", {}).get("few_shot") or "")[:40].replace("|", " ")
        cot = (r.get("outputs", {}).get("cot") or "")[:40].replace("|", " ")
        lines.append(f"| {r.get('id')} | {puzzle_short} | {expected} | {zs} | {fs} | {cot} |")

    with open(outdir / "report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    logger.info(f"Report written to {outdir / 'report.md'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True, help="Path to dataset JSON")
    parser.add_argument("--outdir", required=True, help="Directory for outputs")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="LLM model to call")
    parser.add_argument("--max-items", type=int, default=None, help="Limit number of items")
    args = parser.parse_args()

    run_experiment(Path(args.dataset), Path(args.outdir), model=args.model, max_items=args.max_items)
