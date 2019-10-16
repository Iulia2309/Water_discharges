# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Regim_Program\Date_n.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Date_n(object):
    def setupUi(self, Date_n):
        Date_n.setObjectName("Date_n")
        Date_n.resize(312, 300)
        self.calendarWidget = QtWidgets.QCalendarWidget(Date_n)
        self.calendarWidget.setGeometry(QtCore.QRect(0, -5, 312, 241))
        self.calendarWidget.setObjectName("calendar_n")
        self.pushButton = QtWidgets.QPushButton(Date_n)
        self.pushButton.setGeometry(QtCore.QRect(110, 250, 93, 31))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Date_n)
        QtCore.QMetaObject.connectSlotsByName(Date_n)

    def retranslateUi(self, Date_n):
        _translate = QtCore.QCoreApplication.translate
        Date_n.setWindowTitle(_translate("Date_n", "Дата начала"))
        self.pushButton.setText(_translate("Date_n", "OK"))

