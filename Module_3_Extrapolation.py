#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''Открываем файл Экстрапол (если он есть) и
считываем параметры экстраполяции
'''
import builtins 
import os
import shutil
import math
import numpy
import datetime
import csv
import re

#Записываем в память параметры экстраполяции
try:
    with open(str(builtins.kat)+"/"+str(builtins.opor_year)+"/Экстрапол.txt","r") as inf:

        ekstr_file = []        
        for line in inf:
            line = line.rstrip()
            ekstr_file.append(line)
        #print(ekstr_file )  
        pattern1=r".*экстраполяция вверх"
        pattern2=r".*экстраполяция вниз"
            
        if re.match(pattern1,ekstr_file[3]):
            builtins.eks_vverh = []
            ekstr_file[2]=ekstr_file[2].strip().split()
            builtins.eks_vverh.extend((ekstr_file[2])[:-5])
            for k in range(4,len(ekstr_file)):
                if re.match(pattern2,ekstr_file[k]):
                    #экстраполяция и вверх, и вниз
                    builtins.eks_vniz = []
                    ekstr_file[k-1]=ekstr_file[k-1].strip().split()
                    builtins.eks_vniz.extend((ekstr_file[k-1])[:-5])
                    ekstr_file[k-2]=ekstr_file[k-2].strip().split()
                    builtins.H_max_eks = float((ekstr_file[k-2])[0])
                    ekstr_file[len(ekstr_file)-1]= ekstr_file[len(ekstr_file)-1].strip().split()
                    builtins.H_min_eks = float((ekstr_file[len(ekstr_file)-1])[0])
                    break
                                
                else:
                    if k == len(ekstr_file)-1:
                        #экстраполяция только вверх
                        ekstr_file[len(ekstr_file)-1]= ekstr_file[len(ekstr_file)-1].strip().split()
                        builtins.H_max_eks = float((ekstr_file[len(ekstr_file)-1])[0])

        elif re.match(pattern2,ekstr_file[3]):
            #экстраполяция только вниз
            builtins.eks_vniz = []
            ekstr_file[2]=ekstr_file[2].strip().split()
            builtins.eks_vniz.extend((ekstr_file[2])[:-5])
            ekstr_file[len(ekstr_file)-1]= ekstr_file[len(ekstr_file)-1].strip().split()
            builtins.H_min_eks = float((ekstr_file[len(ekstr_file)-1])[0])
        


except FileNotFoundError:
    #экстраполяция не проводилась
    pass
