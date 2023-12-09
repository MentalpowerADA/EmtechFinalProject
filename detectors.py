import cv2
import numpy as np
import os
import errno
import sys
import csv
directory = r'C:\Users\janss\OneDrive\Desktop\ActivityDatabase\ActivityFaceDataset\paul'

def faceDetect(src, dst):
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            img = cv2.rectangle(src,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.merge(src,dst)

def read_images(path):
        c = 0
        X, y = [], []
        for filename in os.listdir(path):
            if filename.endswith('.pgm'):
                filepath = os.path.join(path, filename)
                im = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                X.append(np.asarray(im, dtype=np.uint8))
                y.append(c)
                c += 1
        return [X, y]

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
names = ['Paul', 'Paul']  # Put your names here for faces to recognize
[X, y] = read_images(directory)
y = np.asarray(y, dtype=np.int32)
model = cv2.face.LBPHFaceRecognizer_create()
model.train(X, y)

def face_rec(src, dst, status):
    names = ['Paul', 'Paul']
    faces = face_cascade.detectMultiScale(src, 1.3, 5)
    cv2.putText(src, "Face Biometrics", ((int(src.shape[0] / 2)) - 15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    if (status == 4):
        cv2.putText(src, "Too many failed attempts!!", ((int(src.shape[0] / 2)) - 15, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    if (status == 3):
        cv2.putText(src, "Scanning face...", ((int(src.shape[0] / 2)) - 15, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    if (status == 1):
        cv2.putText(src, "Face Recognized", ((int(src.shape[0] / 2)) - 15, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    if (status == 2):
        cv2.putText(src, "Scan Failed: No Face Recognized", ((int(src.shape[0] / 2)) - 15, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    for (x, y, w, h) in faces:
            gray = cv2.cvtColor(src[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY)
            roi = cv2.resize(gray, (200, 200), interpolation=cv2.INTER_LINEAR)

            try:
                params = model.predict(roi)
                if (params[0] != 0 and params[1] < 50):
                    cv2.rectangle(src, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    label = names[0]
                    #cv2.putText(src, label + ", " + str(params[1]), (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    ret = True
                else:
                    cv2.rectangle(src, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    #cv2.putText(src, "???", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    ret = False
            except:
                continue
            cv2.merge(src,dst)
            if (ret == True):
                return 1
            else:
                return 0
