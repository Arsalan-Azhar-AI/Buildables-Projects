from pathlib import Path
from dotenv import load_dotenv
import os


load_dotenv()


def get_api_key() -> str:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise EnvironmentError(
        "GROQ_API_KEY not found. Create a .env file or set environment variable GROQ_API_KEY"
        )
    return key




DEFAULT_MODEL = "llama-3.3-70b-versatile"