from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key,)
class ChatImplementation:
  def __init__(self,client):
    self.client = client

  def summarize_article(article, temperature=0.7):
    response = self.client.chat.completions.create(
        model="llama3-8b-8192",  # you can also use "gpt-4o" or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes articles."},
            {"role": "user", "content": f"Summarize this article in 3-4 sentences:\n\n{article}"}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content

article_text = """
[PASTE YOUR NEWS ARTICLE CONTENT HERE]
"""

print("🔹 Original Article Length:", len(article_text.split()), "words\n")

sumarize=ChatImplementation(client)

# Summaries with different temperatures
for temp in [0.1, 0.7, 1.0]:
    print(f"\n--- Summary with temperature={temp} ---")
    print(sumarize.summarize_article(article_text, temperature=temp))


# ---------- PART 2: INTERACTIVE Q&A ----------
print("\n========== Q&A Section ==========\n")
questions = [
    "What is the main issue discussed in the article?",
    "Who are the key people or organizations involved?",
    "What future impact could this have?"
]

for q in questions:
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions about news articles."},
            {"role": "user", "content": f"Based on the article below, {q}\n\nArticle:\n{article_text}"}
        ],
        temperature=0.5
    )
    print(f"Q: {q}")
    print("A:", response.choices[0].message.content, "\n")

