import cv2
import mysql
import numpy
import mysql.connector
import os

#Ket noi
mysql = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        port='3306',
        database='face'
    )


#Test connect
#print(mysql)

def Select():
    mycursorS = mysql.cursor()
    mycursorS.execute("SELECT* FROM `faces`")
    # for people in cursor:
    #for people in mycursorS:
        #print(people)
    mysql.close()

def SelectID(name):
    mycursorS = mysql.cursor()
    mycursorS.execute("SELECT ID FROM `faces` where name = '"+name+"'")
    # for people in cursor:
    for people in mycursorS:
        #print(people[0])
        return people[0]
    mysql.close()

def Insert(Name, Age, Gender, Dis):
#def Insert():
    mycursorI = mysql.cursor()
    query ="INSERT INTO `faces`(`Name`, `Age`, `Gender`, `Description`) VALUES (%s, %s, %s, %s)"
    val = (Name, Age, Gender, Dis)
    try:
        mycursorI.execute(query, val)
        mysql.commit()
        print("Insert thanh cong")
    except:
        mysql.rollback()
        print("Loi Insert.......")
        mysql.close()

name = input("Enter your Name: ")
age = input("Enter your Age: ")
gender = input("Enter your Gender: ")
description = input("Enter your Description: ")

#Select()

Insert(name, age, gender, description)

id = SelectID(name)

##print(id)
#load tv
faces_cascade = cv2.CascadeClassifier("venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)
sampleNum = 0

while(True):
    #camera ghi hinh
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faces_cascade.detectMultiScale(gray, 1.3, 5)

    for(x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (8,255,8), 2)
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        #So anh lay tang dan
        sampleNum +=1
        #Luu anh da chup khuon mat vao file du lieu
        cv2.imwrite(("DataSet/User." + str(id)+ '.' + str(sampleNum) + ".jpg"), (gray[y:y + h, x:x + w]))
        #cv2.imwrite(("DataSet/User." + str(sampleNum) + ".jpg"), (gray[y:y + h, x:x + w]))

    cv2.imshow('frame', frame)

    # wait for 100 miliseconds
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    #Thoat ra neu so luong anh nhieu hon 100
    if sampleNum>300:
        break

cap.release()
cv2.destroyAllWindows()