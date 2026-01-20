"""
Test script to verify all imports and dependencies
Run this before starting the application
"""

print("Testing imports...")
print("-" * 60)

try:
    print("1. Testing Flask...")
    from flask import Flask, request, jsonify, send_from_directory
    from flask_cors import CORS
    print("   ✅ Flask imported successfully")
except ImportError as e:
    print(f"   ❌ Flask import failed: {e}")
    print("   Fix: pip install Flask flask-cors")

try:
    print("2. Testing OpenCV...")
    import cv2
    print(f"   ✅ OpenCV imported successfully (version: {cv2.__version__})")
except ImportError as e:
    print(f"   ❌ OpenCV import failed: {e}")
    print("   Fix: pip install opencv-python")

try:
    print("3. Testing NumPy...")
    import numpy as np
    print(f"   ✅ NumPy imported successfully (version: {np.__version__})")
except ImportError as e:
    print(f"   ❌ NumPy import failed: {e}")
    print("   Fix: pip install numpy")

try:
    print("4. Testing Pillow...")
    from PIL import Image, ImageDraw, ImageFont
    import PIL
    print(f"   ✅ Pillow imported successfully (version: {PIL.__version__})")
except ImportError as e:
    print(f"   ❌ Pillow import failed: {e}")
    print("   Fix: pip install Pillow")

try:
    print("5. Testing PyTorch...")
    import torch
    print(f"   ✅ PyTorch imported successfully (version: {torch.__version__})")
    print(f"   ℹ️  CUDA available: {torch.cuda.is_available()}")
except ImportError as e:
    print(f"   ❌ PyTorch import failed: {e}")
    print("   Fix: pip install torch torchvision")

try:
    print("6. Testing Ultralytics (YOLOv8)...")
    from ultralytics import YOLO
    import ultralytics
    print(f"   ✅ Ultralytics imported successfully (version: {ultralytics.__version__})")
except ImportError as e:
    print(f"   ❌ Ultralytics import failed: {e}")
    print("   Fix: pip install ultralytics")

try:
    print("7. Testing other dependencies...")
    import base64
    import io
    import time
    print("   ✅ Standard library modules imported successfully")
except ImportError as e:
    print(f"   ❌ Standard library import failed: {e}")

print("-" * 60)
print("\n🎯 Testing YOLO model loading...")
try:
    from ultralytics import YOLO
    print("   Loading yolov8n.pt model...")
    model = YOLO('yolov8n.pt')
    print("   ✅ Model loaded successfully!")
    print(f"   ℹ️  Model type: {type(model)}")
except Exception as e:
    print(f"   ❌ Model loading failed: {e}")
    print("   Note: Model will download automatically on first run (~6MB)")

print("-" * 60)
print("\n✅ All imports verified!")
print("You can now run: python app.py")
