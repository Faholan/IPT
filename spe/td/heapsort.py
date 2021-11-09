"""TD tri par tas - à rendre.

Copyright (C) 2021  Faholan <https://github.com/Faholan>
"""
from random import randint
import typing as t

# Partie 4 - Tri par tas


# Question 1 - Fonction échange
def echange(lst: t.List[t.Any], i: int, j: int) -> None:
    """Echange deux éléments d'une liste."""
    lst[i], lst[j] = lst[j], lst[i]


# Question 2 - Reconstituer
def reconstituer(lst: t.List[t.Any], i: int, j: int) -> None:
    """Reconstitue récursivement l'arbre."""
    if 2 * i + 1 < j:
        if 2 * i + 2 < j:
            if lst[2 * i + 1] > lst[2 * i + 2]:
                index = 2 * i + 1
            else:
                index = 2 * i + 2
        else:
            index = 2 * i + 1
        if lst[index] > lst[i]:
            echange(lst, i, index)
            reconstituer(lst, index, j)


# Question 3 - Mise en tas
def mise_en_tas(lst: t.List[t.Any]) -> None:
    """Mise en tas d'une liste."""

    def _mise_en_tas(i: int) -> None:
        reconstituer(lst, i, len(lst))
        if i != 0:
            _mise_en_tas(i - 1)

    _mise_en_tas(len(lst) // 2 - 1)


# Question 4 - mise en tas
def heapsort(lst: t.List[t.Any]) -> None:
    """Heap sort."""
    mise_en_tas(lst)
    for i in range(len(lst) - 1):
        reconstituer(lst, 0, len(lst) - i)
        echange(lst, 0, -1 - i)


def randomlist(length: int, values: int) -> t.List[int]:
    """Create random lists of integers."""
    return [randint(0, values) for _ in range(length)]  # nosec
    # The pseudo-random generator isn't used for a cryptographic purpose
