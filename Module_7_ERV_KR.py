#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Расчёт ежедневных расходов воды по выбранной опорной КР
и средним суточным значениям уровней воды
"""
import builtins 
import os
import shutil
import math
import datetime
import csv
import re
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

#Вычисляем значение расхода воды по опорной КР для каждого ЕУВ
builtins.Q_KR = []
if len(builtins.par_KR) == 2:
    builtins.H_min = float((builtins.par_KR[0])[0])
    builtins.H_max = float((builtins.par_KR[0])[1])
    for i in range(len(builtins.H_euv)):
        if builtins.H_min <= builtins.H_euv[i]/100 <= builtins.H_max:
            if len(builtins.par_KR[1]) != 4:
                Q_KR_i = 0
                for k in range(len(builtins.par_KR[1])):
                    Q_KR_i += float((builtins.par_KR[1])[k])*((builtins.H_euv[i]/100)**k)
            elif len(builtins.par_KR[1]) == 4 and (builtins.par_KR[1])[3] != 'Glushkov':
                Q_KR_i = 0
                for k in range(len(builtins.par_KR[1])):
                    Q_KR_i += float((builtins.par_KR[1])[k])*((builtins.H_euv[i]/100)**k)
            elif len(builtins.par_KR[1]) == 4 and (builtins.par_KR[1])[3] == 'Glushkov':
                Q_KR_i = float((builtins.par_KR[j+1])[0])*((builtins.H_euv[i]/100) - float((builtins.par_KR[1])[2]))**float((builtins.par_KR[1])[1])
        elif builtins.H_euv[i]/100 < builtins.H_min:
            try:
                if H_min_eks:
                    if builtins.H_euv[i]/100>=builtins.H_min_eks:
                        Q_KR_i = 0
                        for j in range(len(builtins.eks_vniz)):
                            Q_KR_i += float(builtins.eks_vniz[j])*((builtins.H_euv[i]/100)**j)
                    elif builtins.H_euv[i]/100 < builtins.H_min_eks:
                       QMessageBox.warning(None, "Внимание!", "Значение среднего суточного уровня воды ниже "+
                                            "диапазона экстраполяции вниз! Выполните экстраполяцию вниз "+
                                            "с использованием данных прошлых лет!")
                        #sys.exit()


            except NameError:
                QMessageBox.warning(None, "Внимание!", "Значение срочного уровня воды ниже диапазона"+
                                                 "принятой опорной КР! Выполните экстраполяцию вниз"+
                                                 "в программе РЕЧНОЙ СТОК и запишите её параметры в БД!")
                #sys.exit()
                
        elif builtins.H_euv[i]/100 > builtins.H_max_eks:
            try:
                if H_max_eks:
                    if builtins.H_euv[i]/100<=builtins.H_max_eks:
                        Q_KR_i = 0
                        for j in range(len(builtins.eks_vverh)):
                            Q_KR_i += float(builtins.eks_vverh[j])*((builtins.H_euv[i]/100)**j)

                    elif builtins.H_euv[i]/100 > builtins.H_max_eks:
                        QMessageBox.warning(None, "Внимание!", "Значение среднего суточного уровня воды превышает "+
                                            "диапазон экстраполяции вверх! Выполните экстраполяцию вверх "+
                                            "с использованием данных прошлых лет!")

                        #sys.exit()
                        
            except NameError:
                QMessageBox.warning(None, "Внимание!", "Значение среднего суточного уровня воды превышает диапазон "+
                                                 "принятой опорной КР! Выполните экстраполяцию вверх "+
                                                 "в программе РЕЧНОЙ СТОК и запишите её параметры в БД!")
                #sys.exit()
                
        elif builtins.H_euv[i]/100 > builtins.H_max:
            if builtins.H_euv[i]/100<=builtins.H_max_eks:
                Q_KR_i = 0
                for j in range(len(builtins.eks_vverh)):
                    Q_KR_i += float(builtins.eks_vverh[j])*((builtins.H_euv[i]/100)**j)

                
        builtins.Q_KR.append(Q_KR_i)
       
elif len(builtins.par_KR) > 2:
    builtins.H_min = float((builtins.par_KR[0])[0])
    builtins.H_max = float((builtins.par_KR[len(builtins.par_KR)-2])[1])
    for i in range(len(builtins.H_euv)):
        if builtins.H_min <= builtins.H_euv[i]/100 <= builtins.H_max:
            for j in range(0,len(builtins.par_KR),2):
                H_min = float((builtins.par_KR[j])[0])
                H_max = float((builtins.par_KR[j])[1])
                if H_min <= builtins.H_euv[i]/100 <= H_max:
                    if len(builtins.par_KR[j+1]) != 4:
                        Q_KR_i = 0
                        for k in range(len(builtins.par_KR[j+1])):
                            Q_KR_i += float((builtins.par_KR[j+1])[k])*((builtins.H_euv[i]/100)**k)
                    elif len(builtins.par_KR[j+1]) == 4 and (builtins.par_KR[j+1])[3] != 'Glushkov':
                        Q_KR_i = 0
                        for k in range(len(builtins.par_KR[j+1])):
                            Q_KR_i += float((builtins.par_KR[j+1])[k])*((builtins.H_euv[i]/100)**k)
                    elif len(builtins.par_KR[j+1]) == 4 and (builtins.par_KR[j+1])[3] == 'Glushkov':
                        Q_KR_i = float((builtins.par_KR[j+1])[0])*((builtins.H_euv[i]/100) - float((builtins.par_KR[j+1])[2]))**float((builtins.par_KR[j+1])[1])
        elif builtins.H_euv[i]/100 < builtins.H_min:
            try:
                if H_min_eks:
                    if builtins.H_euv[i]/100>=builtins.H_min_eks:
                        Q_KR_i = 0
                        for j in range(len(builtins.eks_vniz)):
                            Q_KR_i += float(builtins.eks_vniz[j])*((builtins.H_euv[i]/100)**j)
                    elif builtins.H_euv[i]/100 < builtins.H_min_eks:
                        QMessageBox.warning(None, "Внимание!", "Значение среднего суточного уровня воды ниже "+
                                            "диапазона экстраполяции вниз! Выполните экстраполяцию вниз "+
                                            "с использованием данных прошлых лет!")
                        #sys.exit()
                        
            except NameError:
                QMessageBox.warning(None, "Внимание!", "Значение срочного уровня воды ниже диапазона "+
                                                 "принятой опорной КР! Выполните экстраполяцию вниз "+
                                                 "в программе РЕЧНОЙ СТОК и запишите её параметры в БД!")
                #sys.exit()
                
        elif builtins.H_euv[i]/100 > builtins.H_max_eks:
            try:
                if H_max_eks:
                    if builtins.H_euv[i]/100<=builtins.H_max_eks:
                        Q_KR_i = 0
                        for j in range(len(builtins.eks_vverh)):
                            Q_KR_i += float(builtins.eks_vverh[j])*((builtins.H_euv[i]/100)**j)
                    elif builtins.H_euv[i]/100 > builtins.H_max_eks:
                        QMessageBox.warning(None, "Внимание!", "Значение среднего суточного уровня воды превышает "+
                                            "диапазон экстраполяции вверх! Выполните экстраполяцию вверх "+
                                            "с использованием данных прошлых лет!")
                        #sys.exit()
                        
            except NameError:
                QMessageBox.warning(None, "Внимание!", "Значение среднего суточного уровня воды превышает диапазон "+
                                                 "принятой опорной КР! Выполните экстраполяцию вверх "+
                                                 "в программе РЕЧНОЙ СТОК и запишите её параметры в БД!")
                #sys.exit()
                
        elif builtins.H_euv[i]/100 > builtins.H_max:
            if builtins.H_euv[i]/100<=builtins.H_max_eks:
                Q_KR_i = 0
                for j in range(len(builtins.eks_vverh)):
                    Q_KR_i += float(builtins.eks_vverh[j])*((builtins.H_euv[i]/100)**j)  
        
        builtins.Q_KR.append(Q_KR_i) 
   
                    

builtins.Q_KR_dates=dict(zip(builtins.daty,builtins.Q_KR))
 
import Module_8_OI__q_dates_IRV

