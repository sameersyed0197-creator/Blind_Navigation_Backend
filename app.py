from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import base64
import io
import time
import os
import sys

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

try:
    from ultralytics import YOLO
except ImportError as e:
    print(f"❌ Error importing ultralytics: {e}")
    print("Fix: pip install ultralytics")
    sys.exit(1)

app = Flask(__name__, static_folder='../frontend')
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

print("Loading YOLOv8 Nano model...")
try:
    model = YOLO('yolov8n.pt')
    model.fuse()  # Optimize for inference
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("Model will download automatically on first run...")
    model = YOLO('yolov8n.pt')
    model.fuse()

CLASS_NAMES = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
    'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat',
    'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
    'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
    'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
    'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# Indoor objects only - no animals
INDOOR_OBJECTS = {
    'person', 'chair', 'couch', 'bed', 'dining table', 'tv', 'laptop', 'mouse',
    'keyboard', 'cell phone', 'bottle', 'cup', 'book', 'clock', 'vase',
    'backpack', 'handbag', 'umbrella', 'suitcase', 'bench', 'potted plant',
    'sink', 'refrigerator', 'microwave', 'oven', 'toaster', 'toilet'
}

# Label corrections for better accuracy
LABEL_CORRECTIONS = {
    'microwave': 'phone',
    'cell phone': 'keyboard'
}

PRIORITY = {'person', 'chair', 'couch', 'bed', 'dining table', 'tv', 'laptop', 'keyboard', 'mouse', 'cell phone'}

def get_instruction(detections, w, h):
    if not detections:
        return "Path clear. Move forward safely."
    
    closest = max(detections, key=lambda x: x['area'])
    x_center = closest['x_center']
    name = closest['name'].replace('_', ' ')
    area_percent = (closest['area'] / (w * h)) * 100
    
    if area_percent > 30:
        distance = "very close"
    elif area_percent > 15:
        distance = "close"
    elif area_percent > 5:
        distance = "medium distance"
    else:
        distance = "far"
    
    if x_center < w * 0.35:
        position = "on your left"
        action = "Turn right"
    elif x_center > w * 0.65:
        position = "on your right"
        action = "Turn left"
    else:
        position = "directly ahead"
        action = "Stop"
    
    if area_percent > 20:
        return f"{action}! {name.capitalize()} is {distance}, {position}."
    else:
        return f"{name.capitalize()} {position}. {action.lower()}."

@app.route('/detect', methods=['POST', 'OPTIONS'])
def detect():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response, 200
    
    start_time = time.time()
    
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
            
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        h, w = img_array.shape[:2]
        if max(h, w) > 320:
            scale = 320 / max(h, w)
            new_w, new_h = int(w * scale), int(h * scale)
            img_array = cv2.resize(img_array, (new_w, new_h), interpolation=cv2.INTER_AREA)
            h, w = new_h, new_w
        
        results = model(img_array, conf=0.25, iou=0.45, verbose=False, max_det=5, device='cpu', imgsz=320, half=False)
        
        detections = []
        boxes_data = []
        
        for result in results:
            if result.boxes is None:
                continue
                
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                
                if class_id >= len(CLASS_NAMES):
                    continue
                    
                obj_name = CLASS_NAMES[class_id]
                
                # Skip animals and outdoor objects
                if obj_name not in INDOOR_OBJECTS:
                    continue
                
                # Apply label corrections
                if obj_name in LABEL_CORRECTIONS:
                    obj_name = LABEL_CORRECTIONS[obj_name]
                
                min_conf = 0.25 if obj_name in PRIORITY else 0.35
                
                if confidence < min_conf:
                    continue
                
                x_center = (x1 + x2) / 2
                y_center = (y1 + y2) / 2
                area = (x2 - x1) * (y2 - y1)
                area_percent = (area / (w * h)) * 100
                
                if area_percent > 30:
                    depth = 'very_close'
                elif area_percent > 15:
                    depth = 'close'
                elif area_percent > 5:
                    depth = 'near'
                else:
                    depth = 'far'
                
                detections.append({
                    'x_center': float(x_center),
                    'y_center': float(y_center),
                    'area': float(area),
                    'name': obj_name,
                    'confidence': confidence
                })
                
                boxes_data.append({
                    'x1': float(x1),
                    'y1': float(y1),
                    'x2': float(x2),
                    'y2': float(y2),
                    'label': obj_name.replace('_', ' '),
                    'confidence': confidence,
                    'depth': depth
                })
        
        instruction = get_instruction(detections, w, h)
        process_time = time.time() - start_time
        fps = 1 / process_time if process_time > 0 else 0
        
        print(f"✅ {len(detections)} objects detected | {process_time:.3f}s | {fps:.1f} FPS")
        
        return jsonify({
            'instruction': instruction,
            'detections': len(detections),
            'boxes': boxes_data,
            'fps': round(fps, 1),
            'process_time': round(process_time, 3)
        }), 200, {'Access-Control-Allow-Origin': '*'}
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model': 'YOLOv8n Fine-Tuned', 'timestamp': time.time()})

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 BLIND NAVIGATION SYSTEM - FINE-TUNED AI")
    print("="*60)
    print("✅ Server ready at: http://localhost:5000")
    print("✅ Health check: http://localhost:5000/health")
    print("✅ Model: YOLOv8n Fine-Tuned on COCO")
    print("="*60 + "\n")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
