import datetime
import os
import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


from ui_splash_screen import Ui_SplashScreen
from ui_login import Ui_Form
from main import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.Btn_loggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 180, True))
        self.ui.pushButton_4.clicked.connect(lambda: exit())
        self.ui.pushButton_6.clicked.connect(lambda: self.showMinimized())
        self.ui.pushButton_5.clicked.connect(lambda:  UIFunctions.maximize_restore(self))
        self.ui.pushButton.clicked.connect(lambda: self.ui.Pages.setCurrentWidget(self.ui.PagesPage2_2))
        self.ui.pushButton_3.clicked.connect(lambda: self.logout())
        self.ui.pushButton_1.clicked.connect(lambda: self.ui.Pages.setCurrentWidget(self.ui.PagesPage1_2))
        self.ui.pushButton_7.clicked.connect(lambda: self.ui.Pages.setCurrentWidget(self.ui.page))
        '''self.timer = QTimer()
        self.timer.timeout.connect(lambda : UIFunctions.viewCam(self))'''
        self.timer2 = QTimer()
        self.timer2.timeout.connect(lambda: UIFunctions.viewCam2(self))
        self.ui.control_bt_2.clicked.connect(lambda : UIFunctions.controlTimer(self))
        self.ui.pushButton_11.clicked.connect(lambda: UIFunctions.controlTimer2(self))
        self.show()
    def logout(self):
        self.login = SplashScreen.login(self)
        self.close()

    def takeSnapshot(self):
        pass
class Login(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton.clicked.connect(lambda : self.login())
    def login(self):
        user = self.ui.lineEdit_3.text()
        password = self.ui.lineEdit_2.text()
        if user == '' and password == '':
            self.main = MainWindow()
            self.main.show()
            self.close()
        else:
            self.ui.notlogin.setText("Đăng nhập thất bại.")


counter = 0
class SplashScreen(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(35)
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))
        self.show()

    def progress(self):
        global counter
        self.ui.progressBar.setValue(counter)
        if counter > 100:
            # STOP TIMER
            self.timer.stop()
            self.login()
            self.close()
        counter += 1
    def login(self):
        self.login = Login()
        self.login.show()


if __name__ == "__main__":
    app = QApplication()
    window = SplashScreen()
    sys.exit(app.exec_())
