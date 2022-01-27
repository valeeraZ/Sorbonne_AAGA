class BinaryHeap:
    def __init__(self):
        self.heap = [0]

    def shift_up(self, i):
        while i // 2 > 0:
            if self.heap[i] < self.heap[i // 2]:
                tmp = self.heap[i // 2]
                self.heap[i // 2] = self.heap[i]
                self.heap[i] = tmp
            i = i // 2

    def insert(self, k):
        """
        insert k into the mean_heap
        """
        self.heap.append(k)
        self.shift_up(len(self.heap) - 1)

    def shift_down(self, i):
        while (i * 2) <= len(self.heap) - 1:
            mc = self.min_child(i)
            if self.heap[i] > self.heap[mc]:
                tmp = self.heap[i]
                self.heap[i] = self.heap[mc]
                self.heap[mc] = tmp
            i = mc

    def min_child(self, i):
        if i * 2 + 1 > len(self.heap) - 1:
            return i * 2
        else:
            if self.heap[i * 2] < self.heap[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1

    def del_min(self):
        """
        delete the minimum element of the heap &
        returns the resulted heap
        """
        self.heap[1] = self.heap[-1]
        self.heap.pop()
        self.shift_down(1)
        return self.heap[1:]

    def build_heap(self, vals):
        i = len(vals) // 2
        self.heap = [0] + vals[:]
        while i > 0:
            self.shift_down(i)
            i = i - 1

    def return_heap(self):
        return self.heap[1:]


if __name__ == "__main__":
    """Tests"""
    bh = BinaryHeap()
    bh.build_heap([9, 6, 5, 2, 3])
    print(bh.return_heap())

    print(bh.del_min())
    print(bh.del_min())
    print(bh.del_min())
    print(bh.del_min())
    print(bh.del_min())
