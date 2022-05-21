import cv2
import numpy as np
import os
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'DataSet'

def getImagesAndLabels(path):
    #Lay duong dan cua du lieu anh trong thu muc
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    print(imagePaths)

    faces=[]
    IDs=[]

    for imagePath in imagePaths:
        faceImg=Image.open(imagePath).convert('L')
        faceNp=np.array(faceImg,'uint8')
        print(faceNp)
        #Cat de lay ID cua hinh anh
        ID=int(os.path.split(imagePath)[-1].split('.')[1])

        faces.append(faceNp)
        print(ID)
        IDs.append(ID)

        cv2.imshow('trainning',faceNp)
        cv2.waitKey(10)
    return faces,IDs

faces, IDs = getImagesAndLabels(path)

#trainning
recognizer.train(faces, np.array(IDs))

#Luu vao phai
#if not os.path.exists('recognizer'):
#    os.makedirs('recognizer')

recognizer.save('recognizer/trainningData.yml')
cv2.destroyAllWindows()