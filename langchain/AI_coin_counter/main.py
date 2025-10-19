import cv2
import cvzone
import numpy as np

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

totalMoney = 0


def empty(a):
    pass

cv2.namedWindow("Settings")
cv2.resizeWindow("Settings", 640, 240)
cv2.createTrackbar("Threshold1", "Settings", 23, 255, empty)
cv2.createTrackbar("Threshold2", "Settings", 33, 255, empty)
cv2.createTrackbar("area", "Settings", 64,1000, empty)

def preProcess(img):
    thresh1 = cv2.getTrackbarPos("Threshold1", "Settings")
    thresh2 = cv2.getTrackbarPos("Threshold2", "Settings")
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # imgGray=img
    imgPreProcess = cv2.GaussianBlur(imgGray, (5,5), 3)
    imgPreProcess = cv2.Canny(imgPreProcess, thresh1, thresh2)
    kernel = np.ones((3,3), np.uint8)
    imgPreProcess = cv2.dilate(imgPreProcess, kernel, iterations=2)
    imgPreProcess = cv2.morphologyEx(imgPreProcess, cv2.MORPH_CLOSE, kernel)
    
    return imgGray, imgPreProcess
    
    

while True:
    success, img = cap.read()
    
    imgGray, imgPreProcess = preProcess(img)
    
    minArea = cv2.getTrackbarPos("area", "Settings")
    
    imgContour, contourFound = cvzone.findContours(img, imgPreProcess, minArea)
    
    if contourFound:
        for count, contour in enumerate(contourFound):
            # print(contour)
            peri = cv2.arcLength(contour['cnt'], True)
            approx = cv2.approxPolyDP(contour['cnt'], 0.02*peri, True)
            if len(approx)>5:
                area = contour['area']
                # print(area)
                
                if area>30:
                    totalMoney += 5
    
    imgBlack = np.zeros((480, 640, 3), np.uint8)
    
    
    finalStacked_images = cvzone.stackImages([img, imgGray, imgPreProcess, imgContour], 2, 0.5)
    
    cvzone.putTextRect(finalStacked_images, f'Rs {totalMoney}', (100,200), scale=10, offset=30, thickness=7)
    
    if success:
        cv2.imshow("Image Stacked", finalStacked_images)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    else:
        break