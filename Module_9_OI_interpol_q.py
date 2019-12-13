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

print("module 9")
def r(tau):
    r = math.cos((2*3.14*tau)/builtins.T_n)
    if r>=0:
        return r
    else:
        return 0

def P_1_int(m_p, r01, r02, r12):
    return ((1+m_p)*r01-r02*r12)/((1+m_p)**2-r12**2)

def P_2_int(m_p, r01, r02, r12):
    return ((1+m_p)*r02-r01*r12)/((1+m_p)**2-r12**2)

builtins.q_int_dates={}
for i in range(len(builtins.daty)):
    print(builtins.daty[i])
    for j in range(len(builtins.dates_irv_r)):
        print(builtins.dates_irv_r[j])
        if builtins.daty[i]!=builtins.dates_irv_r[j]:
            if (j==0 and builtins.daty[i]<builtins.dates_irv_r[j] and \
                builtins.dates_max[0]>=builtins.dates_irv_r[j]):
                print('1')
                #период до 1-го ИРВ в периоде; максимум после периода
                tau_02=int((builtins.dates_irv_r[j]-builtins.daty[i]).days)
                r_02=r(tau_02)
                P2=P_2_int(builtins.mera_pogr, 0, r_02, 0)
                q_int = P2*builtins.q[j]
                builtins.q_int_dates[builtins.daty[i]]=q_int
                print(tau_02, r_02, P2, q_int)
            elif (j==0 and builtins.daty[i]<builtins.dates_irv_r[j] and \
                  builtins.dates_max[0]<builtins.dates_irv_r[j]):
                print('2')
                #период до 1-го ИРВ в периоде; максимум в периоде
                q_int = builtins.q[j]
                print(q_int)
            elif j!=len(builtins.dates_irv_r)-1 and \
                 builtins.daty[i]>builtins.dates_irv_r[j] and \
                 builtins.daty[i]<builtins.dates_irv_r[j+1] and \
                 (builtins.dates_max[0]<=builtins.dates_irv_r[j] or \
                 builtins.dates_max[0]>=builtins.dates_irv_r[j+1]):
                print('3')
                print(builtins.dates_irv_r[j])
                print(builtins.dates_irv_r[j+1])
                print(builtins.dates_max[0])
                #период между двумя ИРВ; максимум не в периоде
                tau_01=int((builtins.daty[i]-builtins.dates_irv_r[j]).days)
                r_01=r(tau_01)
                tau_02=int((builtins.dates_irv_r[j+1]-builtins.daty[i]).days)
                r_02=r(tau_02)
                tau_12=tau_01+tau_02
                r_12=r(tau_12)
                P1=P_1_int(builtins.mera_pogr, r_01, r_02, r_12)
                P2=P_2_int(builtins.mera_pogr, r_01, r_02, r_12)
                q_int = P1*builtins.q[j]+P2*builtins.q[j+1]+\
                    (1-P1-P2)*numpy.mean([builtins.q[j],builtins.q[j+1]])
                print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P1, P2, q_int)
                builtins.q_int_dates[builtins.daty[i]]=q_int
            elif j!=len(builtins.dates_irv_r)-1 and \
                 builtins.daty[i]>builtins.dates_irv_r[j] and \
                 builtins.daty[i]<builtins.dates_irv_r[j+1] and \
                 builtins.dates_max[0]>builtins.dates_irv_r[j] and \
                 builtins.dates_max[0]<builtins.dates_irv_r[j+1] and \
                 builtins.dates_max[0]>builtins.daty[i]:
                print('4')
                #период от предыдущего ИРВ до максимума
                tau_01=int((builtins.daty[i]-builtins.dates_irv_r[j]).days)
                r_01=r(tau_01)
                P1=P_1_int(builtins.mera_pogr, r_01, 0, 0)
                q_int = P1*builtins.q[j]
                print(tau_01, r_01, P1, q_int)
                builtins.q_int_dates[builtins.daty[i]]=q_int
            elif j!=len(builtins.dates_irv_r)-1 and \
                 builtins.daty[i]>builtins.dates_irv_r[j] and \
                 builtins.daty[i]<builtins.dates_irv_r[j+1] and \
                 builtins.dates_max[0]>builtins.dates_irv_r[j] and \
                 builtins.dates_max[0]<builtins.dates_irv_r[j+1] and \
                 builtins.dates_max[0]==builtins.daty[i]:
                print('5')
                #максимум в расчетный день
                tau_01=int((builtins.daty[i]-builtins.dates_irv_r[j]).days)
                tau_02=int((builtins.dates_irv_r[j+1]-builtins.daty[i]).days)
                print("tau_01=",tau_01," tau_02=",tau_02)
                if tau_01 <= tau_02:
                    r_01=r(tau_01)
                    print(r_01)
                    P1=P_1_int(builtins.mera_pogr, r_01, 0, 0)
                    print(P1)
                    q_int = P1*builtins.q[j]
                    print(tau_01, tau_02, r_01, P1, q_int)
                elif tau_02 > tau_01:
                    r_02=r(tau_02)
                    print(r_02)
                    P2=P_2_int(builtins.mera_pogr, 0, r_02, 0)
                    print(P2)
                    q_int = P2*builtins.q[j+1]
                    print(tau_01, tau_02, r_02, P2, q_int)

                builtins.q_int_dates[builtins.daty[i]]=q_int    
            elif j!=len(builtins.dates_irv_r)-1 and \
                 builtins.daty[i]>builtins.dates_irv_r[j] and \
                 builtins.daty[i]<builtins.dates_irv_r[j+1] and \
                 builtins.dates_max[0]>builtins.dates_irv_r[j] and \
                 builtins.dates_max[0]<builtins.dates_irv_r[j+1] and \
                 builtins.dates_max[0]<builtins.daty[i]:
                print('6')
                #период от максимума до последующего ИРВ
                tau_02=int((builtins.dates_irv_r[j+1]-builtins.daty[i]).days)
                r_02=r(tau_02)
                P2=P_2_int(builtins.mera_pogr, 0, r_02, 0)
                q_int = P2*builtins.q[j+1]
                print(tau_02, r_02, P2, q_int)
                builtins.q_int_dates[builtins.daty[i]]=q_int
            elif j==len(builtins.dates_irv_r)-1 and \
                 builtins.daty[i]>builtins.dates_irv_r[j] and \
                 builtins.dates_max[0]<=builtins.dates_irv_r[j]:
                print('7')
                #период от последнего ИРВ в периоде; максимум до периода
                tau_01=int((builtins.daty[i]-builtins.dates_irv_r[j]).days)
                r_01=r(tau_01)
                P1=P_1_int(builtins.mera_pogr, r_01, 0, 0)
                q_int = P1*builtins.q[j]
                print(tau_01, r_01, P1, q_int)
                builtins.q_int_dates[builtins.daty[i]]=q_int
                
            elif j==len(builtins.dates_irv_r)-1 and \
                 builtins.daty[i]>builtins.dates_irv_r[j] and \
                 builtins.dates_max[0]>builtins.dates_irv_r[j]:
                print('8')
                #период от последнего ИРВ в периоде; максимум в периоде
                q_int = builtins.q[j]
                builtins.q_int_dates[builtins.daty[i]]=q_int
                print(q_int)
            

