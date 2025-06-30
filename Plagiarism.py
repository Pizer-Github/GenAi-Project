import nltk
nltk.download('punkt')

import wikipedia
from nltk.tokenize import sent_tokenize
import re
from collections import defaultdict

def normalize_sentence(sentence):

    normalized = sentence.lower()
    normalized = re.sub(r'\s+', ' ', normalized)
    normalized = normalized.strip()
    return normalized

def get_sentences_from_text(text):

    sentences = sent_tokenize(text)
    return [normalize_sentence(s) for s in sentences if s.strip()]

def search_wikipedia_for_exact_text(user_input_sentence, max_results=5):

    normalized_user_sentence = normalize_sentence(user_input_sentence)
    found_in_pages = []

    print(f"\nSearching Wikipedia for: '{user_input_sentence}'")

    search_query = f'"{user_input_sentence}"' 
    try:
        search_results = wikipedia.search(search_query, results=max_results)
        if not search_results:

            search_results = wikipedia.search(user_input_sentence, results=max_results)

        if not search_results:
            print("No relevant Wikipedia pages found for the search query.")
            return {}

        print(f"Found potential Wikipedia pages: {search_results}")

        for page_title in search_results:
            try:
                page = wikipedia.page(page_title, auto_suggest=False)
                page_content = page.content
                
                wiki_sentences = get_sentences_from_text(page_content)

                if normalized_user_sentence in wiki_sentences:
                    found_in_pages.append(page_title)

            except wikipedia.exceptions.DisambiguationError as e:
                print(f"  '{page_title}' is a disambiguation page. Trying first option: {e.options[0]}")

                try:
                    page = wikipedia.page(e.options[0], auto_suggest=False)
                    page_content = page.content
                    wiki_sentences = get_sentences_from_text(page_content)
                    if normalized_user_sentence in wiki_sentences:
                        found_in_pages.append(e.options[0])
                except wikipedia.exceptions.PageError:
                    print(f"    Could not retrieve content for '{e.options[0]}'.")
                except Exception as ex:
                    print(f"    An error occurred while processing disambiguation option: {ex}")

            except wikipedia.exceptions.PageError:
                print(f"  Could not retrieve content for '{page_title}' (page does not exist or is malformed).")
            except Exception as e:
                print(f"  An unexpected error occurred while processing page '{page_title}': {e}")

    except wikipedia.exceptions.HTTPTimeoutError:
        print("Wikipedia API request timed out. Please try again.")
        return {}
    except Exception as e:
        print(f"An error occurred during Wikipedia search: {e}")
        return {}

    results = {}
    if found_in_pages:
        results[normalized_user_sentence] = list(set(found_in_pages))
    return results


if __name__ == "__main__":
    while True:
        user_input = input("\nEnter a short sentence to search on Wikipedia (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break

        if not user_input.strip():
            print("Please enter some text.")
            continue

        plagiarism_results = search_wikipedia_for_exact_text(user_input)

        if plagiarism_results:
            print("\nExact match found on Wikipedia:")
            for sentence, sources in plagiarism_results.items():
                print(f"  Sentence: '{sentence}'")
                print(f"    Found in Wikipedia Pages: {', '.join(sources)}")
        else:
            print("\nNo exact match found on Wikipedia for that sentence.")

    print("Exiting plagiarism detection.")