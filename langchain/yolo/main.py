from ultralytics import YOLO

# Load a pre-trained YOLOv5 or YOLOv8 model
model = YOLO("yolov8n.pt")  # or yolov5s.pt if you're using YOLOv5

# For an image
results = model("image.jpg")

# # For video
# results = model("video.mp4")  # This will process the video and run detections
