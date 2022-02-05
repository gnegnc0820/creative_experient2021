# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 13:33:11 2017

@author: nawatalab
"""


import Gene
import STOCH as st
import NO_THRESHOLDS as nt
import K_means as kmeans
import cluster_Ant as cl_ant
import Evaluate as eva
import time
import os
import random

N = 1 #繰り返し回数
M = 20 #GA個体数
L = 20 #GA繰り返し数
probability = 0.03 #突然変異確率

#データ読み込み
fname = "wine.csv"
d = [59, 130, 178] #正解クラスの区切り(wine)
k = 3

#fname = "iris2.csv"
#d = [50, 100, 150] #正解クラスの区切り(iris)
#k = 3



#----STOCH----
def fitnessFunction(alpha1, alpha2):
    P = E = C = 0.0
    Ant = []
    X = []
    count= 0
    for i in range(N):  
        #time.sleep(1)
        #print("i:", i)
        Ant, X, count = st.main(fname, alpha1, alpha2)
        code = cl_ant.ant_label(Ant)
        p, e, c = eva.Evaluate_All(code, X.tolist(), d, fname)
        P = P + p;
        E = E + e;
        C = C + c;
        
        #print("P:" , P)
        
   
    #評価関数
    fitness = abs(P + (-E) - abs(C - k)) / float(N) 
    if fitness < 0 : fitness = 0
    
    
    return fitness

#交叉    
def clossing(ID, parent1, parent2):
    a1 = (parent1.outputAlpha1() + parent2.outputAlpha1()) / 2.0
    a2 = (parent1.outputAlpha2() + parent2.outputAlpha2()) / 2.0
    
    gene = Gene.Gene(ID, a1, a2)
    
    return gene

#良い方を返す
def better(gene1, gene2):
    #print("gene1.fitness:", gene1.outputFitness())
    #print("gene2.fitness:", gene2.outputFitness())
    if gene1.outputFitness() > gene2.outputFitness() :
        
        return gene1
    else :
        return gene2

#最もよい個体を返す    
def best(gene):
    for i in range(M):
        if i == 0:
            best = better(gene[i], gene[i+1])
        else :
            best = better(gene[i], best)
    return best

        
        
"""        
print("STOCH Algorithm : ", N)
print("P:", P/float(N))
print("E:", E/float(N))
print("C:", C/float(N))
print()
#print("count:", count)
"""


#初期個体生成
gene = []
for i in range(M):
    gene.append(Gene.Gene(i, random.uniform(0.95, 1), random.uniform(0, 0.3)))

print("gene1:", gene[0].outputAlpha1())
print("gene1:", gene[0].outputAlpha2())

#遺伝的アルゴリズム
for p in range(L):
    print(p, "世代目")
    #評価値取得
    fitness = []
    sumFit = 0
    for i in range(M):
        
        fit = fitnessFunction(gene[0].outputAlpha1(), gene[0].outputAlpha2())
        print(i, "体目:", fit)
        if i == 0:
            print("alpha1 : ", gene[i].outputAlpha1())
            print("alpha2 : ", gene[i].outputAlpha2())
        #print("fit:", fit)
        fitness.append(fit)
        gene[i].inputFitness(fit)
        #print("fitness[i]", gene[i].outputFitness())
        
        sumFit = sumFit + fitness[i]
    
    #適応度比例選択で親を選択(parent[0], parent[1])して、交叉、新世代生成
    parent = [] 
    newGene = []
    for k in range(M):
        for j in range(2):
            num = random.uniform(0, sumFit)
            #print("num:", num)
            a = 0
            for i in range(M):
                a = a + fitness[i]
                if(a > num):
                    parent.append(gene[i])
                    break
    
        #交叉
        newGene.append(clossing(k, parent[0], parent[1]))
        newGene[0] = best(gene)
    
    #突然変異
    for i in range(M):
        newGene[i].mutation(probability)
    
    #新世代誕生
    gene = newGene

#結果発表
#best = Gene.Gene(0, 0, 0)
bs = best(gene)
        
print("best parameters")
print("alpha1 : ", bs.outputAlpha1())
print("alpha2 : ", bs.outputAlpha2())

       
    
    

            
    





















