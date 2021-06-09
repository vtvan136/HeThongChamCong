import time
from os import environ
environ["KERAS_BACKEND"] = "plaidml.keras.backend"
import sqlite3
import cv2
import numpy as np
import self as self
import torch
from PySide2 import QtCore
from PySide2.QtCore import QTimer, QPropertyAnimation
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QApplication, QMainWindow
from facenet_pytorch import MTCNN, InceptionResnetV1
from matplotlib.pyplot import gray

from ui_main import Ui_MainWindow

from FaKeep import *
GLOBAL_STATE = 1
faceDetect = cv2.CascadeClassifier('Data/face.xml')

def face_match(img):  # img_path= location of photo, data_path= location of data.pt
    mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20)  # initializing mtcnn for face detection
    resnet = InceptionResnetV1(pretrained='vggface2').eval()
    face, prob = mtcnn(img, return_prob=True)
    emb = resnet(face.unsqueeze(0)).detach()  # detech is to make required gradient false
    saved_data = torch.load('data.pt')  # loading data.pt file
    embedding_list = saved_data[0]  # getting embedding data
    name_list = saved_data[1]  # getting list of names
    dist_list = []  # list of matched distances, minimum distance is used to identify the person
    for idx, emb_db in enumerate(embedding_list):
        dist = torch.dist(emb, emb_db).item()
        dist_list.append(dist)
    idx_min = dist_list.index(min(dist_list))
    return name_list[idx_min], min(dist_list)




class UIFunctions(QMainWindow):

    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 1:
            GLOBAL_STATE = 0
            self.showMaximized()
        else:
            GLOBAL_STATE = 1
            self.showNormal()

    def toggleMenu(self, maxWidth, enable):
        if enable:
            width = self.ui.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70

            # SET MAX WIDTH
            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard
            self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()


    def viewCam(self):
        ret, image = self.cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        faces = faceDetect.detectMultiScale(image, scaleFactor=1.3,
                                            minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            print(len(image))
            print(image.shape)
            id, dist = face_match(image)
            print(dist)
            if (dist > 0.25):
                cv2.putText(image, "Name: Unknown", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 2)
        qImg = QImage(image.data,  640,480, 1920, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label_2.setPixmap(QPixmap.fromImage(qImg))


    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture()
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.control_bt.setText("Stop")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.control_bt.setText("Start")


    def viewCam2(self ):
        ret, image = self.cap.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        faces = faceDetect.detectMultiScale(image, scaleFactor=1.3,
                                            minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        qImg = QImage(image.data,  640,480, 1920, QImage.Format_RGB888)
        self.ui.label_10.setPixmap(QPixmap.fromImage(qImg))


    def controlTimer2(self):
        if not self.timer2.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer2.start(20)
            # update control_bt text
            '''self.ui.control_bt.setText("Stop")'''
        # if timer is started
        else:
            ret, image = self.cap.read()
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", image)

            '''self.ui.control_bt.setText("Start")'''






