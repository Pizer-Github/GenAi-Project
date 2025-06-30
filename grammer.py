import google.generativeai as genai
import os

try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    print("Please set the GEMINI_API_KEY environment variable.")
    print("You can get your API key from: https://aistudio.google.com/app/apikey")
    exit()

def check_grammar(text_to_check):
    model = genai.GenerativeModel('gemini-1.5-flash') 
    prompt = f"Correct the grammar and spelling in the following text:\n\n'{text_to_check}'\n\nProvide only the corrected text."

    try:
        response = model.generate_content(prompt)
        corrected_text = response.text.strip()
        return corrected_text
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    while True:
        user_input = input("Enter text to grammar check (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break

        if user_input:
            corrected = check_grammar(user_input)
            print(f"\nOriginal: {user_input}")
            print(f"Corrected: {corrected}\n")
        else:
            print("Please enter some text.")