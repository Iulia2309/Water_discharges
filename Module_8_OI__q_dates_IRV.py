#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Расчет интервалов, весовых коэффициентов и
сглаженных значений q на даты ИРВ
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

builtins.q_int_dates_irv={}
for i in range(len(builtins.dates_irv_r)):
    if i!=0 and i!=len(builtins.dates_irv_r)-1 and \
        (builtins.dates_max <= builtins.dates_irv_r[i-1] or \
        builtins.dates_max >= builtins.dates_irv_r[i+1]):
        #3 ИРВ в одной фазе, расчетная дата посередине, для расчета используются 1-е и 2-е ИРВ
        tau_01=int((builtins.dates_irv_r[i]-builtins.dates_irv_r[i-1]).days)
        r_01=foo.r(tau_01)
        tau_02=int((builtins.dates_irv_r[i+1]-builtins.dates_irv_r[i]).days)
        r_02=foo.r(tau_02)
        tau_12=tau_01+tau_02
        r_12=foo.r(tau_12)

        P0 = foo.P_0(builtins.mera_pogr, r_01, r_02, r_12)
        P1 = foo.P_1(builtins.mera_pogr, r_01, r_02, r_12)
        P2 = foo.P_2(builtins.mera_pogr, r_01, r_02, r_12)

        q_int = P1*builtins.q[i-1]+P0*builtins.q[i]+P2*builtins.q[i+1]+\
        (1-P1-P0-P2)*numpy.mean([builtins.q[i-1],builtins.q[i],builtins.q[i+1]])

        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
    elif i!=0 and i!=len(builtins.dates_irv_r)-1 and \
        builtins.dates_max == builtins.dates_irv_r[i]:
        #Расчетная дата совпадает с максимумом; для расчета используется 1-е ИРВ
        tau_01=int((builtins.dates_irv_r[i]-builtins.dates_irv_r[i-1]).days)
        r_01=foo.r(tau_01)
        tau_02=0
        r_02=0
        tau_12=0
        r_12=0

        P0 = foo.P_0(builtins.mera_pogr, r_01, r_02, r_12)
        P1 = foo.P_1(builtins.mera_pogr, r_01, r_02, r_12)
        P2 = foo.P_2(builtins.mera_pogr, r_01, r_02, r_12)

        q_int = P1*builtins.q[i-1]+P0*builtins.q[i]+\
        (1-P1-P0)*numpy.mean([builtins.q[i-1],builtins.q[i]])

        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
    elif i!=0 and i!=len(builtins.dates_irv_r)-1 and \
         (builtins.dates_max > builtins.dates_irv_r[i-1] and \
          builtins.dates_max < builtins.dates_irv_r[i]):
        #Максимум между 1-м и расчетным ИРВ; для расчета используется 2-е ИРВ 
        tau_01=0
        r_01=0
        tau_02=int((builtins.dates_irv_r[i+1]-builtins.dates_irv_r[i]).days)
        r_02=foo.r(tau_02)
        tau_12=0
        r_12=0

        P0 = foo.P_0(builtins.mera_pogr, r_01, r_02, r_12)
        P1 = foo.P_1(builtins.mera_pogr, r_01, r_02, r_12)
        P2 = foo.P_2(builtins.mera_pogr, r_01, r_02, r_12)

        q_int = P0*builtins.q[i]+P2*builtins.q[i+1]+\
        (1-P0-P2)*numpy.mean([builtins.q[i],builtins.q[i+1]])

        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
    elif i!=0 and i!=len(builtins.dates_irv_r)-1 and \
         (builtins.dates_max > builtins.dates_irv_r[i] and \
          builtins.dates_max < builtins.dates_irv_r[i+1]):
        #Максимум между расчетным и 2-м ИРВ; для расчета используется 1-е ИРВ 
        tau_01=int((builtins.dates_irv_r[i]-builtins.dates_irv_r[i-1]).days)
        r_01=foo.r(tau_01)
        tau_02=0
        r_02=0
        tau_12=0
        r_12=0

        P0 = foo.P_0(builtins.mera_pogr, r_01, r_02, r_12)
        P1 = foo.P_1(builtins.mera_pogr, r_01, r_02, r_12)
        P2 = foo.P_2(builtins.mera_pogr, r_01, r_02, r_12)

        q_int = P1*builtins.q[i-1]+P0*builtins.q[i]+\
        (1-P1-P0)*numpy.mean([builtins.q[i-1],builtins.q[i]])

        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int 
    elif i==0 and builtins.dates_max >= builtins.dates_irv_r[i+1]:
        #1-е в периоде ИРВ; для расчета используется последующее ИРВ, т.к. максимум после него
        tau_01=0
        r_01=0
        tau_02=int((builtins.dates_irv_r[i+1]-builtins.dates_irv_r[i]).days)
        r_02=foo.r(tau_02)
        tau_12=0
        r_12=0

        P0 = foo.P_0(builtins.mera_pogr, r_01, r_02, r_12)
        P1 = foo.P_1(builtins.mera_pogr, r_01, r_02, r_12)
        P2 = foo.P_2(builtins.mera_pogr, r_01, r_02, r_12)

        q_int = P0*builtins.q[i]+P2*builtins.q[i+1]+\
        (1-P0-P2)*numpy.mean([builtins.q[i],builtins.q[i+1]])

        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
    elif i==0 and builtins.dates_max < builtins.dates_irv_r[i+1]:
        #1-е в периоде ИРВ; для расчета используется только само ИРВ, т.к. максимум до следующего ИРВ
        q_int = builtins.q[i]
        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
    elif i==len(builtins.dates_irv_r)-1 and builtins.dates_max <= builtins.dates_irv_r[i-1]:
        #последнее в периоде ИРВ; для расчета используется предыдующее ИРВ, т.к. максимум до него
        tau_01=int((builtins.dates_irv_r[i]-builtins.dates_irv_r[i-1]).days)
        r_01=foo.r(tau_01)
        tau_02=0
        r_02=0
        tau_12=0
        r_12=0

        P0 = foo.P_0(builtins.mera_pogr, r_01, r_02, r_12)
        P1 = foo.P_1(builtins.mera_pogr, r_01, r_02, r_12)
        P2 = foo.P_2(builtins.mera_pogr, r_01, r_02, r_12)

        q_int = P1*builtins.q[i-1]+P0*builtins.q[i]+ \
          (1-P1-P0)*numpy.mean([builtins.q[i-1],builtins.q[i]])

        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
    elif i==len(builtins.dates_irv_r)-1 and builtins.dates_max > builtins.dates_irv_r[i-1]:
        #последнее в периоде ИРВ; для расчета используется только само ИРВ, т.к. максимум после предыдущего ИРВ
        q_int = builtins.q[i]
        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
  

import Module_9_OI_interpol_q
    
        
