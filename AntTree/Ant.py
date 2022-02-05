# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 10:27:20 2017

@author: nawatalab
"""


import numpy as np

#確率論的アルゴリズム:AntTree_STOCH
class Ant():
    def __init__(self, originalData, data, Id, pos, code = 0):
        self.data = originalData / np.linalg.norm(originalData)#実際に計算に使う正規化されたベクトルdata(sorted)
        self.originalData = originalData #オリジナルのデータ
        self.textData = 'none'
        self.a_plus = 0
        self.a_pos = pos #int型
        self.Tsim = 1.0 #類似閾値:この値よりも高類似度のアリ同士は接続される
        self.Tdsim = 0 #非類似閾値:この値よりも低類似度のアリ同士は全く似ていないと判断され、その時点で同じ親に接続される(兄弟になる)
        self.parent = []
        self.children = []
        self.Id = Id
        self.conect = False
        self.label = -1
        self.code = code
        self.name = 'none' #str型 antが表現するものの名称(記事のタイトルなど)
        self.genre = 'none' #
 
    
        
    def set_parent(self, P):
        self.parent.append(P)  #int型リスト(IDが格納)
        self.conect = True
        
    def set_children(self, Lmax, child):
        if len(self.children) < Lmax:
            self.children.append(child) #int型リスト(IDが格納)
            
    def set_plus(self, Id):
        self.a_plus = Id #int型 selfと最も類似度が高いアリのID
        
        
    def set_pos(self, pos):
        self.a_pos = pos
        
        
    def set_label(self, label):
        self.label = label
        
    def dec_Tsim(self, alpha1):
        self.Tsim = self.Tsim * alpha1
        
    def inc_Tdsim(self, alpha2):
        self.Tdsim = self.Tdsim + alpha2
    
    def set_name(self, n):
        self.name = n
    
    def set_genre(self, n):
        self.genre = n
    
    def set_textData(self, t):
        self.textData = t
        
#決定論的アルゴリズム : AntTree_NO=THRESHOLDS
class d_Ant(Ant) : #Antクラスの継承
    first = True #初回かどうか
    
    def fin_first(self) :
        self.first = False
        
    def set_Tdsim(self, Td) : 
        self.conect = not self.conect
        
    def change_conect(self) : 
        self.conect = not self.conect
    
    def disconect(self):
        self.parent.pop()
        self.set_pos(0)
        self.set_plus(0)
        self.change_conect()
        
    def rm_children(self, i):
        self.children.remove(i)
        
        
        
        

