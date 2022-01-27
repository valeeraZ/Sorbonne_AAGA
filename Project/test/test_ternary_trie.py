import os
from hypothesis import given, strategies as st

from src.ternary_trie import ternary_trie_article, test_fusion_bug

dir = './Shakespeare/'
entries = os.listdir(dir)


@given(st.integers(min_value=0, max_value=len(entries) - 1), st.integers(min_value=0, max_value=len(entries) - 1),
       st.integers(min_value=10, max_value=200), st.integers(min_value=10, max_value=500))
def test_ternary_trie_fusion(index1, index2, nb_words1, nb_words2):
    arbre1 = ternary_trie_article(dir + str(entries[index1]), nb_words1)
    arbre2 = ternary_trie_article(dir + str(entries[index2]), nb_words2)
    assert not test_fusion_bug(arbre1, arbre2)
