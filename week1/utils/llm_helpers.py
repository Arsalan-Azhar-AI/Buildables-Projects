import requests, time, re
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from config import GROQ_API_KEY, HUGGINGFACE_API_KEY, LLAMA_MODEL, MISTRAL_MODEL

def estimate_cost(tokens: int, price_per_1k=0.0):
    return (tokens or 0) / 1000 * price_per_1k


def summarize_with_llama(text: str, retries=3, backoff=2) -> dict:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": LLAMA_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize this:\n{text}"}
        ],
        "temperature": 0.5,
        "max_tokens": 300,
    }
    for attempt in range(1, retries+1):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            summary = data["choices"][0]["message"]["content"]
            tokens = data.get("usage", {}).get("total_tokens", 0)
            return {"summary": summary, "tokens": tokens, "cost": estimate_cost(tokens)}
        except Exception as e:
            if attempt < retries:
                time.sleep(backoff ** attempt)
            else:
                return {"summary": f"Error: {str(e)}", "tokens": 0, "cost": 0}



def summarize_with_mistral(text: str) -> dict:
    try:
        tokenizer = AutoTokenizer.from_pretrained(MISTRAL_MODEL, use_auth_token=HUGGINGFACE_API_KEY)
        model = AutoModelForCausalLM.from_pretrained(MISTRAL_MODEL, use_auth_token=HUGGINGFACE_API_KEY)
        summarizer = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=200)
        prompt = f"Summarize this text concisely:\n\n{text}\n\nSummary:"
        output = summarizer(prompt)[0]["generated_text"]
        tokens = len(tokenizer.encode(text))
        return {"summary": output, "tokens": tokens, "cost": estimate_cost(tokens)}
    except Exception as e:
        return {"summary": f"Error: {str(e)}", "tokens": 0, "cost": 0}


def sentiment_analysis(text: str) -> dict:
    sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    return sentiment_model(text)[0]


from collections import Counter
import nltk
nltk.download("punkt")
from nltk.tokenize import word_tokenize

def text_statistics(text: str):
    words = word_tokenize(text.lower())
    freq = Counter(words)
    total_words = len(words)
    unique_words = len(freq)
    return {
        "total_words": total_words,
        "unique_words": unique_words,
        "most_common": freq.most_common(10),
    }
