from transformers import PegasusForConditionalGeneration, PegasusTokenizer
model_name = 'tuner007/pegasus_paraphrase'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

def paraphrase_text_pegasus(text, num_return_sequences=1, num_beams=5):
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    output = model.generate(
        input_ids,
        max_length=256,
        num_beams=num_beams,
        num_return_sequences=num_return_sequences,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    paraphrased_texts = [tokenizer.decode(ids, skip_special_tokens=True) for ids in output]
    return paraphrased_texts
input_text = input ("Enter Text: ")
paraphrase = paraphrase_text_pegasus(input_text)

print(f"Original Text: {input_text}\n")
print("Paraphrase:")
for p in enumerate(paraphrase):
    print(p)

