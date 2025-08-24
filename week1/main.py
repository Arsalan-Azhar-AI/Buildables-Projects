import gradio as gr
from utils.llm_helpers import summarize_with_llama, summarize_with_mistral, sentiment_analysis, text_statistics
from utils.tokenizer_helpers import compare_tokenization

def analyze_text(text):
    llama = summarize_with_llama(text)
    mistral = summarize_with_mistral(text)
    sentiment = sentiment_analysis(text)
    stats = text_statistics(text)
    return llama, mistral, sentiment, stats

iface = gr.Interface(
    fn=analyze_text,
    inputs=gr.Textbox(lines=10, placeholder="Enter text here..."),
    outputs=[
        gr.JSON(label="Llama 3 Summary"),
        gr.JSON(label="Mistral Summary"),
        gr.JSON(label="Sentiment"),
        gr.JSON(label="Text Stats"),
    ],
    title="Text Analysis Tool",
    description="Summarization, Sentiment, Tokenization & Statistics"
)

if __name__ == "__main__":
    iface.launch()
