import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGING_FACE_KEY")

LLAMA_MODEL = "llama3-8b-8192"   # Groq
MISTRAL_MODEL = "openai/gpt-oss-120b"  # HuggingFace
