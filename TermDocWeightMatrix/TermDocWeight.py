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
        self.tdwmdic = {}
        col = []
        for i in range(0, self.doc_count):
            col = []
            data = []
            for j in range(0, len(self.item_list)):
                if self.tdwm[i][j] != 0:
                    col.append(j)
                    data.append(self.tdwm[i][j])
            self.tdwmdic[self.docid_list[i]] = [col, data]
        f = open('tdwm.txt','w')  
        f.write(str(self.tdwmdic))  
        f.close()  
    
    def load_tdwm(self) :
        f = open('tdwm.txt','r')  
        a = f.read()  
        self.tdwmdic = eval(a)  
        f.close() 
        
    def get_tdwm(self) :
        return self.tdwmdic
    
    def get_vd(self, search_docid_list):
        doc_vector = {}
        for i in search_docid_list:         
            doc_vector[i] = self.tdwmdic[i]
        return doc_vector
