import random
import itertools
from collections import defaultdict
import pydot


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
            self.tree[2 * i - 1].right_child = self.tree[2 *
                                                         i - 1].left_child = -1
            self.tree[2 * i].right_child = self.tree[2 * i].left_child = -1

        return self

    def compress(self):
        return self.compress_aux(0)

    def compress_aux(self, i):
        if self.tree[i].is_leaf():
            return ""
        else:
            return "(" + self.compress_aux(self.tree[i].left_child) + ")" + self.compress_aux(self.tree[i].right_child)

    def load_graph(self, graph, index=0, name=None):
        """
        load graph for display the tree

        Args:
            graph: a graph of class Dot
            name: a static increment value, to give meaningless unique name of each node

        """
        tree = self.tree[index]
        if name is None:
            name = [0]
        node = pydot.Node(str(name[0]), label=tree.num, shape='circle')
        if tree.left_child == -1 and tree.right_child == -1:
            node.set('color', 'red')
        graph.add_node(node)
        if tree.left_child != -1:
            name[0] += 1
            node_left = pydot.Node(
                str(name[0]), label=self.tree[tree.left_child].num, shape='circle')
            edge = pydot.Edge(node, node_left)
            graph.add_edge(edge)
            self.load_graph(graph, tree.left_child, name)
        if tree.right_child != -1:
            name[0] += 1
            node_right = pydot.Node(
                str(name[0]), label=self.tree[tree.right_child].num, shape='circle')
            edge = pydot.Edge(node, node_right)
            graph.add_edge(edge)
            self.load_graph(graph, tree.right_child, name)


def gen_combs(n):
    """
    generates all possible lists of size `n`
    where for each list `l`, `l[i]<=i forall i in len(l)`
    """
    combs = [[]]
    for _ in range(n):
        combs_tmp = []
        for comb in combs:
            for i in range(len(comb) + 1):
                combs_tmp.append(comb + [i])
        combs = combs_tmp.copy()

    return combs


def gen_all_trees(n):
    perms = gen_combs(n)
    trees = []
    for perm in perms:
        t = RemyTree(n)
        t.growing_tree_det(n, perm)
        trees.append(t)
    return trees


def test_covering(n):
    trees = gen_all_trees(n)
    trees_compressed = list(map(RemyTree.compress, trees))
    count = defaultdict(int)
    for tc in trees_compressed:
        count[tc] += 1
    return all(map(lambda x: x == count[trees_compressed[0]], count.values()))


def test_small_coverings():
    return all([test_covering(i) for i in range(9)])


def test_load_graph():
    n = 6
    t = RemyTree(n)
    t.growing_tree(n)
    graph = pydot.Dot(graph_type="digraph")
    t.load_graph(graph)
    name = "remy_tree_" + str(n) + ".png"
    graph.write_png(name)


if __name__ == '__main__':
    if test_small_coverings():
        print("the coverings of remy are uniform")
    else:
        print("the coverings of remy are not uniform")
