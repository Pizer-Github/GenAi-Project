# Render Deployment Guide - Memory Optimized

## Problem: Out of Memory Error

Render's free tier has a 512MB memory limit, which is insufficient for loading large AI models like transformers. Here are three solutions:

## Solution 1: Ultra Lightweight (RECOMMENDED for Free Tier)

This uses rule-based processing instead of AI models to fit within memory limits.

### Files to Use:
- `main_ultra_lite.py` (main app)
- `requirements_ultra_lite.txt` (dependencies)

### Render Settings:
```
Build Command: pip install -r requirements_ultra_lite.txt
Start Command: gunicorn main_ultra_lite:app --worker-class uvicorn.workers.UvicornWorker --workers 1 --bind 0.0.0.0:$PORT
Environment Variables:
- ALLOWED_ORIGINS=*
```

### Features:
- ✅ Rule-based paraphrasing (synonym replacement)
- ✅ Basic grammar correction
- ✅ Extractive summarization
- ✅ Similarity-based plagiarism detection
- ✅ File upload support (PDF, TXT, MD)
- ✅ Memory usage: ~50MB

## Solution 2: Optimized AI Models (Requires Paid Plan)

This uses smaller AI models with memory optimization.

### Files to Use:
- `main_optimized.py` (main app)
- `requirements_lite.txt` (dependencies)
- `render_start.sh` (startup script)

### Render Settings:
```
Build Command: pip install -r requirements_lite.txt
Start Command: ./render_start.sh
Environment Variables:
- ALLOWED_ORIGINS=*
- PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
- TOKENIZERS_PARALLELISM=false
```

### Features:
- ✅ AI-powered paraphrasing with T5-small
- ✅ AI grammar correction
- ✅ AI summarization
- ✅ AI plagiarism detection
- ✅ File upload support
- ⚠️  Memory usage: ~800MB (requires paid plan)

## Solution 3: Upgrade to Paid Plan

For full AI capabilities with larger models:
- Upgrade to Render's Starter plan ($7/month)
- Use original `main.py` and `requirements.txt`
- Memory limit: 1GB+

## Deployment Steps (Ultra Lite - Recommended)

1. **Update your files:**
   ```powershell
   # Copy the ultra lite version
   Copy-Item main_ultra_lite.py main.py
   Copy-Item requirements_ultra_lite.txt requirements.txt
   ```

2. **Commit and push to GitHub:**
   ```powershell
   git add .
   git commit -m "Deploy ultra-lightweight version for Render"
   git push origin main
   ```

3. **Update Render settings:**
   - Go to your Render dashboard
   - Select your backend service
   - Update Build Command: `pip install -r requirements.txt`
   - Update Start Command: `gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --workers 1 --bind 0.0.0.0:$PORT`
   - Deploy

## Performance Comparison

| Feature | Original | Optimized | Ultra Lite |
|---------|----------|-----------|------------|
| Memory Usage | ~1.5GB | ~800MB | ~50MB |
| AI Quality | High | Medium | Basic |
| Render Compatibility | ❌ | Paid Only | ✅ Free |
| Processing Speed | Slow | Medium | Fast |

## Testing the Deployment

Once deployed, test these endpoints:

1. **Health Check:**
   ```
   GET https://your-app.onrender.com/health
   ```

2. **Text Processing:**
   ```
   POST https://your-app.onrender.com/paraphrase
   Body: {"text": "This is a test sentence"}
   ```

3. **File Upload:**
   ```
   POST https://your-app.onrender.com/upload/paraphrase
   Body: form-data with file
   ```

## Troubleshooting

If still getting memory errors:
1. Check logs for specific error messages
2. Ensure only 1 worker is used: `--workers 1`
3. Consider upgrading to paid plan for AI models
4. Contact Render support for memory limit increases

The ultra-lite version should work reliably on Render's free tier while providing basic text processing functionality.
