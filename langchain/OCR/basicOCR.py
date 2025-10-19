import easyocr
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


reader = easyocr.Reader(['en'], gpu=True)  

def extract_text_from_image(image_path, detail=0):
    results = reader.readtext(image_path)
    return results

if __name__ == "__main__":
   
    img_list = ['image.png'] 
    
    for i, image_path in enumerate(img_list):
        text = extract_text_from_image(image_path, detail=0)
        
        with open(f"output{i}.txt", 'w') as f:
            for detection in text:
                detected_text = detection[1]
                f.write(f"{detected_text}\n")
            
        