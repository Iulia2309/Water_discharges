#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import Date_k  # Это наш конвертированный файл дизайна
import datetime
import builtins

class DateNach(QtWidgets.QMainWindow, Date_k.Ui_Date_k):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле Date_n.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        #Выбор даты окончания периода
        self.pushButton.clicked.connect(self.zapis_date_k)

    def zapis_date_k(self):

        builtins.date_k = self.calendarWidget.selectedDate().toPyDate()
        builtins.month_k = int(builtins.date_k.month)
        builtins.day_k = int(builtins.date_k.day)
        
        window.close()

        builtins.T_n = int((builtins.date_k - builtins.date_n).days + 1)


app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
window = DateNach()  # Создаём объект класса ExampleApp
window.show()  # Показываем окно
app.exec_()  # и запускаем приложение

