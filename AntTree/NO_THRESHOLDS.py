# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 15:58:34 2017

@author: nawatalab
"""


import Ant
import pandas as pd
import numpy as np
import scipy
import scipy.spatial.distance as dis
import time
import sys


#一匹のアリの接続限界　このアルゴリズムでは十分大きくする
Lmax = 9999



def Sim(i, j):
    ai = np.array(i.data)
    aj = np.array(j.data)
    ans = 0.0
    
    ans = np.linalg.norm(ai - aj) / np.sqrt(len(i.data))
    
    if ans > 1.0:
        ans = 1.0
        
    return 1.0 - ans

#アリの接続解除
#index : antのID
def ant_remove(index, ant):
    #子を持たない場合
    if len(ant[index].children) == 0:
        p = ant[index].parent[0]
        ant[p].rm_children(index)
        ant[index].disconect()
        #ant[index].first = True
        #要注意　サポートに戻った時初回に戻すか
        
    #子を持つ場合 再帰呼び出し
    else :
        for i in ant[index].children:
            ant_remove(i, ant)
            
            
def build_organize(a_pos, ai, ant) :
    #0-1匹のアリがa_posとつながっているとき
    if len(a_pos.children) < 2: 
          #aiとa_posをつなげる
          ai.set_parent(a_pos.Id)
          a_pos.set_children(Lmax, ai.Id)
    #2匹のアリがa_posとつながっている(初回)とき
    elif len(a_pos.children) == 2 and a_pos.first == True :
        #aiとより似ていないアリをa_posから取り去る
        tmp = Sim(ai, ant[a_pos.children[0]])         #a_posの一番目の子とaiとの類似度
        dsim = a_pos.children[0]                      #似てない方をとりあえず1番目の子に設定(dsim :　一番目の子のID)
        if Sim(ai, ant[a_pos.children[1]]) < tmp:     #a_posの2番目の子とaiとの類似度がtmpより小さいとき
              dsim = a_pos.children[1]                #似てないほうを2番目の子に設定
        
        #似ていない方をa_posから取る
        ant_remove(dsim, ant)
        a_pos.fin_first()
        
        #aiとa_posをつなげる
        ai.set_parent(a_pos.Id)
        a_pos.set_children(Lmax, ai.Id)
        
        
    #2匹以上のアリがa_posとつながっているとき
    elif len(a_pos.children) >= 2 and a_pos.first == False : 
        #a_posの子ノードの類似度最小設定
        #----Tdsim : a_posの子同士での最小類似度----
        tmp = 1.0
        for j in a_pos.children : 
            for k in a_pos.children : 
                if Sim(ant[j], ant[k]) < tmp : 
                    tmp = Sim(ant[j], ant[k])
                    a_pos.set_Tdsim(tmp)
                    
        #----a_plus : a_posの子の中で1番aiに類似するデータ
        tmp = 0.0
        for i in a_pos.children : 
            if Sim(ai, ant[i]) > tmp : 
                tmp = Sim(ai, ant[i])
                ai.set_plus(i)
        #===============================================
        
        if Sim(ai, ant[ai.a_plus]) < a_pos.Tdsim : #aiがa_plusと十分似ていない
              #aiとa_posをつなげる
              ai.set_parent(a_pos.Id)
              a_pos.set_children(Lmax, ai.Id)
              
        else : 
            #a_posに移動
            ai.set_pos(ai.a_plus)
            
    return 0
                              
       
def main(fname) : 
    data = []
    ant = []
    
    #データ読み込み
    O_data =pd.read_csv(fname)
    V_data = O_data.values
    np.random.shuffle(V_data) #ランダムに並び替える
    T_data = V_data.tolist()
    #データを0-1に標準化
    vmin = float(V_data.min())
    vmax = float(V_data.max())
    V_data = (V_data - vmin) / (vmax - vmin)
    #標準化されたデータのリスト
    data = V_data.tolist()
    X = []

    for i in range(len(data)) : 
        ant.append(Ant.d_Ant(data[i], i, 0))
        X.append(T_data[i]) #cluster_Ant用
        
    #木の構築
    count1 = 0 #繰り返し上限
    count2 = 0 #接続済みアリのアカウント
    while count1 < 1000 and count2 < len(data) - 1 :
        count2 = 0
        for ai in ant[1:] : #0番目はサポート
            if ai.conect == False : 
                a_pos = ant[ai.a_pos]
                build_organize(a_pos, ai, ant)
            else :
                count2 = count2 + 1
        count1 = count1 + 1
        
    #----サポート(root)の子の中で1番類似するデータ----
    tmp = 0.0
    for i in ant[0].children : 
        if Sim(ant[0], ant[1]) > tmp :
            tmp = Sim(ant[0], ant[i])
            ant[0].set_plus(i)
    #--------------------------------------------
    X = np.array(X)
    
    return ant, X, count1 - 1

    
                 

























 



