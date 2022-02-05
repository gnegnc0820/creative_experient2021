import re
import MeCab
import statistics

mecab = MeCab.Tagger("-Ochasen")

files = [
    ["kaden-channel", 864],
    ["movie-enter", 870],
    ["sports-watch", 900]
]

# 文をMeCab2.1を用いて形態素解析する．
# 形態素解析結果のうち，品詞が名詞で，かつ，品詞分類1が代名詞，数，非自立，副詞可能でない単語を抽出する．
# 抽出した単語のベクトルの総和を文のベクトルとする．ここで単語のベクトルはFastText[6]にWikipediaの全記事を学習させて求める．

words = dict()
# data = dict()
for f in files:
    
    words[f[0]] = list()
    # data[f[0]] = list()
    # print(words)
    
    for i in range(f[1]):
        file_name = f[0] + "/" + str(i+1).zfill(2) + ".txt"
        with open(file_name,"r",encoding="utf-8") as file_obj:

            text = file_obj.read()

            # 品詞が名詞 かつ，ng_pos でない単語を抽出する
            ng_pos = ["代名詞", "数", "非自立", "副詞可能", "サ変接続"]
            nouns = [line.split()[0] for line in mecab.parse(text).splitlines()
                        if ("名詞" in line.split()[-1]) 
                        and all((not(s in line.split()[-1])) for s in ng_pos)]


            # print(" ".join(words))

            for t in nouns:
                # print(str)
                words[f[0]].append(t)

N = 10

rem_words = [
    "http", "com", "T", "livedoor", "article", "news", "detail"
]

for f in files:
    fre_w = list()
    # print(len(words))

    words[f[0]] = [
        s for s in words[f[0]] if all((s != ng_words) for ng_words in rem_words)
    ]

    for i in range(N):
        mode = statistics.mode(words[f[0]])
        fre_w.append((words[f[0]].count(mode) ,mode))
        words[f[0]] = [
            s for s in words[f[0]] if s!=mode
        ]

    print(f[0])
    print(fre_w)
    print()
    
    # print(f[0])
    # print(f"mode :{words[f[0]].count(mode)} {mode}\n")
    # .count("word")
