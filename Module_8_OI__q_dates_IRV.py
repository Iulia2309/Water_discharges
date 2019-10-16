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


builtins.q_int_dates_irv={}
for i in range(len(builtins.dates_irv)):
    if i!=0 and i!=len(builtins.dates_irv)-1:
        tau_01=int((builtins.dates_irv[i]-builtins.dates_irv[i-1]).days)
        r_01=math.cos((2*3.14*tau_01)/builtins.T_n)
        tau_02=int((builtins.dates_irv[i+1]-builtins.dates_irv[i]).days)
        r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
        tau_12=tau_01+tau_02
        r_12=math.cos((2*3.14*tau_12)/builtins.T_n)
        
        P_0=((1+builtins.mera_pogr)**2-(1+builtins.mera_pogr)*\
             (r_02**2+r_01**2)+r_12*(r_02*r_01+r_01*r_02-r_12))/\
             ((1+builtins.mera_pogr)**3-(1+builtins.mera_pogr)*\
              (r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_1=((1+builtins.mera_pogr)**2*r_01-(1+builtins.mera_pogr)*\
             (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3\
             -(1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
             (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3\
             -(1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)

        q_int = P_1*builtins.q[i-1]+P_0*builtins.q[i]+P_2*builtins.q[i+1]+\
                (1-P_1-P_0-P_2)*numpy.mean([builtins.q[i-1],builtins.q[i],builtins.q[i+1]])

        builtins.q_int_dates_irv[builtins.dates_irv[i]]=q_int
        
    elif i==0:
        tau_01=0
        r_01=0
        tau_02=int((builtins.dates_irv[i+1]-builtins.dates_irv[i]).days)
        r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
        tau_12=0
        r_12=0

        P_0=((1+builtins.mera_pogr)**2-(1+builtins.mera_pogr)*\
             (r_02**2+r_01**2)+r_12*(r_02*r_01+r_01*r_02-r_12))/\
             ((1+builtins.mera_pogr)**3-(1+builtins.mera_pogr)*\
              (r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_1=((1+builtins.mera_pogr)**2*r_01-(1+builtins.mera_pogr)*\
             (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3\
             -(1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
             (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3\
             -(1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        q_int = P_0*builtins.q[i]+P_2*builtins.q[i+1]+\
                (1-P_0-P_2)*numpy.mean([builtins.q[i],builtins.q[i+1]])

        builtins.q_int_dates_irv[builtins.dates_irv[i]]=q_int
    elif i==len(builtins.dates_irv)-1:
        tau_01=int((builtins.dates_irv[i]-builtins.dates_irv[i-1]).days)
        r_01=math.cos((2*3.14*tau_01)/builtins.T_n)
        tau_02=0
        r_02=0
        tau_12=0
        r_12=0
        
        P_0=((1+builtins.mera_pogr)**2-(1+builtins.mera_pogr)*\
             (r_02**2+r_01**2)+r_12*(r_02*r_01+r_01*r_02-r_12))/\
             ((1+builtins.mera_pogr)**3-(1+builtins.mera_pogr)*\
              (r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_1=((1+builtins.mera_pogr)**2*r_01-(1+builtins.mera_pogr)*\
             (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3\
             -(1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
             (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3\
             -(1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
       
        q_int = P_1*builtins.q[i-1]+P_0*builtins.q[i]+\
                (1-P_1-P_0)*numpy.mean([builtins.q[i-1],builtins.q[i]])

        builtins.q_int_dates_irv[builtins.dates_irv[i]]=q_int                 

import Module_9_OI_interpol_q
    
        
