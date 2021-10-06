"""Cours sur les algorithmes de tri."""
import typing as t


def tri_rapide_rec(lst: t.List[t.Any]) -> t.List[t.Any]:
    """Sort a list recursively using the quicksort algorithm.

    :param lst: a list to sort
    :type lst: t.List[t.Any]
    :return: the sorted list
    :rtype: t.List[t.Any]
    """
    if len(lst) == 1:
        return lst

    return tri_rapide_rec([x for x in lst if x < lst[0]]) + lst[0:1] + (
        tri_rapide_rec([x for x in lst if x > lst[0]])
    )


def tri_rapide_inplace(lst: t.List[t.Any]) -> None:
    """Sort a list inplace using the quicksort algorithm.

    :param lst: a list to sort
    :type lst: t.List[t.Any]
    :return: the sorted list
    :rtype: t.List[t.Any]
    """
    def _apply(i: int, j: int) -> int:
        """Apply the algorithm between indexes i and j, returning the pivot."""
        elem = lst[i]
        position = i
        for j in range(i + 1, j + 1):
            if lst[j] < elem:
                lst[position] = lst[j]
                lst[j] = lst[position + 1]
                position += 1
        lst[position] = elem
        return position

    def algorithm(i: int, j: int) -> None:
        """Recursively apply the algorithm."""
        if i < j:
            position = _apply(i, j)
            algorithm(i, position - 1)
            algorithm(position + 1, j)

    algorithm(0, len(lst) - 1)

# Cas favorable : T(n) = 2 * T((n-1)/2) + O(n)
# On se limite à n = 2^k
# uk = T(2^k)
# uk/(2^k) = u(k-1)/2^(k-1) + O(1)
# On somme de 1 à k :
# uk/(2^k) = O(k) -> T(2^k) = O(k*2^k)
# T(n) = O(n * ln n)
