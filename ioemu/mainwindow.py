# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(440, 216)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn1 = QtWidgets.QPushButton(self.centralwidget)
        self.btn1.setGeometry(QtCore.QRect(360, 20, 71, 71))
        self.btn1.setObjectName("btn1")
        self.btn2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn2.setGeometry(QtCore.QRect(360, 130, 71, 71))
        self.btn2.setObjectName("btn2")
        self.slider = QtWidgets.QSlider(self.centralwidget)
        self.slider.setGeometry(QtCore.QRect(20, 10, 22, 191))
        self.slider.setOrientation(QtCore.Qt.Vertical)
        self.slider.setObjectName("slider")
        self.led_lbl1 = QtWidgets.QLabel(self.centralwidget)
        self.led_lbl1.setGeometry(QtCore.QRect(50, 10, 101, 201))
        self.led_lbl1.setText("")
        self.led_lbl1.setPixmap(QtGui.QPixmap("ledoff.png"))
        self.led_lbl1.setObjectName("led_lbl1")
        self.led_lbl2 = QtWidgets.QLabel(self.centralwidget)
        self.led_lbl2.setGeometry(QtCore.QRect(150, 10, 101, 201))
        self.led_lbl2.setText("")
        self.led_lbl2.setPixmap(QtGui.QPixmap("ledoff.png"))
        self.led_lbl2.setObjectName("led_lbl2")
        self.led_lbl3 = QtWidgets.QLabel(self.centralwidget)
        self.led_lbl3.setGeometry(QtCore.QRect(260, 10, 101, 201))
        self.led_lbl3.setText("")
        self.led_lbl3.setPixmap(QtGui.QPixmap("ledoff.png"))
        self.led_lbl3.setObjectName("led_lbl3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IO Emulator"))
        self.btn1.setText(_translate("MainWindow", "1"))
        self.btn2.setText(_translate("MainWindow", "2"))

