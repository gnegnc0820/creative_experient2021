# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:33:30 2017

@author: nawatalab
"""


#--------------------------------実行ソースコード-----------------------------------


import STOCH as st
import NO_THRESHOLDS as nt
import cluster_Ant as cl_ant
import Evaluate as eva
import time
import os
import Pseudo_F as p_f
import Visualization as vis



#パラメータ
#alpha1 = 0.985 #wine
#alpha2 = 0.25  #wine


#alpha1 = 0.92 #corners
#alpha2 = 0.1  #corners

#alpha1 = 0.96 #iris
#alpha2 = 0.22 #iris

#alpha1 = 0.92 #10d_data
#alpha2 = 0.1  #10d_data

alpha1 = 0.9
alpha2 = 0.5


N =  1#繰り返し回数
#
# textNum = 400#データ数

#データ読み込み
"""
fname = "wine.csv"
d = [59, 130, 178] #正解クラスの区切り(wine)
k = 3
"""

"""
fname = "iris2.csv"
d = [50, 100, 150] #正解クラスの区切り(iris)
k = 3
"""

# files = [
#     ["kaden-channel", 864],
#     ["movie-enter", 870],
#     ["sports-watch", 900]
# ]

fname = "sample.csv"
# d = [100, 200, 300]
d = [864, 870, 900]
textNum = sum(d)
print(f"textNum: {textNum}")
k = 10 #k-means法で生成するクラスタ数


print ("DataFile is %s \n" %fname)


#----STOCH----
POCAsum = 0.0
Nsum = 0.0
maxScore = 0
minScore = 100
SumP_F = 0.0
maxP_F = 0
minP_F = 10000

for i in range(N):
    print(i+1, '回目')
    s = 0.0

    Ant, X, count = st.main(fname, alpha1, alpha2)

    code = cl_ant.ant_label(Ant)
    # print(code)
    c = max(code) + 1 # c : クラスタ数
    eva.sort_cluster(Ant)
    
    cluster = cl_ant.cluster_list(Ant, c)
    
    st.show_cluster(code, X) #クラスタ内容を表示
    
    print('正解要素率')
    number = 0
    for i in cluster:
        i.determineGenre()
        #print('cl[' + str(i) + ']:', cluster[i].POCA())
        #s += cluster[i].POCA() 
        print('cl[' + str(number) + ']:', i.out_correctN(), '/', i.out_Num(), '(', i.POCA(), ')')
        s += i.out_correctN()
        #print('[', i, ']:', cluster[i].POCA())
        number += 1
    
    score = s / textNum
    #if((s / c) > maxScore): maxScore = s / c
    #if(minScore > (s / c)): minScore = s / c
    if(score > maxScore): maxScore = score
    if(minScore > score): minScore = score
    
    #print('正答率平均:', s / c)
    print('正解要素数:', s)
    print('正答率平均:', score)
    print('クラスタ数:', c)
    
    POCAsum += score
    Nsum += c
   
  
    print()
    print()
    
    Pg = []
    Pg, T, P_F = p_f.main(Ant, cluster, c)
    #print(cluster[0])
    
    SumP_F += P_F
    
    if(P_F > maxP_F): maxP_F = P_F
    if(minP_F > P_F): minP_F = P_F
    
    
    for i in Pg:
        print(i)
    print('T:', T)
    print('sumPg:', sum(Pg))
    print('P_F:', P_F)
    
    
print('----------------------FINISH---------------------')
print(N, '回平均正答率:', POCAsum / N)
print(N, '回平均クラスタ数:', Nsum / N)
print('maxScore:', maxScore)
print('minScore:', minScore)
print()
print(N, '回平均Psuedo_F:', SumP_F / N)
print('max:', maxP_F)
print('min:', minP_F)
print('-------------------パラメータ----------------------')
print('alpha1:', alpha1)
print('alpha2;', alpha2)
print('----------------------------------------------------------------')



print("STOCH Algorithm : ", N)
#クラスタリング結果の可視化
# vis.main(Ant)



"""
#----NO-THRESHOLDS----
P = E = C = 0.0
for i in range(N):
    Ant, X, count = nt.main(fname)
    p, e, c = eva.Evaluate_All(code, X.tolist(), d, fname)
    P = P + p;
    E = E + e;
    C = C + c;
print("NO-THRESHOLDS Algorithm : ", N)
print("P:", P/float(N))
print("E:", E/float(N))
print("C:", C/float(N))
print()
"""



print ("DataFile is %s" %fname)    
    
    
    