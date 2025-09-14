
# 📰 AI News Summarizer & Q\&A Tool

## 📌 Overview

This project is a **Python-based AI tool** that:

1. Summarizes a news article into 3–4 sentences.
2. Lets you ask **interactive questions** about the article.
3. Experiments with **LLM parameters (temperature)** to see how summaries change.

It uses the **Groq API** (you can also adapt it for Gemini or other LLMs).

---

## ⚙️ Features

* Summarizes long articles in seconds.
* Q\&A mode: ask at least 3 questions about the article.
* Tests three different **temperature values**:

  * `0.1` → deterministic, factual
  * `0.7` → balanced, natural
  * `1.0` → creative, fun

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git https://github.com/Arsalan-Azhar-AI/Buildables-Projects.git
cd week4
```

### 2. Install dependencies

Make sure you have **Python 3.8+** installed, then:

```bash
pip install groq
```

### 3. Set your API key

Export your Groq API key as an environment variable:

```bash
export GROQ_API_KEY="your_api_key_here"
```

(Windows PowerShell)

```powershell
setx GROQ_API_KEY "your_api_key_here"
```

---

## 🚀 How to Run

### 1. Add your article

Open `summarizer.py` and paste your news article text in the `article_text` variable.

### 2. Run the script

```bash
python summarizer.py
```

### 3. Example Output

* Original article length (in words).
* Three summaries (different temperatures).
* Q\&A session with at least 3 answers.

---

## 📂 Project Structure

```
📁 week4
 ┣ 📄 summarizer.py       # Main script
 ┣ 📄 observations.md     # Notes on parameter tuning
 ┗ 📄 README.md           # Project documentation
```

---

## 📊 Observations

See observations.md for notes on how temperature affects summaries.

---
