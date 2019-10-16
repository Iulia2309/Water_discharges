#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Расчет ЕРВ методом оптимальной интерполяции
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

builtins.Q_erv_oi={}
builtins.Q_KR_dates=dict(zip(builtins.daty,builtins.Q_KR))

for key in builtins.Q_KR_dates.keys():
    date_r=key
    if key in builtins.q_int_dates:
        Q_erv_oi = builtins.Q_KR_dates[date_r]*(1+builtins.q_int_dates[key])
        builtins.Q_erv_oi[date_r]=Q_erv_oi


builtins.Q_erv_oi_list=[]
for k in sorted(builtins.Q_erv_oi.keys()):
    if 0<=builtins.Q_erv_oi[k]<1:
        builtins.Q_erv_oi_list.append(round(builtins.Q_erv_oi[k],3))
    elif 1<=builtins.Q_erv_oi[k]<10:
        builtins.Q_erv_oi_list.append(round(builtins.Q_erv_oi[k],2))
    elif 10<=builtins.Q_erv_oi[k]<100:
        builtins.Q_erv_oi_list.append(round(builtins.Q_erv_oi[k],1))
    elif builtins.Q_erv_oi[k]>100:
        builtins.Q_erv_oi_list.append(int(builtins.Q_erv_oi[k]))
               

import Module_11_Write_ERV
