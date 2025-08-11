# backend/summarizer.py

from transformers import pipeline

summarizer_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")

def summarize_text(text):
    prompt = f"Summarize this text: {text}"
    result = summarizer_pipeline(prompt, max_length=150, min_length=40, do_sample=False)[0]['generated_text']
    return result
