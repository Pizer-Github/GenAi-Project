# backend/grammar.py

from transformers import pipeline

grammar_pipeline = pipeline("text2text-generation", model="vennify/t5-base-grammar-correction")

def correct_grammar(text):
    result = grammar_pipeline(text, max_length=256)[0]['generated_text']
    return result
