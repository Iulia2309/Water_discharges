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
import foo

builtins.q_int_dates={}
for i in range(len(builtins.daty)):
    for j in range(len(builtins.dates_irv_r)):
        if builtins.daty[i]!=builtins.dates_irv_r[j]:
            if (j==0 and builtins.daty[i]<builtins.dates_irv_r[j] and \
                builtins.dates_max>=builtins.dates_irv_r[j]):
                #период до 1-го ИРВ в периоде; максимум после периода
                tau_02=int((builtins.dates_irv_r[j]-builtins.daty[i]).days)
                r_02=foo.r(tau_02)
                P2=foo.P_2_int(builtins.mera_pogr, 0, r_02, 0)
                q_int = P2*builtins.q[j]
                builtins.q_int_dates[builtins.daty[i]]=q_int
            elif (j==0 and builtins.daty[i]<builtins.dates_irv_r[j] and \
                  builtins.dates_max<builtins.dates_irv_r[j]):
                #период до 1-го ИРВ в периоде; максимум в периоде
                q_int = builtins.q[j]
            elif j!=len(builtins.dates_irv_r)-1 and \
                 builtins.daty[i]>builtins.dates_irv_r[j] and \
                 builtins.daty[i]<builtins.dates_irv_r[j+1] and \
                 (builtins.dates_max<=builtins.dates_irv_r[j] or \
                 builtins.dates_max>=builtins.dates_irv_r[j+1]):
                #период между двумя ИРВ; максимум не в периоде
                tau_01=int((builtins.daty[i]-builtins.dates_irv_r[j]).days)
                r_01=foo.r(tau_01)
                tau_02=int((builtins.dates_irv_r[j+1]-builtins.daty[i]).days)
                r_02=foo.r(tau_02)
                tau_12=tau_01+tau_02
                r_12=foo.r(tau_12)
                P1=foo.P_1_int(builtins.mera_pogr, r_01, r_02, r_12)
                P2=foo.P_2_int(builtins.mera_pogr, r_01, r_02, r_12)
                q_int = P1*builtins.q[j]+P2*builtins.q[j+1]+\
                    (1-P1-P2)*numpy.mean([builtins.q[j],builtins.q[j+1]])
                builtins.q_int_dates[builtins.daty[i]]=q_int
            elif j!=len(builtins.dates_irv_r)-1 and \
                 builtins.daty[i]>builtins.dates_irv_r[j] and \
                 builtins.daty[i]<builtins.dates_irv_r[j+1] and \
                 builtins.dates_max>builtins.dates_irv_r[j] and \
                 builtins.dates_max<builtins.dates_irv_r[j+1] and \
                 builtins.dates_max>builtins.daty[i]:
                #период от предыдущего ИРВ до максимума
                tau_01=int((builtins.daty[i]-builtins.dates_irv_r[j]).days)
                r_01=foo.r(tau_01)
                P1=foo.P_1_int(builtins.mera_pogr, r_01, 0, 0)
                q_int = P1*builtins.q[j]
                builtins.q_int_dates[builtins.daty[i]]=q_int
            elif j!=len(builtins.dates_irv_r)-1 and \
                 builtins.daty[i]>builtins.dates_irv_r[j] and \
                 builtins.daty[i]<builtins.dates_irv_r[j+1] and \
                 builtins.dates_max>builtins.dates_irv_r[j] and \
                 builtins.dates_max<builtins.dates_irv_r[j+1] and \
                 builtins.dates_max==builtins.daty[i]:
                #максимум в расчетный день
                tau_01=int((builtins.daty[i]-builtins.dates_irv_r[j]).days)
                tau_02=int((builtins.dates_irv_r[j+1]-builtins.daty[i]).days)
                if tau_01 <= tau_02:
                    r_01=foo.r(tau_01)
                    P1=foo.P_1_int(builtins.mera_pogr, r_01, 0, 0)
                    q_int = P1*builtins.q[j]
                elif tau_02 > tau_01:
                    r_02=foo.r(tau_02)
                    P2=foo.P_2_int(builtins.mera_pogr, 0, r_02, 0)
                    q_int = P2*builtins.q[j+1]

                builtins.q_int_dates[builtins.daty[i]]=q_int    
            elif j!=len(builtins.dates_irv_r)-1 and \
                 builtins.daty[i]>builtins.dates_irv_r[j] and \
                 builtins.daty[i]<builtins.dates_irv_r[j+1] and \
                 builtins.dates_max>builtins.dates_irv_r[j] and \
                 builtins.dates_max<builtins.dates_irv_r[j+1] and \
                 builtins.dates_max<builtins.daty[i]:
                #период от максимума до последующего ИРВ
                tau_02=int((builtins.dates_irv_r[j+1]-builtins.daty[i]).days)
                r_02=foo.r(tau_02)
                P2=foo.P_2_int(builtins.mera_pogr, 0, r_02, 0)
                q_int = P2*builtins.q[j+1]
                builtins.q_int_dates[builtins.daty[i]]=q_int
            elif j==len(builtins.dates_irv_r)-1 and \
                 builtins.daty[i]>builtins.dates_irv_r[j] and \
                 builtins.dates_max<=builtins.dates_irv_r[j]:
                #период от последнего ИРВ в периоде; максимум до периода
                tau_01=int((builtins.daty[i]-builtins.dates_irv_r[j]).days)
                r_01=foo.r(tau_01)
                P1=foo.P_1_int(builtins.mera_pogr, r_01, 0, 0)
                q_int = P1*builtins.q[j]
                builtins.q_int_dates[builtins.daty[i]]=q_int
                
            elif j==len(builtins.dates_irv_r)-1 and \
                 builtins.daty[i]>builtins.dates_irv_r[j] and \
                 builtins.dates_max>builtins.dates_irv_r[j]:
                #период от последнего ИРВ в периоде; максимум в периоде
                q_int = builtins.q[j]
                builtins.q_int_dates[builtins.daty[i]]=q_int
             
builtins.q_int_dates.update(builtins.q_int_dates_irv)                

import Module_10_ERV_OI
