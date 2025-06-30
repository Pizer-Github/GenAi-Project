# GenAi-Project
 # Paraphraser, Grammar Checker, Plagiarism Checker, and Text Summarizer using Generative AI

## 🚀 Project Overview

This project implements a **web-based application using Generative AI (transformer-based models)** to perform:
- **Paraphrasing**
- **Grammar Checking**
- **Plagiarism Checking**
- **Text Summarization**

Built using:
- Backend: FastAPI + Hugging Face Transformers
- Frontend: React + Axios
- NLP Models: T5, BART, and custom TF-IDF cosine similarity for plagiarism checking

---

 🎯 Objectives
✅ Understand transformer-based generative models in NLP.  
✅ Build a scalable FastAPI backend serving core NLP tasks.  
✅ Develop an intuitive React frontend for user interaction.  
✅ Deploy and test for practical usability and accuracy.

---

 🛠️ Features

  Paraphrasing
- Uses **T5-based models** to generate paraphrased versions of user input while maintaining context.

  Grammar Checking
- Uses **T5 grammar correction models** to identify and correct grammatical errors in user-provided text.

  Plagiarism Checking
- Uses **TF-IDF cosine similarity** to compare user input against reference texts and determine similarity levels.

  Text Summarization
- Uses **BART summarization models** to generate concise summaries of lengthy input texts.

---

  Project Structure

project-root/
│
├── backend/
│ ├── app.py
│ ├── paraphraser.py
│ ├── grammar.py
│ ├── plagiarism.py
│ ├── summarizer.py
│ ├── requirements.txt
│ └── venv/ (virtual environment)
│
└── frontend/
├── src/
├── public/
├── package.json
└── ...


Setup Instructions

1️⃣ Backend (FastAPI)

- Navigate to `backend`:

cd backend
python -m venv venv
# Activate (PowerShell):
.\venv\Scripts\activate
# Install dependencies:
pip install -r requirements.txt
If requirements.txt is not present, install manually:


pip install fastapi uvicorn transformers torch scikit-learn
Run the FastAPI server:
uvicorn app:app --reload --port 8000



2️⃣ Frontend (React)
Navigate to frontend:

cd frontend
npm install
npm start
