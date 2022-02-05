from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from sklearn.cluster import KMeans
import sys
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import pickle
import statistics

files = [
    ["kaden-channel", 864, 0],
    ["movie-enter", 870, 1],
    ["sports-watch", 900, 2]
]

data_path = "wakati-hinshi/vec_datas.dict"
with open(data_path, "rb") as f:
    datas = pickle.load(f)

#ベクトルをリストに格納
# vectors_list=[m.docvecs[n] for n in range(len(m.docvecs))]
vectors_list = datas["kaden-channel"] + datas["movie-enter"] + datas["sports-watch"]

#ドキュメント番号のリスト
doc_nums=range(0,len(vectors_list))

def main():

    #クラスタリング設定
    n_clusters = 10
    kmeans_model = KMeans(n_clusters=n_clusters)# , verbose=0, random_state=1)#, n_jobs=-1)

    #クラスタリング実行
    kmeans_model.fit(vectors_list)
    pred = kmeans_model.fit(vectors_list)

    print(pred)

    #クラスタリングデータにラベル付け
    labels=kmeans_model.labels_
    # print(len(labels))

    res = list()
    s = 0
    # クラスタリング

    # print(len(vectors_list))


    for file in files:
        # 正解のラベルとクラスタリング結果を対応させる
        for i in range(file[1]):
            res.append({"ans":file[2], "res":labels[s], "vec":vectors_list[s]})
            s += 1

    # print(res[100])
    # 各クラスタの正解ラベルを決定する

    tmp = [[] for i in range(10)]
    c_vectors = [[] for i in range(10)]
    center = np.zeros(len(vectors_list[0]))
    # 全データの距離二乗和
    T = 0

    for d in res:
        # print(d["res"])
        # print(tmp)
        tmp[d["res"]].append(d["ans"])
        c_vectors[d["res"]].append(d["vec"])
        # T += np.dot(center, d["vec"])
        T += np.sqrt(np.linalg.norm(d["vec"], ord=2))
    # print(type(T))

    res = list()
    # print(len(center))
    sum_correct = 0
    sumPg = 0
    for x in range(len(tmp)):
        c_mode = statistics.mode(tmp[x])
        s = 0
        Pg = 0
        for t in tmp[x]:
            if t == c_mode:
                s += 1
        
        for d in c_vectors[x]:
            # Pg += np.dot(center, d)
            Pg += np.sqrt(np.linalg.norm(d, ord=2))
            # print(type(d))
        sumPg += Pg
        
        # print(f"クラスタ{x}の正解 : {c_mode}\t要素数{len(tmp[x])}\t正答率{s/len(tmp[x])}")

        n = len(vectors_list)
        G =  10
        pseudoF = ((T-Pg)/(G-1)) / (Pg / (n-G))

        sum_correct += s
        
    # print(f"全体の正答率 :{sum_correct/len(vectors_list)}")
    # print(type(Pg))
    print(f"正答数 : {sum_correct}")
    print(f"正答率 : {sum_correct/len(vectors_list)}")

    pseudoF = ((T-Pg)/(G-1)) / (sumPg / (n-G))
    print(f"P_F : {pseudoF}")

    # print(f"P_F : {pseudoF}")
    # print(f"T : {T}")
    # print(f"sumPg : {T}")
    # print(f"T : {T}")


    # pseudoF = ((T-Pg)/(G-1)) / (Pg / (n-G))
    # Pg : 各クラスタ内距離2乗和
    # T : 全データの距離2乗和
    # n : 全データ数
    # G : クラスタ数

for i in range(10):
    main()