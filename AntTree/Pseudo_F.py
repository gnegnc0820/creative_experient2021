#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 16:40:44 2017

@author: miyamototatsuro
"""



import numpy as np




def Sim(i, j): 
    ai = np.array(i.data)
    aj = np.array(j.data)
    
    ans = 0.0
    #偏角のcos 類似度

    ans = np.dot(ai, aj) / (np.linalg.norm(ai) * np.linalg.norm(aj))

    return ans



#クラスタの中心点(平均グラフ)を求める
#そのクラスタ内のデータの平均値を求める
def graph_average(cl): 
    tmp = np.zeros(len(cl.factors[0].originalData))#tmp : そのクラスタ内のデータの平均
    
    for i in cl.factors:
        tmp += np.array(i.originalData)
      
    
    
        
    tmp = tmp / len(cl.factors)

    
    
    return tmp
    

#クラスタ内の二乗の総和
def squares_inCluster(cluster, k):
    Sum_K = 0.0
    """
    for i in range(k):
        center = graph_average(cluster[i])
        
        Sum = 0.0
        for j in cluster[i].factors:
            v = center - np.array(j.originalData)
            Sum += np.dot(v, v) #内積
        
        Sum_K += Sum 
     """   
    for i in cluster:
        center = graph_average(i)
        
        Sum = 0.0
        for j in i.factors:
            v = center - np.array(j.originalData)
            Sum += np.dot(v, v)
        
        
        print(Sum)
        Sum_K += Sum
    
    
    
    return Sum_K
        


#全データの二乗の総和
def squares_All(ant, k):
    Sum_All = 0.0
    s= np.zeros(len(ant[0].originalData))
    
    #center : 全データの平均値
    for i in ant:
        s += np.array(i.originalData)
    center = s / len(ant)
    
    for i in ant:
        v = center - np.array(i.originalData)
        Sum_All += np.dot(v, v)
        
    return Sum_All


def PseudoF(G, T, Pg, n):
    print(f"n: {n}")
    return ((T - Pg) / (G - 1)) / (Pg / (n - G))



def main(ant, cluster, k):
    #ant : 全データ(ant型)
    #cluster : クラスタのリスト(中身はCluster型)
    #Cluster型はそのクラスタに属するデータ(ant型)を保持する
    #k : クラスタ数    
    #Pg : 各クラスタ内距離2乗算和
    #T : 全データの距離2乗和

    #PseudoFの計算は正規化せれた方のデータであるi.dataで行いたいから
    for i in ant:
        i.originalData = i.data
    
    Pg = []
    for i in cluster:
        Pg.append(i.out_Pg())
    
    #for i in Pg:
        #print(i)
        
    SumPg = sum(Pg)
    
    #print('sumPg:', SumPg)
    
    T = squares_All(ant, k)
    n = len(ant)
    #print('Pg:', Pg)
    #print('T:', T)
    #print('n:', n)
    #print('k:', k)
    
    P_F = PseudoF(k, T, SumPg, n)
    # print('P_F:', P_F)
    print(f"p_f : {P_F}\nT : {T}\nsumPg : {SumPg}")
    
    return Pg, T, P_F
    


    
    