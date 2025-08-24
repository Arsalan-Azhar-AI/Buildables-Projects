import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    f"utils/__init__.py",
    f"utils/llm_helpers.py",
    f"utils/tokenizer_helpers.py",
    f"data/sample_texts",
    f"data/results",
    f"tests/test_main.py",
    f"docs/usage_examples.md",
    "config.py",
    "requirements.txt",
    "README.md",
    "main.py",



]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)


    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    else:
        logging.info(f"{filename} is already exists")