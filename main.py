import os
import tools
import nltk
from InvertedIndex import getIndex
from LanguageAnalysis import stemming
from Serching import searchWord
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
stemming.lemmatize_sentence("a", False)

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

        print("stemming...")
        INPUT_WORDS = stemming.lemmatize_sentence(STATEMENT, True)
        print(INPUT_WORDS)

        DOC_LIST = BoolSearchDel.bool_search(INPUT_WORDS, INDEX)
    elif method == "SCORE":
        print("input the query statement(EXIT to quit):")
        STATEMENT = input()
        if STATEMENT == "EXIT":
            break
        print("input the K:")
        K = input()
        print("stemming...")
        INPUT_WORDS = stemming.lemmatize_sentence(STATEMENT, True)
        print(INPUT_WORDS)
        DOC_LIST = sortDoc.score_search(INPUT_WORDS, tdm, INDEX, K)  
    elif method == "EXIT":
        break
    else:
        DOC_LIST = [];
    print(len(DOC_LIST), "DOCs :")
    print(DOC_LIST)

print("ByeBye!")
