from src.rand_number import rand_int
import pytest 

NB = 0


class Arbre:
    def __init__(self, cle, val, F):
        global NB
        self.id = NB
        NB += 1
        self.cle = cle
        self.val = val
        self.fils = F

    def affiche(self):
        if self.cle == '':
            return ' . '
        g = '( ' + self.cle + (',  ' + str(self.val) if self.val is not None else '') + '  '
        for f in self.fils:
            g += f.affiche() + ' '
        g += ')'
        return g

    def get_mots(self, prefx):
        """
        à partir d'un préfixe, traverser tous les chemins de l'arbre puis composer les mot par le préfixe et les lettres
        Args:
            prefx: le préfixe de mots

        Returns:
            ensemble de mots préfixés trouvés dans l'arbre
        """
        words = set()

        if self.cle == '':
            return words
        if self.val == 0:
            words.add(prefx + self.cle)

        words = words.union(self.fils[0].get_mots(prefx))
        words = words.union(self.fils[1].get_mots(prefx + self.cle))
        words = words.union(self.fils[2].get_mots(prefx))

        return words


def gener_feuille():
    return Arbre('', None, [])


def gener_noeud(cle, val, F):
    return Arbre(cle, val, F)


def cons(mot):
    if mot == '':
        return gener_feuille()
    else:
        if len(mot) == 1:
            return gener_noeud(mot[0], 0, [gener_feuille(), gener_feuille(), gener_feuille()])
        else:
            return gener_noeud(mot[0], None, [gener_feuille(), cons(mot[1:]), gener_feuille()])


def insert(A, mot):
    if mot == '':
        return A
    if A.cle == '':
        return cons(mot)
    if A.cle > mot[0]:
        return gener_noeud(A.cle, A.val, [insert(A.fils[0], mot), A.fils[1], A.fils[2]])
    elif A.cle == mot[0]:
        val = A.val
        if len(mot) == 1:
            val = 0
        return gener_noeud(A.cle, val, [A.fils[0], insert(A.fils[1], mot[1:]), A.fils[2]])
    else:
        val = A.val
        return gener_noeud(A.cle, val, [A.fils[0], A.fils[1], insert(A.fils[2], mot)])


def fusion(A, B):
    if A.cle == '':
        return B
    if B.cle == '':
        return A

    if A.cle < B.cle:
        return gener_noeud(A.cle, A.val, [A.fils[0], A.fils[1], fusion(A.fils[2], B)])
    if A.cle > B.cle:
        return gener_noeud(A.cle, A.val, [fusion(A.fils[0], B), A.fils[1], A.fils[2]])

    if A.val != None:
        val = A.val
    else:
        val = B.val
    return gener_noeud(A.cle, val,
                       [fusion(A.fils[0], B.fils[0]), fusion(A.fils[1], B.fils[1]), fusion(A.fils[2], B.fils[2])])


def ternary_trie_article(filename, nb):
    """
    insérer un nombre donné de mots dans fichier donné à un arbre initialement vide,
    les mots sont choisis uniformément
    Args:
        filename:  le nom du fichier contenant des lignes de mots
        nb: le nombre de mots à insérer dans l'arbre

    Returns:
        l'arbre contenant le `nb` mots choisis uniformément
    """
    arbre = gener_feuille()
    data = []
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            data.append(line)
    for _ in range(nb):
        index, _ = rand_int(len(data))
        mot = data[index]
        arbre = insert(arbre, mot)
        data.remove(mot)
    return arbre


def search(A, mot):
    """
    Chercher le mot donné dans l'arbre A et renvoie True si il y est
    présent, False sinon
    A : arbre
    mot : mot à chercher
    """

    if mot == '':
        return False
    elif len(A.fils) == 0:
        return False
    elif mot[0] < A.cle:
        return search(A.fils[0], mot)
    elif mot[0] > A.cle:
        return search(A.fils[2], mot)
    elif len(mot) == 1:
        return True if mot[0] == A.cle and A.val == 0 else False
    return search(A.fils[1], mot[1:])

@pytest.mark.skip(reason="not for pytest")
def test_fusion_bug(a, b):
    """
    test de déterminer si l'arbre fusionné par arbre a et b est valide
    Args:
        a: l'arbre a à fusionner avec b
        b: l'arbre b à fusionner avec a

    Returns:
        True si l'arbre fusionné est valid, sinon False
    """
    a_b = fusion(a, b)
    words_a_b = a.get_mots("").union(b.get_mots(""))
    for word in words_a_b:
        if not search(a_b, word):
            # print("bug:", word)
            return False
    return True


if __name__ == '__main__':
    arbre1 = ternary_trie_article("./Shakespeare/1henryiv.txt", 10)
    arbre2 = ternary_trie_article("./Shakespeare/1henryvi.txt", 10)
    fusion_arbre = fusion(arbre1, arbre2)
    if test_fusion_bug(arbre1, arbre2):
        print("The fusion function doesn't have bug")
    else:
        print("The fusion function has bug")
