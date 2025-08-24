import matplotlib.pyplot as plt
from transformers import AutoTokenizer

# GPT-2 & BERT tokenizers
gpt_tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize_text(tokenizer, text: str):
    return tokenizer.tokenize(text)

def count_tokens(tokenizer, text: str):
    return len(tokenizer.encode(text))

def visualize_tokens(tokenizer, text: str, title="Token Distribution"):
    tokens = tokenizer.tokenize(text)
    lengths = [len(t) for t in tokens]
    plt.bar(range(len(tokens)), lengths)
    plt.xticks(range(len(tokens)), tokens, rotation=45)
    plt.ylabel("Token length (chars)")
    plt.title(title)
    plt.show()

def compare_tokenization(samples):
    results = []
    for s in samples:
        gpt_tokens = count_tokens(gpt_tokenizer, s)
        bert_tokens = count_tokens(bert_tokenizer, s)
        results.append((s, gpt_tokens, bert_tokens))
    return results
