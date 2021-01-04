"""TP du 04/01/2021."""

from random import randint
from time import time
import typing


LISTS = [
    [randint(-10, 10) for _ in range(1000)],
    [randint(-10, 10) for _ in range(10000)],
    [randint(-10, 10) for _ in range(100000)],
]


def somme(a: typing.List[int], i: int, j: int) -> int:
    """Return sum(a[i:j])."""
    return sum(a[i:j])


def coupeMin1(a: typing.List[int]) -> int:
    """Renvoie la coupe minimale."""
    return min(
        somme(a, i, j) for i in range(len(a)) for j in range(i, len(a) + 1)
    )
# coupeMin effectue n-1 itérations sur i, et n itérations sur a
# Somme effectue au maximum n opérations
# Ainsi, coupeMin est O(n**3)


def tempsexec(index: int, func: typing.Callable) -> float:
    """Return the execution time of the func algorithm with the index list."""
    assert 1 <= index <= len(LISTS)
    start = time()
    func(LISTS[index - 1])
    return time() - start
# Pour liste1, le temps d'exécution est de 2.1 s
# On peut prévoir un temps d'exécution de l'ordre de 2100 s pour liste2
# soit plus d'une demi-heure, et 21000 s pour liste3, soit environ 5h30


def minCoupe(a: typing.List[int], i: int) -> int:
    """Renvoie valeur minimale somme coupe de a de premier élément a[i]."""
    current = final = a[i]
    for j in range(i + 1, len(a)):
        current += a[j]
        if current < final:
            final = current
    return final


def coupeMin2(a: typing.List[int]) -> int:
    """Renvoie la valeur minimale de coupe de a."""
    return min(minCoupe(a, i) for i in range(len(a)))
# coupeMin2 comporte une boucle de longueur n
# minCoupe boucle sur une longueur inférieure à n.
# La complexité de coupeMin2 est donc bien quadratique.
#
# Pour liste1, on obtient un temps de calcul de 0.08 s
# Pour liste2, on obtient un temps de calcul de 3.3s
# On peut prévoire un temps de calcul pour liste3 comprit entre
# 330 s et 800 s, soit entre 5 et 13 minutes
#
# Partie III
# Question 1
# une coupe quelconque de a[0: i+1] est soit incluse dans l'ensemble des coupes
# de a[0: i], soit termine par a[i+1]. Ainsi :
# m[i+1] = min(ci+1, mi)
# c[i+1] est :
# - Soit égal à a[i+1]
# - Soit égal à c[i] + a[i+1]
# Ainsi, c[i+1] = min(c[i], c[i] + a[i+1], a[i+1])


def coupeMin3(a: typing.List[int]):
    """Renvoie la coupe minimale de a."""
    m = c = a[0]
    for i in range(1, len(a)):
        c = min(c + a[i], a[i])
        m = min(c, m)
    return m
# Pour liste1, le temps de calcul est trop faible pour être renvoyé
# Pour liste2, le temps de calcul est de 5 ms
# Pour liste3, le temps de calcul est de 34 ms
#
# Partie IV
# Question 1
# Si on note A la coupe de somme minimale de a.
# Soit A est incluse dans a[0: k]
# Soit A est incluse dans a[k: n]
# Soit A contient des éléments de ces deux parties de a
# Dans ce cas, A est constituée d'une coupe a[i0, k], et d'une coupe a[k: j0]
# On souhaite que la somme des éléments de A soit minimale, c'est-à-dire que
# la somme des éléments de a[i0, k] soit minimale, tout comme celle de
# a[k: j0]
# Ainsi, dans ce cas, a[i0, k] réalise le minimum de la somme sur les coupes
# non vides terminant par a[k-1], et a[k, j0] réalise le minimum des coupes
# commençant par a[k].


def coupeMin4(lst: typing.List[int]) -> int:
    """Renvoie la coupe minimale de la liste."""
    if len(lst) == 1:
        return lst[0]
    k = int(len(lst) / 2)
    return min(
        coupeMin4(lst[:k]),
        coupeMin4(lst[k:]),
        _coupe_left(lst[:k]) + _coupe_right(lst[k:]),
    )


def _coupe_left(lst: typing.List[int]) -> int:
    """Renvoie la coupe minimale contenant le dernier élément de la liste."""
    minimal = current = lst[-1]
    for i in range(1, len(lst)):
        current += lst[-i - 1]
        if current < minimal:
            minimal = current
    return minimal


def _coupe_right(lst: typing.List[int]) -> int:
    """Renvoie la coupe minimale contenant le premier élément de la liste."""
    minimal = current = lst[0]
    for i in range(1, len(lst)):
        current += lst[i]
        if current < minimal:
            minimal = current
    return minimal
# _coupe_right et _coupe_left sont ensemble complexité n.
# On a bien la complexité souhaitée pour coupeMin4
# Le temps d'exécution est de:
# - 6.4 ms pour liste1
# 76 ms pour liste2
# 0.25 s pour liste3


# Exercice bonus
def min_diff(lst: typing.List[int]) -> int:
    """Renvoie la valeur minimale de la différence."""
    minimal = lst[1] - lst[0]
    maximal = lst[0]
    for i in range(2, len(lst)):
        if lst[i - 1] > maximal:
            maximal = lst[i - 1]
        minimal = min(lst[i] - maximal, minimal)
    return minimal