'''
builtins.q_int_dates={}
for j in range(len(builtins.dates_irv_r)):
    for i in range(len(builtins.daty)):
        for k in range(len(builtins.dates_max)):
            if builtins.daty[i]!=builtins.dates_irv_r[j]:
                if (j==0 and builtins.daty[i]<builtins.dates_irv_r[j]):
                    tau_01=0
                    r_01=0
                    tau_02=int((builtins.dates_irv_r[j]-builtins.daty[i]).days)
                    r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
                    tau_12=0
                    r_12=0
                    P_1=0
                    P_2=r_02/(1+builtins.mera_pogr)
                    q_int = P_2*builtins.q[j]
                    builtins.q_int_dates[builtins.daty[i]]=q_int
                    print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P_1, P_2, q_int)
                elif j>=0 and j<len(builtins.dates_irv_r)-1 and builtins.daty[i]>builtins.dates_irv_r[j]\
                     and builtins.daty[i]<builtins.dates_irv_r[j+1]:
                    if builtins.dates_irv_r[j]<builtins.dates_max[k] and  builtins.dates_irv_r[j+1]>builtins.dates_max[k]:
                        if builtins.daty[i]<=builtins.dates_max[k]:
                            tau_01=int((builtins.daty[i]-builtins.dates_irv_r[j]).days)
                            r_01=math.cos((2*3.14*tau_01)/builtins.T_n)
                            tau_02=0
                            r_02=0
                            tau_12=0
                            r_12=0 
                            P_1=r_01/(1+builtins.mera_pogr)
                            P_2=0
                            q_int = P_1*builtins.q[j]
                            builtins.q_int_dates[builtins.daty[i]]=q_int
                        elif builtins.daty[i]>builtins.dates_max[k]:
                            tau_01=0
                            r_01=0
                            tau_02=int((builtins.dates_irv_r[j+1]-builtins.daty[i]).days)
                            r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
                            tau_12=0
                            r_12=0
                            P_1=0
                            P_2=r_02/(1+builtins.mera_pogr)
                            q_int = P_2*builtins.q[j]
                            builtins.q_int_dates[builtins.daty[i]]=q_int
                    else:
                        tau_01=int((builtins.daty[i]-builtins.dates_irv_r[j]).days)
                        r_01=math.cos((2*3.14*tau_01)/builtins.T_n)
                        tau_02=int((builtins.dates_irv_r[j+1]-builtins.daty[i]).days)
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
                     print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P_1, P_2, q_int)
                
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
                    print(P_1, P_2, q_int)
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
                    print(P_1, P_2, q_int)
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
                    print(P_1, P_2, q_int)
                    builtins.q_int_dates[builtins.daty[i]]=q_int
                
                elif j==len(builtins.dates_irv_r)-1:
                    tau_01=int((builtins.daty[i]-builtins.dates_irv_r[j]).days)
                    r_01=math.cos((2*3.14*tau_01)/builtins.T_n)
                    tau_02=0
                    r_02=0
                    tau_12=0
                    r_12=0 
                    P_1=r_01/(1+builtins.mera_pogr)
                    P_2=0
                    q_int = P_1*builtins.q[j]
                    builtins.q_int_dates[builtins.daty[i]]=q_int
                    print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P_1, P_2, q_int)
                    '''
             

builtins.q_int_dates.update(builtins.q_int_dates_irv)                

print(builtins.q_int_dates)

import Module_10_ERV_OI
