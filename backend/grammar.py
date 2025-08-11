# backend/grammar.py

from transformers import pipeline

grammar_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")

def correct_grammar(text):
    prompt = f"Fix the grammar in this text: {text}"
    result = grammar_pipeline(prompt, max_length=256)[0]['generated_text']
    return result
