import numpy as np
from LanguageAnalysis import languageAnalysis
from nltk import word_tokenize

def correct_word(word_list, item_list):
    for i, words in enumerate(word_list):
        tmp = words[0].split(" ")
        res = ""
        for j, word in enumerate(tmp):
            if word not in item_list:
                word_pairs = []
                for item in item_list:
                    word_pairs.append([word, item])
                dis = list(map(edit_distance, word_pairs))
                if min(dis) > 2:
                    return None
                else:
                    word = word_pairs[dis.index(min(dis))][1]
                    # words[words.index(word)] = word_pairs[dis.index(min(dis))][1]
            if j != 0:
                res += " " + word
            else:
                res += word
        word_list[i] = list()
        word_list[i].append(res)
    return word_list


def edit_distance(word_pair):
    m = []
    if len(word_pair[1]) == 0:
        return len(word_pair[0])
    for i in range (len(word_pair[0]) + 1):
        m.append([])
        for j in range (len(word_pair[1]) + 1):
            m[i].append(0)
    for i in range (len(word_pair[0]) + 1):
        m[i][0] = i
    for j in range (len(word_pair[1]) + 1):
        m[0][j] = j
    for i in range (1, len(word_pair[0]) + 1):
        for j in range (1, len(word_pair[1]) + 1):
            if word_pair[0][i - 1] == word_pair[1][j - 1]:
                m[i][j] = min(m[i - 1][j] + 1, m[i][j - 1] + 1, m[i - 1][j - 1])
            else:
                m[i][j] = min(m[i - 1][j] + 1, m[i][j - 1] + 1, m[i - 1][j - 1] + 1)
    return m[len(word_pair[0])][len(word_pair[1])]


if __name__ == "__main__":
    word = input()
    item_list = []
    while True:
        item = input()
        if item != "#":
            item_list.append(item)
        else:
            break
    print(correct_word(word, item_list))