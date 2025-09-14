from typing import List, Dict
import random

def zero_shot_prompt(puzzle: str) -> str:
    return (
    "Answer only with the final single-word/single-line answer. No explanation, no extra text.\n"
    f"Puzzle: {puzzle}"
    )

def few_shot_prompt(puzzle: str, dataset: List[Dict], num_examples: int = 2) -> str:
    """Construct a few-shot prompt using `num_examples` examples from dataset (excluding the current puzzle)."""
    examples = []
    # choose up to num_examples random other items
    candidates = [d for d in dataset if d.get("puzzle") != puzzle and d.get("expected_answer")]
    if not candidates:
        chosen = []
    else:
        chosen = random.sample(candidates, min(len(candidates), num_examples))


    prompt = "Solve the puzzle. I will give you examples:\n\n"
    for ex in chosen:
        prompt += f"Q: {ex['puzzle']}\nA: {ex['expected_answer']}\n\n"


    prompt += f"Now solve this puzzle:\nQ: {puzzle}\nA:"
    return prompt

def cot_prompt(puzzle: str) -> str:
    return (
    "Explain step-by-step. Use numbered steps (Step 1:, Step 2:) and end with 'Answer: <final>'.\n"
    f"Puzzle: {puzzle}"
    )

