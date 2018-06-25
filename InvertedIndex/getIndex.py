import json
import tools
from . import invertedIndex

# get_index()
def get_index():
    idx = invertedIndex.InvertedIndex(_doc_path="\\InvertedIndex\\Reuters", _get_item_list=invertedIndex._test_get_item_list)
    index = idx.get_index()
    return index

def get_item_list():
    idx = invertedIndex.InvertedIndex(_doc_path="\\InvertedIndex\\Reuters", _get_item_list=invertedIndex._test_get_item_list)
    item_list = idx.get_item_list()
    return item_list

def get_doc_count():
    idx = invertedIndex.InvertedIndex(_doc_path="\\InvertedIndex\\Reuters", _get_item_list=invertedIndex._test_get_item_list)
    doc_count = idx.get_doc_count()
    return doc_count