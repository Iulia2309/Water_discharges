# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Regim_Program\Date_k.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Date_k(object):
    def setupUi(self, Date_k):
        Date_k.setObjectName("Date_k")
        Date_k.resize(313, 300)
        self.calendarWidget = QtWidgets.QCalendarWidget(Date_k)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 0, 312, 236))
        self.calendarWidget.setObjectName("calendar_k")
        #self.calendarWidget.setSelectedDate(QtCore.QDate(builtins.year_cal_2,builtins.month_cal_2,builtins.day_cal_2))
        self.pushButton = QtWidgets.QPushButton(Date_k)
        self.pushButton.setGeometry(QtCore.QRect(110, 250, 93, 31))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Date_k)
        QtCore.QMetaObject.connectSlotsByName(Date_k)

    def retranslateUi(self, Date_k):
        _translate = QtCore.QCoreApplication.translate
        Date_k.setWindowTitle(_translate("Date_k", "Дата окончания"))
        self.pushButton.setText(_translate("Date_k", "OK"))

