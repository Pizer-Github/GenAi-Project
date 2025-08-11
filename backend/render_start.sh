#!/bin/bash

# Memory-optimized startup script for Render

echo "Starting TextForge AI with memory optimizations..."

# Set memory-optimized environment variables
export PYTORCH_CUDA_ALLOC_CONF="max_split_size_mb:128"
export TOKENIZERS_PARALLELISM=false
export TRANSFORMERS_CACHE=/tmp/transformers_cache
export HF_HOME=/tmp/huggingface_cache

# Create cache directories in tmp (Render provides limited disk space)
mkdir -p /tmp/transformers_cache
mkdir -p /tmp/huggingface_cache

# Use single worker with optimized memory settings
exec gunicorn main_optimized:app \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 1 \
    --worker-connections 10 \
    --max-requests 100 \
    --max-requests-jitter 10 \
    --timeout 120 \
    --keep-alive 5 \
    --bind 0.0.0.0:$PORT \
    --log-level info \
    --access-logfile - \
    --error-logfile -
