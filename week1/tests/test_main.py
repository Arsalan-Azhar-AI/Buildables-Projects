from utils.llm_helpers import summarize_with_llama, summarize_with_mistral

def test_llama_summary():
    text = "AI is transforming industries."
    result = summarize_with_llama(text)
    assert "summary" in result

def test_mistral_summary():
    text = "AI is transforming industries."
    result = summarize_with_mistral(text)
    assert "summary" in result
