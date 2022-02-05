#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 12:52:35 2017

@author: miyamototatsuro
"""
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
import Ant
import csv
import Cluster
import random
import codecs
from graphviz import Digraph
import random


N =10 #生成クラスタ数
LOOP = 1#繰り返し回数



#データの読み込みと正規化などを行い、リスト化したデータを返す
def loadAntData(fname):
    O_data = pd.read_csv(fname, header=None)
    
    V_data = O_data.values
    

    return V_data #標準化されたデータのリスト




#アリに名前をつける(名前のリストはcsvで受け取る)
#アリに正解ジャンル番号をつける(正解ジャンル番号はcsvで受け取る)
def namingAnt(ant):
    f = codecs.open('textlist.csv', 'r', 'utf-8-sig')
    g = codecs.open('genrelist.csv', 'r', 'utf-8-sig')
    
    ls1 = csv.reader(f) 
    ls2 = csv.reader(g)
    
    textList = []
    genreList = []

    for i in ls1:
        textList.extend(i)
    f.close()
    
    for i in ls2:
        genreList.extend(i)
    g.close()
    #print(textList)

    textList = np.array(textList)       
    genreList = np.array(genreList)
    #print(textList)

    
    for i in range(len(ant)):
        ant[i].set_name(textList[i])
        ant[i].set_genre(genreList[i])



#アリを生成する
def generateAnt(ant, data, T_data):
    X = []
    for i in range(len(data)):
        ant.append(Ant.Ant(T_data[i], data[i], i, 0)) #ant.append(Ant.Ant([], 0, 0)) #root 根 サポート役
        X.append(T_data[i]) #cluster_Ant用
        
    

    return ant, X




##Id(int型)を受け取り、そのIdを持つant型を返す
def searchAnt(ant, Id):
    for i in ant:
        if(i.Id == Id): return i

    return 0

#再帰的に親子関係を辺で結んでいく
def writeResult(ant, antA, G):  
    for i in antA.children:
        r = random.randint(10, 20)
        ai = searchAnt(ant, i)
        G.edge(antA.name, ai.name, penwidth = '1', color = 'white')
        
        writeResult(ant, ai, G)
    
    return 





#-------------------------------------------------------------------------------------
#k-means法だがデータ処理が楽なのでデータはant型で扱う

fname = 'sample.csv'

ARave = 0 #LOOP回繰り返した結果の総平均正答率
maxScore = 0 #LOOP回繰り返したうち最も良かった時の平均正答率
minScore = 100 #LOOP回繰り返したうち最も悪かった時の平均正答率
SUM = 0
ant = []

for i in range(LOOP):

    ant = []
    features = []

    data = loadAntData(fname)
    ant, X = generateAnt(ant, data, data)
    print(type(ant))
    namingAnt(ant)
    
    random.shuffle(ant)
    
    for i in ant:
        features.append(i.originalData)
        
    # K-means クラスタリングをおこなう
    #n_clusters : 生成クラスタ数
    #(メルセンヌツイスターの乱数の種を 10 とする)
    kmeans_model = KMeans(n_clusters=N, random_state=10).fit(features)

    # 分類先となったラベルを取得する
    labels = kmeans_model.labels_
    #print(labels.tolist())
    
    #クラスタリング結果を元にClusterクラスを生成
    #前処理
    tuple = []
    a = ant
    for label, a in zip(labels, a):
        tuple.append((label, a))

    #Clusterクラスを生成 
    cluster = []  
    for i in range(N):
        p = []
        for j in tuple:
            if(i == j[0]):
                p.append(j[1])
    
        cluster.append(Cluster.Cluster(p))
    

    
    #クラスタリング結果表示  
    #ただし要素数が1つしかないクラスタに関しては正答率の計算から除外して考える
    noresult = 0.0  #要素数1のクラスタの数
    print('---------------cluster--------------')
    for i in range(N):  
        a = 1
        print('cl[', i, ']:', cluster[i].out_Num())
    print('------------------------------------')   
    
    s = 0.0   
    for i in range(N):
        cluster[i].determineGenre()
        #score = cluster[i].POCA()
        score = cluster[i].out_correctN()
        #print('cl[' + str(i) + ']:', score)
        s += score
    scoreAve = s / len(data)
    if(scoreAve > maxScore): maxScore = scoreAve
    if(minScore > scoreAve): minScore = scoreAve
    
    print('正答率平均:', scoreAve)
    #print()

    
    SUM += scoreAve
        #print('[', i, ']:', cluster[i].POCA())

  

print('---------------------------結果-----------------------')        
ARave = SUM / LOOP
print('正答率平均:', ARave)
print('max:', maxScore)
print('min:', minScore)
print('クラスタ数:', N)
print('繰り返し回数:', LOOP)

#結果の可視化のために擬似的な木構造を作成する
fakeAnt = Ant.Ant(-1, -1, -1, -1)#擬似的なrootアリ作成
Lmax = 10000
for i in cluster:
    fakeAnt.set_children(Lmax, i.factors[0].Id)
    for j in i.factors[1:]:
        i.factors[0].set_children(Lmax, j.Id)
        
        
        
#=======================================グラフの可視化に関する処理==================================        
        
    
#formatはpngを指定(他にはPDF, PNG, SVGなどが指定可)
#engine : グラフ表示方法を指定(木構造状、放射線状など)デフォルトはdotだがcircoよし
#空グラフ生成
#pdfで生成するとめっちゃ早いけど全貌が見れない
#png, jpgは重いけど全貌が見れる
G = Digraph(format='pdf', engine = 'circo')

#初期化
G.attr('node', shape='circle')
   
#ノードの追加
c = 'none'
G.node('root', fillcolor = 'black', style = 'black', penwidth = '1', width = '3')
for i in ant:
    genre = int(i.genre)
    if(genre == 1): c = 'red'
    elif(genre == 2): c = 'green'
    elif(genre == 3): c = 'blue'
    elif(genre == 4): c = 'orange'
    elif(genre == 5): c = 'white'
    else : c = 'white'
    G.node(i.name, fillcolor = c, style = 'filled', penwidth = '1', width = '3')#width=3にはしないほうがいいファイルサイズが大きくなりすぎる

#擬似rootアリの辺を追加
for i in cluster:
    G.edge('root', i.factors[0].name, penwidth = '1', color = 'white')

#辺の追加
for i in cluster:
    writeResult(ant, i.factors[0], G)
      
# print()するとdot形式で出力される
#print(G)
#AntStructure.pngで保存
G.render('aK-meansStructure')
print('finish')




















    