import os
import gc
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import io
import PyPDF2
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TextForge AI API",
    description="Lightweight AI text processing",
    version="1.0.0"
)

# Production CORS settings
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

class PlagiarismRequest(BaseModel):
    text: str
    reference_texts: list[str] = []

# Simple rule-based implementations to avoid loading heavy models
def simple_paraphrase(text):
    """Simple rule-based paraphrasing"""
    # Basic synonym replacements
    replacements = {
        "good": "excellent", "bad": "poor", "big": "large", "small": "tiny",
        "happy": "joyful", "sad": "sorrowful", "fast": "quick", "slow": "gradual",
        "the": "a", "and": "plus", "but": "however", "because": "since",
        "very": "extremely", "really": "truly", "quite": "rather"
    }
    
    words = text.split()
    result = []
    
    for word in words:
        clean_word = re.sub(r'[^\w]', '', word.lower())
        if clean_word in replacements:
            # Keep original punctuation
            punctuation = re.findall(r'[^\w]', word)
            new_word = replacements[clean_word]
            if word[0].isupper():
                new_word = new_word.capitalize()
            result.append(new_word + ''.join(punctuation))
        else:
            result.append(word)
    
    return ' '.join(result)

def simple_grammar_check(text):
    """Simple rule-based grammar correction"""
    # Basic corrections
    text = re.sub(r'\bi\b', 'I', text)  # Capitalize 'I'
    text = re.sub(r'\.([a-z])', r'. \1', text)  # Space after period
    text = re.sub(r',([a-zA-Z])', r', \1', text)  # Space after comma
    text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single
    text = text.strip()
    
    # Capitalize first letter
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    
    return text

