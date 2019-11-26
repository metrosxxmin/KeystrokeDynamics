

class KeyGraph:
    def __init__(self):
        self.di = [1, 0, -1, 1, 0, -1, 1, 0, -1]
        self.dj = [1, 1, 1, 0, 0, 0, -1, -1, -1]
        self.graph = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
                      ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']'],
                      ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", ],
                      ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', ]]

    def isChain(self, _bias, _next):
        for i in range(len(self.graph)):
            if _bias in self.graph[i]:
                j = self.graph[i].index(_bias)

                for k in range(len(self.di)):
                    ni = i + self.di[k]
                    nj = j + self.dj[k]

                    if self.isRange(ni, nj) and self.graph[ni][nj] == _next:
                        return True
        return False

    def _isRange(self, i, j):
         if i < 0 or i >= len(self.graph):
             return False
         if j < 0 or j >= len(self.graph[i]):
             return False
         return True

    def getGraph(self):
        return self.graph


# for module testing.
if __name__ == "__main__":
    kg = KeyGraph()
    print(kg.isChain('a', 'b'))
    print(kg.isChain('a', 's'))
