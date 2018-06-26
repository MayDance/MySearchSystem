import json
import tools
from . import invertedIndex

# get_index()
_idx = None


def __get_index_object():
    idx = invertedIndex.InvertedIndex()
    return idx


def get_index():
    global _idx
    if _idx is None:
        _idx = __get_index_object()

    return _idx.get_index()


def get_item_list():
    global _idx
    if _idx is None:
        _idx = __get_index_object()
    return _idx.get_item_list()


def get_doc_count():
    global _idx
    if _idx is None:
        _idx = __get_index_object()
    return _idx.get_doc_count()


def get_doc_id_list():
    global _idx
    if _idx is None:
        _idx = __get_index_object()
    return _idx.get_doc_id_list()


def get_item_frequency(word_item):
    global _idx
    if _idx is None:
        _idx = __get_index_object()
    items_frequency = _idx.get_items_frequency()
    if word_item in items_frequency:
        return items_frequency[word_item]
    else:
        return 0

