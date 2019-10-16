#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Открытие файла ИРВ расчетного года и определение ИРВ, входящих в расчетный период
import builtins 
import os
import shutil
import math
import datetime
import csv
import re


try:
    with open(str(builtins.kat)+"/"+str(builtins.year_now)+"/Сумма_ИРВ.txt","r") as inf:
        IRV_file_1 = []
        for line in inf:
            line=line.strip().split()
            IRV_file_1.append(line)


    IRV_file=[]
    for line in IRV_file_1:
        if line!=['99', '0']:
            IRV_file.append(line)       

    daty_irv_str=[]
    for i in range(1,len(IRV_file)):
        daty_irv_str.append((IRV_file[i][1])[:5])

    daty_irv=[]
    for i in daty_irv_str:
        d_irv,m_irv=i.split(".")
        date_irv=datetime.date(builtins.year_now,int(m_irv),int(d_irv))
        daty_irv.append(date_irv)

    H_izm=[]
    Q_izm=[]
    for i in range(1,len(IRV_file)):
        H_izm.append(float(IRV_file[i][3]))
        Q_izm.append(float(IRV_file[i][4]))
    

except FileNotFoundError:
    with open(str(builtins.kat)+"/"+str(builtins.year_now)+"/ИРВ.txt","r") as inf:
        IRV_file = []
        for line in inf:
            line=line.strip().split()
            IRV_file.append(line)

    daty_irv_str=[]
    for i in range(1,len(IRV_file)):
        if len(IRV_file[i][1])==5:
            daty_irv_str.append(IRV_file[i][1])
        elif len(IRV_file[i][1])>5:
            daty_irv_str.append((IRV_file[i][1])[:5])

    daty_irv=[]
    for i in daty_irv_str:
        d_irv,m_irv=i.split(".")
        date_irv=datetime.date(builtins.year_now,int(m_irv),int(d_irv))
        daty_irv.append(date_irv)

    H_izm=[]
    Q_izm=[]
    for i in range(1,len(IRV_file)):
        if len(IRV_file[i][1])==5:
            H_izm.append(float(IRV_file[i][4]))
            Q_izm.append(float(IRV_file[i][5]))
        elif len(IRV_file[i][1])>5:
            H_izm.append(float(IRV_file[i][3]))
            Q_izm.append(float(IRV_file[i][4]))
           
  

builtins.H_izm=[]
builtins.Q_izm=[]
builtins.dates_irv=[]
for i in range(len(daty_irv)):
    if daty_irv[i] >= builtins.date_n and daty_irv[i] <= builtins.date_k:
        builtins.H_izm.append(H_izm[i])
        builtins.Q_izm.append(Q_izm[i])
        builtins.dates_irv.append(daty_irv[i])
               
  
import Module_5_q_calculation
        





