# -*- coding: utf-8 -*-
from InvertedIndex import getIndex
from scoreQuery import getScore
import numpy as np
import math

def get_matrix(index) :
    item_list = getIndex.get_item_list()
    doc_count = getIndex.get_doc_count()
    tdwm = np.zeros((doc_count, len(item_list)))
    for i in range(0, len(item_list)):
        index_item = index[item_list[i]]
        idf = math.log10(doc_count/index_item['df'])
        print(index_item['doc_list'])
        for key in index_item['doc_list']:
            tdwm[key][i]=index_item['doc_list'][key]['tf']*idf
    
    return tdwm