from groq import Groq
from typing import Any, Dict, List, Optional
import time
import logging
from .config import get_api_key


logger = logging.getLogger(__name__)


class GroqClientWrapper:
    """Simple wrapper to centralize Groq calls and retries."""


    def __init__(self, api_key: Optional[str] = None, model: str = None):
        self.api_key = api_key or get_api_key()
        self.model = model
        self.client = Groq(api_key=self.api_key)


    def chat(self,
    messages: List[Dict[str, str]],
    temperature: float = 0.0,
    max_tokens: int = 300,
    response_format: Optional[Dict[str, Any]] = None,
    retries: int = 3,
    backoff: float = 1.0,
    ) -> Dict[str, Any]:
        """Call Groq chat completions with a simple retry/backoff.


        Returns the raw `choices[0].message` dict (or raises).
        """
        for attempt in range(1, retries + 1):
            try:
                params = dict(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                )
                if response_format is not None:
                    params["response_format"] = response_format


                response = self.client.chat.completions.create(**params)
                return response.choices[0].message

            except Exception as e:
                logger.warning(f"Groq call failed (attempt {attempt}/{retries}): {e}")
                if attempt == retries:
                    raise
                time.sleep(backoff * attempt)