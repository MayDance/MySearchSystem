import os
import tools
import html
import operator
import copy
import nltk
from SpellCorrect import SpellCorrect
from InvertedIndex import getIndex
from LanguageAnalysis import languageAnalysis
from Searching import searchWord
from BoolSearch import BoolSearchDel
from scoreQuery import sortDoc
from TermDocWeightMatrix import TermDocWeight


# 该函数是为了输出搜索结果写的，可注释
def getWord(word):
    deleteSignal = [',', '.', ';', '&', ':', '>', "'", '`', '(', ')', '+', '!', '*', '"', '?']
    for i in deleteSignal:
        word = word.replace(i, '').lower()
    tokens = nltk.word_tokenize(word)
    for word, pos in nltk.pos_tag(tokens):
        if pos.startswith('J'):
            wordnet_pos = nltk.corpus.wordnet.ADJ
        elif pos.startswith('V'):
            wordnet_pos = nltk.corpus.wordnet.VERB
        elif pos.startswith('N'):
            wordnet_pos = nltk.corpus.wordnet.NOUN
        elif pos.startswith('R'):
            wordnet_pos = nltk.corpus.wordnet.ADV
        else:
            wordnet_pos = nltk.corpus.wordnet.NOUN
        word = nltk.WordNetLemmatizer().lemmatize(word, wordnet_pos)
        return word
    return word


print("The first time to load this System?[Y]/[N]")
choose = input()
if choose == "Y":
    nltk.download("wordnet")
    nltk.download("averaged_perceptron_tagger")
    nltk.download("punkt")
    nltk.download("maxnet_treebank_pos_tagger")
print("getting index...")
INDEX = getIndex.get_index()
item_list = getIndex.get_item_list()
doc_num = getIndex.get_doc_count()
doc_list = getIndex.get_doc_id_list()
tdm = TermDocWeight.TermDocWeight(INDEX, item_list, doc_list, doc_num)
if choose == "Y":
    print("building vector space...")
    tdm.build_tdwm()
print("getting vector space")
tdm.load_tdwm()
# print(item_list)
# print(doc_num)
# print(doc_list)

DTWEIGHT = tdm.get_tdwm()
print(type(DTWEIGHT));
print("loading the wordnet...")

LOOP = True
print("=================Searching System=================")

while LOOP:
    print("input the search method(EXIT to quit):")
    method = input()
    if method == "BOOL":
        print("input the query statement(EXIT to quit):")
        STATEMENT = input()
        if STATEMENT == "EXIT":
            break

        print("Normalizing query statement...")
        INPUT_WORDS = languageAnalysis.normalize(STATEMENT, True)
        print(" ".join(INPUT_WORDS))
        POSTPHRASE = BoolSearchDel.infix_to_postfix(INPUT_WORDS)
        OLD_INPUT_WORDS = copy.deepcopy(POSTPHRASE)
        P = []
        for i in POSTPHRASE:
            P = str(POSTPHRASE[0][i]).split(' ')
        corrected = SpellCorrect.correct_word([P,], item_list)
        if corrected != None:
            if not operator.eq(OLD_INPUT_WORDS, corrected):
                print("Maybe you are searching for %s" % " ".join(list(map(" ".join, corrected))))
                DOC_LIST = BoolSearchDel.bool_search(POSTPHRASE, INDEX)
            else:
                DOC_LIST = BoolSearchDel.bool_search(POSTPHRASE, INDEX)
        else:
            print("Nothing found. Please check if you spell correctly.")
            DOC_LIST = []
    elif method == "SCORE":
        print("input the query statement(EXIT to quit):")
        STATEMENT = input()
        if STATEMENT == "EXIT":
            break
        print("input the K:")
        K = input()
        print("Normalizing query statement...")
        INPUT_WORDS = languageAnalysis.normalize(STATEMENT, True)
        print(" ".join(INPUT_WORDS))
        OLD_INPUT_WORDS = INPUT_WORDS.copy()
        corrected = SpellCorrect.correct_word([INPUT_WORDS, ], item_list)
        if corrected != None:
            if OLD_INPUT_WORDS != corrected[0]:
                print("Maybe you are searching for %s" % " ".join(INPUT_WORDS))
            DOC_LIST, score = sortDoc.score_search(INPUT_WORDS, tdm, INDEX, K)
            # 以下是为了输出搜索结果写的，可注释
            path = 'LanguageAnalysis/Reuters/'
            INPUT_WORDS = [v.lower() for v in INPUT_WORDS]
            for i in range(len(DOC_LIST)):
                print(
                    '\033[0;36m-----' + str(int(DOC_LIST[i])) + '.html: (score ' + str(score[i]) + ')' + '-----\033[0m')
                fname = path + str(int(DOC_LIST[i])) + '.html'
                f = open(fname, 'r')
                lineList = f.read().split('\n')
                f.close()
                for i in range(0, len(lineList)):
                    lineList[i] = lineList[i].rstrip('\n')
                    wordList = lineList[i].split(' ')
                    wordList = [w for w in wordList if w != '']
                    intersection = [v for v in wordList if getWord(v) in INPUT_WORDS]
                    if len(intersection) > 0:
                        start = 0
                        current = 0
                        end = 0
                        for j in range(len(wordList)):
                            if getWord(wordList[j]) in INPUT_WORDS:
                                current = j
                                if j > end:
                                    start = max(j - 5, 0)
                                    end = min(j + 5, len(wordList))
                                    print('>> ', end='')
                                    for k in range(start, end):
                                        if getWord(wordList[k]) in INPUT_WORDS:
                                            print('\033[0;31m', end='')
                                            print(html.unescape(wordList[k]), end=' ')
                                            print('\033[0m', end='')
                                        else:
                                            print(html.unescape(wordList[k]), end=' ')
                                    print('')
            # 以上是为了输出搜索结果写的，可注释
            DOC_LIST = [str(int(x)) + '.html' for x in DOC_LIST]
        else:
            print("Nothing found. Please check if you spell correctly.")
            DOC_LIST = []
    elif method == "EXIT":
        break
    else:
        DOC_LIST = []
    print(len(DOC_LIST), "DOCs :")
    print(DOC_LIST)

print("ByeBye!")
