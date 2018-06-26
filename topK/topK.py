import numpy as np


class TopK:
    def __init__(self, k, score, docID):
        self.k = k
        self.score = score
        self.docID = docID
        self.heap = np.array([])
        self.len = 0
        self.build_heap()

    def build_heap(self):
        self.heap = np.array([self.score, self.docID])
        self.heap = np.transpose(self.heap)
        self.heap = np.row_stack((np.array([0, 0]), self.heap))
        self.len = len(self.heap)
        i = (self.len - 1) // 2
        while i > 0:
            self.heapify(i)
            i = i - 1

    def heapify(self, i):
        max = 0
        while max != i:
            l = i << 1
            r = i + 1
            max = i
            if l < self.len and self.heap[l][0] > self.heap[max][0]:
                max = l
            if r < self.len and self.heap[r][0] > self.heap[max][0]:
                max = r
            if max != i:
                self.swap(max, i)
                i = max
                max = 0

    def swap(self, a, b):
        t = self.heap[a][0]
        self.heap[a][0] = self.heap[b][0]
        self.heap[b][0] = t
        t = self.heap[a][1]
        self.heap[a][1] = self.heap[b][1]
        self.heap[b][1] = t

    def get_topk(self):
        doc = []
        for i in range(min(self.k, self.len - 1)):
            doc.append(self.heap[1][1])
            self.swap(1, self.len - 1)
            np.delete(self.heap, self.len - 1, 0)
            self.len = self.len - 1
            self.heapify(1)
        return doc


if __name__ == '__main__':
    score = [10, 3, 8, 7]
    docID = [1, 2, 3, 4]
    t = TopK(6, score, docID)
    # print(t.heap)
    doc = t.get_topk()
    print(doc)
