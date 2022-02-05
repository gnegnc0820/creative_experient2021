#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 12:14:28 2018

@author: miyamototatsuro
"""

from collections import Counter
import numpy as np


def Sim(i, j): 
    ai = np.array(i.data)
    aj = np.array(j.data)
    
    ans = 0.0
    #偏角のcos 類似度

    ans = np.dot(ai, aj) / (np.linalg.norm(ai) * np.linalg.norm(aj))

    return ans




class Cluster():
    def __init__(self, ants):
        self.p = []        
        self.factors = ants#list型 [ant1, ant6, ..., ant23]
        
        
    #そのクラスタのクラスタ内距離2乗和
    def out_Pg(self):
        Sum = 0.0
        s = np.zeros(len(self.factors[0].originalData))
        
        #データの平均値を求める
        for i in self.factors:
            s += np.array(i.originalData)
        
        center = s / len(self.factors)#データの平均値
        
        for i in self.factors:
            v = center - np.array(i.originalData)
            Sum += np.dot(v, v)#距離2乗和
        
        self.Pg = Sum#Pg : クラスタ内距離2乗和
        
        return Sum

    

    #そのクラスタの正答率を返す
    #Percentage of Correct Answers    
    def POCA(self):
        correct = 0
        for i in self.p:
            if(i == self.genre):
                correct += 1
        
        return correct / len(self.p)
    
    #クラスタのジャンルを決定する
    #クラスタの要素のうち最も多いものをそのクラスタの正解ジャンルと定義する
    def determineGenre(self):
        for i in self.factors:
            self.p.append(i.genre)
        
        
        
        c = Counter(self.p)


        q = c.most_common(1) #q[0][0] : そのクラスタの正解ジャンル
        self.genre = q[0][0]
                
    
    #そのクラスタの正解要素数を返す
    def out_correctN(self):
        correct = 0
        for i in self.p:
            if(i == self.genre):
                correct += 1
        
        return correct
    
    def out_Num(self):
        return len(self.factors)
        
        
        
        
        