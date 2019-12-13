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

print("module 8")

def r(tau):
    r = math.cos((2*3.14*tau)/builtins.T_n)
    if r>=0:
        return r
    else:
        return 0

def P_0(m_p, r01, r02, r12):
    return ((1+m_p)**2-(1+m_p)*\
            (r02**2+r01**2)+r_12*(r02*r01+r01*r02-r12))/\
            ((1+m_p)**3-(1+m_p)*\
             (r12**2+r02**2+r01**2)+2*r01*r12*r02)
def P_1(m_p, r01, r02, r12):
    return ((1+m_p)**2*r_01-(1+m_p)*\
            (r12*r02+r01)+r12*r02)/((1+m_p)**3-\
                                         (1+m_p)*(r12**2+r02**2+r01**2)+2*r01*r12*r02)
def P_2(m_p, r01, r02, r12):
    return ((1+m_p)**2*r02-(1+m_p)*\
            (r12*r01+r02)+r12*r01)/((1+m_p)**3-\
                                        (1+m_p)*(r12**2+r02**2+r01**2)+2*r01*r12*r02)
builtins.q_int_dates_irv={}
for i in range(len(builtins.dates_irv_r)):
    print(builtins.dates_irv_r[i])
    if i!=0 and i!=len(builtins.dates_irv_r)-1 and \
       (builtins.dates_max[0] <= builtins.dates_irv_r[i-1] or \
        builtins.dates_max[0] >= builtins.dates_irv_r[i+1]):
        #3 ИРВ в одной фазе, расчетная дата посередине, для расчета используются 1-е и 2-е ИРВ
        tau_01=int((builtins.dates_irv_r[i]-builtins.dates_irv_r[i-1]).days)
        r_01=r(tau_01)
        #r_01=math.cos((2*3.14*tau_01)/builtins.T_n)
        tau_02=int((builtins.dates_irv_r[i+1]-builtins.dates_irv_r[i]).days)
        r_02=r(tau_02)
        #r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
        tau_12=tau_01+tau_02
        r_12=r(tau_12)
        #r_12=math.cos((2*3.14*tau_12)/builtins.T_n)

        P0 = P_0(builtins.mera_pogr, r_01, r_02, r_12)
        P1 = P_1(builtins.mera_pogr, r_01, r_02, r_12)
        P2 = P_2(builtins.mera_pogr, r_01, r_02, r_12)
        '''
        P_0=((1+builtins.mera_pogr)**2-(1+builtins.mera_pogr)*\
             (r_02**2+r_01**2)+r_12*(r_02*r_01+r_01*r_02-r_12))/\
        ((1+builtins.mera_pogr)**3-(1+builtins.mera_pogr)*\
         (r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_1=((1+builtins.mera_pogr)**2*r_01-(1+builtins.mera_pogr)*\
             (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3- \
                                          (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
            (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3-\
                                        (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
                                        '''
        q_int = P1*builtins.q[i-1]+P0*builtins.q[i]+P2*builtins.q[i+1]+\
        (1-P1-P0-P2)*numpy.mean([builtins.q[i-1],builtins.q[i],builtins.q[i+1]])
        

        print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P1, P0, P2, q_int)

        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
    elif i!=0 and i!=len(builtins.dates_irv_r)-1 and \
         builtins.dates_max[0] == builtins.dates_irv_r[i]:
        #Расчетная дата совпадает с максимумом; для расчета используется 1-е ИРВ
        tau_01=int((builtins.dates_irv_r[i]-builtins.dates_irv_r[i-1]).days)
        r_01=r(tau_01)
        #r_01=math.cos((2*3.14*tau_01)/builtins.T_n)
        tau_02=0
        r_02=0
        tau_12=0
        r_12=0

        P0 = P_0(builtins.mera_pogr, r_01, r_02, r_12)
        P1 = P_1(builtins.mera_pogr, r_01, r_02, r_12)
        P2 = P_2(builtins.mera_pogr, r_01, r_02, r_12)
        '''
        P_0=((1+builtins.mera_pogr)**2-(1+builtins.mera_pogr)*\
             (r_02**2+r_01**2)+r_12*(r_02*r_01+r_01*r_02-r_12))/\
        ((1+builtins.mera_pogr)**3-(1+builtins.mera_pogr)*\
         (r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_1=((1+builtins.mera_pogr)**2*r_01-(1+builtins.mera_pogr)*\
             (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3- \
                                          (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
            (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3-\
                                        (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        '''
        q_int = P1*builtins.q[i-1]+P0*builtins.q[i]+\
        (1-P1-P0)*numpy.mean([builtins.q[i-1],builtins.q[i]])

        print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P1, P0, P2, q_int)

        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
    elif i!=0 and i!=len(builtins.dates_irv_r)-1 and \
         (builtins.dates_max[0] > builtins.dates_irv_r[i-1] and \
          builtins.dates_max[0] < builtins.dates_irv_r[i]):
        #Максимум между 1-м и расчетным ИРВ; для расчета используется 2-е ИРВ 
        tau_01=0
        r_01=0
        tau_02=int((builtins.dates_irv_r[i+1]-builtins.dates_irv_r[i]).days)
        r_02=r(tau_02)
        #r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
        tau_12=0
        r_12=0

        P0 = P_0(builtins.mera_pogr, r_01, r_02, r_12)
        P1 = P_1(builtins.mera_pogr, r_01, r_02, r_12)
        P2 = P_2(builtins.mera_pogr, r_01, r_02, r_12)
        '''
        
        P_0=((1+builtins.mera_pogr)**2-(1+builtins.mera_pogr)*\
             (r_02**2+r_01**2)+r_12*(r_02*r_01+r_01*r_02-r_12))/\
        ((1+builtins.mera_pogr)**3-(1+builtins.mera_pogr)*\
         (r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_1=((1+builtins.mera_pogr)**2*r_01-(1+builtins.mera_pogr)*\
             (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3- \
                                          (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
            (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3-\
                                        (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
                                        '''
        q_int = P0*builtins.q[i]+P2*builtins.q[i+1]+\
        (1-P0-P2)*numpy.mean([builtins.q[i],builtins.q[i+1]])

        print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P1, P0, P2, q_int)

        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
    elif i!=0 and i!=len(builtins.dates_irv_r)-1 and \
         (builtins.dates_max[0] > builtins.dates_irv_r[i] and \
          builtins.dates_max[0] < builtins.dates_irv_r[i+1]):
        #Максимум между расчетным и 2-м ИРВ; для расчета используется 1-е ИРВ 
        tau_01=int((builtins.dates_irv_r[i]-builtins.dates_irv_r[i-1]).days)
        r_01=r(tau_01)
        #r_01=math.cos((2*3.14*tau_01)/builtins.T_n)
        tau_02=0
        r_02=0
        tau_12=0
        r_12=0

        P0 = P_0(builtins.mera_pogr, r_01, r_02, r_12)
        P1 = P_1(builtins.mera_pogr, r_01, r_02, r_12)
        P2 = P_2(builtins.mera_pogr, r_01, r_02, r_12)
        '''
        P_0=((1+builtins.mera_pogr)**2-(1+builtins.mera_pogr)*\
             (r_02**2+r_01**2)+r_12*(r_02*r_01+r_01*r_02-r_12))/\
        ((1+builtins.mera_pogr)**3-(1+builtins.mera_pogr)*\
         (r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_1=((1+builtins.mera_pogr)**2*r_01-(1+builtins.mera_pogr)*\
             (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3- \
                                          (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
            (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3-\
                                        (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
                                        '''
        q_int = P1*builtins.q[i-1]+P0*builtins.q[i]+\
        (1-P1-P0)*numpy.mean([builtins.q[i-1],builtins.q[i]])

        print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P1, P0, P2, q_int)

        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int 
    elif i==0 and builtins.dates_max[0] >= builtins.dates_irv_r[i+1]:
        #1-е в периоде ИРВ; для расчета используется последующее ИРВ, т.к. максимум после него
        tau_01=0
        r_01=0
        tau_02=int((builtins.dates_irv_r[i+1]-builtins.dates_irv_r[i]).days)
        r_02=r(tau_02)
        #r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
        tau_12=0
        r_12=0

        P0 = P_0(builtins.mera_pogr, r_01, r_02, r_12)
        P1 = P_1(builtins.mera_pogr, r_01, r_02, r_12)
        P2 = P_2(builtins.mera_pogr, r_01, r_02, r_12)
        '''

        P_0=((1+builtins.mera_pogr)**2-(1+builtins.mera_pogr)*\
                (r_02**2+r_01**2)+r_12*(r_02*r_01+r_01*r_02-r_12))/\
            ((1+builtins.mera_pogr)**3-(1+builtins.mera_pogr)*\
            (r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_1=((1+builtins.mera_pogr)**2*r_01-(1+builtins.mera_pogr)*\
                (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3-\
                                            (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
                (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3-\
                                            (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
                                            '''
        q_int = P0*builtins.q[i]+P2*builtins.q[i+1]+\
        (1-P0-P2)*numpy.mean([builtins.q[i],builtins.q[i+1]])

        print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P1, P0, P2, q_int)

        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
    elif i==0 and builtins.dates_max[0] < builtins.dates_irv_r[i+1]:
        #1-е в периоде ИРВ; для расчета используется только само ИРВ, т.к. максимум до следующего ИРВ
        q_int = builtins.q[i]
        print(q_int)
        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
    elif i==len(builtins.dates_irv_r)-1 and builtins.dates_max[0] <= builtins.dates_irv_r[i-1]:
        #последнее в периоде ИРВ; для расчета используется предыдующее ИРВ, т.к. максимум до него
        tau_01=int((builtins.dates_irv_r[i]-builtins.dates_irv_r[i-1]).days)
        r_01=r(tau_01)
        #r_01=math.cos((2*3.14*tau_01)/builtins.T_n)
        tau_02=0
        r_02=0
        tau_12=0
        r_12=0

        P0 = P_0(builtins.mera_pogr, r_01, r_02, r_12)
        P1 = P_1(builtins.mera_pogr, r_01, r_02, r_12)
        P2 = P_2(builtins.mera_pogr, r_01, r_02, r_12)
        '''
        P_0=((1+builtins.mera_pogr)**2-(1+builtins.mera_pogr)*\
                (r_02**2+r_01**2)+r_12*(r_02*r_01+r_01*r_02-r_12))/\
            ((1+builtins.mera_pogr)**3-(1+builtins.mera_pogr)*\
            (r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_1=((1+builtins.mera_pogr)**2*r_01-(1+builtins.mera_pogr)*\
                (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3-\
                                            (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
        P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
                (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3-\
                                            (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
                                            '''
       
        q_int = P1*builtins.q[i-1]+P0*builtins.q[i]+\
            (1-P1-P0)*numpy.mean([builtins.q[i-1],builtins.q[i]])

        print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P1, P0, P2, q_int)

        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
    elif i==len(builtins.dates_irv_r)-1 and builtins.dates_max[0] > builtins.dates_irv_r[i-1]:
        #последнее в периоде ИРВ; для расчета используется только само ИРВ, т.к. максимум после предыдущего ИРВ
        q_int = builtins.q[i]
        print(q_int)
        builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
    
        
