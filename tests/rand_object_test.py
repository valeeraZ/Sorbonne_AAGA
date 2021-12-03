import datetime
import unittest

import networkx
import pydot
from ppbtree import print_tree

from rand_object import gen_permutation_1, gen_permutation_2, remy_tree_generator, gen_bst, count_nodes, label_bst


def test_gen_permutation():
    start_1 = datetime.datetime.now()
    _, bits_used_1 = gen_permutation_1(20000)
    end_1 = datetime.datetime.now()
    time_used_1 = end_1 - start_1

    start_2 = datetime.datetime.now()
    _, bits_used_2 = gen_permutation_2(20000)
    end_2 = datetime.datetime.now()
    time_used_2 = end_2 - start_2

    print()
    print("gen_permutation_1 takes time:", time_used_1, ", uses bits:", bits_used_1)
    print("gen_permutation_2 takes time:", time_used_2, ", uses bits:", bits_used_2)


def test_gen_remy_tree():
    root = remy_tree_generator(6)
    graph = pydot.Dot(graph_type="digraph")
    root.load_graph(graph)
    graph.write_png("remy_6.png")
    print()
    print("See remy_6.png for output of graph")


def test_gen_binary_tree():
    root = gen_bst(6)
    graph = pydot.Dot(graph_type="digraph")
    root.load_graph(graph)
    graph.write_png("bst_6.png")
    print()
    print("See bst_6.png for output of graph without label")
    label_bst(root)
    graph = pydot.Dot(graph_type="digraph")
    root.load_graph(graph)
    graph.write_png("bst_6_label.png")
    print()
    print("See bst_6_label.png for output of graph with label")


class RandObjectTest(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
