import random


class Node:

    def __init__(self, num):
        self.left_child = -1
        self.right_child = -1
        self.parent = -1
        self.num = num

    def __str__(self):
        return "num : " + str(self.num) + " parent: " + str(self.parent) + " left_child : " + str(self.left_child) + " right_child : " + str(self.right_child)

    def __repr__(self):
        return "num : " + str(self.num) + " parent: " + str(self.parent) + " left_child : " + str(self.left_child) + " right_child : " + str(self.right_child)

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.num == other.num and self.parent == other.parent and self.left_child == other.left_child and self.right_child == other.right_child

    def is_leaf(self):
        return self.left_child == -1 and self.right_child == -1

class RemyTree:
    tree = None

    def __init__(self, N):
        random.seed()
        self.tree = [Node(i) for i in range(2 * N + 1)]

    def __str__(self):
        return str(self.tree)

    def __eq__(self, other):
        if not isinstance(other, RemyTree):
            return False
        return self.tree == other.tree

    def change_leaves(self, a, b):
        parentA = self.tree[a].parent
        parentB = self.tree[b].parent
        if self.tree[parentA].right_child == a:
            self.tree[parentA].right_child = b
        else:
            self.tree[parentA].left_child = b
        self.tree[a].parent = parentB
        if self.tree[parentB].right_child == b:
            self.tree[parentB].right_child = a
        else:
            self.tree[parentB].left_child = a
        self.tree[b].parent = parentA

    def growing_tree(self, n):
        if n == 0:
            return self

        self.tree[0].left_child = 1
        self.tree[0].right_child = 2
        self.tree[0].num = 0
        self.tree[1].parent = self.tree[2].parent = 0
        self.tree[1].right_child = self.tree[1].left_child = -1
        self.tree[2].right_child = self.tree[2].left_child = -1

        for i in range(2, n + 1):
            nb = random.randint(0, i - 1)
            self.change_leaves(i - 1, nb + i - 1)
            self.tree[i - 1].right_child = 2 * i - 1
            self.tree[i - 1].left_child = 2 * i
            self.tree[i - 1].num = i - 1
            self.tree[2 * i - 1].parent = self.tree[2 * i].parent = i - 1
            self.tree[2 * i - 1].right_child = self.tree[2 *
                                                         i - 1].left_child = -1
            self.tree[2 * i].right_child = self.tree[2 * i].left_child = -1

    def growing_tree_det(self, n, l):
        if n == 0:
            return self

        self.tree[0].left_child = 1
        self.tree[0].right_child = 2
        self.tree[0].num = 0
        self.tree[1].parent = self.tree[2].parent = 0
        self.tree[1].right_child = self.tree[1].left_child = -1
        self.tree[2].right_child = self.tree[2].left_child = -1

        for i, nb in zip(range(2, n + 1), l):
            self.change_leaves(i - 1, nb + i - 1)
            self.tree[i - 1].right_child = 2 * i - 1
            self.tree[i - 1].left_child = 2 * i
            self.tree[i - 1].num = i - 1
            self.tree[2 * i - 1].parent = self.tree[2 * i].parent = i - 1
            self.tree[2 * i - 1].right_child = self.tree[2 * i - 1].left_child = -1
            self.tree[2 * i].right_child = self.tree[2 * i].left_child = -1

        return self

    def compress(self):
        return self.compress_aux(0)
        
    def compress_aux(self, i):
        if self.tree[i].is_leaf():
            return ""
        else:
            return "(" + self.compress(self.tree[i].left_child) + ")" + self.compress(self.tree[i].right_child)
