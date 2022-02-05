#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 15:31:46 2018

@author: miyamototatsuro
"""

import codecs

N = 1000

for i in range(N):
    textname = 'tx' + str(i + 1) + '.txt'
    #textname = 'extext.txt'

    
    f = codecs.open(textname, 'r', 'utf-8')
    lines = f.readlines()
    
    #不要な文字の削除
    String = []
    for i in lines:
        String.append(i.replace('>', '').replace('<', '').replace('-', '').replace('*', '').replace('|', '').replace('!', '').replace('?', '').replace('@', ''))      
    f.close()
    
    
    #不要文字削除後の文字列を上書きする(追加記入ではない)
    #for文の範囲を指定する
    f = codecs.open(textname, 'w', 'utf-8')
    for s in String[6:len(String) - 2]:
        f.write(s)  
    f.close()

