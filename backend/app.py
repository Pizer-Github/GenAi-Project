from fastapi import FastAPI, Request
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from paraphraser import paraphrase_text
from grammar import correct_grammar
from summarizer import summarize_text
from plagiarism import check_plagiarism

app = FastAPI()

class TextRequest(BaseModel):
    text: str

class PlagiarismRequest(BaseModel):
    text: str
    reference_texts: list[str]

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
    result = check_plagiarism(req.text, req.reference_texts)
    return result
