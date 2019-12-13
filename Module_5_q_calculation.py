#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Вычисление относительных отклонений ИРВ расчетного года от опорной КР
import builtins 
import os
import shutil
import math
import datetime
import csv
import re
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

#Вычисляем значение расхода воды по опорной КР для уровня воды при измерении расхода
#для всех ИРВ, даже если есть 2 и более за одни сутки
builtins.Q_KR_izm = []
if len(builtins.par_KR) == 2:
    builtins.H_min = float((builtins.par_KR[0])[0])
    builtins.H_max = float((builtins.par_KR[0])[1])
    for i in range(len(builtins.H_izm)):
        if builtins.H_min <= builtins.H_izm[i]/100 <= builtins.H_max:
            if len(builtins.par_KR[1]) != 4:
                Q_KR_izm_i = 0
                for k in range(len(builtins.par_KR[1])):
                    Q_KR_izm_i += float((builtins.par_KR[1])[k])*(builtins.H_izm[i]/100)**k
            elif len(builtins.par_KR[1]) == 4 and (builtins.par_KR[1])[3] != 'Glushkov':
                Q_KR_izm_i = 0
                for k in range(len(builtins.par_KR[1])):
                    Q_KR_izm_i += float((builtins.par_KR[1])[k])*(builtins.H_izm[i]/100)**k
            elif len(builtins.par_KR[1]) == 4 and (builtins.par_KR[1])[3] == 'Glushkov':
                Q_KR_izm_i = float((builtins.par_KR[j+1])[0])*(builtins.H_izm[i]/100\
                             - float((builtins.par_KR[1])[2]))**float((builtins.par_KR[1])[1])
            Q_KR_izm.append(Q_KR_izm_i)
    

elif len(builtins.par_KR) > 2:
    builtins.H_min = float((builtins.par_KR[0])[0])
    builtins.H_max = float((builtins.par_KR[len(builtins.par_KR)-2])[1])
    for i in range(len(builtins.H_izm)):
        if builtins.H_min <= builtins.H_izm[i]/100 <= builtins.H_max:
            for j in range(0,len(builtins.par_KR),2):
                H_min = float((builtins.par_KR[j])[0])
                H_max = float((builtins.par_KR[j])[1])
                if H_min <= builtins.H_izm[i]/100 <= H_max:
                    if len(builtins.par_KR[j+1]) != 4:
                        Q_KR_izm_i = 0
                        for k in range(len(builtins.par_KR[j+1])):
                            Q_KR_izm_i += float((builtins.par_KR[j+1])[k])*(builtins.H_izm[i]/100)**k
                    elif len(builtins.par_KR[j+1]) == 4 and (builtins.par_KR[j+1])[3] != 'Glushkov':
                        Q_KR_izm_i = 0
                        for k in range(len(builtins.par_KR[j+1])):
                            Q_KR_izm_i += float((builtins.par_KR[j+1])[k])*(builtins.H_izm[i]/100)**k
                    elif len(builtins.par_KR[j+1]) == 4 and (builtins.par_KR[j+1])[3] == 'Glushkov':
                        Q_KR_izm_i = float((builtins.par_KR[j+1])[0])*(builtins.H_izm[i]/100\
                                    - float((builtins.par_KR[j+1])[2]))**float((builtins.par_KR[j+1])[1])
        Q_KR_izm.append(Q_KR_izm_i)
   

builtins.q_mp = []
for i in range(len(builtins.Q_KR_izm)):

    q_i = (builtins.Q_izm[i] - builtins.Q_KR_izm[i])/builtins.Q_KR_izm[i]
    builtins.q_mp.append(q_i)

print(builtins.q_mp)
sum_sqr = 0
for i in range(len(builtins.q_mp)):
    sum_sqr = sum_sqr + builtins.q_mp[i]**2

builtins.mera_pogr = (builtins.error/100)**2/((sum_sqr/(len(builtins.q_mp)-1))-(builtins.error/100)**2)
print(builtins.mera_pogr)

