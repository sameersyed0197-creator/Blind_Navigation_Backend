from ultralytics import YOLO
import os

"""
Fine-tune YOLOv8n for Indoor Navigation
This script fine-tunes the pre-trained YOLOv8n model on indoor-specific data
"""

def finetune_model():
    print("="*60)
    print("🔧 FINE-TUNING YOLOv8n FOR INDOOR NAVIGATION")
    print("="*60)
    
    # Load pre-trained YOLOv8n model
    model = YOLO('yolov8n.pt')
    print("✅ Loaded pre-trained YOLOv8n model")
    
    # Fine-tune on COCO dataset (indoor subset)
    # Focus on indoor classes: person, chair, couch, bed, table, door, etc.
    results = model.train(
        data='coco128.yaml',  # Small COCO subset for quick training
        epochs=10,            # Reduced for CPU (was 50)
        imgsz=640,            # Image size
        batch=4,              # Reduced batch for CPU (was 16)
        patience=5,           # Early stopping patience
        save=True,            # Save checkpoints
        device='cpu',         # Use CPU
        project='indoor_nav', # Project name
        name='yolov8n_finetuned',
        exist_ok=True,
        pretrained=True,      # Start from pre-trained weights
        optimizer='Adam',
        lr0=0.001,            # Initial learning rate
        weight_decay=0.0005,
        warmup_epochs=1,      # Reduced for CPU
        cos_lr=True,          # Cosine learning rate scheduler
        close_mosaic=5,       # Disable mosaic augmentation for last N epochs
        amp=False,            # Disabled for CPU
        fraction=0.5,         # Use 50% of dataset for faster training
        cache=False,          # Don't cache images (saves RAM)
        workers=2,            # Reduced workers for CPU
        verbose=True
    )
    
    print("\n" + "="*60)
    print("✅ FINE-TUNING COMPLETED!")
    print("="*60)
    print(f"📁 Model saved to: indoor_nav/yolov8n_finetuned/weights/best.pt")
    print(f"📊 Training results: indoor_nav/yolov8n_finetuned/")
    print("\nTo use the fine-tuned model:")
    print("1. Copy 'best.pt' to backend folder")
    print("2. Rename to 'yolov8n_finetuned.pt'")
    print("3. Update app.py: model = YOLO('yolov8n_finetuned.pt')")
    print("="*60)
    
    return results

if __name__ == '__main__':
    # Check if GPU is available
    import torch
    if torch.cuda.is_available():
        print(f"🚀 GPU detected: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️  No GPU detected. Training will use CPU (slower)")
    
    # Start fine-tuning
    finetune_model()
