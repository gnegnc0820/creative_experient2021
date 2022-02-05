#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 11:45:38 2017

@author: miyamototatsuro
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 13:35:37 2017

@author: miyamototatsuro
"""

# -*- coding: utf-8 -*-

#----------------------textファイルを読み込み、表現ベクトルを獲得するソースコード(英テキストデータ対象)-----------------



from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import numpy as np
import codecs
import MeCab


textNum = 5 #解析対象テキストの数


# 空のリストを作成（学習データとなる各文書を格納）
training_docs = []
 
# 各文書を表すTaggedDocumentクラスのインスタンスを作成
# words：文書に含まれる単語のリスト（単語の重複あり）
# tags：文書の識別子（リストで指定．1つの文書に複数のタグを付与できる）



f = []
st = []
sent = []

for i in range(textNum):
    #テキストファイル名を指定
    textname = 'arxiv' + str(i + 1) + '.txt'
    
    f.append(codecs.open(textname, 'r', 'utf-8'))
    
    st.append(f[i].read()) #リストst[]にファイルの中身を格納
    st[i] = st[i].split() #スペースで区切る(単語ごとに区切る)
    f[i].close() 
    
    tagname = 'd' + str(i + 1)
    sent.append(TaggedDocument(words = st[i], tags = [tagname]))
    training_docs.append(sent[i])
    print(textname)


# 学習実行（パラメータを調整可能）
# documents:学習データ（TaggedDocumentのリスト）
# min_count=1:最低1回出現した単語を学習に使用する
# dm=0:学習モデル=DBOW（デフォルトはdm=1:学習モデル=DM）
model = Doc2Vec(documents=training_docs, min_count=1, dm=0)
 
# 学習したモデルを保存
model.save('doc2vec.model')
 
# 保存したモデルを読み込む場合
# model = Doc2Vec.load('doc2vec.model')
 
# ベクトル'd1'を表示（型はnumpy.ndarray）
#print(model.docvecs['d1'])


X = []
for i in range(textNum):
    tagname = 'd' + str(i + 1)
    X.append(model.docvecs[tagname])

np.savetxt("sample.csv", X, delimiter=",")

print(model.docvecs.most_similar('d1'))
"""
# 各文書と最も類似度が高い文書を表示（デフォルト値：10個）
print(model.docvecs.most_similar('d1'))
print(model.docvecs.most_similar('d2'))
print(model.docvecs.most_similar('d3'))
print(model.docvecs.most_similar('d4'))
"""

