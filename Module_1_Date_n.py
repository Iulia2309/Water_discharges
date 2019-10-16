#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import Date_n  # Это наш конвертированный файл дизайна
import datetime
import builtins

class DateNach(QtWidgets.QMainWindow, Date_n.Ui_Date_n):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле Date_n.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        #Выбор даты начала периода
        self.pushButton.clicked.connect(self.zapis_date_n)
        

    def zapis_date_n(self):

        builtins.date_n = self.calendarWidget.selectedDate().toPyDate()
        
        builtins.year_now = builtins.date_n.year
        builtins.month_n = int(builtins.date_n.month)
        builtins.day_n = int(builtins.date_n.day)
    
        window.close()

        


app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
window = DateNach()  # Создаём объект класса ExampleApp
window.show()  # Показываем окно
app.exec_()  # и запускаем приложение

