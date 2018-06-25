import json
import tools
from . import invertedIndex

# get_index()
_idx = None


def __get_index_object():
    idx = invertedIndex.InvertedIndex(doc_path="\\InvertedIndex\\Reuters", get_item_list=invertedIndex._test_get_item_list)
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