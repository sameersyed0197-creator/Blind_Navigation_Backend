"""
Safe startup script for Blind Navigation System
Handles OS-specific issues and import errors
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🚀 BLIND NAVIGATION SYSTEM - STARTUP")
print("=" * 60)

# Check Python version
print(f"Python version: {sys.version}")
if sys.version_info < (3, 9):
    print("❌ Python 3.9 or higher required!")
    sys.exit(1)

# Check imports
print("\nChecking dependencies...")
missing = []

try:
    import flask
    print("✅ Flask")
except ImportError:
    print("❌ Flask")
    missing.append("Flask")

try:
    import cv2
    print("✅ OpenCV")
except ImportError:
    print("❌ OpenCV")
    missing.append("opencv-python")

try:
    import numpy
    print("✅ NumPy")
except ImportError:
    print("❌ NumPy")
    missing.append("numpy")

try:
    import PIL
    print("✅ Pillow")
except ImportError:
    print("❌ Pillow")
    missing.append("Pillow")

try:
    import torch
    print("✅ PyTorch")
except ImportError:
    print("❌ PyTorch")
    missing.append("torch")

try:
    import ultralytics
    print("✅ Ultralytics")
except ImportError:
    print("❌ Ultralytics")
    missing.append("ultralytics")

if missing:
    print("\n❌ Missing packages:", ", ".join(missing))
    print("\nFix: pip install", " ".join(missing))
    sys.exit(1)

print("\n✅ All dependencies installed!")
print("=" * 60)

# Start the application
print("\nStarting application...\n")

try:
    from app import app
    
    print("=" * 60)
    print("🚀 BLIND NAVIGATION SYSTEM - READY")
    print("=" * 60)
    print("✅ Server: http://localhost:5000")
    print("✅ Health: http://localhost:5000/health")
    print("=" * 60)
    print("\nPress CTRL+C to stop\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    
except KeyboardInterrupt:
    print("\n\n👋 Shutting down gracefully...")
    sys.exit(0)
except Exception as e:
    print(f"\n❌ Error starting application: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
