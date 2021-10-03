import cv2
import socket
import struct
import mediapipe as mp
import numpy as np;
import matplotlib.pyplot as plt
mp_drawing = mp.solutions.drawing_utils
#mp_holistic = mp.solutions.holistic
mPose = mp.solutions.pose
pose = mPose.Pose()

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("hack_app/sample1_encoded.mp4")
#success, image = cap.read()
cv2.namedWindow("Main")

professorOffset = 100

while True:
    #with mp_holistic.Holistic(
    #        min_detection_confidence=0.5,
    #        min_tracking_confidence=0.5) as holistic:

    widthOfProfessor = 0
    heightOfProfessor = 0
    topLeftPoint = [0, 0]
    furthestLeft = 1
    furthestRight = 0
    furthestTop = 1
    furthestBottom = 0
    windowX = cv2.getWindowImageRect("Main")[0]
    windowY = cv2.getWindowImageRect("Main")[1]
    windowWidth = cv2.getWindowImageRect("Main")[2]
    windowHeight = cv2.getWindowImageRect("Main")[3]

    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    imagePoseDetection = image.copy()
    imageBlackboardDetection = image.copy()
    image.flags.writeable = False
    imagePoseDetection.flags.writeable = False
    imageBlackboardDetection.flags.writeable = False
    imgRGB = cv2.cvtColor(imagePoseDetection, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(imagePoseDetection, results.pose_landmarks, mPose.POSE_CONNECTIONS)

    for id,lm in enumerate(results.pose_landmarks.landmark):
        #get furthest left point
        if (lm.x < furthestLeft):
            furthestLeft = lm.x
        #get furthest right point
        if (lm.x > furthestRight):
            furthestRight = lm.x
        #get furthest top point
        if (lm.y < furthestTop):
            furthestTop = lm.y
        #get furthest bottom point
        if (lm.y > furthestBottom):
            furthestBottom = lm.y
    #calculate width and height
    widthOfProfessor = round(((windowWidth * furthestRight) - (windowWidth * furthestLeft)) + (professorOffset * 2))
    heightOfProfessor = round(((windowHeight * furthestBottom) - (windowHeight * furthestTop)) - professorOffset)
    topLeftPoint[0] = max(round((furthestLeft * (windowWidth - widthOfProfessor/2)) - professorOffset),0)
    topLeftPoint[1] = max(round((furthestTop * (windowHeight - heightOfProfessor/2))),0)

    # (x, y, w, h) = cv2.boundingRect(c)
    # cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 20)
    # roi = frame[y:y+h, x:x+w]

    #cv2.rectangle(image,(topLeftPoint[0],topLeftPoint[1]),(topLeftPoint[0] + widthOfProfessor,topLeftPoint[1] + heightOfProfessor),(255,255,255),20)
    #cv2.circle(image, (round(windowWidth/2),round(windowHeight/2)), radius=20, color=(255, 0, 255), thickness=-1)

    professorCropped = image[topLeftPoint[1]:topLeftPoint[1] + heightOfProfessor,topLeftPoint[0]:topLeftPoint[0] + widthOfProfessor]
    blackboardCropped = imageBlackboardDetection[85:windowHeight - 80,95:windowWidth-100]

    #Find blackboard
    #imageBlackboardDetection = cv2.cvtColor(imageBlackboardDetection, cv2.COLOR_BGR2GRAY) #Turn it grayscale
    #ret, thresh = cv2.threshold(imageBlackboardDetection, 150, 255, cv2.THRESH_BINARY) #Apply binary threshold

    cv2.imshow("Blackboard", blackboardCropped)
    cv2.imshow("Professor", professorCropped)
    cv2.imshow('Main', imagePoseDetection)
    cv2.waitKey(5)

    #print("Width of professor: ", widthOfProfessor)
    #print("Height of professor: ", heightOfProfessor)
    #print("Top Left Point: ", topLeftPoint)
    #print(windowWidth,windowHeight)