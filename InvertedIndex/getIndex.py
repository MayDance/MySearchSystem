import json
import tools
from . import invertedIndex

# get_index()
def get_index():
    idx = invertedIndex.InvertedIndex()
    index = idx.get_index()
    return index

def get_item_list():
    idx = invertedIndex.InvertedIndex()
    item_list = idx.get_item_list()
    return item_list

def get_doc_count():
    idx = invertedIndex.InvertedIndex()
    doc_count = idx.get_doc_count()
    return doc_count