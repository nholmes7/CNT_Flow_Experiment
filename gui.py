# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(889, 583)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.s1c1_button = QtWidgets.QPushButton(self.centralwidget)
        self.s1c1_button.setGeometry(QtCore.QRect(40, 10, 71, 21))
        self.s1c1_button.setText("")
        self.s1c1_button.setObjectName("s1c1_button")
        self.s1c2_button = QtWidgets.QPushButton(self.centralwidget)
        self.s1c2_button.setGeometry(QtCore.QRect(10, 40, 21, 71))
        self.s1c2_button.setText("")
        self.s1c2_button.setObjectName("s1c2_button")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 40, 71, 71))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(140, 140, 71, 71))
        self.pushButton_4.setObjectName("pushButton_4")
        self.s2c2_button = QtWidgets.QPushButton(self.centralwidget)
        self.s2c2_button.setGeometry(QtCore.QRect(110, 140, 21, 71))
        self.s2c2_button.setText("")
        self.s2c2_button.setObjectName("s2c2_button")
        self.s2c1_button = QtWidgets.QPushButton(self.centralwidget)
        self.s2c1_button.setGeometry(QtCore.QRect(140, 110, 71, 21))
        self.s2c1_button.setText("")
        self.s2c1_button.setObjectName("s2c1_button")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(240, 240, 71, 71))
        self.pushButton_7.setObjectName("pushButton_7")
        self.s3c2_button = QtWidgets.QPushButton(self.centralwidget)
        self.s3c2_button.setGeometry(QtCore.QRect(210, 240, 21, 71))
        self.s3c2_button.setText("")
        self.s3c2_button.setObjectName("s3c2_button")
        self.s3c1_button = QtWidgets.QPushButton(self.centralwidget)
        self.s3c1_button.setGeometry(QtCore.QRect(240, 210, 71, 21))
        self.s3c1_button.setText("")
        self.s3c1_button.setObjectName("s3c1_button")
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(340, 340, 71, 71))
        self.pushButton_10.setObjectName("pushButton_10")
        self.s4c2_button = QtWidgets.QPushButton(self.centralwidget)
        self.s4c2_button.setGeometry(QtCore.QRect(310, 340, 21, 71))
        self.s4c2_button.setText("")
        self.s4c2_button.setObjectName("s4c2_button")
        self.s4c1_button = QtWidgets.QPushButton(self.centralwidget)
        self.s4c1_button.setGeometry(QtCore.QRect(340, 310, 71, 21))
        self.s4c1_button.setText("")
        self.s4c1_button.setObjectName("s4c1_button")
        self.pollButton = QtWidgets.QPushButton(self.centralwidget)
        self.pollButton.setGeometry(QtCore.QRect(320, 10, 89, 25))
        self.pollButton.setObjectName("pollButton")
        self.recordButton = QtWidgets.QPushButton(self.centralwidget)
        self.recordButton.setGeometry(QtCore.QRect(320, 40, 89, 25))
        self.recordButton.setObjectName("recordButton")
        self.tareButton = QtWidgets.QPushButton(self.centralwidget)
        self.tareButton.setGeometry(QtCore.QRect(320, 70, 89, 25))
        self.tareButton.setObjectName("tareButton")
        self.paramsButton = QtWidgets.QPushButton(self.centralwidget)
        self.paramsButton.setGeometry(QtCore.QRect(320, 100, 89, 25))
        self.paramsButton.setObjectName("paramsButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 430, 401, 23))
        self.progressBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 400, 111, 17))
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 490, 89, 25))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 490, 291, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 470, 111, 17))
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setObjectName("label_3")
        self.plotWidget = PlotWidget(self.centralwidget)
        self.plotWidget.setGeometry(QtCore.QRect(430, 10, 441, 371))
        self.plotWidget.setObjectName("plotWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 889, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_3.setText(_translate("MainWindow", "1"))
        self.pushButton_4.setText(_translate("MainWindow", "2"))
        self.pushButton_7.setText(_translate("MainWindow", "3"))
        self.pushButton_10.setText(_translate("MainWindow", "4"))
        self.pollButton.setText(_translate("MainWindow", "Poll"))
        self.recordButton.setText(_translate("MainWindow", "Record"))
        self.tareButton.setText(_translate("MainWindow", "Tare"))
        self.paramsButton.setText(_translate("MainWindow", "Parameters"))
        self.progressBar.setFormat(_translate("MainWindow", "%p Pa"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Pressure Drop</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Browse"))
        self.label_2.setText(_translate("MainWindow", "~/Documents/flow_experiment/data"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Save Path</span></p></body></html>"))
from pyqtgraph import PlotWidget