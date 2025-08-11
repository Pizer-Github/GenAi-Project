# backend/plagiarism.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def check_plagiarism(input_text, reference_texts):
    """
    Check for plagiarism by comparing input text with reference texts
    using TF-IDF vectorization and cosine similarity.
    
    Args:
        input_text (str): Text to check for plagiarism
        reference_texts (list): List of reference texts to compare against
    
    Returns:
        dict: Plagiarism analysis results
    """
    if not reference_texts:
        return {
            "plagiarism_detected": False,
            "max_similarity": 0.0,
            "similarity_scores": [],
            "message": "No reference texts provided for comparison."
        }
    
    # Combine input text with reference texts for vectorization
    all_texts = [input_text] + reference_texts
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),  # Use unigrams and bigrams
        max_features=1000
    )
    
    try:
        # Fit and transform all texts
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # Calculate cosine similarities between input text and each reference text
        input_vector = tfidf_matrix[0]  # First vector is input text
        reference_vectors = tfidf_matrix[1:]  # Rest are reference texts
        
        similarities = cosine_similarity(input_vector, reference_vectors).flatten()
        
        # Convert to regular Python floats for JSON serialization
        similarity_scores = [float(score) for score in similarities]
        max_similarity = float(max(similarities))
        
        # Determine if plagiarism is detected (threshold: 0.3)
        plagiarism_threshold = 0.3
        plagiarism_detected = max_similarity > plagiarism_threshold
        
        # Create result message
        if plagiarism_detected:
            message = f"Potential plagiarism detected! Maximum similarity: {max_similarity:.2%}"
        else:
            message = f"No significant plagiarism detected. Maximum similarity: {max_similarity:.2%}"
        
        return {
            "plagiarism_detected": plagiarism_detected,
            "max_similarity": max_similarity,
            "similarity_scores": similarity_scores,
            "threshold": plagiarism_threshold,
            "message": message
        }
        
    except Exception as e:
        return {
            "plagiarism_detected": False,
            "max_similarity": 0.0,
            "similarity_scores": [],
            "error": f"Error during plagiarism check: {str(e)}",
            "message": "Unable to perform plagiarism check due to an error."
        }
