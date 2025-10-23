from ultralytics import YOLO

# Load model
model = YOLO("yolov8n.pt")

# Run prediction
results = model(r"langchain\yolo\download.jpg")

# Loop through results
for result in results:
    boxes = result.boxes  # All detected bounding boxes
    for box in boxes:
        cls_id = int(box.cls[0])                   # Class ID
        label = result.names[cls_id]               # Class name (like 'apple')
        conf = float(box.conf[0])                  # Confidence score
        xyxy = box.xyxy[0].tolist()                # Bounding box coordinates [x1, y1, x2, y2]

        print(f"Detected: {label}")
        print(f"Confidence: {conf:.2f}")
        print(f"Bounding box: {xyxy}")
        print("-" * 30)
