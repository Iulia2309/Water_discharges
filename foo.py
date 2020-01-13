#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Функции для расчета АКФ и
весовых коэффициентов
"""
import builtins 
import math

#АКФ
def r(tau):
    r = math.cos((2*3.14*tau)/builtins.T_n)
    if r>=0:
        return r
    else:
        return 0

#Весовые коэффициенты на даты ИРВ
def P_0(m_p, r01, r02, r12):
    return ((1+m_p)**2-(1+m_p)*(r02**2+r01**2)+r12*(r02*r01+r01*r02-r12))/ \
           ((1+m_p)**3-(1+m_p)*(r12**2+r02**2+r01**2)+2*r01*r12*r02)
def P_1(m_p, r01, r02, r12):
    return ((1+m_p)**2*r01-(1+m_p)*(r12*r02+r01)+r12*r02)/ \
           ((1+m_p)**3-(1+m_p)*(r12**2+r02**2+r01**2)+2*r01*r12*r02)
def P_2(m_p, r01, r02, r12):
    return ((1+m_p)**2*r02-(1+m_p)*(r12*r01+r02)+r12*r01)/ \
           ((1+m_p)**3-(1+m_p)*(r12**2+r02**2+r01**2)+2*r01*r12*r02)

#Весовые коэффициенты на даты между ИРВ
def P_1_int(m_p, r01, r02, r12):
    return ((1+m_p)*r01-r02*r12)/((1+m_p)**2-r12**2)

def P_2_int(m_p, r01, r02, r12):
    return ((1+m_p)*r02-r01*r12)/((1+m_p)**2-r12**2)
