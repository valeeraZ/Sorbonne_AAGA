import random
import itertools
from collections import defaultdict
from src.remy_bug import RemyTree
import pytest
# import pydot


class RemyTreeValid(RemyTree):
    def __init__(self, N):
        super().__init__(N)
        self.root = 0

    def growing_tree(self, n):
        """
        generates a random remy tree of size `n`
        """
        if n == 0:
            return self
        self.tree[0].num = 0
        self.tree[0].left_child = -1
        self.tree[0].left_child = -1
        self.tree[0].parent = -1
        for i in range(1, 2 * n, 2):
            index = random.randint(0, i - 1)
            direction = random.randint(0, 1)
            parent = self.tree[index].parent
            if parent == -1:
                self.root = i
            elif self.tree[parent].left_child == index:
                self.tree[parent].left_child = i
            else:
                self.tree[parent].right_child = i
            self.tree[i].parent = parent
            if direction == 0:
                self.tree[i].left_child = i + 1
                self.tree[i].right_child = index
            else:
                self.tree[i].right_child = i + 1
                self.tree[i].left_child = index
            self.tree[index].parent = i
            self.tree[i + 1].num = i + 1
            self.tree[i + 1].left_child = -1
            self.tree[i + 1].right_child = -1
            self.tree[i + 1].parent = i

    def growing_tree_det(self, n, l):
        """
        generates deterministic remy tree i.e
        use a predetermined list `l` instead of random ints
        """
        if n == 0:
            return self
        self.tree[0].num = 0
        self.tree[0].left_child = -1
        self.tree[0].left_child = -1
        self.tree[0].parent = -1
        for i, (index, direction) in zip(range(1, 2 * n, 2), l):
            parent = self.tree[index].parent
            if parent == -1:
                self.root = i
            elif self.tree[parent].left_child == index:
                self.tree[parent].left_child = i
            else:
                self.tree[parent].right_child = i
            self.tree[i].parent = parent
            if direction == 0:
                self.tree[i].left_child = i + 1
                self.tree[i].right_child = index
            else:
                self.tree[i].right_child = i + 1
                self.tree[i].left_child = index
            self.tree[index].parent = i
            self.tree[i + 1].num = i + 1
            self.tree[i + 1].left_child = -1
            self.tree[i + 1].right_child = -1
            self.tree[i + 1].parent = i

    def compress(self):
        """
        compress the tree using an injective function phi where
        phi(tree(left,right)) = (phi(left)) right
        """
        return self.compress_aux(self.root)


def gen_combs(n):
    """
    generates all possible lists couples (i,dir) of size `2*n`
    where for each list `l`, `l[i]<=i forall i in len(l)`
    and dir in [0,1]
    """
    res = []
    for i in range(0, 2 * n - 1, 2):
        comb_direction = list(
            map(list, list(itertools.product(range(i + 1), [0, 1]))))
        res.append(comb_direction)
    perms = list(itertools.product(*res))
    return perms


def gen_all_trees(n):
    """
    generates all possible trees of size `n`
    """
    perms = gen_combs(n)
    trees = []
    for perm in perms:
        t = RemyTreeValid(n)
        t.growing_tree_det(n, perm)
        trees.append(t)
    return trees


@pytest.mark.skip(reason="not for pytest")
def test_covering(n):
    "test a covering of size n"
    trees = gen_all_trees(n)
    trees_compressed = list(map(RemyTreeValid.compress, trees))
    count = defaultdict(int)
    for tc in trees_compressed:
        count[tc] += 1
    return all(map(lambda x: x == count[trees_compressed[0]], count.values()))


@pytest.mark.skip(reason="not for pytest")
def test_small_coverings():
    "tests for small coverings"
    n = 7
    return all([test_covering(i) for i in range(n)])


if __name__ == '__main__':
    if test_small_coverings():
        print("the coverings of remy_valid are uniform")
    else:
        print("the coverings of remy_valid are not uniform")
