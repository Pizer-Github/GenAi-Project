# backend/paraphraser.py

from transformers import pipeline

paraphrase_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")

def paraphrase_text(text):
    prompt = f"Paraphrase this text: {text}"
    result = paraphrase_pipeline(prompt, max_length=256, num_return_sequences=1)[0]['generated_text']
    return result
