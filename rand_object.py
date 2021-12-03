from rand_number import rand_int
import pydot


def gen_permutation_1(n):
    """generate a permutation of values from 1 to n

    Args:
        n: the greater value of range

    Returns: (permutation, bits used)
        * a list containing the permutation of elements 1,2...n
        * the bits used during the generation
    """
    elements = [i for i in range(1, n + 1)]
    res = []
    bit_used = 0
    for i in range(n):
        r, bit = rand_int(n - i)
        bit_used += bit
        res.append(elements.pop(r))
    return res, bit_used


def gen_permutation_2(n):
    """generate a permutation of values from 1 to n

    Args:
        n: the greater value of range

    Returns:
        (permutation, bits used)
        * a list containing the permutation of elements 1,2...n
        * the bits used during the generation
    """
    res = [i for i in range(1, n + 1)]
    bit_used = 0
    for i in range(n):
        r, bit = rand_int(n - i)
        r += i
        bit_used += bit
        tmp = res[i]
        res[i] = res[r]
        res[r] = tmp
    return res, bit_used


class Node:
    def __init__(self, value=None, left=None, right=None, parent=None, parent_dir=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.parent_dir = parent_dir

    def __str__(self):
        return self.value

    def load_graph(self, graph, name=None):
        """
        load graph for display the tree

        Args:
            graph: a graph of class Dot
            name: a static increment value, to give meaningless unique name of each node

        """
        if name is None:
            name = [0]
        node = pydot.Node(str(name[0]), label=self.value, shape='circle')
        if self.left is None and self.right is None:
            node.set('color', 'red')
        graph.add_node(node)
        if self.left:
            name[0] += 1
            node_left = pydot.Node(str(name[0]), label=self.left.value, shape='circle')
            edge = pydot.Edge(node, node_left)
            graph.add_edge(edge)
            self.left.load_graph(graph, name)
        if self.right:
            name[0] += 1
            node_right = pydot.Node(str(name[0]), label=self.right.value, shape='circle')
            edge = pydot.Edge(node, node_right)
            graph.add_edge(edge)
            self.right.load_graph(graph, name)


def remy_tree_generator(n):
    """Generate a pseudo random binary tree which is implementation of Algorithm Rémy

    * See https://fr.wikipedia.org/wiki/Algorithme_de_R%C3%A9my

    Args:
        n: the size of tree to generate

    Returns:
        the root of this tree
    """
    nodes = [Node(str(0))]
    i = 0
    while i < n:
        i += 1
        index = rand_int(len(nodes))[0]
        new_internal_node = Node('x')
        new_internal_node.parent = nodes[index].parent
        new_internal_node.parent_dir = nodes[index].parent_dir

        node = nodes[index]
        direction = rand_int(2)[0]
        new_node = Node(str(i))

        node.parent = new_internal_node
        new_node.parent = new_internal_node
        if direction == 0:  # left
            new_internal_node.left = node
            new_internal_node.right = new_node
            node.parent_dir = 0
            new_node.parent_dir = 1
        else:
            new_internal_node.left = new_node
            new_internal_node.right = node
            node.parent_dir = 1
            new_node.parent_dir = 0

        nodes[index] = new_internal_node
        if nodes[index].parent is not None:
            if nodes[index].parent_dir == 0:
                nodes[index].parent.left = new_internal_node
            else:
                nodes[index].parent.right = new_internal_node
        nodes.append(new_node)
        nodes.append(node)

    return nodes[0]


def gen_bst(n):
    """
    Generate a pseudo random binary search tree's structure without label

    Args:
        n: the size of tree to generate

    Returns:
        the root of this tree
    """

    root = Node('x')
    leaves = [root]
    nodes = []
    i = 0
    while i < n:
        index = rand_int(len(leaves))[0]
        leave = leaves[index]
        leaves.remove(leave)
        left_child = Node('x')
        right_child = Node('x')
        new_internal_node = Node('x', left_child, right_child, leave.parent, leave.parent_dir)

        if new_internal_node.parent is not None:
            if new_internal_node.parent_dir == 0:
                new_internal_node.parent.left = new_internal_node
            else:
                new_internal_node.parent.right = new_internal_node

        left_child.parent = new_internal_node
        left_child.parent_dir = 0

        right_child.parent = new_internal_node
        right_child.parent_dir = 1

        nodes.append(new_internal_node)
        leaves.append(left_child)
        leaves.append(right_child)
        i += 1
    return nodes[0]


def count_nodes(bst):
    """
    count the number of left child's and right child's nodes

    Args:
        bst: the binary search tree's root

    Returns:
        (number of left child's nodes, number of right child's nodes)

    """
    if bst is None:
        return 0, 0
    if bst.left is None and bst.right is None:
        return 0, 0
    return (1 + count_nodes(bst.left)[0] + count_nodes(bst.left)[1],
            1 + count_nodes(bst.right)[0] + count_nodes(bst.right)[1])


def label_bst(bst, range_min=0, range_max=None):
    """
    label a binary search tree from 1

    Args:
        bst: the binary search tree
        range_min: min border for label node, which the label > range_min
        range_max: max border for label node, which the label < range_max

    """
    nl, nr = count_nodes(bst)
    bst.value = range_min + nl + 1
    if bst.left:
        label_bst(bst.left, range_min, bst.value)
    if bst.right:
        label_bst(bst.right, bst.value, range_max)
