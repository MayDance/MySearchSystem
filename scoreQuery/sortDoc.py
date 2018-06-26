from InvertedIndex import getIndex
from TermDocWeightMatrix import TermDocWeight
from topK import topK
import numpy as np
import math

def score_search(words, tdm, index, K):
    tmplist = []
    for term in words:
        for key in index[term]['doc_list']:
            tmplist.append(key)
    tmplist=sorted(tmplist)
    doclist=[]
    for i in range(0, len(tmplist)):
        if tmplist[i] not in doclist:
            doclist.append(tmplist[i])
    #print(doclist)
    vd = tdm.get_vd(doclist)
    q = get_query_vector(words)
    kq = math.sqrt(len(words))
    vd = np.array(vd)
    q = np.array(q)
    #print(vd.shape)
    #print(q.shape)
    vd1 = np.square(vd) #全部平方
    vd2 = np.sum(vd1, axis=1) #平方和
    vd3 = np.sqrt(vd2) #开根号 根号Vd的平方和
    vdq = np.dot(vd, q) #点乘
    score = vdq/vd3/kq #得到score
    #print(score)
    #print(score.shape)
    #doclist1=np.array(doclist)
    #print(doclist1.shape)
    score1=score.tolist()
    t = topK.TopK(int(K), score1, doclist)
    # print(t.heap)
    doc = t.get_topk()
    #print(doc)
    return doc
 
def get_query_vector(words):
    item_list = getIndex.get_item_list()
    v = np.zeros(len(item_list))
    for term in words:
        v[item_list.index(term)]=1;
    return v 

