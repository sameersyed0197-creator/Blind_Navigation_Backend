# 🦯 Blind Navigation System - Backend

Flask backend with YOLOv8n object detection for indoor navigation.

## 🚀 Deploy on Railway (Recommended - 8GB RAM)

### One-Click Deploy:
1. Go to https://railway.app
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select **"Blind_Navigation_Backend"**
5. Railway auto-detects settings (railway.json)
6. Click **"Deploy"**
7. Wait 5-10 minutes
8. Click **"Generate Domain"** to get your URL

### Environment Variables:
- `PORT` - Auto-set by Railway
- No other variables needed!

## 📦 Model Auto-Download

YOLOv8n model (~6MB) downloads automatically on first run. No manual setup needed!

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```

Server runs on http://localhost:5000

## 📊 API Endpoints

### POST /detect
Detects objects and returns navigation instruction.

**Request:**
```json
{
  "image": "data:image/jpeg;base64,..."
}
```

**Response:**
```json
{
  "instruction": "Keyboard on your left. Turn right.",
  "detections": 3,
  "boxes": [...],
  "fps": 2.5
}
```

### GET /health
Health check endpoint.

## 🎯 Features

- ✅ YOLOv8n (fastest YOLO model)
- ✅ Indoor object detection only
- ✅ Label corrections (microwave→phone, cell phone→keyboard)
- ✅ Optimized for CPU (416px images)
- ✅ CORS enabled for frontend

## 🛠️ Tech Stack

- Flask 3.0.0
- Ultralytics YOLOv8
- PyTorch (CPU)
- OpenCV
- Gunicorn (production)

## 💰 Cost: ₹0

Railway free tier: 500 hours/month + 8GB RAM

---
**Built for visually impaired navigation** 🦯
