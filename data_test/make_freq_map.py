import re
import MeCab
import statistics
import pickle
import numpy as np
from numpy.core.fromnumeric import size

from sklearn.decomposition import PCA

import matplotlib.pyplot as plt

mecab = MeCab.Tagger("-Ochasen")

files = [
    ["kaden-channel", 864, "red"],
    ["movie-enter", 870, "blue"],
    ["sports-watch", 900, "orange"]
]

data = None
with open("freq_words", "rb") as f:
    data = pickle.load(f)

print(type(data))

plt.figure(figsize=(10,10))

vec = list()
words = list()

for i in range(len(files)):
    for d in data[i]:    
        vec.append(d[2])
        words.append([d[1],files[i][2]])

X = np.array(vec)

pca = PCA(n_components=2)
pca.fit(X)
X_2d = pca.transform(X)


for i in range(len(X_2d)):
    plt.plot(X_2d[i][0],X_2d[i][1], ms=8.0, zorder=5, marker="x", color=words[i][1])
    # plt.annotate(words[i][0], (X_2d[i][0],X_2d[i][1]), size=10, fontname="MS Gothic")

plt.show()