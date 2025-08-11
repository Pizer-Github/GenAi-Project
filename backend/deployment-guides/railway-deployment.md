# Railway Deployment Guide

Railway is excellent for Python/Node.js apps with generous free tier.

## Prerequisites:
1. GitHub account
2. Railway account (https://railway.app)

## Step 1: Prepare Your Code

### Backend (`railway-backend.py`):
```python
import os
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import io
import PyPDF2

# Your existing imports...
from paraphraser import paraphrase_text
from grammar import correct_grammar
from summarizer import summarize_text
from plagiarism import check_plagiarism

app = FastAPI()

# Update CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your existing code...

# Add this for Railway
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
```

### Create `requirements.txt`:
```txt
fastapi==0.115.14
uvicorn[standard]==0.31.1
transformers==4.52.3
torch==2.7.0
scikit-learn==1.5.2
numpy==2.2.6
pydantic==2.11.7
PyPDF2==3.0.1
python-multipart==0.0.20
```

## Step 2: Deploy Backend

1. **Push to GitHub**: Create a repository with your backend code
2. **Connect Railway**: 
   - Go to railway.app
   - Click "Deploy from GitHub"
   - Select your repository
   - Choose backend folder if needed
3. **Environment Variables**: Railway auto-detects Python apps
4. **Custom Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

## Step 3: Deploy Frontend

### Update `frontend/src/App.js`:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-backend-url.railway.app';
```

### Add to `package.json`:
```json
{
  "scripts": {
    "build": "react-scripts build",
    "start": "react-scripts start"
  }
}
```

### Deploy Options:
1. **Netlify**: Connect GitHub repo, auto-deploy on push
2. **Vercel**: Similar to Netlify, great for React apps
3. **Railway**: Can also host frontend

## Environment Variables:
- Backend: No special env vars needed
- Frontend: `REACT_APP_API_URL=https://your-backend-url.railway.app`

## Advantages:
✅ Free tier available
✅ Auto-deploys from GitHub
✅ Handles SSL certificates
✅ Built-in monitoring
✅ Easy scaling
