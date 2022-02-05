#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 17:02:09 2017

@author: miyamototatsuro
"""

#----------------------------textファイルを読み込み、表現ベクトルを獲得するソースコード(日本テキストデータ対象)---------------
#Bag of Words

from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import numpy as np
import codecs
import MeCab
from gensim import corpora 
from gensim import models
import csv
 


textNum = 400 #対象データの個数


#------------------------------------------MeCabの処理-------------------------------------------------
def tokenize(text):
    '''
    とりあえず形態素解析して名詞だけ取り出す感じにしてる
    文書のベクトル化で名詞以外の品詞も使うことができるが名詞だけの方が精度が良い
    '''
    node = mecab.parseToNode(text)
    while node:
        #yield node.surface.lower()
        #node = node.next
        #print(node.feature.split(',')[0])
        if (node.feature.split(',')[0] == '名詞'):
            yield node.surface.lower()
        node = node.next


def get_words(contents):
    '''
    記事群のdictについて、形態素解析してリストにして返す
    '''
    ret = []
    for k, content in contents.items():
        ret.append(get_words_main(content))
    return ret


def get_words_main(content):
    '''
    一つの記事を形態素解析して返す
    '''
    return [token for token in tokenize(content)]

#--------------------------------------------------------------------------------------------------------


def Sim(i, j): 
    ai = np.array(i)
    aj = np.array(j)
    
    #print(ai)
    #print(aj)
    
    ans = 0.0
    #偏角のcos 類似度
    #ans = dis.cosine(ai, aj)
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





mecab = MeCab.Tagger('mecabrc')
mecab.parse('') #これがないとUnicodeerror

f = []
training_docs = []
st = []
wd = []
sent = []

print('読み込みデータ数:', textNum)

for i in range(textNum):
    textname = 'tx' + str(i + 1) + '.txt'
    
    f.append(codecs.open(textname, 'r', 'utf-8'))
    
    st.append(f[i].read())
    f[i].close() 
    
    w = get_words({textname:st[i]})
    wd.append(w[0])
    
        



# 文書毎の単語のリスト(documents)からgensim.corporaを使い単語辞書を作成
# documents = [
#              ['John', 'likes', 'to', watch', 'movies', 'Mary', 'likes' 'movies', 'too'],
#              ['John', 'also', 'likes', 'to', 'watch', 'football', 'games'],
#             ]
dic = corpora.Dictionary(wd)
# 単語辞書から出現頻度の少ない単語及び出現頻度の多すぎる単語を排除
#「出現頻度がno_below文書未満の単語」及び、「(no_above*100)％以上の文書で登場する単語」を排除した。
dic.filter_extremes(no_below=2, no_above=0.9)


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
#次元数は10程度が良い結果に
#おそらくLSIでの次元削減がかなり有効
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




np.savetxt('sample.csv', X, delimiter=',', fmt = '%.18e')


print('finish')

#for i in range(textNum):
    #ans = Sim(X[52], X[i])
    #if(ans > 0.7): print('[', i + 1, ']:', ans)










