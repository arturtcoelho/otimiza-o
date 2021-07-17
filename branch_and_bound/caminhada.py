#!/usr/bin/env python3

from functools import wraps
from time import time
from sys import stderr
import math

# number of tests realized
TESTS = 100

# function used to time the tests
def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('test took: %2.10f sec' % (te-ts), file=stderr)
        return result
    return wrap

# read graph and add to a 'matrix'
n = int(input())
graph = [[None for _ in range(n)] for i in range(n)]
for i in range(n-1):
    node = input().split(' ')
    for j in range(i, n-1):
        if (int(node[j-i]) != 0):
            graph[i][j+1] = int(node[j-i])
            graph[j+1][i] = int(node[j-i])

# # print n nodes m vertices
# print(n)
# print(sum([sum([1 for g in gr if g]) for gr in graph])/2)

class Path_finder():

    def __init__(self, graph) -> None:
        self.graph = graph
        self.n = len(graph)

        # run tests with each bounding function
        self.test_get_path0()
        self.test_get_path1()
        self.test_get_path2()
        self.test_get_path3()
        print(file=stderr)
        print(f"number of tests realized: {TESTS}", file=stderr)

    @timing
    def test_get_path0(self):

        # test unbounded
        self.bounding_function = self.unbounded
        for _ in range(TESTS):
            self.paths = []
            self.paths2 = []
            self.nodes_visited = 0
            self.get_path(0, graph[0], [0], [0], 0)
            self.get_best_path()

        print(self.best_path_len)
        print(self.best_path)
        print(file=stderr)
        print("Nodes visited (unbounded):", self.nodes_visited, file=stderr)

    @timing
    def test_get_path1(self):

        # test bounded one
        self.bounding_function = self.bounding_1
        for _ in range(TESTS):
            self.paths = []
            self.paths2 = []
            self.nodes_visited = 0
            self.get_path(0, graph[0], [0], [0], 0)
            self.get_best_path()
            
        print(file=stderr)
        # print(self.best_path_len)
        # print(self.best_path)
        print("Nodes visited (bounding 1):", self.nodes_visited, file=stderr)
    
    @timing
    def test_get_path2(self):

        # test bounded two
        self.bounding_function = self.bounding_2
        for _ in range(TESTS):
            self.paths = []
            self.paths2 = []
            self.nodes_visited = 0
            self.get_path(0, graph[0], [0], [0], 0)
            self.get_best_path()

        print(file=stderr)
        # print(self.best_path_len)
        # print(self.best_path)
        print("Nodes visited (bounding 2):", self.nodes_visited, file=stderr)

    @timing
    def test_get_path3(self):

        # test bounded three
        self.bounding_function = self.bounding_1_modified
        for _ in range(TESTS):
            self.paths = []
            self.paths2 = []
            self.nodes_visited = 0
            self.get_path(0, graph[0], [0], [0], 0)
            self.get_best_path()

        print(file=stderr)
        # print(self.best_path_len)
        # print(self.best_path)
        print("Nodes visited (bounding 1 modified):", self.nodes_visited, file=stderr)

    def get_path(self, n, node, path, path2, last):
        
        self.nodes_visited += 1

        # if found exit, adds to path list and returns
        if (node[0] and last != 0):
            self.paths.append(path + [0])
            self.paths2.append(path2 + [node[0]])
            return
        
        for i in range(len(node)):
            if node[i] and i not in path: # if is not visited
                if self.bounding_function((path, self.graph[i], i, n)):
                    # if its not cut by the bounding function
                    self.get_path(i, self.graph[i], path + [i], path2 + [node[i]], n)

    def unbounded(self, arg):
        # always accepts the branch
        return True

    def bounding_1(self, arg):
        path, node, index, last = arg

        # searchs for a possible path back to origin
        if (node[0] and last != 0):
            return True

        for i in range(len(node)):
            if node[i] and i not in path: 
                return self.bounding_1((path.copy() + [index], self.graph[i], i, index))
        
        # returns false if it cannot find a possible way back

        return False

    def bounding_2(self, arg):
        path, node, index, last = arg
        path = path[1:]

        neighbors = [i for i, n in enumerate(node) if node[i]]
        
        # accepts it if it has neighbors with more ways
        for n in neighbors:
            if n not in path: return True

        # cuts lonely branchs with no way back
        return False

    def bounding_1_modified(self, arg):
        path, node, index, last = arg

        if (len(path) < self.n/2): return True

        # searchs for a possible path back to origin
        if (node[0] and last != 0):
            return True

        for i in range(len(node)):
            if node[i] and i not in path: 
                return self.bounding_1((path.copy() + [index], self.graph[i], i, index))
        
        # returns false if it cannot find a possible way back

        return False

    def get_best_path(self):
        self.max_path = max(self.paths2, key=lambda k: sum(k))

        for i in range(len(self.paths)):
            if self.max_path == self.paths2[i]:
                self.best_path_len = sum(self.max_path)
                self.best_path = " ".join(map(lambda k: str(k+1), self.paths[i]))
                return

Path_finder(graph)
