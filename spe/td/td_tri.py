"""TD tri - 06/10/2021.

Copyright (C) 2021  Faholan <https://github.com/Faholan>
"""
from random import randint
import typing as t

# Partie 1 - Tri par dénombrement
# Question 1 - Tri par dénombrement


def enumeration_sort(n_max: int, lst: t.List[int]) -> t.List[int]:
    """Implement the enumeration sort.

    :param n_max: The maximum of the list
    :type n_max: int
    :param lst: The list to sort
    :type lst: List[int]
    :return: The sorted list
    :rtype: List[int]
    """
    occurences = [0] * (n_max + 1)
    for elem in lst:
        occurences[elem] += 1

    result: t.List[int] = []
    for k, num in enumerate(occurences):
        result += [k] * num

    return result

# Question 2 - Tri sélection


def selection_sort(lst: t.List[t.Any]) -> t.List[t.Any]:
    """Implement the selection sort.

    :param lst: The list to sort
    :type lst: List[Any]
    :return: The sorted list
    :rtype: List[Any]
    """
    if len(lst) <= 1:
        return lst

    min_pos, cur_min = 0, lst[0]

    for pos, elem in enumerate(lst):
        if elem < cur_min:
            min_pos, cur_min = pos, elem

    lst[0], lst[min_pos] = cur_min, lst[0]

    return [cur_min] + selection_sort(lst[1:])


# Partie 2 - Coupe maximale dans un tableau
# Question 1
def cumul(lst: t.List[int]) -> t.List[int]:
    """Calculate the partial sums of lst.

    :param lst: The reference list
    :type lst: List[int]
    :return: The list of partial sums
    :rtype: List[int]
    """
    result = [lst[0]]
    for elem in lst[1:]:
        result.append(result[-1] + elem)
    return result
# Cet algorithme est linéaire


# Question 2
def maxsomme(lst: t.List[int]) -> int:
    """Calculate lst's maximal subsum.

    :param lst: A list of integers
    :type lst: List[int]
    :return: The maximal subsum
    :rtype: int
    """
    cumulated = cumul(lst)

    cur_max = max(cumulated)
    # Maximum beginning from 0
    # Maximum beginning from another element
    for i in range(len(lst) - 1):
        for j in range(i + 1, len(lst)):
            if cumulated[j] - cumulated[i] > cur_max:
                cur_max = cumulated[j] - cumulated[i]

    return cur_max
# Cet algorithme est en O(n²)


# Question 3
def _maxsomme2(lst: t.List[int]) -> t.Tuple[int, int, int, int]:
    """Calculate (s, msg, ms, msd).

    :param lst: The reference list
    :type lst: List[int]
    :return: The tuple (s, msg, ms, msd)
    :rtype: Tuple[int, int, int, int]
    """
    if len(lst) == 1:
        return lst[0], lst[0], lst[0], lst[0]

    pos = len(lst) // 2

    s1, msg1, ms1, msd1 = _maxsomme2(lst[:pos])
    s2, msg2, ms2, msd2 = _maxsomme2(lst[pos:])

    return (
        s1 + s2,
        max(s1 + msg2, msg1),
        max(ms1, ms2, msd1 + msg2),
        max(msd1 + s2, msd2),
    )


def maxsomme2(lst: t.List[int]) -> int:
    """Calculate the maximum of the subsums.

    :param lst: The reference list
    :type lst: List[int]
    :return: The maximum of all subsums
    :rtype: int
    """
    return _maxsomme2(lst)[2]

# Partie 3 - Problème de sélection
# Question 1 - Algorithme naïf


def quicksort(lst: t.List[int]) -> t.List[int]:
    """Sort a list using the quicksort algorithm.

    :param lst: The list to sort
    :type lst: List[Any]
    :return: The sorted list
    :rtype: List[Any]
    """
    if len(lst) == 1:
        return lst

    return quicksort([x for x in lst if x < lst[0]]) + lst[0:1] + (
        quicksort([x for x in lst if x > lst[0]])
    )


def selection_naive(lst: t.List[int], position: int) -> int:
    """Get the element in the given position in the sorted list.

    :param lst: The unsorted which from which to fetch
    :type lst: List[int]
    :param position: The position of the element to fetch
    :type position: int
    :return: The fetched element
    :rtype: int
    """
    return quicksort(lst)[position]


def naive_median(lst: t.List[int]) -> int:
    """Naively get the median element in a list.

    :param lst: The list you want the median of
    :type lst: List[int]
    :return: The list's median element
    :rtype: int
    """
    return selection_naive(lst, len(lst) // 2)


# Question 2 - algorithme diviser pour régner
def quick_select(lst: t.List[int], position: int) -> int:
    """Select the given element with a cuicksort-like algorithm.

    :param lst: The list of elements to fetch from
    :type lst: List[int]
    :param position: The position of the element you want
    :type position: int
    :return: The fetched element
    :rtype: int
    """
    # All indexes are from 0
    value = lst[-1]
    greater = [x for x in lst[:-1] if x > value]
    smaller = [x for x in lst[:-1] if x <= value]
    lst.append(value)

    if position == len(smaller):
        return value

    if len(smaller) < position:
        return quick_select(greater, position - len(smaller) - 1)

    return quick_select(smaller, position)

# Si l'on supppose qu'en moyenne la liste est partagée en deux, comme à
# chaque fois on divise la liste en deux, et qu'on n'en traite qu'une moitié :
# T(n) <= T(n/2) + O(n)
# Inférieur ou égal car on peut renvoyer à toute étape
# On pose uk = T(2^k), et on se place dans le cas d'égalité
# On a :
# uk = u(k-1) + O(2^k)
# En sommant :
# uk = O(Somme(2^j))
# uk = O(2^(k+1) - 1)
# Ainsi, on a T(n) = O(n)
# Dans le pire des cas, on a :
# T(n) = T(n-1) + O(n)
# On retrouve l'équation du pire des cas du tri rapide
# Donc la complexité dans le pire des cas est O(n²)

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
