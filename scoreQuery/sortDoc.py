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
    #vd = np.array(vd)
    #print(vd)
    q = np.array(q)
    #print(vd.shape)
    #print(q.shape)
    score=[]
    for i in doclist:
        tmp = vd[i]
        #print(tmp)
        tmpcol = tmp[0]
        tmpv = tmp[1]
        tmpv = np.array(tmpv)
        tmpv1 = np.square(tmpv)
        tmpdoc = math.sqrt(np.sum(tmpv1))
        dotres = 0
        for j in range(0, len(tmpcol)):
            dotres += q[tmpcol[j]]*tmpv[j]
        score.append(dotres/tmpdoc/kq)
    #print(score)
    #print(score.shape)
    #doclist1=np.array(doclist)
    #print(doclist1.shape)
    t = topK.TopK(int(K), score, doclist)
    # print(t.heap)
    doc, score = t.get_topk()
    #print(doc)
    return doc, score
 
def get_query_vector(words):
    item_list = getIndex.get_item_list()
    v = np.zeros(len(item_list))
    for term in words:
        v[item_list.index(term)]=1
    return v 

