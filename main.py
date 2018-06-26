import os
import tools
import nltk
from SpellCorrect import SpellCorrect
from InvertedIndex import getIndex
from LanguageAnalysis import languageAnalysis
from Searching import searchWord
from BoolSearch import BoolSearchDel
from scoreQuery import sortDoc
from TermDocWeightMatrix import TermDocWeight

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
#print(item_list)
#print(doc_num)
#print(doc_list)

DTWEIGHT = tdm.get_tdwm()
print(DTWEIGHT);
print(DTWEIGHT.sum(axis=1))
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
        print(INPUT_WORDS)

        DOC_LIST = BoolSearchDel.bool_search(INPUT_WORDS, INDEX)
    elif method == "SCORE":
        print("input the query statement(EXIT to quit):")
        STATEMENT = input()
        if STATEMENT == "EXIT":
            break
        print("input the K:")
        K = input()
        print("Normalizing query statement...")
        INPUT_WORDS = languageAnalysis.normalize(STATEMENT, True)
        print(INPUT_WORDS)
        valid_input = True
        for word in INPUT_WORDS:
            if word in item_list:
                continue
            else:
                corrected = SpellCorrect.correct_word(word, item_list)
                if corrected != None:
                    INPUT_WORDS[INPUT_WORDS.index(word)] = corrected
                else:
                    print("Nothing found. Please check if you spell correctly.")
                    valid_input = False
                    break
        if valid_input:
            DOC_LIST = sortDoc.score_search(INPUT_WORDS, tdm, INDEX, K)
        else:
            DOC_LIST = []
    elif method == "EXIT":
        break
    else:
        DOC_LIST = [];
    print(len(DOC_LIST), "DOCs :")
    print(DOC_LIST)

print("ByeBye!")
