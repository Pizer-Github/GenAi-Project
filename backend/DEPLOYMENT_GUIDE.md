# 🚀 TextForge AI Deployment Guide

## Quick Start Options

### 1. **Instant Local Network** (5 minutes)
Perfect for testing with friends/colleagues on same network.

**Steps:**
1. Get your IP address: `ipconfig` (look for IPv4)
2. Update backend CORS to allow all origins
3. Start backend: `uvicorn app:app --host 0.0.0.0 --port 8000`
4. Update frontend API_BASE_URL to your IP
5. Start frontend: `npm start -- --host 0.0.0.0`

**Access:** `http://YOUR_IP:3000`

### 2. **Cloud Deployment** (30 minutes)
Production-ready, accessible worldwide.

**Recommended Platforms:**
- **Railway** (easiest, free tier)
- **Render** (similar to Railway)
- **Vercel + Railway** (frontend + backend)

### 3. **Professional Docker** (1 hour)
Full containerization for any cloud provider.

## 📋 Pre-Deployment Checklist

### Backend Preparation:
- [ ] Install `python-multipart` for file uploads
- [ ] Update CORS settings for production domains
- [ ] Set environment variables for production
- [ ] Test all API endpoints
- [ ] Optimize model loading (consider caching)

### Frontend Preparation:
- [ ] Update API_BASE_URL to production backend
- [ ] Build production bundle: `npm run build`
- [ ] Test all features in production mode
- [ ] Optimize bundle size if needed

### Security Considerations:
- [ ] Set specific CORS origins (not "*")
- [ ] Add rate limiting
- [ ] Implement file size/type validation
- [ ] Add HTTPS in production
- [ ] Set up monitoring/logging

## 🔧 Environment Variables

### Backend (.env):
```env
# Optional - customize as needed
MODEL_CACHE_DIR=/app/models
MAX_FILE_SIZE=52428800  # 50MB
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Frontend (.env):
```env
REACT_APP_API_URL=https://your-backend-domain.com
REACT_APP_MAX_FILE_SIZE=52428800
```

## ☁️ Cloud Platform Comparison

| Platform | Pros | Cons | Best For |
|----------|------|------|----------|
| **Railway** | Easy, auto-deploy, free tier | Limited free hours | Small projects |
| **Render** | Simple, good free tier | Slower cold starts | Hobby projects |
| **Vercel** | Excellent for React | Functions have time limits | Frontend + simple backend |
| **Heroku** | Established, many addons | Expensive, no free tier | Enterprise |
| **DigitalOcean** | Flexible, good pricing | Requires more setup | Full control needed |

## 🚀 Deployment Commands

### Railway:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

### Docker:
```bash
# Build and run locally
docker-compose up --build

# Deploy to any cloud with Docker support
docker build -t textforge-backend ./backend
docker build -t textforge-frontend ./frontend
```

### Traditional VPS:
```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip nodejs npm nginx

# Setup backend
pip install -r requirements_simple.txt
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000

# Setup frontend
npm run build
# Configure nginx to serve build folder
```

## 🔍 Troubleshooting

### Common Issues:
1. **CORS Errors**: Check allowed origins in backend
2. **File Upload Fails**: Ensure `python-multipart` is installed
3. **Model Loading Slow**: First request takes time to load models
4. **Memory Issues**: AI models require ~2GB RAM minimum

### Performance Tips:
- Enable model caching
- Use CDN for frontend assets
- Implement request queuing for heavy AI processing
- Consider GPU instances for faster inference

## 📊 Monitoring

### Basic Monitoring:
- Health check endpoints
- Error logging
- Performance metrics
- File upload statistics

### Advanced:
- Sentry for error tracking
- Prometheus for metrics
- Grafana for dashboards
- Uptime monitoring

## 💰 Cost Estimation

### Free Tier Options:
- Railway: 500 hours/month free
- Render: 750 hours/month free
- Vercel: Unlimited static hosting

### Paid Hosting (Monthly):
- Railway Pro: $5/month
- Render: $7/month
- DigitalOcean Droplet: $5-10/month
- AWS/GCP: $10-50/month (depending on usage)

## 🎯 Recommended Deployment Path

1. **Start with Railway** - Easiest, free tier available
2. **Add custom domain** - Professional appearance
3. **Monitor usage** - Track performance and costs
4. **Scale as needed** - Upgrade or move to more powerful platform
5. **Add CI/CD** - Automatic deployments from GitHub

Your TextForge AI application is ready for the world! 🌍
