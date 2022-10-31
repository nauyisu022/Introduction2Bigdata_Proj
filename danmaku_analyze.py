import jieba, csv, paddle, collections, glob,os

paddle.enable_static()
jieba.enable_paddle()
jieba.load_userdict('jieba/user_dict.txt')




def make_word_lists(csv_file_path):
    with open(csv_file_path, 'r') as f:
        reader = csv.reader((line.replace('\0', '') for line in f))
        words = []
        for row in reader:
            try:
                x = jieba.lcut(row[0],cut_all=False)
            except Exception:
                x = []
            words += x
    return words


def repeat_filter(word):
    repeat_cha = ['哈', '6', '啊']
    for cha in repeat_cha:
        if word[0] == cha:
            flag = True
            for c in word:
                if c != cha:
                    flag = False
                    break
            if flag:
                word = cha * 3
    return word


def save_week_words(words,week):
    # if not os.path.exists("data/words"):
    #     os.makedirs("data/words")
    with open('data/words/Week_words{}.csv'.format(week), 'w', encoding='utf-8-sig') as f:
        csvfile = csv.writer(f)
        for word in words:
            csvfile.writerow([word, ])


def word_count(words):
    counts = {}
    for word in words:
        if len(word) == 1:  # 单个词语不计算在内
            continue
        else:
            word = repeat_filter(word)
            counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1
    items = list(counts.items())  # 将键值对转换成列表
    items.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序
    return counts

for week in range(1,2):
    csv_list = glob.glob('data/danmaku/Week{}/*.csv'.format(week))
    words=[]
    for csv_file_path in csv_list:
        words += make_word_lists(csv_file_path)
        save_week_words(words,week)
    print(week)



# words = []
# i = 0
# for csv_file_path in csv_list[:200]:
#     words += make_word_lists(csv_file_path)
#     print(i)
#     i = i + 1
#
# counts = word_count(words)
# print(counts)
