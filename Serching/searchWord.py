import queue
import os
import tools
from Serching import operateDocList


def search_single_word(index, word):
    if word not in index:
        return []
    else:
        # 将所有文档id变为数字
        docList = [int(key) for key in index[word]['doc_list'].keys()]
        # 将文档的id排序
        docList.sort()
        return docList


# 短语查询支持
def search_bool_phrase(index, word_list, flag):
    if len(word_list) == 0:
        return []
    doc_queue = queue.Queue()
    for word in word_list:
        doc_queue.put(search_single_word(index, word))

    while doc_queue.qsize() > 1:
        list1 = doc_queue.get()
        list2 = doc_queue.get()
        doc_queue.put(operateDocList.and_list(list1, list2))
    doc_list = doc_queue.get()

    if len(word_list) == 1:
        if flag:
            return doc_list
        else:
            return operateDocList.minus_list(tools.wholeDocList, doc_list)

    res_list = []

    for doc_id in doc_list:
        # doc_id = str(doc_id)
        # print(index[word_list[0]]["doc_list"])
        for loc in index[word_list[0]]["doc_list"][doc_id]["positions"]:
            file_loc = loc
            has_find = True
            for word in word_list[1:len(word_list)]:
                file_loc += 1
                try:
                    index[word]["doc_list"][doc_id]["positions"].index(file_loc)
                except:
                    has_find = False
                    break
            if has_find:
                res_list.append(int(doc_id))
                break
    if flag:
        return res_list
    else:
        return operateDocList.minus_list(tools.wholeDocList, res_list)
