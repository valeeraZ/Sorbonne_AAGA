class BinaryHeap:
    def __init__(self):
        self.heap = [0]

    def shiftUp(self, i):
        while i // 2 > 0:
            if self.heap[i] < self.heap[i // 2]:
                tmp = self.heap[i // 2]
                self.heap[i // 2] = self.heap[i]
                self.heap[i] = tmp
            i = i // 2

    def insert(self, k):
        self.heap.append(k)
        self.shiftUp(len(self.heap) - 1)

    def shiftDown(self, i):
        while (i * 2) <= len(self.heap) - 1:
            mc = self.minChild(i)
            if self.heap[i] > self.heap[mc]:
                tmp = self.heap[i]
                self.heap[i] = self.heap[mc]
                self.heap[mc] = tmp
            i = mc

    def minChild(self, i):
        if i * 2 + 1 > len(self.heap) - 1:
            return i * 2
        else:
            if self.heap[i * 2] < self.heap[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1

    def delMin(self):
        root = self.heap[1]
        self.heap[1] = self.heap[-1]
        self.heap.pop()
        self.shiftDown(1)
        return self.heap[1:]

    def buildHeap(self, vals):
        i = len(vals) // 2
        self.heap = [0] + vals[:]
        while i > 0:
            self.shiftDown(i)
            i = i - 1

    def returnHeap(self):
        return self.heap[1:]


if __name__ == "__main__":
    bh = BinaryHeap()
    bh.buildHeap([9, 6, 5, 2, 3])
    print(bh.returnHeap())

    print(bh.delMin())
    print(bh.delMin())
    print(bh.delMin())
    print(bh.delMin())
    print(bh.delMin())
