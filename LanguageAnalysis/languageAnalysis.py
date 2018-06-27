import json
import os
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag


class LangAnalysis:
    def __init__(self):
        self.__doc_path = os.getcwd() + "/LanguageAnalysis/Reuters"
        self.__ir_path = os.getcwd() + "/LanguageAnalysis/Intermediate"

    def get_doc_count(self):
        _doc_file_names = os.listdir(self.__doc_path)
        _doc_count = len(_doc_file_names)
        return _doc_count

    def get_doc_id_list(self):
        _doc_id_list = list()
        _get_doc_id = lambda _doc_file_name: int(_doc_file_name.split(".")[0])
        _doc_file_names = os.listdir(self.__doc_path)
        for _doc_file_name in _doc_file_names:
            _doc_id_list.append(_get_doc_id(_doc_file_name))
        _doc_id_list.sort()
        #print(_doc_id_list)
        return _doc_id_list

    def get_file_list(self):
        _get_doc_id = lambda _doc_file_name: int(_doc_file_name.split(".")[0])
        _doc_file_names = os.listdir(self.__doc_path)
        _doc_file_names.sort(key=_get_doc_id)
        return _doc_file_names

    def test_analysis(self, _doc_file_name):
        lemmatizer = WordNetLemmatizer()

        if not os.path.exists(self.__ir_path):
            os.makedirs(self.__ir_path)
        file = open(self.__doc_path + "/" + _doc_file_name, 'r')
        content = file.read()
        tokens = word_tokenize(content)
        tokens_file = open(self.__ir_path + "/" + "tokens.txt", 'w')
        tokens_file.write(json.dumps(tokens))

        tokens_stemming = []
        for word, pos in pos_tag(tokens):
            wordnet_pos = __get_wordnet_pos(pos) or wordnet.NOUN
            tokens_stemming.append(lemmatizer.lemmatize(word, pos=wordnet_pos))
        stemming_file = open(self.__ir_path + "/" + "stemming.txt", "w")
        stemming_file.write(json.dumps(tokens_stemming))

    def get_item_list(self, _doc_file_name):
        file = open(self.__doc_path + "/" + _doc_file_name, 'r')
        content = file.read()
        words = normalize(content, False)
        file.close()
        return words


__deleteSignal = [',', '.', ';', '&', ':', '>', "'", '`', '(', ')', '+', '!', '*', '"', '?']
__deleteSignalForInput = [',', '.', ';', '&', ':', '>', "'", '`', '+', '!', '*', '"', '?']


def normalize(sentence, forinput):
    res = []
    result = []
    lemmatizer = WordNetLemmatizer()
    for word, pos in pos_tag(word_tokenize(sentence)):
        wordnet_pos = __get_wordnet_pos(pos) or wordnet.NOUN
        res.append(lemmatizer.lemmatize(word, pos=wordnet_pos))

    for word in res:
        # 如果是 's什么的，直接排除
        if word[0] is '\'':
            continue

        # 去除标点符号
        if not forinput:
            for c in __deleteSignal:
                word = word.replace(c, '')
        else:
            for c in __deleteSignalForInput:
                word = word.replace(c, '')

        # 排除空的字符串
        if len(word) is 0 or word[0] is '-':
            continue

        # 如果分解的单词中有/,则将其中的每个单词添加到结果中
        if word.find('/') > 0:
            rs = word.split('/')
            for w in rs:
                w = __getWord(w)
                result.append(w)
        else:
            word = __getWord(word)
            result.append(word)

    return result


def __getWord(word):
    if word.istitle():
        word = word.lower()
        word = WordNetLemmatizer().lemmatize(word, pos='n')
    else:
        word = WordNetLemmatizer().lemmatize(word, pos='n')
    return word


def __get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


if __name__ == "__main__":
    langAnalysis = LangAnalysis()
    file_names = langAnalysis.get_file_list()
    file_name = file_names[0]
    langAnalysis.test_analysis(file_name)