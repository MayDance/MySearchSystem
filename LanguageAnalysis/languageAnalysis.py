import json
import os
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag


class LangAnalysis:
    def __init__(self):
        self.__doc_path = os.getcwd() + "\\LanguageAnalysis\\Reuters"
        self.__ir_path = os.getcwd() + "\\LanguageAnalysis\\Intermediate"

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
        return _doc_id_list

    def get_file_list(self):
        _get_doc_id = lambda _doc_file_name: int(_doc_file_name.split(".")[0])
        _doc_file_names = os.listdir(self.__doc_path)
        _doc_file_names.sort(key=_get_doc_id)
        return _doc_file_names

    def get_item_list(self, _doc_file_name):
        file = open(self.__doc_path + "\\" + _doc_file_name, 'r')
        content = file.read()
        words = normalize(content, False)
        file.close()
        return words


__deleteSignal = [',', '.', ';', '&', ':', '>', "'", '`', '(', ')', '+', '!', '*', '"', '?']
__deleteSignalForInput = [',', '.', ';', '&', ':', '>', "'", '`', '+', '!', '*', '"', '?']


def normalize(sentence, forinput):
    res = []
    lemmatizer = WordNetLemmatizer()
    for word, pos in pos_tag(word_tokenize(sentence)):
        wordnet_pos = __get_wordnet_pos(pos) or wordnet.NOUN
        res.append(lemmatizer.lemmatize(word, pos=wordnet_pos))

    result = __filter(res, forinput)

    return result


def __get_file_list():
    _get_doc_id = lambda _doc_file_name: int(_doc_file_name.split(".")[0])
    _doc_file_names = os.listdir(os.getcwd() + "\\Reuters")
    _doc_file_names.sort(key=_get_doc_id)
    return _doc_file_names



def __getWord(word):
    if word.istitle():
        word = word.lower()
        word = WordNetLemmatizer().lemmatize(word, pos='n')
    else:
        word = WordNetLemmatizer().lemmatize(word, pos='n')
    return word


def __filter(res, forinput):
    result = []
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


def __test_analysis(langAnalysis, _doc_file_name):
    lemmatizer = WordNetLemmatizer()
    _get_doc_id = lambda _doc_file_name: int(_doc_file_name.split(".")[0])

    file = open(os.getcwd() + "\\Reuters" + "\\" + _doc_file_name, 'r')
    content = file.read()
    tokens = word_tokenize(content)
    tokens_file = open(os.getcwd() + "\\Intermediate\\Tokenize\\" + str(_get_doc_id(_doc_file_name)) + ".t", 'w')
    tokens_file.write(json.dumps(tokens))

    tokens_stemming = []
    for word, pos in pos_tag(tokens):
        wordnet_pos = __get_wordnet_pos(pos) or wordnet.NOUN
        tokens_stemming.append(lemmatizer.lemmatize(word, pos=wordnet_pos))
    stemming_file = open(os.getcwd() + "\\Intermediate\\Stemming\\" + str(_get_doc_id(_doc_file_name)) + ".s", "w")
    stemming_file.write(json.dumps(tokens_stemming))

    filtered = __filter(tokens_stemming, False)
    filtered_file = open(os.getcwd() + "\\Intermediate\\Filter\\" + str(_get_doc_id(_doc_file_name)) + ".f", "w")
    filtered_file.write(json.dumps(filtered))


if __name__ == "__main__":
    langAnalysis = LangAnalysis()
    file_names = __get_file_list()
    if not os.path.exists(os.getcwd() + "\\Intermediate"):
        os.makedirs(os.getcwd() + "\\Intermediate")
    if not os.path.exists(os.getcwd() + "\\Intermediate\\Tokenize"):
        os.makedirs(os.getcwd() + "\\Intermediate\\Tokenize")
    if not os.path.exists(os.getcwd() + "\\Intermediate\\Stemming"):
        os.makedirs(os.getcwd() + "\\Intermediate\\Stemming")
    if not os.path.exists(os.getcwd() + "\\Intermediate\\Filter"):
        os.makedirs(os.getcwd() + "\\Intermediate\\Filter")
    for file_name in file_names:
        __test_analysis(langAnalysis, file_name)