 # -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 10:28:28 2017

@author: nawatalab
"""


"""
     if a_pos == ant[0] :の時アルゴリズム解説
            #ai : 移動アリ
            #a_pos : 移動アリが乗っているアリ(下にいるアリ)  (この場合はすなわち常に a_pos = a0)     
            #ant[ai.plus] : a_pos(=a0)の子のうち最もaiと類似度が高いアリ
        
            if(a_posに何も繋がっていない,最初の一回だけ):
                a0とaiを接続する(a_posとaiに親子関係をセット)
                繋げたaiを、とりあえずa0と最も類似度が高いアリとして設定する
            else:    
                if(aiとant[ai.plus]が十分に似ていたら):
                    aiをant[ai.plus]の背中に移動
                else
                    if(aiとant[ai.plus]が似ていなさすぎていたら):#すなわちant[ai.plus]は最も類似度が高いアリにも関わらずaiと全然似ていない
                        if(a0が接続限界に達しているなら):
                            ai.Tsimを更新する
                            aiをant[ai.plus]の背中に移動させる
                        else:
                            a0とaiを接続する(a_posとaiに親子関係をセット)  
                    else:(ai.Tdsim < Sim(ai, ai.plus) < ai.Tsim の時) 似ているとも似ていないとも言えない時
                        ai.Tsimを更新する
                        ai.Tdsimを更新する
