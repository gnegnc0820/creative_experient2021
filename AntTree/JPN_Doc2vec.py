#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 14:20:26 2017

@author: miyamototatsuro
"""

#----------------------------textファイルを読み込み、表現ベクトルを獲得するソースコード(日本テキストデータ対象)-----------------------
#Doc2vec

from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import numpy as np
import codecs
import MeCab
from gensim import corpora 
from gensim import models

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



print()
print()
print('Leaning.....')
print()
print()


mecab = MeCab.Tagger('mecabrc')
mecab.parse('') #これがないとUnicodeerror


f = []
training_docs = []
st = []
wd = []
sent = []

for i in range(textNum):
    textname = 'tx' + str(i + 1) + '.txt'
    
    f.append(codecs.open(textname, 'r', 'utf-8'))
    
    st.append(f[i].read())
    f[i].close() 
    
    w = get_words({textname:st[i]})
    wd.append(w[0])
    
    tagname = 'd' + str(i + 1)
    sent.append(TaggedDocument(words = wd[i], tags = [tagname]))
    training_docs.append(sent[i])
    #print(textname)
    #print(wd[i])


# 学習実行（パラメータを調整可能）
# documents:学習データ（TaggedDocumentのリスト）
# min_count=1:最低1回出現した単語を学習に使用する
# dm=0:学習モデル=DBOW（デフォルトはdm=1:学習モデル=DM）
# DBOWは単語の順序が考慮されないがシンプルな構造
#size : 生成する文書ベクトルの要素数
#iter : 反復回数
#window : ウィンドウサイズ
model = Doc2Vec(size = 10, documents=training_docs, min_count=1, dm=0, iter = 30, window = 5, workers = 2)
 
# 学習したモデルを保存
model.save('doc2vec.model')

 
X = []
for i in range(textNum):
    tagname = 'd' + str(i + 1)
    X.append(model.docvecs[tagname])




# ベクトル'd1'を表示（型はnumpy.ndarray）
print(model.docvecs['d1'])


np.savetxt("sample.csv", X, delimiter=",")
print('finish')
 


print(model.docvecs.most_similar('d1'))
print()


#print(model.most_similar("動物"))
#print(model.most_similar(positive=["世界中"], negative=["日本"]))



"""
# 各文書と最も類似度が高い文書を表示（デフォルト値：10個）
print(model.docvecs.most_similar('d1'))
print(model.docvecs.most_similar('d2'))
print(model.docvecs.most_similar('d3'))
print(model.docvecs.most_similar('d4'))
"""
for i in range(textNum):
    ans = Sim(X[89], X[i])
    if(ans > 0.7): 
        print('[', i + 1, ']:', ans)




    