def simple_summarize(text):
    """Simple extractive summarization"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    if len(sentences) <= 3:
        return text
    
    # Take first and last sentences, and one from middle
    summary_sentences = [
        sentences[0],
        sentences[len(sentences)//2],
        sentences[-1]
    ]
    
    return '. '.join(summary_sentences) + '.'

def simple_plagiarism_check(text, reference_texts):
    """Simple similarity-based plagiarism detection"""
    text_words = set(text.lower().split())
    
    similarities = []
    for ref_text in reference_texts:
        ref_words = set(ref_text.lower().split())
        if len(text_words) == 0 or len(ref_words) == 0:
            similarity = 0.0
        else:
            intersection = text_words.intersection(ref_words)
            similarity = len(intersection) / len(text_words.union(ref_words))
        similarities.append(similarity)
    
    max_similarity = max(similarities) if similarities else 0.0
    is_plagiarized = max_similarity > 0.3
    
    return {
        "is_plagiarized": is_plagiarized,
        "similarity_percentage": max_similarity * 100,
        "message": f"{'Potential plagiarism detected' if is_plagiarized else 'No significant plagiarism detected'}"
    }

@app.get("/")
def root():
    return {
        "message": "TextForge AI API - Ultra Lite",
        "version": "1.0.0",
        "status": "healthy",
        "features": ["paraphrase", "grammar", "plagiarism", "summarize", "file_upload"],
        "note": "Using lightweight rule-based processing for memory efficiency"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "TextForge AI Backend is running!"}

@app.post("/paraphrase")
def paraphrase_endpoint(req: TextRequest):
    try:
        result = simple_paraphrase(req.text)
        return {"paraphrased": result}
    except Exception as e:
        logger.error(f"Paraphrase error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing text")

@app.post("/grammar")
def grammar_endpoint(req: TextRequest):
    try:
        result = simple_grammar_check(req.text)
        return {"corrected": result}
    except Exception as e:
        logger.error(f"Grammar error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing text")

@app.post("/summarize")
def summarize_endpoint(req: TextRequest):
    try:
        result = simple_summarize(req.text)
        return {"summary": result}
    except Exception as e:
        logger.error(f"Summarize error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing text")

@app.post("/plagiarism")
def plagiarism_endpoint(req: PlagiarismRequest):
    try:
        if not req.reference_texts:
            default_references = [
                "To be or not to be, that is the question.",
                "It was the best of times, it was the worst of times.",
                "In the beginning was the Word, and the Word was with God.",
                "Four score and seven years ago our fathers brought forth on this continent a new nation.",
                "I have a dream that one day this nation will rise up and live out the true meaning of its creed."
            ]
            reference_texts = default_references
        else:
            reference_texts = req.reference_texts
        
        result = simple_plagiarism_check(req.text, reference_texts)
        return result
    except Exception as e:
        logger.error(f"Plagiarism error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing text")

def extract_text_from_pdf(pdf_content: bytes) -> str:
    """Extract text from PDF file content using PyPDF2."""
    try:
        pdf_file = io.BytesIO(pdf_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text_content = ""
        for page_num in range(min(len(pdf_reader.pages), 5)):  # Limit to 5 pages
            page = pdf_reader.pages[page_num]
            text_content += page.extract_text() + "\n"
        
        # Clean up memory
        del pdf_file, pdf_reader
        gc.collect()
        
        return text_content.strip()
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Error extracting text from PDF: {str(e)}"
        )

async def extract_text_from_file(file: UploadFile) -> str:
    """Extract text content from uploaded file."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file extension
    allowed_extensions = ['.txt', '.md', '.pdf']
    file_extension = '.' + file.filename.split('.')[-1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not supported. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Read file content with size limit
        content = await file.read()
        if len(content) > 1024 * 1024:  # 1MB limit
            raise HTTPException(status_code=400, detail="File too large. Max 1MB.")
        
        # Handle different file types
        if file_extension == '.pdf':
            text_content = extract_text_from_pdf(content)
        else:
            # Handle text files (.txt, .md)
            try:
                text_content = content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    text_content = content.decode('latin-1')
                except UnicodeDecodeError:
                    raise HTTPException(status_code=400, detail="Unable to read file")
        
        # Validate content length
        if len(text_content.strip()) == 0:
            raise HTTPException(status_code=400, detail="File appears to be empty")
        
        # Limit text size for processing
        if len(text_content) > 5000:
            text_content = text_content[:5000] + "... (truncated)"
            
        # Clean up memory
        del content
        gc.collect()
            
        return text_content.strip()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# File upload endpoints
@app.post("/upload/paraphrase")
async def upload_paraphrase_endpoint(file: UploadFile = File(...)):
    try:
        text_content = await extract_text_from_file(file)
        result = simple_paraphrase(text_content)
        return {
            "filename": file.filename,
            "original_text": text_content,
            "paraphrased": result
        }
    except Exception as e:
        logger.error(f"Upload paraphrase error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing file")

@app.post("/upload/grammar")
async def upload_grammar_endpoint(file: UploadFile = File(...)):
    try:
        text_content = await extract_text_from_file(file)
        result = simple_grammar_check(text_content)
        return {
            "filename": file.filename,
            "original_text": text_content,
            "corrected": result
        }
    except Exception as e:
        logger.error(f"Upload grammar error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing file")

@app.post("/upload/summarize")
async def upload_summarize_endpoint(file: UploadFile = File(...)):
    try:
        text_content = await extract_text_from_file(file)
        result = simple_summarize(text_content)
        return {
            "filename": file.filename,
            "original_text": text_content,
            "summary": result
        }
    except Exception as e:
        logger.error(f"Upload summarize error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing file")

@app.post("/upload/plagiarism")
async def upload_plagiarism_endpoint(file: UploadFile = File(...)):
    try:
        text_content = await extract_text_from_file(file)
        
        # Use default reference texts
        default_references = [
            "To be or not to be, that is the question.",
            "It was the best of times, it was the worst of times.",
            "In the beginning was the Word, and the Word was with God.",
            "Four score and seven years ago our fathers brought forth on this continent a new nation.",
            "I have a dream that one day this nation will rise up and live out the true meaning of its creed."
        ]
        
        result = simple_plagiarism_check(text_content, default_references)
        return {
            "filename": file.filename,
            "original_text": text_content,
            **result
        }
    except Exception as e:
        logger.error(f"Upload plagiarism error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing file")

# For production deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main_ultra_lite:app", host="0.0.0.0", port=port)
