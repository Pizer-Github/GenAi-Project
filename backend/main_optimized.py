import os
import gc
import logging
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import io
import PyPDF2

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TextForge AI API",
    description="AI-powered text processing: Paraphrasing, Grammar Checking, Plagiarism Detection, and Summarization",
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

# Global variables for lazy loading models
_paraphraser = None
_grammar_checker = None
_summarizer = None
_plagiarism_checker = None

def get_paraphraser():
    """Lazy load paraphraser to save memory"""
    global _paraphraser
    if _paraphraser is None:
        logger.info("Loading paraphraser model...")
        from paraphraser import paraphrase_text
        _paraphraser = paraphrase_text
        # Force garbage collection
        gc.collect()
    return _paraphraser

def get_grammar_checker():
    """Lazy load grammar checker to save memory"""
    global _grammar_checker
    if _grammar_checker is None:
        logger.info("Loading grammar checker model...")
        from grammar import correct_grammar
        _grammar_checker = correct_grammar
        # Force garbage collection
        gc.collect()
    return _grammar_checker

def get_summarizer():
    """Lazy load summarizer to save memory"""
    global _summarizer
    if _summarizer is None:
        logger.info("Loading summarizer model...")
        from summarizer import summarize_text
        _summarizer = summarize_text
        # Force garbage collection
        gc.collect()
    return _summarizer

def get_plagiarism_checker():
    """Lazy load plagiarism checker to save memory"""
    global _plagiarism_checker
    if _plagiarism_checker is None:
        logger.info("Loading plagiarism checker model...")
        from plagiarism import check_plagiarism
        _plagiarism_checker = check_plagiarism
        # Force garbage collection
        gc.collect()
    return _plagiarism_checker

@app.get("/")
def root():
    return {
        "message": "TextForge AI API",
        "version": "1.0.0",
        "status": "healthy",
        "features": ["paraphrase", "grammar", "plagiarism", "summarize", "file_upload"]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "TextForge AI Backend is running!"}

@app.post("/paraphrase")
def paraphrase_endpoint(req: TextRequest):
    try:
        paraphraser = get_paraphraser()
        result = paraphraser(req.text)
        # Force garbage collection after processing
        gc.collect()
        return {"paraphrased": result}
    except Exception as e:
        logger.error(f"Paraphrase error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing text")

@app.post("/grammar")
def grammar_endpoint(req: TextRequest):
    try:
        grammar_checker = get_grammar_checker()
        result = grammar_checker(req.text)
        # Force garbage collection after processing
        gc.collect()
        return {"corrected": result}
    except Exception as e:
        logger.error(f"Grammar error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing text")

@app.post("/summarize")
def summarize_endpoint(req: TextRequest):
    try:
        summarizer = get_summarizer()
        result = summarizer(req.text)
        # Force garbage collection after processing
        gc.collect()
        return {"summary": result}
    except Exception as e:
        logger.error(f"Summarize error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing text")

@app.post("/plagiarism")
def plagiarism_endpoint(req: PlagiarismRequest):
    try:
        # If no reference texts provided, use some default ones for demonstration
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
        
        plagiarism_checker = get_plagiarism_checker()
        result = plagiarism_checker(req.text, reference_texts)
        # Force garbage collection after processing
        gc.collect()
        return result
    except Exception as e:
        logger.error(f"Plagiarism error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing text")

def extract_text_from_pdf(pdf_content: bytes) -> str:
    """
    Extract text from PDF file content using PyPDF2.
    """
    try:
        pdf_file = io.BytesIO(pdf_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text_content = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_content += page.extract_text() + "\n"
        
        # Clean up memory
        del pdf_file, pdf_reader
        gc.collect()
        
        return text_content.strip()
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Error extracting text from PDF: {str(e)}. Please ensure it's a valid PDF file."
        )

# File upload helper function
async def extract_text_from_file(file: UploadFile) -> str:
    """
    Extract text content from uploaded file.
    Supports .txt, .md, and .pdf files.
    """
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
        # Read file content
        content = await file.read()
        
        # Handle different file types
        if file_extension == '.pdf':
            text_content = extract_text_from_pdf(content)
        else:
            # Handle text files (.txt, .md)
            try:
                text_content = content.decode('utf-8')
            except UnicodeDecodeError:
                # Try other encodings
                try:
                    text_content = content.decode('latin-1')
                except UnicodeDecodeError:
                    raise HTTPException(
                        status_code=400, 
                        detail="Unable to read file. Please ensure it's a valid text file."
                    )
        
        # Validate content length
        if len(text_content.strip()) == 0:
            raise HTTPException(status_code=400, detail="File appears to be empty")
        
        # Limit file size - reduce limits for memory constraints
        max_length = 20000 if file_extension == '.pdf' else 5000
        if len(text_content) > max_length:
            raise HTTPException(
                status_code=400, 
                detail=f"File content too large. Please keep content under {max_length//1000}KB."
            )
            
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
        paraphraser = get_paraphraser()
        result = paraphraser(text_content)
        
        # Clean up memory
        gc.collect()
        
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
        grammar_checker = get_grammar_checker()
        result = grammar_checker(text_content)
        
        # Clean up memory
        gc.collect()
        
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
        summarizer = get_summarizer()
        result = summarizer(text_content)
        
        # Clean up memory
        gc.collect()
        
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
        
        plagiarism_checker = get_plagiarism_checker()
        result = plagiarism_checker(text_content, default_references)
        
        # Clean up memory
        gc.collect()
        
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
    uvicorn.run("main_optimized:app", host="0.0.0.0", port=port)
