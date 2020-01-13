#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Получение из файла ЕУВ данных о средних
суточных уровнях воды
"""
import builtins 
import os
import shutil
import math
import datetime
import csv
import re
from collections import OrderedDict

sut=datetime.timedelta(1)

builtins.daty=[builtins.date_n]
data=builtins.date_n
while data<builtins.date_k:
    data=data+sut
    builtins.daty.append(data)

with open(str(builtins.kat)+"/"+str(builtins.year_now)+"/ЕУВ.txt","r") as inf:
    euv_file=[]
    for line in inf:
        line=line.strip().split(' ')
        euv_file.append(line)
euv=[]
for i in range(2,len(euv_file)-5):
    euv.append((euv_file[i])[1:14])

m1=[]
for i in range(len(euv)):
    m1.append(euv[i][0])
m2=[]
if int(year_now)%4!=0:
    for i in range(len(euv)-3):
        m2.append(euv[i][1])
elif int(year_now)%4==0:
    for i in range(len(euv)-2):
        m2.append(euv[i][1])
m3=[]
for i in range(len(euv)):
    m3.append(euv[i][2])
m4=[]
for i in range(len(euv)-1):
    m4.append(euv[i][3])
m5=[]
for i in range(len(euv)):
    m5.append(euv[i][4])
m6=[]
for i in range(len(euv)-1):
    m6.append(euv[i][5])
m7=[]
for i in range(len(euv)):
    m7.append(euv[i][6])
m8=[]
for i in range(len(euv)):
    m8.append(euv[i][7])
m9=[]
for i in range(len(euv)-1):
    m9.append(euv[i][8])
m10=[]
for i in range(len(euv)):
    m10.append(euv[i][9])
m11=[]
for i in range(len(euv)-1):
    m11.append(euv[i][10])
m12=[]
for i in range(len(euv)):
    m12.append(euv[i][11])

euv_m=[]
euv_m.append(m1)
euv_m.append(m2)
euv_m.append(m3)
euv_m.append(m4)
euv_m.append(m5)
euv_m.append(m6)
euv_m.append(m7)
euv_m.append(m8)
euv_m.append(m9)
euv_m.append(m10)
euv_m.append(m11)
euv_m.append(m12)

euv_per=[]
if builtins.month_n != builtins.month_k:
    euv_per.append((euv_m[builtins.month_n-1])[(builtins.day_n-1):])

    for mes in range(builtins.month_n,builtins.month_k-1):
        euv_per.append(euv_m[mes])

    euv_per.append((euv_m[builtins.month_k-1])[:builtins.day_k])
else:
    euv_per.append((euv_m[builtins.month_n-1])[(builtins.day_n-1):builtins.day_k])

builtins.H_euv=[]
for mes in euv_per:
    for i in range(len(mes)):
        builtins.H_euv.append(float(mes[i]))

'''
Нижеизложенный блок используется, если в периоде отмечено
неустановившееся движение потока
'''
pattern = "неуст. движ. потока"
match = re.search(pattern, builtins.reason)
if match:
    builtins.dict_H = {}
    for i in range(len(builtins.H_euv)):
        builtins.dict_H[builtins.daty[i]] = builtins.H_euv[i]
    

    #Дата максимума паводка/половодья (если есть несколько одинаковых максимумов,
    #за дату максимума принимается первая дата

    builtins.dates_max = max(builtins.dict_H, key=builtins.dict_H.get)


else:
    pass

import Module_7_ERV_KR

