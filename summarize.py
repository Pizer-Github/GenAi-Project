   
import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()



try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    print("Please ensure you have set the GEMINI_API_KEY environment variable in your .env file.")
    exit()


def list_gemini_models():
    """Lists all available Gemini models and their capabilities."""
    """print("\n--- Available Gemini Models ---")
    found_generate_content_models = False
    for m in genai.list_models():

        if 'generateContent' in m.supported_generation_methods:
            print(f"Name: {m.name}")
            print(f"  Display Name: {m.display_name}")
            print(f"  Description: {m.description}")
            print(f"  Input Token Limit: {m.input_token_limit}")
            print(f"  Output Token Limit: {m.output_token_limit}")
            print(f"  Supported Methods: {m.supported_generation_methods}")
            print("-" * 30)
            found_generate_content_models = True
    if not found_generate_content_models:
        print("No models found that support 'generateContent'. This might indicate an API key issue or regional restriction.")"""


def summarize_text(text, model_name="gemini-pro", max_output_tokens=200):

    if not text.strip():
        return "Error: Input text cannot be empty."

    try:
        model = genai.GenerativeModel(model_name)
        

        prompt = f"Summarize the following text concisely and accurately:\n\n{text}\n\nSummary:"


        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens,
                temperature=0.7
            )
        )
        

        if response.candidates and hasattr(response.candidates[0], 'text'):
            return response.candidates[0].text
        else:
            return "Error: Could not generate a summary. The model might have blocked the response due to safety concerns or generated no text."

    except Exception as e:
        return f"An error occurred during summarization: {e}"

if __name__ == "__main__":
    list_gemini_models()
    print("--- Gemini API Text Summarizer ---")
    print("Enter the text you want to summarize (type 'END' on a new line to finish):")

    user_input_lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        user_input_lines.append(line)

    input_text = "\n".join(user_input_lines)

    if input_text.strip():
        print("\nSummarizing...")
        summary = summarize_text(input_text, model_name="gemini-2.5-pro")
        print("\n--- Summary ---")
        print(summary)
    else:
        print("No text provided for summarization.")