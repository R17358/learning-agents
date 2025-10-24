import cv2
import os
import time
import google.generativeai as genai
from PIL import Image
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def open_camera(save_path: str) -> str:
    """Opens camera, auto-captures after 6 seconds, detects object using Gemini, 
    and returns the detected object name for search.
    
    Returns:
        Detected object name as string (e.g., "iPhone 15 Pro", "Nike shoes")
    """
    try:
        
        os.makedirs("images", exist_ok=True) 
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            return " Camera could not be opened"
        
        print("\n Camera opened! Auto-capturing in 6 seconds...")
        print(" Position your object in frame...")
        
        start_time = time.time()
        countdown_interval = 1 
        last_countdown = 6
        
        captured_frame = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            elapsed = time.time() - start_time
            remaining = max(0, 6 - elapsed)
            
            countdown_text = f"Capturing in: {int(remaining)}s"
            cv2.putText(frame, countdown_text, (10, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            
            cv2.imshow('Camera Feed - Auto Capture', frame)
            
            
            if elapsed >= 6:
                captured_frame = frame.copy()
                cv2.imwrite(save_path, captured_frame)
                print(f" Image captured and saved: {os.path.abspath(save_path)}")
                
                white_frame = frame.copy()
                white_frame[:] = (255, 255, 255)
                cv2.imshow('Camera Feed - Auto Capture', white_frame)
                cv2.waitKey(200)
                
                break
            
            key = cv2.waitKey(1)
            if key == ord('q') or key == ord('Q'):
                print(" Capture cancelled by user.")
                cap.release()
                cv2.destroyAllWindows()
                return "Capture cancelled"
        
        cap.release()
        cv2.destroyAllWindows()
        
        if captured_frame is None:
            return " Failed to capture image"
        
       
        print("\n🔍 Detecting object using Gemini Vision...")
        detected_object = detect_object_gemini(save_path)
        
        if detected_object:
            print(f"✨ Detected: {detected_object}")
            return detected_object
        else:
            return " Could not detect object in image"
    
    except Exception as e:
        return f" Error: {str(e)}"


def detect_object_gemini(image_path: str) -> str:
    """
    Uses Gemini Vision to detect and identify the main object in an image.
    
    Args:
        image_path: Path to the captured image
        
    Returns:
        Detected object name as a short search query (e.g., "iPhone 15 Pro")
    """
    try:
        img = Image.open(image_path)
        
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = """What is the main object in this image? 
        Provide ONLY a short, specific name suitable for web search (2-5 words).
        Be specific about brands, models, or types if visible.
        Examples: "iPhone 15 Pro", "Nike Air Jordan", "MacBook Pro laptop", "Sony headphones"
        
        Reply with ONLY the object name, nothing else."""
        
        response = model.generate_content([prompt, img])
        
        detected_object = response.text.strip()
        
        # Remove quotes if present
        detected_object = detected_object.replace('"', '').replace("'", '')
        
        return detected_object
    
    except Exception as e:
        print(f" Gemini detection error: {str(e)}")
        return None


def detect_using_gemini(save_path: str)->str:
    # Test the camera tool
    detected_object = open_camera(save_path)
    return detected_object
    
    