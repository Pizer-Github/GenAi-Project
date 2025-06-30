# backend/paraphraser.py

from transformers import pipeline

paraphrase_pipeline = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")

def paraphrase_text(text):
    result = paraphrase_pipeline(text, max_length=256, num_return_sequences=1)[0]['generated_text']
    return result
