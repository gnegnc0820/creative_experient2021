#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 16:09:39 2018

@author: miyamototatsuro
"""

#----------------------------textファイルを読み込み、表現ベクトルを獲得するソースコード(日本テキストデータ対象)---------------
#Bag of Words

from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import numpy as np
import codecs
from gensim import corpora 
from gensim import models
 


textNum = 2000 #対象データの個数


def Sim(i, j):
    ai = np.array(i)
    aj = np.array(j)
    
    #print(ai)
    #print(aj)
    
    ans = 0.0
    #偏角のcos 類似度
    ai = ai / np.linalg.norm(ai)
    aj = aj / np.linalg.norm(aj)
    ans = np.dot(ai, aj) / (np.linalg.norm(ai) * np.linalg.norm(aj))
    if(ans > 2): print(ans)
    #正規化ユークリッド距離
    #ans = np.linalg.norm(ai-aj) / np.sqrt(len(i.data))
    #ans = np.linalg.norm(ai-aj)
    #print("norm:", ans)
    
    #if ans > 1.0 :
        #print ans, 0i.data, 0j.data
        #ans = 1.0
    #ansが0に近い　=> オブジェクト間の距離が近い => 似ている   
    
    #return 1.0 - ans 
    return ans




f = []
training_docs = []
st = []
wd = []
sent = []

for i in range(textNum):
    
    #テキストファイル名を指定
    textname = 'tx' + str(i + 1) + '.txt'
    
    f.append(codecs.open(textname, 'r', 'utf-8'))
    
    st.append(f[i].read()) #リストst[]にファイルの中身を格納
    st[i] = st[i].split() #スペースで区切る(単語ごとに区切る)
    f[i].close() 
    
    wd = st

        



# 文書毎の単語のリスト(documents)からgensim.corporaを使い単語辞書を作成
# documents = [
#              ['John', 'likes', 'to', watch', 'movies', 'Mary', 'likes' 'movies', 'too'],
#              ['John', 'also', 'likes', 'to', 'watch', 'football', 'games'],
#             ]
dic = corpora.Dictionary(wd)
# 単語辞書から出現頻度の少ない単語及び出現頻度の多すぎる単語を排除
#「出現頻度がno_below文書未満の単語」及び、「(no_above*100)％以上の文書で登場する単語」を排除した。
dic.filter_extremes(no_below=10, no_above=0.9)
# Bag of Wordsベクトルの作成
bow_corpus = [dic.doc2bow(d) for d in wd]


# TF-IDFによる重み付け
tfidf_model = models.TfidfModel(bow_corpus)
tfidf_corpus = tfidf_model[bow_corpus]



#for doc in tfidf_corpus:
    #print(doc)


# LSIによる次元削減
#獲得する表現ベクトルの要素数は,num_topicsにより変化させることができる
#ただし最大でもデータ数まで
#次元の呪いの関係上、要素数が多ければ良いとは言えない
lsi_model = models.LsiModel(tfidf_corpus, id2word=dic, num_topics=10)
lsi_corpus = lsi_model[tfidf_corpus]


#LSI_corpusの中身をVに格納
V = []
for doc in lsi_corpus:
    V.append(doc)

#文書の表現ベクトルをXに格納
v = []
X = []
for i in V:
    for j in i: 
        v.append(j[1])
        
    X.append(v)
    v = []







np.savetxt("sample.csv", X, delimiter=",")
print('finish')

for i in range(textNum):
    ans = Sim(X[52], X[i])
    #if(ans > 0.6): print('[', i + 1, ']:', ans)





