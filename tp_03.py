"""All the work done on 02/11/2020."""
from math import factorial
from random import randint
import typing
# La fonction len permet de calculer la durée de sa randonnée


def altmax(alt: typing.List[int]) -> int:
    """Renvoie l'altitude max atteinte."""
    return max(alt)


def denivmax(alt: typing.List[int]) -> int:
    """Renvoie le dénivelé maximum."""
    return max([alt[i] - alt[i - 1] for i in range(1, len(alt))])


def denivmax_2(alt: typing.List[int]) -> int:
    """Renvoie l'heure de début du dénivelé max."""
    deniv = [alt[i] - alt[i - 1] for i in range(1, len(alt))]
    return deniv.index(max(deniv)) + 1


def denivtotal(alt: typing.List[int]) -> int:
    """Renvoie la somme des dénivelés positifs."""
    return sum([
        alt[i] - alt[i - 1] for i in range(1, len(alt)) if alt[i] > alt[i - 1]
    ])


def sommets(alt: typing.List[int]) -> typing.List[int]:
    """Renvoie la liste des sommets."""
    l_sommets = [alt[0]] if alt[0] > alt[1] else []
    for i in range(1, len(alt) - 1):
        if alt[i - 1] < alt[i] and alt[i] > alt[i + 1]:
            l_sommets.append(alt[i])
    if alt[-1] > alt[-2]:
        l_sommets.append(alt[-1])
    return l_sommets


def max_0_consecutif(tableau: typing.List[int]) -> int:
    """Renvoie le nombre maximal de 0 consécutifs."""
    max_0 = 0
    counter = 0
    for i in tableau:
        if i:
            if counter > max_0:
                max_0 = counter
            counter = 0
        else:
            counter += 1
    return max(max_0, counter)


def absents(num: int = 100) -> float:
    """Renvoie le nombre moyens d'éléments absents, pour n répétitions."""
    list_abs = []
    for _ in range(num):
        curr = [randint(0, 99) for __ in range(100)]
        list_abs.append(sum([1 for i in range(100) if i not in curr]))
    return sum(list_abs) / len(list_abs)
# On trouve une valeur de 36.8


def descr(n_max: int) -> typing.Tuple[
    typing.List[int],
    typing.List[int],
    typing.List[int],
    typing.List[int]
]:
    """Fonction de "description" du slicing."""
    if not n_max % 2 or n_max < 2:
        raise ValueError("n_max must be greater than 1 and a multiple of 2.")
    base = list(range(n_max + 1))
    return (
        base[:int(len(base) / 2)],
        base[int(len(base) / 2):],
        base[::2],
        base[1::2]
    )


def _out_shuffle(base: typing.List[int]) -> typing.List[int]:
    if len(base) % 2:
        raise ValueError("The length of base must be a multiple of 2.")
    full = base.copy()
    full[::2] = base[len(base) // 2:]
    full[1::2] = base[:len(base) // 2]
    return full


def out_shuffle(n_max: int) -> typing.List[int]:
    """Fait le out_shuffle à n cartes."""
    return _out_shuffle(list(range(n_max + 1)))


def _in_shuffle(base: typing.List[int]) -> typing.List[int]:
    if len(base) % 2:
        raise ValueError("The length of base must be a multiple of 2.")
    full = base.copy()
    full[::2] = base[:len(base) // 2]
    full[1::2] = base[len(base) // 2:]
    return full


def in_shuffle(n_max: int) -> typing.List[int]:
    """Fait le in_shuffle à n cartes."""
    return _in_shuffle(list(range(n_max + 1)))


def test_shuffle(n_max: int, func: typing.Callable) -> int:
    """Fait le test question 3-4."""
    base = list(range(n_max + 1))
    shuffled = func(base)
    counter = 1
    while shuffled != base:
        counter += 1
        shuffled = func(shuffled)
    return counter
# test_shuffle(52, _out_shuffle)
# Pour le out_shuffle, il faut 52 itérations pour revenir à la liste de départ.
# test_shuffle(52, _in_shuffle)
# Pour le in_shuffle, il suffit de 8 itérations.


def eras(n_max: int) -> typing.List[int]:
    """Effectue le crible d'Erastothème."""
    if n_max < 2:
        raise ValueError("n_max must be at least 2")
    i = 0
    primes = list(range(2, n_max + 1))
    while i < len(primes):
        temp = primes[i + 1:].copy()
        for elem in temp:
            if not elem % primes[i]:
                primes.remove(elem)
        i += 1
    return primes


def primes_3(n_max: int) -> typing.List[int]:
    """Third method for primes."""
    if n_max < 2:
        raise ValueError("n_max must be at least 2.")
    l_1 = list(range(2, n_max + 1))
    l_2 = [len([x for x in range(1, y + 1) if not y % x]) for y in l_1]
    return [elem for i, elem in enumerate(l_1) if l_2[i] == 2]
# Le directeur va libérer
# Les occupants de toutes les cellules qui ont un nombre impair de diviseurs
# C'est-à-dire les occupants des cellules dont le numéro est pas un carré parfait


def josephus(n: int, m: int) -> typing.List[int]:
    """Renvoie la permutation de Joséphus associée à n et m."""
    joseph = []
    cercle = [i + 1 for i in range(n)]
    curr = - 1
    while len(joseph) < n:
        for _ in range(m):
            curr = (curr + 1) % n
            while curr + 1 in joseph:
                curr = (curr + 1) % n
        joseph.append(cercle[curr])
    return joseph


def permutation(n: int) -> int:
    """Renvoie la n-ième permutation des chiffres."""
    curr = n
    total = ""
    chiffres = list(range(10))
    for i in range(10):
        quotient, curr = divmod(curr, factorial(9 - i))
        total += str(chiffres.pop(quotient))
    return int(total)
# 2783915604


def hamming(n: int) -> int:
    """Renvoie le n-ième nombre de Hamming."""
    hammings = [
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [2, 0, 0],
        [0, 0, 1],
        [1, 1, 0],
        [3, 0, 0],
        [0, 2, 0],
        [1, 0, 1],
        [2, 1, 0],
        [0, 1, 1],
        [4, 0, 0],
        [1, 2, 0],
        [2, 0, 1],
        [3, 1, 0],
        [0, 0, 2],
        [0, 3, 0],
    ]
    base, rest = divmod(n, 18)
    exponents = [base, base, base]
    exponents += hammings[rest]
    return 2 ** exponents[0] * 3 ** exponents[1] * 5 ** exponents[2]
# La suite est similaire toutes les 18 itérations, avec un facteur 30
# supplémentaire
# 91297581665113611259115979754590511595360241199911147000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
