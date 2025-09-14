
# 🧩 AI Prompting Assignment – Zero-Shot, Few-Shot, and Chain-of-Thought

## 📌 Overview

This project explores **prompting strategies** for Large Language Models (LLMs) by testing them on a dataset of logic puzzles.
We compare **Zero-Shot**, **Few-Shot**, and **Chain-of-Thought (CoT)** prompting, then grade each strategy using an automatic grader.
Finally, a summary report is generated to highlight which prompting method performs best.

---

## 📂 Project Structure

```
.
├── resources/
│   └── datasets/
│       └── logic-puzzles.json     # Input dataset
├── src/
│   └── ai_prompting/
│       ├── __init__.py
│       ├── config.py              # Default model settings
│       ├── llm_client.py          # Groq API wrapper
│       ├── prompts.py             # Prompt builders (Zero/Few-Shot/CoT)
│       ├── grader.py              # Automatic scoring of responses
│       └── run.py                 # Main experiment runner
├── outputs/                       # Generated results & reports
├── requirements.txt
├── .env                           # API key stored here (not shared)
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone & enter project folder

```bash
git clone https://github.com/Arsalan-Azhar-AI/Buildables-Projects.git
cd week3
```

### 2. Create a virtual environment

```bash
python -m venv .venv
# Activate it:
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_api_key_here
```

---

## 🚀 Running Experiments

Run the script with your dataset and an output folder:

```bash
python -m ai_prompting.run \
  --dataset resources/datasets/logic-puzzles.json \
  --outdir outputs/logic \
  --max-items 10
```

* `--dataset`: Path to input dataset JSON
* `--outdir`: Output folder (will be created if missing)
* `--max-items`: Limit to N items for quick tests (optional)

---

## 📊 Outputs

After running, you’ll find:

* `outputs/logic/results.json` → All model responses
* `outputs/logic/scores.json` → Grading results
* `outputs/logic/report.md` → Human-readable summary report

---

## 📝 Report Structure

The generated report includes:

* **Average scores** (correctness, clarity, completeness, conciseness)
* **Comparative insights** (which strategy performed best)
* **Per-item table** (first 50 puzzles with outputs)

Example insight from report:

```
Overall best strategy by mean correctness: Chain-of-Thought (CoT)
```
