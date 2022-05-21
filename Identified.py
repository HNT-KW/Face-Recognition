import numbers

import cv2
import numpy as np
from PIL import Image
import pickle
import mysql.connector
from screeninfo import get_monitors

#Ket noi
mysql = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        port='3306',
        database='face'
    )


faceDetect = cv2.CascadeClassifier("venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
cam = cv2.VideoCapture(0);
rec = cv2.face.LBPHFaceRecognizer_create();
rec.read("recognizer\\trainningData.yml")
id = 0
# set text style
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (203, 23, 252)
map_cursor = {}

def getMapProfile():
    mycursorS = mysql.cursor()
    mycursorS.execute("SELECT* FROM `faces`")
    for cursor in mycursorS:
        #print(people)
        map_cursor[cursor[0]] = cursor
    mysql.close()



def getProfile(id):
    mycursor = map_cursor[id]
    return mycursor

getMapProfile()
while (True):
    # camera read
    ret, img = cam.read();
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5);
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        id, conf = rec.predict(gray[y:y + h, x:x + w])
        if(conf < 40):
            profile = getProfile(id)
        # set text to window
            if (profile != None):
                # cv2.PutText(cv2.fromarray(img),str(id),(x+y+h),font,(0,0,255),2);
                cv2.putText(img, "Name: " + str(profile[1]), (x, y + h + 30), fontface, fontscale, fontcolor, 2)
                cv2.putText(img, "Age: " + str(profile[2]), (x, y + h + 60), fontface, fontscale, fontcolor, 2)
                cv2.putText(img, "Gender: " + str(profile[3]), (x, y + h + 90), fontface, fontscale, fontcolor, 2)
        else:
            cv2.putText(img, "Name: " + "None", (x, y + h + 30), fontface, fontscale, fontcolor, 2)
            cv2.putText(img, "Age: " + "None", (x, y + h + 60), fontface, fontscale, fontcolor, 2)
            cv2.putText(img, "Gender: " + "None", (x, y + h + 90), fontface, fontscale, fontcolor, 2)

    monitor = get_monitors()[0]
    monitor_height = monitor.height
    monitor_width = monitor.width
    #scale_percent = int(monitor.height * 100 / img.shape[0])  # percent of original size
    #width = int(img.shape[1] * scale_percent / 100)
    #height = int(img.shape[0] * scale_percent / 100)
    #dim = (width, height)

    # resize image
    #resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


    monitor_height = monitor_height - 20
    locate_y = int((monitor_height - img.shape[0]) / 2)
    locate_x = int((monitor_width - img.shape[1]) / 2)
    cv2.imshow('Face', img)
    cv2.moveWindow('Face', locate_x, locate_y)
    if cv2.waitKey(20) == ord('q'):
        break;
cam.release()
cv2.destroyAllWindows()