if builtins.mera_pogr <= 0 or builtins.mera_pogr >= 1:
    QMessageBox.information(None, 'Информация', "Расчет ЕРВ за выбранный период " \
                            "по методу оптимальной интерполяции невозможен! "\
                            "Выполните расчет ЕРВ за выбранный период в программе РЕЧНОЙ СТОК")

    raise SystemExit

#Для дальнейших расчетов будем использовать осредненные значения Qизм и Hизм за сутки,
#когда было 2 и более ИРВ
builtins.Q_KR_izm = []
if len(builtins.par_KR) == 2:
    builtins.H_min = float((builtins.par_KR[0])[0])
    builtins.H_max = float((builtins.par_KR[0])[1])
    for i in range(len(builtins.H_izm_r)):
        if builtins.H_min <= builtins.H_izm_r[i]/100 <= builtins.H_max:
            if len(builtins.par_KR[1]) != 4:
                Q_KR_izm_i = 0
                for k in range(len(builtins.par_KR[1])):
                    Q_KR_izm_i += float((builtins.par_KR[1])[k])*(builtins.H_izm_r[i]/100)**k
            elif len(builtins.par_KR[1]) == 4 and (builtins.par_KR[1])[3] != 'Glushkov':
                Q_KR_izm_i = 0
                for k in range(len(builtins.par_KR[1])):
                    Q_KR_izm_i += float((builtins.par_KR[1])[k])*(builtins.H_izm_r[i]/100)**k
            elif len(builtins.par_KR[1]) == 4 and (builtins.par_KR[1])[3] == 'Glushkov':
                Q_KR_izm_i = float((builtins.par_KR[j+1])[0])*(builtins.H_izm_r[i]/100\
                             - float((builtins.par_KR[1])[2]))**float((builtins.par_KR[1])[1])
            Q_KR_izm.append(Q_KR_izm_i)
    

elif len(builtins.par_KR) > 2:
    builtins.H_min = float((builtins.par_KR[0])[0])
    builtins.H_max = float((builtins.par_KR[len(builtins.par_KR)-2])[1])
    for i in range(len(builtins.H_izm_r)):
        if builtins.H_min <= builtins.H_izm_r[i]/100 <= builtins.H_max:
            for j in range(0,len(builtins.par_KR),2):
                H_min = float((builtins.par_KR[j])[0])
                H_max = float((builtins.par_KR[j])[1])
                if H_min <= builtins.H_izm_r[i]/100 <= H_max:
                    if len(builtins.par_KR[j+1]) != 4:
                        Q_KR_izm_i = 0
                        for k in range(len(builtins.par_KR[j+1])):
                            Q_KR_izm_i += float((builtins.par_KR[j+1])[k])*(builtins.H_izm_r[i]/100)**k
                    elif len(builtins.par_KR[j+1]) == 4 and (builtins.par_KR[j+1])[3] != 'Glushkov':
                        Q_KR_izm_i = 0
                        for k in range(len(builtins.par_KR[j+1])):
                            Q_KR_izm_i += float((builtins.par_KR[j+1])[k])*(builtins.H_izm_r[i]/100)**k
                    elif len(builtins.par_KR[j+1]) == 4 and (builtins.par_KR[j+1])[3] == 'Glushkov':
                        Q_KR_izm_i = float((builtins.par_KR[j+1])[0])*(builtins.H_izm_r[i]/100\
                                    - float((builtins.par_KR[j+1])[2]))**float((builtins.par_KR[j+1])[1])
        Q_KR_izm.append(Q_KR_izm_i)
   

builtins.q = []
for i in range(len(builtins.Q_KR_izm)):

    q_i = (builtins.Q_izm_r[i] - builtins.Q_KR_izm[i])/builtins.Q_KR_izm[i]
    builtins.q.append(q_i)

builtins.q_dates=dict(zip(builtins.dates_irv_r,builtins.q))
print(builtins.q_dates)

import Module_6_EUV


