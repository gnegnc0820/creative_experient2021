from os import write
import re
import MeCab
import pickle
import numpy as np

files = [
    ["kaden-channel", 864, 1],
    ["movie-enter", 870, 2],
    ["sports-watch", 900, 3]
]

# 文をMeCab2.1を用いて形態素解析する．
# 形態素解析結果のうち，品詞が名詞で，かつ，品詞分類1が代名詞，数，非自立，副詞可能でない単語を抽出する．
# 抽出した単語のベクトルの総和を文のベクトルとする．ここで単語のベクトルはFastText[6]にWikipediaの全記事を学習させて求める．

# # 日本語wikipediaから学習した300次元のモデル
# model_path = "../wiki_fasttext.pickle"
# model = None
# with open(model_path, "rb") as f:
#     model = pickle.load(f)

# 保存用のデータオブジェクト
data = dict()
for name in files:
    data[name[0]] = list()


X = list()
for f in files:
    for i in range(f[1]):
        file_name = "wakati-hinshi/"+f[0]+"/"+str(i+1).zfill(2) # +".txt"
        with open(file_name+".vector","rb") as file_obj:
            vec = pickle.load(file_obj)
            # data[f[0]].append(vec)
            X.append(vec)

# for i in range(textNum):
#     tagname = 'd' + str(i + 1)
#     X.append(model.docvecs[tagname])

np.savetxt("sample.csv", X, delimiter=",")

d = []
n = []
numfile = open("genrelist.csv", "w")
namefile = open("textlist.csv", "w")

for file in files:
    for x in range(file[1]):
        numfile.write(str(file[2]) + "\n")
        namefile.write(file[0] + str(x+1) + "\n")
        
        # n.append(file[2])
        # d.append(file[0] + str(x+1))

numfile.close()
namefile.close()

# d = np.array(d,dtype=object)
# n = np.array(n,dtype=object)

# np.savetxt("textlist.csv", d, delimiter=",")
# np.savetxt("genrelist.csv", n, delimiter=",")

    # f = codecs.open('textlist.csv', 'r', 'utf-8-sig')
    # g = codecs.open('genrelist.csv', 'r', 'utf-8-sig')
# print(data["kaden-channel"][0])
# write_obj = open("wakati-hinshi/vec_datas.dict", "wb")
# pickle.dump(data, write_obj)
# write_obj.close