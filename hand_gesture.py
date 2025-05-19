import cv2
import mediapipe as mp
import time
import webbrowser
import HandTrackingModule as htm


BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
wCam, hCam = 640, 480  
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0


detector = htm.handDetector(detectionCon=0.7)
numberOfFingers = 0


stable_fingers = None  
stable_start_time = None  
stable_duration = 2  

def sum_dict(dict):
    result = 0
    for key in dict:
        result += dict[key]
    return result

while True:
    fingers = {"4": 0, "8": 0, "12": 0, "16": 0, "20": 0}

    success, img = cap.read()
    img = detector.findHands(img)
    landmarks = detector.findPosition(img, draw=False)


    if len(landmarks) != 0:

        # Thumb
        x4, y4 = landmarks[4][1], landmarks[4][2]
        x3, y3 = landmarks[3][1], landmarks[3][2]

        if x4 > x3:
            fingers["4"] = 1

        # Index finger
        x8, y8 = landmarks[8][1], landmarks[8][2]
        x6, y6 = landmarks[6][1], landmarks[6][2]

        if y8 <= y6:
            fingers["8"] = 1

        # Middle finger
        x12, y12 = landmarks[12][1], landmarks[12][2]
        x10, y10 = landmarks[10][1], landmarks[10][2]

        if y12 <= y10:
            fingers["12"] = 1

        # Ring finger
        x16, y16 = landmarks[16][1], landmarks[16][2]
        x14, y14 = landmarks[14][1], landmarks[14][2]

        if y16 <= y14:
            fingers["16"] = 1

        # Little finger
        x20, y20 = landmarks[20][1], landmarks[20][2]
        x18, y18 = landmarks[18][1], landmarks[18][2]

        if y20 <= y18:
            fingers["20"] = 1


    current_fingers = sum_dict(fingers)


    if stable_fingers == current_fingers:
    
        if stable_start_time is None:
            stable_start_time = time.time()
        elif time.time() - stable_start_time >= stable_duration:

            if current_fingers == 1:
                webbrowser.open("https://www.instagram.com")
                break
            elif current_fingers == 2:
                webbrowser.open("https://www.facebook.com")
                break
            elif current_fingers == 3:
                webbrowser.open("https://www.twitter.com")
                break
            elif current_fingers == 4:
                webbrowser.open("https://www.youtube.com")
                break
            elif current_fingers == 5:
                webbrowser.open("https://www.google.com")
                break
    else:
     
        stable_fingers = current_fingers
        stable_start_time = None

  
    cv2.rectangle(img, (25, 150), (100, 400), GREEN, cv2.FILLED)
    cv2.putText(img, f'{current_fingers}', (35, 300), cv2.FONT_HERSHEY_PLAIN, 6, BLUE, 2)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, BLUE, 2)

 
    cv2.imshow("Image", img)
    cv2.waitKey(1)
