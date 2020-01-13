#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''Программа позволяет вычислить режимные ЕРВ в заданном периоде
в условиях нарушения однозначности связи Q(H)
используя метод оптимальной интерполяции относительных отклонений ИРВ
от принятой опорной КР (МКР)
'''
import builtins 
import os
import shutil
import math
import numpy
import datetime
import csv
import re
from collections import OrderedDict
import matplotlib.pyplot as plt
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import Prog_Form  # Это наш конвертированный файл дизайна

class Optimal(QtWidgets.QMainWindow, Prog_Form.Ui_Regim):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле Prog_Form.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        #Выбор рабочего каталога, где хранится БД Сток для данного ГП
        self.pushButton.clicked.connect(self.kat_choise)

        #Выбор опорной КР
        self.radioButton.toggled.connect(self.opor_KR)
        self.radioButton_2.toggled.connect(self.opor_KR)

        #Выбор причины нарушения однозначности связи Q(H)
        self.checkBox.toggled.connect(self.reasons)
        self.checkBox_2.toggled.connect(self.reasons)
        self.checkBox_3.toggled.connect(self.reasons)
        self.checkBox_4.toggled.connect(self.reasons)
        self.checkBox_5.toggled.connect(self.reasons)
        
        #Выбор даты начала периода
        self.pushButton_2.clicked.connect(self.d_n)

        #Выбор даты окончания периода
        self.pushButton_3.clicked.connect(self.d_k)

        #Ввод погрешности ИРВ
        self.lineEdit.textChanged.connect(self.pogr_IRV)

        #Кнопка начала вычислений ЕРВ
        self.pushButton_4.clicked.connect(self.calc_ERV)

    def kat_choise(self):

        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории
        
        builtins.kat = directory
        
        builtins.kod_gp = builtins.kat[-5:]

        #Из файла "пост" папки выбранного поста вытаскиваем название поста
        with open(builtins.kat+"/пост.txt","r") as inf:
            s1 = inf.readline().strip()
            s2 = inf.readline().strip()
            builtins.nazv_gp = 'р. '+s1+' - '+s2
            
        QMessageBox.information(None, "Информация","Выбран ГП "+builtins.kod_gp+" "+builtins.nazv_gp)

        self.pushButton.setStyleSheet("""QPushButton:!hover { background-color: light grey  }""")

        self.radioButton.setEnabled(True)
        self.radioButton_2.setEnabled(True)

        self.radioButton.setStyleSheet("""QRadioButton:!hover { background-color: rgb(0, 255, 0);  }""")
        self.radioButton_2.setStyleSheet("""QRadioButton:!hover { background-color: rgb(0, 255, 0);  }""") 


    def opor_KR(self, button):
        
        if self.radioButton.isChecked():
            self.radioButton.setStyleSheet("""QRadioButton:!hover { background-color: light grey }""")
            self.radioButton_2.setStyleSheet("""QRadioButton:!hover { background-color: light grey  }""")

            self.comboBox.setEnabled(True)

            try:
                #Выбор года
                #Открываем папку выбранного поста и выбираем год, по которому берётся опорная КР
                self.goda = []        
                for i in os.listdir(builtins.kat):
                    if str(i).isdigit():
                        self.goda.append(i)
                        self.comboBox.addItem(i)

                self.comboBox.setStyleSheet("""QComboBox:!hover { background-color: rgb(0, 255, 0); }
                QComboBox:pressed { background-color: light grey }""")

                self.comboBox.activated[str].connect(self.par_opor_gKR)
                                
                
                
            except AttributeError:
                
                QMessageBox.critical(None, 'Ошибка!', "Выберите пост!")
                self.pushButton.setStyleSheet("""QPushButton:!hover { background-color: red  }""")
            
        elif self.radioButton_2.isChecked():
            
            self.radioButton.setStyleSheet("""QRadioButton:!hover { background-color: light grey }""")
            self.radioButton_2.setStyleSheet("""QRadioButton:!hover { background-color: light grey  }""") 

            #Определяем текущий год
            d = datetime.date.today()
            builtins.y_today = str(d.year)
            
            #Открываем файл МНКР в папке выбранного поста и считываем параметры МКР
            try: 
                with open(builtins.kat+"/МНКР.txt","r") as inf:
                    mkr_file=[]
                    for line in inf:
                        line=line.strip().split()
                        mkr_file.append(line)
 
                s = (mkr_file[3])[1]

                #Вытаскиваем из файла МНКР.txt сведения о годах, по которым построена МКР
                builtins.years_mkr = []

                for i in range(len(s)-1):
                    if (s[i]+s[i+1]).isdigit():
                        if 0 <= int(s[i]+s[i+1]) < int(builtins.y_today):
                            builtins.years_mkr.append('20'+(s[i]+s[i+1]))
                        elif int(builtins.y_today) <=  int(s[i]+s[i+1]) <= 99:
                            builtins.years_mkr.append('19'+(s[i]+s[i+1]))
            
                for j in range(len(s)):     
                    if s[j] == '-':
                        if (s[j-2]+s[j-1]).isdigit() and (s[j+1]+s[j+2]).isdigit():
                            g_nach = int(s[j-2]+s[j-1])
                            g_kon = int(s[j+1]+s[j+2])
                            if 0 <= g_nach < int(builtins.y_today):
                                if len(str(g_nach)) == 1:
                                    g_nach = '200'+ str(g_nach)
                                elif len(str(g_nach)) == 2:
                                    g_nach = '20'+ str(g_nach)
                            elif int(builtins.y_today) <= g_nach <= 99:
                                g_nach = '19'+ str(g_nach)
                            if 0 <= g_kon < int(builtins.y_today):
                                if len(str(g_kon)) == 1:
                                    g_kon = '200'+ str(g_kon)
                                elif len(str(g_kon)) == 2:
                                    g_kon = '20'+ str(g_kon)
                            elif int(builtins.y_today) <= g_kon <= 99:
                                g_kon = '19'+ str(g_kon)
                            if int(g_kon) - int(g_nach) > 1:
                                for k in range(int(g_nach)+1,int(g_kon)):
                                    builtins.years_mkr.append(str(k))
            
                builtins.years_mkr.sort()                
                years_str=''
                for y in range(len(builtins.years_mkr)-1):
                    years_str += years_mkr[y]+', '
                years_str += builtins.years_mkr[len(builtins.years_mkr)-1]
                
                QMessageBox.information(None, "Информация","Многолетняя КР за " + years_str + " годы")

                self.checkBox.setEnabled(True)
                self.checkBox_2.setEnabled(True)
                self.checkBox_3.setEnabled(True)
                self.checkBox_4.setEnabled(True)
                self.checkBox_5.setEnabled(True)

                self.checkBox.setStyleSheet("""QCheckBox:!hover { background-color: rgb(0, 255, 0); }""")
                self.checkBox_2.setStyleSheet("""QCheckBox:!hover { background-color: rgb(0, 255, 0); }""")
                self.checkBox_3.setStyleSheet("""QCheckBox:!hover { background-color: rgb(0, 255, 0); }""")
                self.checkBox_4.setStyleSheet("""QCheckBox:!hover { background-color: rgb(0, 255, 0); }""")
                self.checkBox_5.setStyleSheet("""QCheckBox:!hover { background-color: rgb(0, 255, 0); }""")

                #Записываем параметры опорной МКР: диапазоны уровней и коэффициенты
                builtins.par_KR=[]

                pattern = r":"
                for i in range(1,len(mkr_file)):
                    if i%3 == 0:
                        builtins.par_KR.append((mkr_file[i-2])[3:5])
                        iskl = 0
                        for j in range(len(mkr_file[i-1])):
                            if re.search(pattern, (mkr_file[i-1])[j]):
                                iskl += 1
                                par = (mkr_file[i-1])[:j]
                                par.append(((mkr_file[i-1])[j].split(":"))[0])
                                builtins.par_KR.append(par)
                         
                        if iskl == 1:
                            pass
                        elif iskl == 0:
                            builtins.par_KR.append(mkr_file[i-1])

                st_sv_l=[]
                for llne in builtins.par_KR:
                    st_sv_l.append(len(line))

                builtins.st_sv=max(st_sv_l)
                        

            except AttributeError:
                
                QMessageBox.critical(None, 'Ошибка!', "Выберите пост!")
                self.pushButton.setStyleSheet("""QPushButton:!hover { background-color: red  }""")

            except FileNotFoundError:
                
                 QMessageBox.critical(None, "Ошибка!", "Файл параметров МКР не найден!"+"\n"+
                                      "Зайдите в программу Речной Сток,"+"\n"+
                                      "постройте МКР и запишите её параметры в Базу Данных!")


    def par_opor_gKR(self):

        self.comboBox.setStyleSheet("""QComboBox:!hover { background-color: light grey  }""")

        self.checkBox.setEnabled(True)
        self.checkBox_2.setEnabled(True)
        self.checkBox_3.setEnabled(True)
        self.checkBox_4.setEnabled(True)
        self.checkBox_5.setEnabled(True)

        self.checkBox.setStyleSheet("""QCheckBox:!hover { background-color: rgb(0, 255, 0); }""")
        self.checkBox_2.setStyleSheet("""QCheckBox:!hover { background-color: rgb(0, 255, 0); }""")
        self.checkBox_3.setStyleSheet("""QCheckBox:!hover { background-color: rgb(0, 255, 0); }""")
        self.checkBox_4.setStyleSheet("""QCheckBox:!hover { background-color: rgb(0, 255, 0); }""")
        self.checkBox_5.setStyleSheet("""QCheckBox:!hover { background-color: rgb(0, 255, 0); }""")


        builtins.opor_year = self.comboBox.currentText()

        #Открываем файл КР в папке выбранного года и считываем параметры годовой КР
        try:
            with open(builtins.kat+"/"+builtins.opor_year+"/КР.txt","r") as inf:
                KR_file = []
                for line in inf:
                    line=line.strip().split()
                    KR_file.append(line)
  
            builtins.par_KR=[]
            for i in range(2,len(KR_file)):
                if i%2!=0:
                    if len(KR_file[i]) == 5:
                        if float((KR_file[i])[2]) >= 10.0:
                            #Прямая линия
                            builtins.par_KR.append((KR_file[i])[1:-2])
                            pattern = r"годовая"
                            repl = ""
                            (KR_file[i])[3] = re.sub(pattern,repl,(KR_file[i])[3])
                            builtins.par_KR.append((KR_file[i])[1:-1]+['Glushkov'])
                    else:
                        builtins.par_KR.append((KR_file[i])[1:-2])
                else:
                    builtins.par_KR.append((KR_file[i])[5:7])

            if len(builtins.par_KR) == 2:
                builtins.st_sv=len(builtins.par_KR[1])
            elif len(builtins.par_KR) > 2:
                st_sv_l=[]
                for i in range(1,len(builtins.par_KR),2):
                    st_sv_l.append(len(builtins.par_KR[i]))

                builtins.st_sv=max(st_sv_l)

            import Module_3_Extrapolation

      
        except FileNotFoundError:
             QMessageBox.critical(None, "Ошибка!", "Файл параметров КР "+builtins.opor_year+" года не найден!"+"\n"+
                                  "Зайдите в программу Речной Сток, постройте КР "+builtins.opor_year+" года"+"\n"+
                                  "и запишите её параметры в Базу Данных!")
   
    def reasons(self):
        self.checkBox.setStyleSheet("""QCheckBox:!hover { background-color: light grey }""")
        self.checkBox_2.setStyleSheet("""QCheckBox:!hover { background-color: light grey }""")
        self.checkBox_3.setStyleSheet("""QCheckBox:!hover { background-color: light grey }""")
        self.checkBox_4.setStyleSheet("""QCheckBox:!hover { background-color: light grey }""")
        self.checkBox_5.setStyleSheet("""QCheckBox:!hover { background-color: light grey }""")

        self.pushButton_2.setEnabled(True)
        self.pushButton_2.setStyleSheet("""QPushButton:!hover { background-color: rgb(0, 255, 0); }""")

    def d_n(self):

        QMessageBox.about(None, 'Указание', "Выберите дату начала периода!")

        import Module_1_Date_n
        
        self.pushButton_2.setStyleSheet("""QPushButton:!hover { background-color: light grey }""")

        self.pushButton_3.setEnabled(True)
        self.pushButton_3.setStyleSheet("""QPushButton:!hover { background-color: rgb(0, 255, 0); }""")
            

    def d_k(self):

        QMessageBox.about(None, 'Указание', "Выберите дату окончания периода!")

        import Module_2_Date_k

        self.pushButton_3.setStyleSheet("""QPushButton:!hover { background-color: light grey }""")

        self.lineEdit.setEnabled(True)
        self.lineEdit.setStyleSheet("""QLineEdit:!hover { background-color: rgb(0, 255, 0); }""")

    def pogr_IRV(self):
        if self.lineEdit.text() != "":
            self.lineEdit.setStyleSheet("""QLineEdit:!hover { background-color: white }""")

            self.pushButton_4.setEnabled(True)
            self.pushButton_4.setStyleSheet("""QPushButton:!hover { background-color: rgb(0, 255, 0); }""")

    def calc_ERV(self):

        if self.checkBox.isChecked() and self.checkBox_2.isChecked() and self.checkBox_3.isChecked():

            builtins.reason = "неуст. движ. потока, перем. подпора и деформ. русла"

        elif self.checkBox.isChecked() and self.checkBox_2.isChecked():

            builtins.reason = "неуст. движ. потока и перем. подпора"

        elif self.checkBox.isChecked() and self.checkBox_3.isChecked():

            builtins.reason = "неуст. движ. потока и деформ. русла" 

        elif self.checkBox_2.isChecked() and self.checkBox_3.isChecked():

            builtins.reason = "перем. подпора и деформ. русла"

        elif self.checkBox.isChecked():
            
            builtins.reason = "неуст. движ. потока"
            
        elif self.checkBox_2.isChecked():

            builtins.reason = "перем. подпора"
            
        elif self.checkBox_3.isChecked():

            builtins.reason = "деформ. русла"
            
        elif self.checkBox_4.isChecked():

            builtins.reason = "зараст. русла"

        elif self.checkBox_5.isChecked():

            builtins.reason = "лед. явл."    

        builtins.error = float(self.lineEdit.text())

        self.pushButton_4.setStyleSheet("""QPushButton:!hover { background-color: light grey }""")


        import Module_4_IRV

        self.close()
        sys.exit()


        
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Optimal()  # Создаём объект класса Optimal
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

    


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
