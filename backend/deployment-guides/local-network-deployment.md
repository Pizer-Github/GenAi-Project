# Local Network Deployment

## Quick Local Network Access

### Backend Changes:
1. Update CORS in `backend/app.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local network
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. Start backend with external access:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Frontend Changes:
1. Find your IP address:
```bash
ipconfig  # Windows
# Look for IPv4 Address (e.g., 192.168.1.100)
```

2. Update `src/App.js`:
```javascript
const API_BASE_URL = 'http://YOUR_IP_ADDRESS:8000';
// e.g., const API_BASE_URL = 'http://192.168.1.100:8000';
```

3. Start frontend:
```bash
npm start -- --host 0.0.0.0
```

### Access:
- Backend: `http://YOUR_IP:8000`
- Frontend: `http://YOUR_IP:3000`
- Other devices on network can access these URLs