'''

builtins.q_int_dates_irv={}
for i in range(len(builtins.dates_irv_r)):
    for j in range(len(builtins.dates_max)):
        print(builtins.dates_irv_r[i])
        if i!=0 and i!=len(builtins.dates_irv_r)-1 and \
            (builtins.dates_max[j] <= builtins.dates_irv_r[i-1] or \
             builtins.dates_max[j] >= builtins.dates_irv_r[i+1]:
             tau_01=int((builtins.dates_irv_r[i]-builtins.dates_irv_r[i-1]).days)
             r_01=math.cos((2*3.14*tau_01)/builtins.T_n)
             tau_02=int((builtins.dates_irv_r[i+1]-builtins.dates_irv_r[i]).days)
             r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
             tau_12=tau_01+tau_02
             r_12=math.cos((2*3.14*tau_12)/builtins.T_n)
        
             P_0=((1+builtins.mera_pogr)**2-(1+builtins.mera_pogr)*\
                  (r_02**2+r_01**2)+r_12*(r_02*r_01+r_01*r_02-r_12))/\
             ((1+builtins.mera_pogr)**3-(1+builtins.mera_pogr)*\
              (r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
             P_1=((1+builtins.mera_pogr)**2*r_01-(1+builtins.mera_pogr)*\
                  (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3- \
                                               (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
             P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
                  (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3-\
                                               (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
             q_int = P_1*builtins.q[i-1]+P_0*builtins.q[i]+P_2*builtins.q[i+1]+\
             (1-P_1-P_0-P_2)*numpy.mean([builtins.q[i-1],builtins.q[i],builtins.q[i+1]])

             print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P_1, P_0, P_2, q_int)

             builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
        
        elif i==0 and builtins.dates_max[j] >= builtins.dates_irv_r[i+1]:
            tau_01=0
            r_01=0
            tau_02=int((builtins.dates_irv_r[i+1]-builtins.dates_irv_r[i]).days)
            r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
            tau_12=0
            r_12=0

            P_0=((1+builtins.mera_pogr)**2-(1+builtins.mera_pogr)*\
                 (r_02**2+r_01**2)+r_12*(r_02*r_01+r_01*r_02-r_12))/\
             ((1+builtins.mera_pogr)**3-(1+builtins.mera_pogr)*\
              (r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
            P_1=((1+builtins.mera_pogr)**2*r_01-(1+builtins.mera_pogr)*\
                 (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3-\
                                              (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
            P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
                 (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3-\
                                              (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
            q_int = P_0*builtins.q[i]+P_2*builtins.q[i+1]+\
            (1-P_0-P_2)*numpy.mean([builtins.q[i],builtins.q[i+1]])

            print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P_1, P_0, P_2, q_int)

            builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
        elif i==len(builtins.dates_irv)-1 and builtins.dates_max[j] <= builtins.dates_irv_r[i-1]:
            tau_01=int((builtins.dates_irv_r[i]-builtins.dates_irv_r[i-1]).days)
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
                 (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3-\
                                              (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
            P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
                 (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3-\
                                              (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
       
            q_int = P_1*builtins.q[i-1]+P_0*builtins.q[i]+\
             (1-P_1-P_0)*numpy.mean([builtins.q[i-1],builtins.q[i]])

            print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P_1, P_0, P_2, q_int)

            builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
        elif i != 0 and builtins.dates_irv_r[i] == builtins.dates_max[j] and len(builtins.dates_max) == 1:
            print('дата ИРВ ', builtins.dates_irv_r[i], ' соответствует экстремуму')
            tau_01=int((builtins.dates_irv_r[i]-builtins.dates_irv_r[i-1]).days)
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
                 (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3-\
                                              (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
            P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
                (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3-\
                                             (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
       
            q_int = P_1*builtins.q[i-1]+P_0*builtins.q[i]+\
             (1-P_1-P_0)*numpy.mean([builtins.q[i-1],builtins.q[i]])

            print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P_1, P_0, P_2, q_int)

            builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
             
        elif i != 0 and builtins.dates_irv_r[i] == builtins.dates_max[j]  len(builtins.dates_max) > 1 and\
             j != 0 and builtins.dates_max[j-1] < builtins.dates_irv_r[i-1]:
            tau_01=int((builtins.dates_irv_r[i]-builtins.dates_irv_r[i-1]).days)
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
                (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3-\
                                            (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
            P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
                (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3-\
                                            (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
       
            q_int = P_1*builtins.q[i-1]+P_0*builtins.q[i]+\
            (1-P_1-P_0)*numpy.mean([builtins.q[i-1],builtins.q[i]])

            print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P_1, P_0, P_2, q_int)

            builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
             
        elif i != len(builtins.dates_irv_r) and builtins.dates_irv_r[i] == builtins.dates_max[j]  len(builtins.dates_max) > 1 and\
             j != len(builtins.dates_max) and builtins.dates_max[j+1] > builtins.dates_irv_r[i+1]:
            tau_01=0
            r_01=0
            tau_02=int((builtins.dates_irv_r[i+1]-builtins.dates_irv_r[i]).days)
            r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
            tau_12=0
            r_12=0

            P_0=((1+builtins.mera_pogr)**2-(1+builtins.mera_pogr)*\
                 (r_02**2+r_01**2)+r_12*(r_02*r_01+r_01*r_02-r_12))/\
             ((1+builtins.mera_pogr)**3-(1+builtins.mera_pogr)*\
              (r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
            P_1=((1+builtins.mera_pogr)**2*r_01-(1+builtins.mera_pogr)*\
                 (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3-\
                                              (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
            P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
                 (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3-\
                                              (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
            q_int = P_0*builtins.q[i]+P_2*builtins.q[i+1]+\
            (1-P_0-P_2)*numpy.mean([builtins.q[i],builtins.q[i+1]])

            print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P_1, P_0, P_2, q_int)

            builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
             
        elif i != 0 and builtins.dates_irv_r[i] != builtins.dates_max[j] and \
             builtins.dates_max[j] > builtins.dates_irv_r[i] and builtins.dates_max[j] < builtins.dates_irv_r[i+1]:
             tau_01=int((builtins.dates_irv_r[i]-builtins.dates_irv_r[i-1]).days)
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
                  (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3-\
                                               (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
             P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
                 (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3-\
                                              (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
       
             q_int = P_1*builtins.q[i-1]+P_0*builtins.q[i]+\
              (1-P_1-P_0)*numpy.mean([builtins.q[i-1],builtins.q[i]])

             print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P_1, P_0, P_2, q_int)

             builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int      
             
         elif i != 0 and builtins.dates_irv_r[i] != builtins.dates_max[j] and \
            tau_01=0
            r_01=0
            tau_02=int((builtins.dates_irv_r[i+1]-builtins.dates_irv_r[i]).days)
            r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
            tau_12=0
            r_12=0

            P_0=((1+builtins.mera_pogr)**2-(1+builtins.mera_pogr)*\
                 (r_02**2+r_01**2)+r_12*(r_02*r_01+r_01*r_02-r_12))/\
             ((1+builtins.mera_pogr)**3-(1+builtins.mera_pogr)*\
              (r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
            P_1=((1+builtins.mera_pogr)**2*r_01-(1+builtins.mera_pogr)*\
                 (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3-\
                                              (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
            P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
                 (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3-\
                                              (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
            q_int = P_0*builtins.q[i]+P_2*builtins.q[i+1]+\
            (1-P_0-P_2)*numpy.mean([builtins.q[i],builtins.q[i+1]])

            print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P_1, P_0, P_2, q_int)

            builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int   
             
        elif i != 0 and builtins.dates_irv_r[i] == builtins.dates_max[j] and \
             builtins.dates_max[j]
            tau_01=0
            r_01=0
            tau_02=int((builtins.dates_irv_r[i+1]-builtins.dates_irv_r[i]).days)
            r_02=math.cos((2*3.14*tau_02)/builtins.T_n)
            tau_12=0
            r_12=0

            P_0=((1+builtins.mera_pogr)**2-(1+builtins.mera_pogr)*\
                 (r_02**2+r_01**2)+r_12*(r_02*r_01+r_01*r_02-r_12))/\
             ((1+builtins.mera_pogr)**3-(1+builtins.mera_pogr)*\
              (r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
            P_1=((1+builtins.mera_pogr)**2*r_01-(1+builtins.mera_pogr)*\
                 (r_12*r_02+r_01)+r_12*r_02)/((1+builtins.mera_pogr)**3-\
                                              (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
            P_2=((1+builtins.mera_pogr)**2*r_02-(1+builtins.mera_pogr)*\
                 (r_12*r_01+r_02)+r_12*r_01)/((1+builtins.mera_pogr)**3-\
                                              (1+builtins.mera_pogr)*(r_12**2+r_02**2+r_01**2)+2*r_01*r_12*r_02)
            q_int = P_0*builtins.q[i]+P_2*builtins.q[i+1]+\
            (1-P_0-P_2)*numpy.mean([builtins.q[i],builtins.q[i+1]])

            print(tau_01, tau_02, tau_12, r_01, r_02, r_12, P_1, P_0, P_2, q_int)

            builtins.q_int_dates_irv[builtins.dates_irv_r[i]]=q_int
            '''
      

import Module_9_OI_interpol_q
    
        
