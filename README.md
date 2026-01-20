# 🦯 Blind Navigation System - Backend

Flask backend with YOLOv8n object detection for indoor navigation.

## 🚀 Deploy on Render (Free)

### One-Click Deploy:
1. Fork this repo
2. Go to https://render.com
3. New Web Service → Connect this repo
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type**: Free
5. Deploy!

### Environment Variables (Optional):
- `PORT` - Auto-set by Render
- `PYTHON_VERSION` - 3.10 (recommended)

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

Render free tier: 750 hours/month

---
**Built for visually impaired navigation** 🦯
