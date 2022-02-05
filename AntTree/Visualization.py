#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 18:58:48 2018

@author: miyamototatsuro
"""


#N = 400#データ数　

from graphviz import Digraph


##Id(int型)を受け取り、そのIdを持つant型を返す
def searchAnt(ant, Id):
    for i in ant:
        if(i.Id == Id): return i

    return 0

#再帰的に親子関係を辺で結んでいく
def writeResult(ant, antA, G):  
    for i in antA.children:
        ai = searchAnt(ant, i)
        G.edge(antA.name, ai.name, penwidth = '7')
        writeResult(ant, ai, G)
    
    return 



#if __name__ == '__main__'
def main(ant):
    print()
    print()
    print('グラフ作成中')
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
    for i in ant:
        genre = int(i.genre)
        if(genre == 1): c = 'red'
        elif(genre == 2): c = 'green'
        elif(genre == 3): c = 'blue'
        elif(genre == 4): c = 'orange'
        elif(genre == 5): c = 'white'
        else : c = 'white'
        G.node(i.name, fillcolor = c, style = 'filled', penwidth = '5', width = '2')#width=3にはしないほうがいいファイルサイズが大きくなりすぎる

    #辺の追加
    writeResult(ant, ant[0], G)
            
    # print()するとdot形式で出力される
    #print(G)

    #AntStructure.pngで保存
    G.render('AntStructure')
    print('finish')
    
    
    






