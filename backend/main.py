import os
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import io
import PyPDF2

from paraphraser import paraphrase_text
from grammar import correct_grammar
from summarizer import summarize_text
from plagiarism import check_plagiarism

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
    return {"paraphrased": paraphrase_text(req.text)}

@app.post("/grammar")
def grammar_endpoint(req: TextRequest):
    return {"corrected": correct_grammar(req.text)}

@app.post("/summarize")
def summarize_endpoint(req: TextRequest):
    return {"summary": summarize_text(req.text)}

@app.post("/plagiarism")
def plagiarism_endpoint(req: PlagiarismRequest):
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
        
    result = check_plagiarism(req.text, reference_texts)
    return result

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
        
        # Limit file size - increase limit for PDFs as they may contain more text
        max_length = 50000 if file_extension == '.pdf' else 10000
        if len(text_content) > max_length:
            raise HTTPException(
                status_code=400, 
                detail=f"File content too large. Please keep content under {max_length//1000}KB."
            )
            
        return text_content.strip()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# File upload endpoints
@app.post("/upload/paraphrase")
async def upload_paraphrase_endpoint(file: UploadFile = File(...)):
    text_content = await extract_text_from_file(file)
    result = paraphrase_text(text_content)
    return {
        "filename": file.filename,
        "original_text": text_content,
        "paraphrased": result
    }

@app.post("/upload/grammar")
async def upload_grammar_endpoint(file: UploadFile = File(...)):
    text_content = await extract_text_from_file(file)
    result = correct_grammar(text_content)
    return {
        "filename": file.filename,
        "original_text": text_content,
        "corrected": result
    }

@app.post("/upload/summarize")
async def upload_summarize_endpoint(file: UploadFile = File(...)):
    text_content = await extract_text_from_file(file)
    result = summarize_text(text_content)
    return {
        "filename": file.filename,
        "original_text": text_content,
        "summary": result
    }

@app.post("/upload/plagiarism")
async def upload_plagiarism_endpoint(file: UploadFile = File(...)):
    text_content = await extract_text_from_file(file)
    
    # Use default reference texts
    default_references = [
        "To be or not to be, that is the question.",
        "It was the best of times, it was the worst of times.",
        "In the beginning was the Word, and the Word was with God.",
        "Four score and seven years ago our fathers brought forth on this continent a new nation.",
        "I have a dream that one day this nation will rise up and live out the true meaning of its creed."
    ]
    
    result = check_plagiarism(text_content, default_references)
    return {
        "filename": file.filename,
        "original_text": text_content,
        **result
    }

# For production deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
