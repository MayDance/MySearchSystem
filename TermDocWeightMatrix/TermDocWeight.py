# -*- coding: utf-8 -*-
import numpy as np
import math


class TermDocWeight:
    def __init__(self, index, item_list, docid_list, doc_count) :
        self.index = index
        self.item_list = item_list
        self.docid_list = docid_list
        self.doc_count = doc_count
        self.num_to_docid = np.zeros((doc_count, 2))
        #self.tdwm = np.zeros((doc_count, len(item_list)))
        #self.build_tdwm()
            
    def build_tdwm(self) :
        self.tdwm = np.zeros((self.doc_count, len(self.item_list)))
        for i in range(0, len(self.item_list)):
            index_item = self.index[self.item_list[i]]
            idf = math.log10(self.doc_count/index_item['df'])
            item_doc = index_item['doc_list']
            #print(item_doc)
            for key in item_doc:
                #print(key)
                num = (self.docid_list).index(key)
                self.tdwm[num][i]=item_doc[key]['tf']*idf
        np.save("tdwm.npy", self.tdwm)
    
    def load_tdwm(self) :
        self.tdwm = np.load("tdwm.npy")

    def get_tdwm(self) :
        return self.tdwm
    
    def get_vd(self, search_docid_list):
        doc_vector = []
        for i in search_docid_list:         
            doc_vector.append(self.tdwm[self.docid_list.index(i)])
        return doc_vector
