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

#Вычисляем значение расхода воды по опорной КР для уровня воды при измерении расхода
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
   

builtins.q = []
for i in range(len(builtins.Q_KR_izm)):

    q_i = (builtins.Q_izm[i] - builtins.Q_KR_izm[i])/builtins.Q_KR_izm[i]
    builtins.q.append(q_i)

sum_sqr = 0
for i in range(len(builtins.q)):
    sum_sqr = sum_sqr + builtins.q[i]**2

builtins.mera_pogr = (builtins.error/100)**2/((sum_sqr/(len(builtins.q)-builtins.st_sv))-(builtins.error/100)**2)
                                  

builtins.q_dates=dict(zip(builtins.dates_irv,builtins.q))

import Module_6_EUV


