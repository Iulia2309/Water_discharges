#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Запись ЕРВ, вычисленных методом оптимальной интерполяции,
в отдельный текстовый файл
"""
import builtins 
import os
import shutil
import math
import numpy
import datetime
import csv
import re
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

ouf=open(str(builtins.kat)+"/"+str(builtins.year_now)+"/"+"ЕРВ "+builtins.reason+" опт.инт..txt","w")

with open(str(builtins.kat)+"/"+str(builtins.year_now)+"/"+"ЕРВ "+builtins.reason+" опт.инт..txt","r+") as ouf:
    ouf.write(str(builtins.kod_gp)+' '+builtins.nazv_gp+'\n')
    ouf.write(str(builtins.year_now)+'\n')

    m=[['-' for i in range(31)]for j in range(12)]
    
    if year_now%4==0:
        d_v_m=[31,29,31,30,31,30,31,31,30,31,30,31]
    else:
        d_v_m=[31,28,31,30,31,30,31,31,30,31,30,31]

    if builtins.month_n != builtins.month_k:
   
        j=builtins.month_n-1
        for i in range(builtins.day_n-1,d_v_m[j]):
            m[j][i]=builtins.Q_erv_oi_list[-builtins.day_n+i+1]
            
        k=d_v_m[builtins.month_n-1]
        for j in range(builtins.month_n,builtins.month_k-1):
            for i in range(d_v_m[j]):
                m[j][i]=builtins.Q_erv_oi_list[-builtins.day_n+k+i+1]
           
            k+=d_v_m[j]
            
        j=builtins.month_k-1
        for i in range(builtins.day_k):
            m[j][i]=builtins.Q_erv_oi_list[-builtins.day_n+k+i+1]

    else:
        j=builtins.month_n-1
        for i in range(builtins.day_n-1,builtins.day_k):
            m[j][i]=builtins.Q_erv_oi_list[-builtins.day_n+i+1]

    for i in range(31):
        if len(str(i+1)) == 1:
            ouf.write(str(i+1)+3*' ')
        elif len(str(i+1)) == 2:
            ouf.write(str(i+1)+2*' ')
        for j in range(12):
            if len(str(m[j][i])) == 1:
                ouf.write(str(m[j][i])+5*' ')
            elif len(str(m[j][i])) == 2:
                ouf.write(str(m[j][i])+4*' ')
            elif len(str(m[j][i])) == 3:
                ouf.write(str(m[j][i])+3*' ')
            elif len(str(m[j][i])) == 4:
                ouf.write(str(m[j][i])+2*' ')     
        ouf.write('\n')

#Строим гидрограф
hydrograph = plt.figure(figsize=(8, 6)) 

#наносим на гидрограф ИРВ
x_1 = builtins.dates_irv
y_1 = builtins.Q_izm

#наносим на гидрограф ЕРВ, вычисленные по методу оптимальной интерполяции
x_2 = builtins.daty
y_2 = builtins.Q_erv_oi_list
        
#название графика и подписи осей
plt.title("Гидрограф периода "+builtins.reason+" "+str(builtins.year_now)+" г.")
plt.xlabel("Даты")
plt.ylabel("Q,куб.м/с")

#представляем точки (х,у) кружочками диаметра 10
plt.scatter(x_1, y_1, color='b', s=10)
plt.plot(x_2, y_2, 'c')
 
#Сетка
plt.grid(True, linestyle='-', color='0.75')

#Сохраняем гидрограф в папке расчетного года
plt.savefig(fname=str(builtins.kat)+"/"+str(builtins.year_now)+"/"+"Гидрограф периода "+\
            builtins.reason+".png", fmt="png")

#показываем гидрограф
plt.show()

QMessageBox.information(None, "Информация","Расчёт  ЕРВ за период "+builtins.reason+" завершён!"+"\n"
                    "Посмотрите таблицу рассчитанных ежедневных расходов воды "\
                    "(файл ЕРВ "+builtins.reason+" опт.инт. в папке поста "+str(builtins.kod_gp)+\
                    " за "+str(builtins.year_now)+" год)")

                  




