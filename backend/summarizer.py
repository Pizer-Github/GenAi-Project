# backend/summarizer.py

from transformers import pipeline

summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    result = summarizer_pipeline(text, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
    return result
