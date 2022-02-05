# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:25:15 2017



@author: nawatalab
"""


import Cluster


#アリにクラスタを振り分ける
def ant_label(ant):
    All_ant = ant
    index = ant[0].a_plus
    ant[index].set_label(0)
    ant[0].set_label(0)
    label = 1
    
    #print("idex:", index)
    #print("support children:", ant[0].children)
    
    #サポートの子どもにラベルをつける
    for i in ant[0].children:
        if ant[i].label == -1:
            ant[i].set_label(label)
            label = label + 1
            
    #すべてのアリにラベルを再帰的につけていく
    gave_label(All_ant, ant[0], label)
    
    tmp = []
    for ai in ant:
        tmp.append(ai.label)

        
    return tmp

def gave_label(All_ant,  ant, label):
    if ant.label == -1:
        ant.set_label(label)
    if len(ant.children) > 0:
        for i in ant.children:
            gave_label(All_ant, All_ant[i], ant.label)
            


#クラスタごとにリストに分割
def cluster_list(ant, k):
    cl = []
    cluster = []
    
    for i in range(k):
        cl.append([])
        
    
    for i in ant:
        cl[i.label].append(i)
    
    for i in range(k):
        cluster.append(Cluster.Cluster(cl[i]))
        
    
 
    return cluster
    










    
    

