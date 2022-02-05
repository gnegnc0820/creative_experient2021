# -*- coding: utf-8 -*-
"""
Created on Fri May 19 13:07:11 2017

@author: nawatalab
"""

import numpy as np
import copy

#=================================問題=============================
#次元数dimと、行列Aは与えられるものとする
"""
#----------問題1(ランク計算)----------
A = np.array([[1, 3, -1, 1],
              [2, 6, -2, 4]])
"""
"""
#----------問題2(ランク計算)----------
A = np.array([[1, 3, 2, 0],
              [2, 8, 5, 1],
              [-1, -1, -1, 1]])
"""
"""
#----------問題3(ランク計算)----------

A = np.array([[1, 3, 2, 0, 4],
              [2, 8, 5, 1, 2],
              [-1, -1, -1, 1, 2],
              [3, 2, 3, 1, 1],
              [1, -2, 7, 1, 2]])
"""

#----------問題4(ランク計算)----------
A = np.array([[1, 3, 2],
              [2, 8, 5],
              [-1, -1, -1],
              [3, 2, 4]])

#====================================================================


ZERO = 0.00000000001 #0のこと

#正方行列に整形
def shapeArray(a):
    dim = 0
    m = len(a)
    n = len(a[0])
    
    #行数の方が大きいとき(縦長行列のとき)
    diff = abs(m - n)
    if(m > n):
        dim = m
        tmp = tmp2 = np.zeros((1, diff))        
        for i in range(m - 1):
            tmp2 = np.vstack((tmp2, tmp))
        a = np.hstack((a, tmp2))
    #列数の方が大きいとき(横長行列のとき)
    elif(m < n):
        dim = n
        tmp = np.zeros((1, n))
        for i in range(diff):
            a = np.vstack((a, tmp))
    else:
        dim = m
    
    return a, dim
            
#単位行列生成
def generateUnitMatrix():    
    unitMatrix = []
    for i in range(dim):
        tmp = []
        for j in range(dim):
            if i == j : tmp.append(1.0)
            else : tmp.append(0.0)
        unitMatrix.append(tmp)    
    return unitMatrix
    
#Aのx行でy行を消す を表す行列Exyを作る
def generateE(x, y, a, E, invE):
    #単位行列生成
    e = generateUnitMatrix()
    inve = generateUnitMatrix()
    
    value = -a[y][x] / a[x][x]

    e[y][x] = value
    inve[y][x] = -value
    
    E.append(e)
    invE.append(inve)
    
    return e

#行列aのx行目とy行目を入れ替える
def exchangeLine(x, y, a):
    tmp = copy.deepcopy(a)
    a[x] = tmp[y]
    a[y] = tmp[x]

#行列aのx行とy行を入れ替える交換行列Pを作る
def generateP(x, y, P):
    #単位行列生成
    p = generateUnitMatrix()   
    exchangeLine(x, y, p)
    P.append(p)
    
    return p

#上三角行列Uを生成
def generateUpper(a, E, invE):
    x = 0
    while x < dim:
        #対角要素が0でない行を見つける(pibot)とりあえずxとする
        pibot = x            
        #もしピボット選択できなかったら(ピボット要素 == 0)
        if abs(a[x][x]) < ZERO:
            for i in range(x + 1, dim):
                if abs(a[i][x]) > ZERO:
                    #交換行列Pを生成し、aとの積をとる(=任意の行を交換)
                    a = np.dot(generateP(x, i, P), a)
                    break
        #うまくピボット選択できたら
        else:                      
            for i in range(pibot + 1, dim):
                if abs(a[i][pibot]) > ZERO:
                    a = np.dot(generateE(pibot, i, a, E, invE), a)   
        x += 1           
    return a

#行列Aのランクを計算する
def rank(A):
    rank = 0
    for i in range(dim):
        a = sum(A[i])
        if(abs(a) > ZERO):
            rank += 1
    return rank

#------------------------実行-----------------------------

E = []      #Eを順にまとめたリスト
invE = []   #Eの逆行列を順にまとめたリスト
P = []      #交換行列P
U = []      #上三角行列

#元行列をコピー
a = copy.deepcopy(A)

a, dim = shapeArray(a)


    
U = generateUpper(a, E, invE)

r = rank(U)

print("A:")
print(A)
print()

print("U:")
print(U)  
print()   

print("rank:", r)
