"""MIT License

Copyright (c) 2021 Faholan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from time import time

from matplotlib.pyplot import plot, show


def syracuse(term: int) -> int:
    """Get the next term."""
    return 3 * term + 1 if term % 2 else term // 2


def tempsdevol(term: int) -> int:
    """Get the flight time of an integer."""
    counter = 0
    while term != 1:
        counter += 1
        term = syracuse(term)
    return counter


def altitude(term: int) -> int:
    """Renoive l'altitude maximale d'un entier."""
    alt = term
    while term != 1:
        if term > alt:
            alt = term
        term = syracuse(term)
    return alt


def tempsdarret(start: int) -> int:
    """Renvoie le temps d'arrêt de u."""
    counter = 0
    current = start
    while current >= start:
        counter += 1
        current = syracuse(current)
    return counter


def verification(total: int) -> float:
    """Renvoie le temps nécessaire pour vérifier les valeurs c de 2 à m."""
    start = time()
    for i in range(2, total + 1):
        tempsdarret(i)
    return time() - start


# On obtient un temps de 1.2 s pour m = 10**6

# Le temps d'arrêt d'un entier pair est de 1, car u1 = u0 / 2 < u0

# Pour u0 = 4n + 1
# u1 = 12n + 4
# u2 = 6n + 2
# u3 = 3n + 1 < u0
# Donc le temps d'arrêt pour un entier de la forme 4n + 1 vaut 3.
# 4n + 2 est pair, et donc seul le cas 4n + 3 est intéressant (on peut se rapporter à un des cas 4n, 4n + 1, 4n + 2 et 4n + 3 quel que soit l'entier de départ.)
def verification_2(total: int) -> float:
    """Verification - version 2."""
    start = time()
    for i in range(3, total + 1, 4):
        tempsdarret(i)
    return time() - start
# On gagne 0.4s par rapport à la fonction précédente
# On vérifie en 10s l'hypothèse pour m = 10 ** 7


def altitude_max(total: int) -> tuple:
    """Renvoie l'altitude max atteinte pour i <= m."""
    alt = 1
    i_max = 1
    for i in range(2, total + 1):
        term = i
        while term >= i:  # Sinon on se ramène à un cas déjà traité
            if term > alt:
                alt = term
                i_max = i
            term = syracuse(term)
    return i_max, alt
# On obtient (704511, 56991483520)
# L'altitude maximale atteinte vaut 56991483520 pour c = 704511


def temps_max(total: int) -> float:
    """Verification - version 2."""
    tps = 1
    i_tps = 1
    for i in range(3, total + 1, 4):
        curr = tempsdarret(i)
        if curr > tps:
            tps = curr
            i_tps = i
    return i_tps, tps
# On obtient (626331, 287) : Un temps de vol de 287 pour i=626331


def duree_record(total: int) -> float:
    """Renvoie la durée record ainsi que l'index correspondant."""
    indexes = [1, 2]
    curr_max = 1  # 1 et 2 sont des vols en altitude de durée record
    for i in range(3, total + 1, 4):
        curr = tempsdarret(i)
        if curr > curr_max:
            curr_max = curr
            indexes.append(i)
    return indexes
# [1, 2, 3, 7, 27, 703, 10087, 35655, 270271, 362343, 381727, 626331]


def graphique(start: int) -> None:
    """Show the graph."""
    display = [start]
    term = start
    while term > 1:
        term = syracuse(term)
        display.append(term)
    plot(display)
    show()


# On sait déjà qu'on a besoin de considérer uniquement les entiers de la forme
# 16n + 7, 16n + 11 et 16n + 15
# On peut ignorer un terme si, en un nombre faible d'étapes, on arrive à
# revenir à un entier plus petit
def check_5(rep: int) -> list:
    """Partie 5."""
    total = [i for i in range(7, 2 ** 16) if i % 16 in (7, 11, 15)]
    counter = 0
    for k in total:
        a, b = 65536, k  # u = a*n + b
        test = True
        for _ in range(rep):
            if b % 2:
                a *= 3
                b = 3 * b + 1
            else:
                a //= 2
                b //= 2
            if (a <= 65536 and b < k) or (a < 65536 and b <= k):
                # Terme plus petit que le terme initial
                test = False
                break
        if test:
            counter += 1
    return counter
# En acceptant 10 itérations, on trouve 8192 k possibles. (12, 5 %)
# En montant à 100 itérations, on trouve 114 k possibles. (0.17 %)
