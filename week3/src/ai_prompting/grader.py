from pydantic import BaseModel, Field
import json
from typing import Dict, Any
from .llm_client import GroqClientWrapper

class AnswerQuality(BaseModel):
    correctness: int = Field(description="0..3")
    clarity: int = Field(description="0..3")
    completeness: int = Field(description="0..3")
    conciseness: int = Field(description="0..3")

GRADER_SYSTEM_PROMPT = """
You are a strict grader. Compare Model Response to Expected Answer.
Return ONLY a JSON object with integer fields correctness, clarity, completeness, conciseness (0..3).
Rules:
- correctness: 3 exact, 2 mostly correct, 1 partial, 0 wrong.
- If no step-by-step text present, set clarity <=1 and completeness <=1.
- Return nothing but the JSON.
"""

def grade_score(client: GroqClientWrapper, puzzle: str, expected: str, model_output: str) -> AnswerQuality:
    messages = [
    {"role": "system", "content": GRADER_SYSTEM_PROMPT},
    {"role": "user", "content": f"Puzzle: {puzzle}\nExpected Answer: {expected}\nModel Response: {model_output}\n"},
    ]

    try:
        msg = client.chat(messages=messages, response_format={"type": "json_object"}, max_tokens=300)
        content = msg.content
        # content may be dict already depending on wrapper
        if isinstance(content, dict):
            parsed = content
        else:
            parsed = json.loads(content)

    except Exception as e:
        # fallback: conservative default
        parsed = {"correctness": 0, "clarity": 0, "completeness": 0, "conciseness": 0}


        return AnswerQuality(**parsed)