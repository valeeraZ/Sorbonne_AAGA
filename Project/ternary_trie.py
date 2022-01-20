from rand_number import rand_int

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
    # print(arbre.affiche())
    return arbre

cpt = 0

def search_bug(arbre):
    global cpt
    cpt += 1
    if arbre.cle == '':
        return True
    if (arbre.cle < arbre.fils[0].cle != '') or (arbre.cle > arbre.fils[2].cle != ''):
        print("Bug observed in ", arbre.cle, arbre.fils[0].cle, arbre.fils[1].cle)
        return False
    else:
        return search_bug(arbre.fils[0]) and search_bug(arbre.fils[1]) and search_bug(arbre.fils[2])


arbre1 = ternary_trie_article("Shakespeare/1henryiv.txt", 300)
arbre2 = ternary_trie_article("Shakespeare/1henryvi.txt", 400)
print("arbre1 n'a pas de bug ?", search_bug(arbre1))
print(cpt)
cpt = 0
print("arbre2 n'a pas de bug ?", search_bug(arbre2))
print(cpt)
cpt = 0
print("fusion of arbre1 and arbre2 has bug?", search_bug(fusion(arbre1, arbre2)))
print(cpt)
cpt = 0
