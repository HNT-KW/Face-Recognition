import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier("venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
    #cv2.CascadeClassifier("venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
    #cv2.CascadeClassifier(cv2.data.hearcascades + "haarcascade_frontalface_default.xml")
    #cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_alt.xml")
cap = cv2.VideoCapture(0)

while(True):
    #camera ghi hinh
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray)

    for(x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (8,255,8), 2)

    cv2.imshow("Detecting face", frame)
    #Doi trong 1 miligiay hoac nhan q de thoat
    if(cv2.waitKey(1) & 0xFF== ord('q')):
        break
cap.release()
cv2.destroyAllWindows()