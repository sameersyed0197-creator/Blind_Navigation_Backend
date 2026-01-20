---
title: Blind Navigation System
emoji: 🦯
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# 🦯 Blind Navigation System - Backend API

AI-powered indoor navigation system for visually impaired people using YOLOv8n object detection.

## 🎯 Features

- Real-time object detection with YOLOv8n
- Indoor object filtering (no animals)
- Label corrections for better accuracy
- Audio navigation instructions
- CORS enabled for frontend integration

## 🚀 API Endpoints

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

## 🔧 Tech Stack

- Flask 3.0.0
- Ultralytics YOLOv8n
- PyTorch (CPU)
- OpenCV
- Gunicorn

## 💡 Usage

This is the backend API. Use with the frontend at:
https://github.com/sameersyed0197-creator/Indoor_Navigation_System

## 📝 License

MIT License - Built for accessibility
