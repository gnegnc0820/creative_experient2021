# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 16:18:37 2017

@author: nawatalab
"""

import operator
import pandas as pd
import numpy as np
import csv # CSVファイルを扱うためのモジュールのインポート

def Evaluate_All(code, X, num, fname):
    T = set_Ans(fname, num)
    C = []
    for i in range(max(code) + 1):
        
        C.append(make_cluster(code, X, i))
        
    P = Purity(C, T) #純度
    E = Entropy(C, T) #エントロピー
    Class = len(C) #クラス数
    
    return P, E, Class

def set_Ans(fname, num):
    data = pd.read_csv(fname)
    data = data.values
    data = data.tolist()

    s = 0
    T = []
    #for i in range(len(data)/num):
    for e in num:
        T.append(data[s:e])
        s = e
        #if e > len(data) : e = len(data)

    #print("Answer Data")
    return T
    
#Id(int型)を受け取り、そのIdを持つant型を返す
def searchAnt(ant, Id):
    for i in ant:
        if(i.Id == Id): return i

    return 0

#再帰的にクラスタリング結果をXにリストとして格納する
def writeResult(ant, X, antA):  
    for i in antA.children:
        ai = searchAnt(ant, i)
        p = [ai.Id, ai.parent, ai.children, ai.a_plus, ai.conect, ai.Tsim, ai.Tdsim, ai.a_pos, ai.name]
        X.append(p)
        writeResult(ant, X, ai)
    
    return





def sort_cluster(ant):
    ant.sort(key = operator.attrgetter('label'))
    
    file = open('result.csv', 'w', newline = '')
    writer = csv.writer(file, lineterminator = ',')
    
        
    

    X = []
    #print("Id parent children a_plus conect Tsim Tdsim Pos")
    p = ["id", "parent", "children", "a_plus", "conect", "Tsim", "Tdsim", "pos", "name"]
    X.append(p)

    ai = ant[0]
    X.append([ai.Id, ai.parent, ai.children, ai.a_plus, ai.conect, ai.Tsim, ai.Tdsim, ai.a_pos, ai.name])
    
    
    writeResult(ant, X, ant[0])

    
    for i in X:
        writer.writerow(i + list('\n'))
        #writer.writerow(i)
    
    #for i in X:
     #   file.write(i + "\n")
    
    file.close()
    
    #np.savetxt("result.csv", X, delimiter=",")
    
 
    
    


        



def make_cluster(code, X, label):
    C = []
    i = 0
    for s in code:
        if s == label:
            C.append(X[i])
        i = i + 1
        
    return C

def check_contains(C, T):
    count = 0
    #print len(C), len(T)
    for i in C:
        for j in T:
            #print i, j
            if i == j:
                count = count + 1
                break
    #print(count)
    #print('-' *5)
    return count

def Purity(C, T):
    Np = len(T) * len(T[0]) #データ数
    #print 'Np:', Np
    #print len(C[0]), len(C[1]), len(C[2]), len(C[3])
    Max = 0
    Ans = 0
    tmp_Ans = []
    for i in C:
        Max = 0
        for j in T:
            tmp = check_contains(i, j)
            if tmp > Max : Max = tmp
        tmp_Ans.append(Max)
        #print(tmp_Ans)
        
    for i in range(len(T)):
        if len(tmp_Ans) == 0 : break
        Ans = Ans + max(tmp_Ans)
        tmp_Ans.remove(max(tmp_Ans))
        
    #print Ans
    
    #print("Purity :", Ans / float(Np))
    return Ans / float(Np)

def Entropy(C, T):
    Np = len(T) * len(T[0]) #データ数
    Ans = 0
    Ci = 0
    Entr_C = 0
    for i in C:
        Ni = float(len(i))
        Ans = 0
        for j in T:
            Nti = check_contains(i, j)
            if not Nti == 0:
                Ans = Ans + (Nti / Ni) * np.log(Nti / Ni)
                
        Entr_C = Entr_C + (-1.0 / np.log(Np) * Ans)
    
    #print("Entr_C", Entr_C / len(C))
    return Entr_C / len(C)
        
        














