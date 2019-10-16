# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Regim_Program\Prog_Form.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

class Ui_Regim(object):
    def setupUi(self, Regim):
        Regim.setObjectName("Regim")
        Regim.setEnabled(True)
        Regim.resize(552, 565)
        
        self.pushButton = QtWidgets.QPushButton(Regim)
        self.pushButton.setGeometry(QtCore.QRect(330, 30, 111, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("""QPushButton:!hover { background-color: rgb(0, 255, 0); }
        QPushButton:pressed { background-color: white }""")
        
        self.label = QtWidgets.QLabel(Regim)
        self.label.setGeometry(QtCore.QRect(20, 10, 281, 71))
        self.label.setAutoFillBackground(False)
        self.label.setWordWrap(True)
        self.label.setOpenExternalLinks(False)
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(Regim)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 271, 51))
        self.label_2.setObjectName("label_2")
        
        self.label_3 = QtWidgets.QLabel(Regim)
        self.label_3.setGeometry(QtCore.QRect(20, 160, 271, 51))
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        
        self.label_4 = QtWidgets.QLabel(Regim)
        self.label_4.setGeometry(QtCore.QRect(20, 330, 291, 61))
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        
        self.label_5 = QtWidgets.QLabel(Regim)
        self.label_5.setGeometry(QtCore.QRect(20, 410, 291, 81))
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        
        self.radioButton = QtWidgets.QRadioButton(Regim)
        self.radioButton.setGeometry(QtCore.QRect(330, 100, 101, 21))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setEnabled(False)

        self.comboBox = QtWidgets.QComboBox(Regim)
        self.comboBox.setGeometry(QtCore.QRect(450, 100, 81, 25))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setEnabled(False)
        
        self.radioButton_2 = QtWidgets.QRadioButton(Regim)
        self.radioButton_2.setGeometry(QtCore.QRect(330, 130, 111, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.setEnabled(False)
        
        self.checkBox = QtWidgets.QCheckBox(Regim)
        self.checkBox.setGeometry(QtCore.QRect(330, 170, 201, 21))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setEnabled(False)
        
        self.checkBox_2 = QtWidgets.QCheckBox(Regim)
        self.checkBox_2.setGeometry(QtCore.QRect(330, 200, 151, 20))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.setEnabled(False)
        
        self.checkBox_3 = QtWidgets.QCheckBox(Regim)
        self.checkBox_3.setGeometry(QtCore.QRect(330, 230, 151, 20))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.setEnabled(False)
        
        self.checkBox_4 = QtWidgets.QCheckBox(Regim)
        self.checkBox_4.setGeometry(QtCore.QRect(330, 260, 131, 20))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_4.setEnabled(False)
        
        self.checkBox_5 = QtWidgets.QCheckBox(Regim)
        self.checkBox_5.setGeometry(QtCore.QRect(330, 290, 141, 20))
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_5.setEnabled(False)
        
        self.pushButton_2 = QtWidgets.QPushButton(Regim)
        self.pushButton_2.setGeometry(QtCore.QRect(330, 350, 161, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setEnabled(False)
        
        self.pushButton_3 = QtWidgets.QPushButton(Regim)
        self.pushButton_3.setGeometry(QtCore.QRect(330, 390, 161, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setEnabled(False)
        
        self.pushButton_4 = QtWidgets.QPushButton(Regim)
        self.pushButton_4.setGeometry(QtCore.QRect(180, 500, 191, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setEnabled(False)
        
        self.lineEdit = QtWidgets.QLineEdit(Regim)
        self.lineEdit.setGeometry(QtCore.QRect(330, 440, 50, 31))
        self.lineEdit.setObjectName("listWidget")
        self.lineEdit.setEnabled(False)

        self.retranslateUi(Regim)
        QtCore.QMetaObject.connectSlotsByName(Regim)

    def retranslateUi(self, Regim):
        _translate = QtCore.QCoreApplication.translate
        Regim.setWindowTitle(_translate("Regim", "Ввод данных"))
        self.pushButton.setText(_translate("Regim", "Выбрать"))
        self.label.setText(_translate("Regim", "1)Выберите папку с Базой Данных программы РЕЧНОЙ СТОК для нужного поста"))
        self.label_2.setText(_translate("Regim", "2)Выберите опорную кривую расходов"))
        self.label_3.setText(_translate("Regim", "3)Выберите причину (причины) нарушения однозначности связи Q(H)"))
        self.label_4.setText(_translate("Regim", "4)Выберите даты начала и окончания периода нарушения однозначности связи Q(H)"))
        self.label_5.setText(_translate("Regim", "5)Введите величину погрешности измерения расходов в расчетном периоде в процентах"))
        self.radioButton.setText(_translate("Regim", "Годовая"))
        self.radioButton_2.setText(_translate("Regim", "Многолетняя"))
        self.checkBox.setText(_translate("Regim", "Неустановившееся движение"))
        self.checkBox_2.setText(_translate("Regim", "Переменный подпор"))
        self.checkBox_3.setText(_translate("Regim", "Деформация русла"))
        self.checkBox_4.setText(_translate("Regim", "Зарастание русла"))
        self.checkBox_5.setText(_translate("Regim", "Ледовые явления"))
        self.pushButton_2.setText(_translate("Regim", "Дата начала периода"))
        self.pushButton_3.setText(_translate("Regim", "Дата окончания периода"))
        self.pushButton_4.setText(_translate("Regim", "Вычислить режимные ЕРВ"))

