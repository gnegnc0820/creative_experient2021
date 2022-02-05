import re
import MeCab


mecab = MeCab.Tagger("-Ochasen")

files = [
    ["kaden-channel", 864],
    ["movie-enter", 870],
    ["sports-watch", 900]
]

# 文をMeCab2.1を用いて形態素解析する．
# 形態素解析結果のうち，品詞が名詞で，かつ，品詞分類1が代名詞，数，非自立，副詞可能でない単語を抽出する．
# 抽出した単語のベクトルの総和を文のベクトルとする．ここで単語のベクトルはFastText[6]にWikipediaの全記事を学習させて求める．

for f in files:
    for i in range(f[1]):
        file_name = f[0]+"/"+str(i+1).zfill(2)+".txt"
        with open(file_name,"r",encoding="utf-8") as file_obj:
            
            words = list()
            data = list()

            text = file_obj.read()

            # 品詞が名詞 かつ，ng_pos でない単語を抽出する
            ng_pos = ["代名詞", "数", "非自立", "副詞可能"]
            nouns = [line.split()[0] for line in mecab.parse(text).splitlines()
                        if ("名詞" in line.split()[-1]) 
                        and all((not(s in line.split()[-1])) for s in ng_pos)]


            # print(" ".join(words))
            for str in nouns:
                print(str)
            
            print()
            exit()

            with open("wakati-hinshi/"+file_name, "w", encoding="utf-8") as write_file_obj:
                for d in data:
                #     write_file_obj.write(" ".join(d)+"\n")
                #     # print(d)
                    write_file_obj.write(d)
