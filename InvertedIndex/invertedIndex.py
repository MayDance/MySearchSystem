import os
import logging
import tqdm
import pickle

from . import vbCode
from LanguageAnalysis import languageAnalysis


class InvertedIndex:
    def __init__(self, _store_path="\\index_files"):
        self.__inverted_index = dict()
        self.__store_path = os.getcwd() + _store_path
        self.__store_file_name = 'index.index'
        self.__analyzer = languageAnalysis.LangAnalysis()
        self.__doc_count = self.__analyzer.get_doc_count()
        self.__doc_id_list = self.__analyzer.get_doc_id_list()
        if os.path.exists(self.__store_path):
            index_file_names = os.listdir(self.__store_path)
            if self.__store_file_name not in index_file_names:
                self.__create_index()
            else:
                self.__load_index()
        else:
            os.makedirs(self.__store_path)
            self.__create_index()

    def __load_index(self):
        # file = open(self.__store_path + "\\" + self.__store_file_name, 'r')
        # content = file.read()
        # self.__inverted_index = json.JSONDecoder().decode(content)
        # file.close()
        # self.__another_store_index()
        print("start to load index", flush=True)
        _file = open(self.__store_path + "\\" + self.__store_file_name, 'rb')
        _temp_data = pickle.load(_file)
        _temp_inverted_index = _temp_data["index_data"]
        self.__doc_count = _temp_data["doc_count"]
        self.__doc_id_list = _temp_data["doc_id_list"]
        #print(self.__doc_id_list)
        _progress_bar = tqdm.tqdm(total=len(_temp_inverted_index))
        self.__inverted_index = dict()
        for _temp_index_item in _temp_inverted_index:
            _word_item = _temp_index_item[0]
            self.__inverted_index[_word_item] = dict()
            _temp_doc_id_list = vbCode.vb_decode(_temp_index_item[1])
            _doc_id_list = list()
            for _i, _dis in enumerate(_temp_doc_id_list):
                if _i == 0:
                    _doc_id_list.append(_dis)
                else:
                    _doc_id_list.append(_dis + _doc_id_list[_i - 1])
            self.__inverted_index[_word_item]["df"] = len(_doc_id_list)
            for _i, _doc_id in enumerate(_doc_id_list):
                if _i == 0:
                    self.__inverted_index[_word_item]["doc_list"] = dict()
                _temp_position_list = vbCode.vb_decode(_temp_index_item[_i + 2])
                _positions = list()
                for _j, _dis in enumerate(_temp_position_list):
                    if _j == 0:
                        _positions.append(_dis)
                    else:
                        _positions.append(_dis + _positions[_j - 1])
                self.__inverted_index[_word_item]["doc_list"][_doc_id] = dict()
                self.__inverted_index[_word_item]["doc_list"][_doc_id]["tf"] = len(_positions)
                self.__inverted_index[_word_item]["doc_list"][_doc_id]["positions"] = _positions
            _progress_bar.update(1)
        _progress_bar.close()
        print("")
        print("loading finished")

    def __store_index(self):
        _temp_inverted_index = list()
        _inverted_index = self.__inverted_index
        _temp_item_list = list(_inverted_index.keys())
        _temp_item_list.sort()
        print("start to store index", flush=True)
        _progress_bar = tqdm.tqdm(total=len(_temp_item_list))
        for _word_item in _temp_item_list:
            _temp_index_item = _inverted_index[_word_item]
            _temp_inverted_index_item = list()
            _temp_inverted_index_item.append(_word_item)
            _temp_doc_id_list = list(_temp_index_item["doc_list"].keys())
            _temp_doc_id_list.sort(key=lambda _param_doc_id: int(_param_doc_id))
            _temp_doc_id_int_list = list()
            for _i, _doc_id in enumerate(_temp_doc_id_list):
                _doc_id_dis = int(_doc_id)
                if _i != 0:
                    _doc_id_dis = int(_doc_id) - int(_temp_doc_id_list[_i-1])
                _temp_doc_id_int_list.append(_doc_id_dis)
            # _temp_inverted_index_item.append(_temp_doc_id_list)
            _temp_inverted_index_item.append(bytes(vbCode.vb_encode(_temp_doc_id_int_list)))
            for _doc_id in _temp_doc_id_list:
                _ori_position_list = _temp_index_item["doc_list"][_doc_id]["positions"]
                _temp_position_list = list()
                for _i, _position in enumerate(_ori_position_list):
                    if _i != 0:
                        _temp_position_list.append(_position - _ori_position_list[_i - 1])
                    else:
                        _temp_position_list.append(_position)
                # _temp_inverted_index_item.append(_ori_position_list)
                _temp_inverted_index_item.append(bytes(vbCode.vb_encode(_temp_position_list)))
            _temp_inverted_index.append(_temp_inverted_index_item)
            _progress_bar.update(1)
        _progress_bar.close()
        print("")
        print("Storing finished")
        _file = open(self.__store_path + "\\" + self.__store_file_name, 'wb')
        pickle.dump({"doc_id_list": self.__doc_id_list, "doc_count": self.__doc_count, "index_data": _temp_inverted_index}, _file)
        _file.close()

    def get_index(self):
        return self.__inverted_index.copy()  # shallow copy

    def get_item_list(self):
        return list(self.__inverted_index.keys())

    def get_doc_count(self):
        return self.__doc_count

    def get_doc_id_list(self):
        return self.__doc_id_list

    def __create_index(self):
        logging.basicConfig(
            level=logging.DEBUG,
            filename=self.__store_path + '\\index_creating.log',
            filemode="w",
            format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        )
        logging.debug("start to create index")
        print("start to create index", flush=True)
        _inverted_index = self.__inverted_index
        _doc_file_names = self.__analyzer.get_file_list()
        _doc_count = self.__doc_count
        _get_doc_id = lambda _doc_file_name: int(_doc_file_name.split(".")[0])
        _progress_bar = tqdm.tqdm(total=_doc_count)
        for _doc_file_name in _doc_file_names:
            logging.debug("start process " + _doc_file_name)
            _doc_id = _get_doc_id(_doc_file_name)
            _item_list = self.__analyzer.get_item_list(_doc_file_name)
            # logging.debug("items: " + ','.join(_item_list))
            _item_list_without_repetition = list()
            for _position, _word_item in enumerate(_item_list):
                if _word_item not in _inverted_index:
                    _inverted_index[_word_item] = {"df": 0, "doc_list":{}}
                if _word_item not in _item_list_without_repetition:
                    _inverted_index[_word_item]["df"] += 1
                    _item_list_without_repetition.append(_word_item)
                if _doc_id not in _inverted_index[_word_item]["doc_list"]:
                    _inverted_index[_word_item]["doc_list"][_doc_id] = {"tf": 0, "positions": []}
                _inverted_index[_word_item]["doc_list"][_doc_id]["tf"] += 1
                _inverted_index[_word_item]["doc_list"][_doc_id]["positions"].append(_position)
            logging.debug("end process " + _doc_file_name)
            _progress_bar.update(1)
        _progress_bar.close()

        print("")
        logging.debug("creating finished")
        print("creating finished")
        self.__store_index()



if __name__ == "__main__":
    # nltk.download("wordnet")
    # nltk.download("averaged_perceptron_tagger")
    # nltk.download("punkt")
    # nltk.download("maxnet_treebank_pos_tagger")

    invertedIndex = InvertedIndex()
    index = invertedIndex.get_index()
    item_list = invertedIndex.get_item_list()
    doc_count = invertedIndex.get_doc_num()
    test_index_item = index["nice"]
    print(test_index_item)
