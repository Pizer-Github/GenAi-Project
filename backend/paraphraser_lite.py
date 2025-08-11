# Memory-optimized paraphraser using lightweight model
import os
import gc
from transformers import pipeline

# Global variable for lazy loading
_paraphrase_pipeline = None

def get_paraphrase_pipeline():
    """Lazy load paraphrase pipeline to save memory"""
    global _paraphrase_pipeline
    if _paraphrase_pipeline is None:
        # Use an even smaller model to fit in 512MB
        _paraphrase_pipeline = pipeline(
            "text2text-generation", 
            model="t5-small",  # Smaller than flan-t5-small
            device_map="auto" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu",
            torch_dtype="float16" if os.environ.get("CUDA_VISIBLE_DEVICES") else None
        )
        # Force garbage collection
        gc.collect()
    return _paraphrase_pipeline

def paraphrase_text(text):
    """Paraphrase text with memory optimization"""
    if len(text.strip()) == 0:
        return text
    
    # Limit text length to prevent memory issues
    if len(text) > 1000:
        text = text[:1000] + "..."
    
    try:
        pipeline = get_paraphrase_pipeline()
        prompt = f"paraphrase: {text}"
        result = pipeline(
            prompt, 
            max_length=min(len(text) + 50, 256),
            min_length=min(len(text) - 20, 10),
            num_return_sequences=1,
            do_sample=False,
            early_stopping=True
        )[0]['generated_text']
        
        # Clean up memory
        gc.collect()
        
        return result
    except Exception as e:
        # Fallback: return original text with minor modifications
        return text.replace(".", " .").replace(",", " ,").strip()
