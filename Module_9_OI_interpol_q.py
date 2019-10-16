#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Расчет интервалов, весовых коэффициентов и
интерполированных значений q между датами ИРВ
"""
import builtins 
import os
import shutil
import math
import numpy
import datetime
import csv
import re


builtins.q_int_dates={}
for j in range(len(builtins.dates_irv)):
    for i in range(len(builtins.daty)):
        if builtins.daty[i]!=builtins.dates_irv[j]:
            if j==0 and builtins.daty[i]<builtins.dates_irv[j]:
                tau_01=0
                r_01=0
                tau_02=int((builtins.dates_irv[j]-builtins.daty[i]).days)
                r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
                tau_12=0
                r_12=0
                P_1=0
                P_2=r_02/(1+builtins.mera_pogr)
                q_int = P_2*builtins.q[j]

                builtins.q_int_dates[builtins.daty[i]]=q_int
            elif j==0 and builtins.daty[i]>builtins.dates_irv[j]\
                    and builtins.daty[i]<builtins.dates_irv[j+1]:
                tau_01=int((builtins.daty[i]-builtins.dates_irv[j]).days)
                r_01=math.cos((2*3.14*tau_01)/builtins.T_n)
                tau_02=int((builtins.dates_irv[j+1]-builtins.daty[i]).days)
                r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
                tau_12=tau_01+tau_02
                r_12=math.cos((2*3.14*tau_12)/builtins.T_n)
                P_1=((1+builtins.mera_pogr)*r_01-r_02*r_12)/\
                     ((1+builtins.mera_pogr)**2-r_12**2)
                P_2=((1+builtins.mera_pogr)*r_02-r_01*r_12)/\
                     ((1+builtins.mera_pogr)**2-r_12**2)
                q_int = P_1*builtins.q[j]+P_2*builtins.q[j+1]+\
                (1-P_1-P_2)*numpy.mean([builtins.q[j],builtins.q[j+1]])

                builtins.q_int_dates[builtins.daty[i]]=q_int
            elif j!=0 and j!=len(builtins.dates_irv)-1 and\
                 builtins.daty[i]>builtins.dates_irv[j] and \
                 builtins.daty[i]<builtins.dates_irv[j+1]:
                tau_01=int((builtins.daty[i]-builtins.dates_irv[j]).days)
                r_01=math.cos((2*3.14*tau_01)/builtins.T_n)
                tau_02=int((builtins.dates_irv[j+1]-builtins.daty[i]).days)
                r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
                tau_12=tau_01+tau_02
                r_12=math.cos((2*3.14*tau_12)/builtins.T_n)
                P_1=((1+builtins.mera_pogr)*r_01-r_02*r_12)/\
                     ((1+builtins.mera_pogr)**2-r_12**2)
                P_2=((1+builtins.mera_pogr)*r_02-r_01*r_12)/\
                     ((1+builtins.mera_pogr)**2-r_12**2)
                q_int = P_1*builtins.q[j]+P_2*builtins.q[j+1]+\
                (1-P_1-P_2)*numpy.mean([builtins.q[j],builtins.q[j+1]])

                builtins.q_int_dates[builtins.daty[i]]=q_int
            elif j==len(builtins.dates_irv)-2 and \
                 builtins.daty[i]>builtins.dates_irv[j] and \
                 builtins.daty[i]<builtins.dates_irv[j+1]:
                tau_01=int((builtins.daty[i]-builtins.dates_irv[j]).days)
                r_01=math.cos((2*3.14*tau_01)/builtins.T_n)
                tau_02=int((builtins.dates_irv[j+1]-builtins.daty[i]).days)
                r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
                tau_12=tau_01+tau_02
                r_12=math.cos((2*3.14*tau_12)/builtins.T_n)

                P_1=((1+builtins.mera_pogr)*r_01-r_02*r_12)/\
                     ((1+builtins.mera_pogr)**2-r_12**2)
                P_2=((1+builtins.mera_pogr)*r_02-r_01*r_12)/\
                     ((1+builtins.mera_pogr)**2-r_12**2)
                q_int = P_1*builtins.q[j]+P_2*builtins.q[j+1]+\
                (1-P_1-P_2)*numpy.mean([builtins.q[j],builtins.q[j+1]])

                builtins.q_int_dates[builtins.daty[i]]=q_int
            elif j==len(builtins.dates_irv)-1 and builtins.daty[i]>builtins.dates_irv[j]:
                tau_01=int((builtins.daty[i]-builtins.dates_irv[j]).days)
                r_01=math.cos((2*3.14*tau_01)/builtins.T_n)
                tau_02=0
                r_02=0
                tau_12=0
                r_12=0
                P_1=r_01/(1+builtins.mera_pogr)
                P_2=0
                q_int = P_1*builtins.q[j]

                builtins.q_int_dates[builtins.daty[i]]=q_int
             

builtins.q_int_dates.update(builtins.q_int_dates_irv)                

import Module_10_ERV_OI
