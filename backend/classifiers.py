from rtree import index
from heapq import heappop, heappush, heapify

class KNNClassifierSeq:
        def __init__(self, train_set):
                self.train_set = train_set
        
        def classify(self, vec, k, max_dist):
                max_heap = []
                for i in range(k):
                        max_heap.append((-max_dist, "none"))
                for train_label, train_vec in self.train_set:
                        distance = -((sum([(x1 - x2)**2 for x1, x2 in zip(vec, train_vec)]))**(1/2))
                        if max_heap[0][0] < distance:
                                heappop(max_heap)
                                heappush(max_heap,(distance, train_label))
                nearest = [(distance, label) for distance, label in max_heap if label != "none"]
                if len(nearest) > 0:
                        fr_dict = {}
                        for distance, label in nearest:
                                if label in fr_dict:
                                        fr_dict[label][0] += 1
                                        if fr_dict[label][1] < distance:
                                                fr_dict[label][1] = distance
                                else:
                                        fr_dict[label] = [1, distance]
                        fr_list = sorted(fr_dict.items(), key = lambda x : x[1])
                        return fr_list[-1][0], fr_list[-1][1][0]
                else:
                        return "No se parece a nadie", 0

class KNNClassifierRTree:
        def __init__(self, train_set):
                self.train_set = train_set
                self.idx = index.Index(properties = index.Property(dimension = len(train_set[0][1])))
                for i in range(len(train_set) - 1):
                        self.idx.insert(i, train_set[i][1]*2)
        
        def classify(self, vec, k):
                nearest = list(self.idx.nearest(vec.tolist()*2, k))
                if len(nearest) > 0:
                        fr_dict = {}
                        for n in nearest:
                                label = self.train_set[n][0]
                                if label in fr_dict:
                                        fr_dict[label] += 1
                                else:
                                        fr_dict[label] = 1
                        return sorted(fr_dict.items(), key = lambda x : x[1])[-1]
                else:
                        return "No se parece a nadie", 0

class HyperCubeClassifierRTree:
        def __init__(self, train_set):
                self.train_set = train_set
                self.idx = index.Index(properties = index.Property(dimension = len(train_set[0][1])))
                for i in range(len(train_set) - 1):
                        self.idx.insert(i, train_set[i][1]*2)
        
        def classify(self, vec, r):
                lis = vec.tolist()
                nearest = list(self.idx.intersection([x-r for x in lis] + [x+r for x in lis]))
                if len(nearest) > 0:
                        fr_dict = {}
                        for n in nearest:
                                label = self.train_set[n][0]
                                if label in fr_dict:
                                        fr_dict[label] += 1
                                else:
                                        fr_dict[label] = 1
                        return sorted(fr_dict.items(), key = lambda x : x[1])[-1]
                else:
                        return "No se parece a nadie", 0