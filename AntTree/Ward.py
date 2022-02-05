#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 12:51:10 2018

@author: miyamototatsuro
"""


# 使用ライブラリ
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster, set_link_color_palette

 

# 1. 入力データの読み込み
X = np.loadtxt('sample.csv', delimiter=',')

 

# 2. クラスター分析（ward法）を行う
z = linkage(X, method='ward')

 

# 3. 図のフォーマットを指定
plt.figure(figsize=(40, 25))
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 50
plt.title('Hierarchical Clustering Dendrogram', fontsize=60)
plt.xlabel('Observation Points', fontsize=55)
plt.ylabel('Distance', fontsize=55)

 

# 4. デンドログラムの作成
set_link_color_palette(['purple', 'lawngreen', 'green', 'blue', 'orange', 'red']) # ６クラスタまでの色を指定



dendrogram(z, leaf_font_size=20, color_threshold=7, above_threshold_color='black')
plt.show()
plt.gcf()
plt.savefig("single.png")

print('running......')

# 5. 各地点のクラスタ―番号の出力
#group = fcluster(z, 10, criterion='distance') # ユークリッド平方距離で分けたい場合
group = fcluster(z, 6, criterion='maxclust') # クラスタ数で分けたい場合
print(group)