"""


import Ant
import pandas as pd
import numpy as np
import scipy.cluster
import scipy.spatial.distance as dis
import time
from pylab import *
import matplotlib.pyplot as plt
from scipy.stats import norm
import csv
import codecs
import time
import random


Lmax = 10 #一匹のアリの接続限界
#seed = int(time.time()) #乱数生成を固定するための値(適当で良い)
                        #分類結果を多様にするためにtimeを代入しているが固定整数にすると実行時のアリのシャッフルを固定できる
# textNum = 400 #対象データの数
textNum = 2634


#乱数固定でランダムシャッフルを行う
def constant_shuffle(array, seed):
    np.random.seed(seed)
    np.random.shuffle(array)

#クラスタ数を表示
def show_cluster(code, X):

    clusterNum = []

    for i in range(textNum):
        clusterNum.append(code.count(i))
    
    del(clusterNum[clusterNum.index(0):])
    
    print('---------------clusters---------------')
    for i in range(len(clusterNum)):
        print('cluster[' + str(i) + ']:' + str(clusterNum[i]))
    print('--------------------------------------')
    print()
    print()

    
    


#データの読み込みと正規化などを行い、リスト化したデータを返す
def loadAntData(fname, seed):
    O_data = pd.read_csv(fname, header=None, nrows = textNum)
    
    V_data = O_data.values
    constant_shuffle(V_data, seed) #データをランダムに並び替える

    T_data = V_data.tolist()



    return V_data.tolist(), T_data #標準化されたデータのリスト


#アリに名前をつける(名前のリストはcsvで受け取る)
#アリに正解ジャンル番号をつける(正解ジャンル番号はcsvで受け取る)
def namingAnt(ant, seed):
    f = codecs.open('textlist.csv', 'r', 'utf-8-sig')
    g = codecs.open('genrelist.csv', 'r', 'utf-8-sig')

    """
    #antに文書を文字列で保持させる(あってもなくても良い)
    for i in range(textNum):
        textname = 'tx' + str(i + 1) + '.txt'
    
        t = codecs.open(textname, 'r', 'utf-8')   
        ant[i].set_textData(t.read())
        t.close() 
    """
    
    
    
    ls1 = csv.reader(f) 
    ls2 = csv.reader(g)
    
    textList = []
    genreList = []
    
    
    for ls, i in zip(ls1, range(textNum)):
        textList.extend(ls)
    f.close()
    
    for ls, i in zip(ls2, range(textNum)):
        genreList.extend(ls)
    g.close()
    #print(textList)

    textList = np.array(textList)       
    genreList = np.array(genreList)
    #print(textList)

    constant_shuffle(textList, seed)
    constant_shuffle(genreList, seed)
    
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

#2つのベクトルのコサイン類似度を返す
def _cos_sim(v1, v2):
    """
    2つのベクトルのコサイン類似度を返す
    """
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


#オブジェクト間の類似度(0-1)
#返す値が大きいほど類似度が高い
def Sim(i, j): 
    ai = np.array(i.originalData)
    aj = np.array(j.originalData)
    
    #print(ai)
    #print(aj)
    

    
    ans = 0.0
    #偏角のcos 類似度
    #ans = dis.cosine(ai, aj)
    #print(np.dot(ai,aj))
    #print(np.linalg.norm(ai))
    ans = np.dot(ai, aj) / (np.linalg.norm(ai) * np.linalg.norm(aj))
    #print(ans)
    #if(ans < 0.2): print(ans)
    
    #正規化ユークリッド距離
    #ans = np.linalg.norm(ai-aj) / np.sqrt(len(i.data))
    #ans = np.linalg.norm(ai-aj)
    #print(ans)
    #print("norm:", 1/ans)
    
    #if ans > 1.0 :
        #print ans, 0i.data, 0j.data
        #ans = 1.0
    #ansが0に近い　=> オブジェクト間の距離が近い => 似ている   
    
    #return 1.0 - ans 
    return ans

#a_posに接続されている全てのアリから一匹選びそのアリを返す(ant型を返す)
def randomSelectAnt(ant, a_pos):
    tmp = [a_pos.Id]
    tmp.append(a_pos.parent[0]) #a_posに繋がっている親アリIDを取得 (1つ上の階層に戻れる)
    #tmp.append(ant[a_pos.parent[0]].parent[0]) #さらにその親アリのIDを取得(2つ上の階層に戻れる)
    
    for i in a_pos.children: #a_posに繋がっている全ての子アリIDを取得　
        tmp.append(i)
    
           
    return ant[np.random.choice(tmp)] #--------a_posの近傍からランダムに選択(確率的なところ)-----------
        

#a_posに接続されている子アリのうち最もaiとの類似度が高いアリを返す(ant型を返す)
def mostSimilarAnt(ant, ai, a_pos):
    tmp = 0.0
    for i in a_pos.children:
        if Sim(ai, ant[i]) > tmp:
            tmp = Sim(ai, ant[i])
            ai.set_plus(i)
            
    return ant[ai.a_plus]

#2匹のアリの親子関係をセットする,引数は前者が親、後者が子
def setRelation(a_pos, ai):
    ai.set_parent(a_pos.Id)
    a_pos.set_children(Lmax, ai.Id)

#アリを組織化する(クラスタリング部分)  
def build_organize(a_pos, ai, ant, alpha1, alpha2): #(ant型, ant型, ant型, float, float)
    if a_pos == ant[0]: #a_posがサポートのとき
        if len(a_pos.children) == 0: #サポートにアリが全くつながっていない場合
            setRelation(a_pos, ai) #2匹のアリa_pos, ai間の親子関係をセット(この時a_pos = a0)
            a_pos.set_plus(ai.Id)#plusは、自分自身と、自分と繋がっている全てのアリとの類似度を比較し最も類似度が高いアリのID
            a_pos.set_parent(0)
            #print(ai.Id)
        else: #サポートにアリが一匹以上つながっている場合
            a_plus = mostSimilarAnt(ant, ai, a_pos)#a_plus : a_pos につながっている子の中で一番aiに類似するアリ
            
            if Sim(ai, a_plus) >= ai.Tsim: #類似度が高ければ移動
                ai.set_pos(a_plus.Id) #aiをa_plusに移動
            else:
                #Tdsim:全く似ていないというボーダーライン
                #すなわちTdsimを下回る類似度の2匹のアリたちはどうしようもなく似ていない
                
                #移動アリaiと、それと一番類似度が高いアリa_plusさえ全然似ていないならば
                if Sim(ai, a_plus) < ai.Tdsim: 
                    if len(a_pos.children) >= Lmax:
                        ai.dec_Tsim(alpha1) #類似閾値を更新(類似判定をちょっと甘めにする)
                        ai.set_pos(a_plus.Id) #aiをa_plusに移動
                    else: #Lmaxに達していないなら    
                        #print(ai.Id)
                        setRelation(a_pos, ai) #2匹のアリa＿pos, ai間の親子関係をセット
                else:
                    #現在の位置を保つ　a_pos = a0のまま
                    ai.set_pos(0)
                    ai.dec_Tsim(alpha1)
                    ai.inc_Tdsim(alpha2)
    else: #a_pos がその他のアリのとき
        a_k = randomSelectAnt(ant, a_pos) #a_k : a_posに接続されている全てのアリからランダムに一匹選んだもの(ant型)
        a_plus = mostSimilarAnt(ant, ai, a_pos) #a_plus : a_pos の子の中で一番aiに類似するデータ   
        
        if Sim(ai, a_pos) >= ai.Tsim:
            if Sim(ai, a_plus) < ai.Tdsim:
                if len(a_pos.children) >= Lmax:
                    ai.set_pos(a_k.Id) #aiをa_kに移動
                else:
                    setRelation(a_pos, ai) #2匹のアリa＿pos, ai間の親子関係をセット
            else:
                ai.dec_Tsim(alpha1)
                ai.inc_Tdsim(alpha2)
                ai.set_pos(a_k.Id) #aiをa_kに移動
        else:
            ai.dec_Tsim(alpha1)
            ai.inc_Tdsim(alpha2)
            ai.set_pos(a_k.Id) #a_kに移動
    return 0
    
#if __name__ == '__main__'
def main(fname, alpha1, alpha2):
    data = []
    ant = []
    X = []
    seed = time.time()
    seed = int(seed - random.randint(100000, 100000000))

    
    #データの読み込み
    data, T_data = loadAntData(fname, seed) #標準化されたデータのリスト
    # print(len(data))
 
    #アリを生成する
    ant, X = generateAnt(ant, data, T_data) 
    
    #アリに名前をつける
    namingAnt(ant, seed)
  
    #木の構築
    count1 = 0 #繰り返し上限
    count2 = 0 #接続済みのアリのカウント
    
    while count1 < 1000 and count2 < len(data) - 1:
        count2 = 0
        #if count1 % 100 == 0 : print("count1:", count1)
        for ai in ant[1:]: #ant[0] 即ちサポートは除く
            #print(ai.name)
            if ai.conect == False:
                a_pos = ant[ai.a_pos] #ここで左辺a_posはant型オブジェクト
                                      #しかし右辺ant[ai.a_pos]のa_posはint型フィールド
                                      #全くの別物
                build_organize(a_pos, ai, ant, alpha1, alpha2)
            else:
                count2 = count2 + 1
                #print('done:', ai.name)
        count1 += 1
        #print(count1)
                                 
    #サポート役のアリの子のうち、最もサポート役のアリに類似するアリを探す
    #最終的にサポート役のアリはそのアリと同じクラスタとみなす              
    #tmp = alpha1
    tmp = 0.0
    for i in ant[0].children:
        if Sim(ant[0], ant[i]) > tmp:
            tmp = Sim(ant[0], ant[i])
            ant[0].set_plus(i)
    
    
    tmp = ant[0].children.index(ant[0].a_plus)
    ant[0].children[0], ant[0].children[tmp] = ant[0].children[tmp], ant[0].children[0]
        
    X = np.array(X)

    return ant, X, count1-1
    #print "id data parent children a_plus conect Tsim Tdsim Pos"
    #for ai in ant:
    #   print ai.id, si.data, ai.parent, ai.children, ai.a_plus, ai.connect, ai.Tsim, ai.Tsim, ai.a_pos
    #print "count1:", count1, "count2:", count2
        
                
                
                
                
                
                
                
    