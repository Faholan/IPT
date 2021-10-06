"""Exos récursivité.

Copyright (C) 2021  Faholan <https://github.com/Faholan>
"""

import typing as t

Numeric = t.Union[int, float]


# Question 9
def _purge(num_list: t.List[int], start: int = 0) -> None:
    """Remove the multiples of the designated number from the list."""
    i = start + 1
    while i < len(num_list):
        if num_list[i] % num_list[start] == 0:
            num_list.pop(i)
        else:
            i += 1


def get_smallest_prime_divider(num: int) -> int:
    """Get the smallest prime divider of an integer."""
    for i in range(2, abs(num) + 1):
        if num % i == 0:
            return i
    raise ValueError("1 has no prime divider")
    # The smallest prime divider is also the smallest divider


def _get_dividers(num: int, candidates: t.List[int]) -> t.List[int]:
    """Get the prime dividers of a number recursively."""
    if num == 1:
        return []

    _purge(candidates)

    if num % candidates[0]:
        return _get_dividers(num, candidates[1:])

    while not num % candidates[0]:
        num //= candidates[0]

    results = _get_dividers(num, candidates[1:])
    results.append(candidates[0])
    return results


def get_prime_dividers(num: int) -> t.List[int]:
    """Get all prime dividers of a number."""
    if num == 0:
        raise ValueError("Infinite number of dividers")

    num = abs(num)

    return _get_dividers(num, list(range(2, num + 1)))


def eratosthene(num: int) -> t.List[int]:
    """Get the prime numbers up to a given one."""
    results = list(range(2, num + 1))

    i = 0
    while results[i] ** 2 < results[-1]:
        _purge(results, i)
        i += 1
    # If a number isn't prime, it has a divider smaller than its square root
    return results


# Question 11

def pgcd(a: int, b: int) -> int:
    """Renvoie le PGCD de a et de b."""
    x, y = max(a, b), min(a, b)

    while y != 0:
        x, y = y, x % y
    return x


def euler(n: int) -> int:
    """Calculate Euler's indicator."""

    def _euler(candidates: t.List[int]) -> int:
        """Proceed with the algorithm."""
        if not candidates:
            return 0

        if pgcd(candidates[0], n) == 1:
            return 1 + _euler(candidates[1:])

        _purge(candidates)
        return _euler(candidates[1:])

    return _euler(list(range(1, n)))

# Si l'on note uk la longueur de la liste à l'itération k de _euler, alors on
# a, si uk != 0, u(k+1) < un, car la tête de liste n'est pas passée à l'appel
# suivant.
# (La fonction _purge termine bien car len(num_list) - i est strictement
# décroissante)
# L'algorithme se terminant lorsque uk atteint 0, l'algorithme termine bien
# On a également l'invariant de boucle suivant : soit x € [2, n - 1], x^n = 1
# Si x n'est pas en tête de liste à l'itération k, alors x est présent dans la
# liste à l'itération k+1
# En effet, si l'on note q la tête de la liste, il y a deux cas :
# Soitq est premier avec n, auquel cas x appartient à la queue de liste,
# qui est passée.
# Soit q n'est pas premier avec n. Dans ce cas, on retire tous les multiples
# de q. Or : q^n != 1 -> pour tout k, (kq)  n != 1
# Donc x appartient à la sous-liste passée à l'itération suivante.
# Enfin, l'algorithme parcours un à un tous les éléments de la liste qui ne
# sont pas retirés à une quelconque itération.
# Les éléments premiers avec n sont donc parcourus, et leur nombre est renvoyé:
# la valeur de retour, initialisée à 0, est incrémentée de 1 pour chaque
# élément premier avec n.


# Question 11
def polynome_horner(coeffs: t.List[Numeric], x: Numeric) -> Numeric:
    """Get the value of P(x)."""

    def _horner(index: int) -> Numeric:
        """Implement a step of the algorithm."""
        if index == len(coeffs) - 1:
            return coeffs[-1]

        return coeffs[index] + x * _horner(index + 1)

    return _horner(0)


# Question 12
def bissextile(annee: int) -> bool:
    """Test if the year is leap."""
    if not annee % 400:
        return True

    return annee % 100 != 0 and annee % 4 == 0


MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def jour_semaine(date: t.Tuple[int, int, int]) -> int:
    """Get the dow of a date."""
    day, month, year = date

    if day != 1:
        return (day - 2 + jour_semaine((1, month, year))) % 7 + 1

    if year > 1970:  # Epoch
        return (
            (1 if bissextile(year - 1) else 0)
            + jour_semaine((1, month, year - 1))
        ) % 7 + 1
        # 365 / 366 % 7

    if year < 1970:
        return (
            (-3 if bissextile(year + 1) else -2)
            + jour_semaine((1, month, year + 1))
        ) % 7 + 1

    if month != 1:
        return (
            MONTH_DAYS[month - 2] + jour_semaine((1, month - 1, 1970)) - 1
        ) % 7 + 1

    return 4  # 1/1/1970: Thursday
