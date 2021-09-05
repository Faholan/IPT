"""All the work done on 19/03/2021 in IPT class.

MIT License

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
import typing

import numpy as np


def recherche_pivot_max(terms: np.ndarray, i: int) -> int:
    """Recherche du pivot maximal."""
    cur, index = abs(terms[i][i]), i
    for j in range(i+1, len(terms)):
        if abs(terms[j][i]) > cur:
            cur = abs(terms[j][i])
            index = j
    return index


def echange_ligne(terms: np.ndarray, i: int, j: int) -> None:
    """Echange deux lignes."""
    terms[i], terms[j] = np.copy(terms[j]), np.copy(terms[i])


def transvection(terms: np.ndarray, i: int, j: int, mu: float) -> None:
    """Transvection."""
    terms[j] += mu * terms[i]


def triangularisation(terms: np.ndarray, constants: np.ndarray) -> None:
    """Triangularisation du système."""
    for i in range(len(terms) - 1):
        j = recherche_pivot_max(terms, i)
        echange_ligne(terms, i, j)
        echange_ligne(constants, i, j)
        for j in range(i + 1, len(terms)):
            mu = -terms[j][i] / terms[i][i]
            transvection(terms, i, j, mu)
            transvection(constants, i, j, mu)


def remontee(terms: np.ndarray, constants: np.ndarray) -> typing.List[float]:
    """Effectue la remontée."""
    sols = [0. for _ in range(len(constants))]
    for i in range(len(terms) - 1, -1, -1):
        for j in range(i + 1, len(terms)):
            constants[i][0] -= terms[i][j] * sols[j]
        sols[i] = constants[i][0] / terms[i][i]
    return [round(i, 7) for i in sols]


def gauss(terms: np.ndarray, constants: np.ndarray) -> typing.List[float]:
    """Algorithme du pivot de Gauss."""
    terms = np.copy(terms) * 1.
    constants = np.copy(constants) * 1.
    triangularisation(terms, constants)
    return remontee(terms, constants)


# D'après la loi des mailles :
# R1 * i1 + R2 * i2 = E
# R1 * i1 + R3 * i3 + R4 * i4 = E
# R1 * i1 + R3 * i3 + (R5+R6) * i5 = E
# D'après la loi des noeuds :
# -i1 +i2 +i4 +i5 = 0
# i3 -i4 -i5 = 0


def reseau_elec(
    e: float,
    r1: float,
    r2: float,
    r3: float,
    r4: float,
    r5: float,
    r6: float,
) -> typing.List[float]:
    """Calcule les différents courants."""
    return gauss(
        np.array(
            [
                [r1, r2, 0, 0, 0],
                [r1, 0, r3, r4, 0],
                [r1, 0, r3, 0, r5 + r6],
                [-1, 1, 0, 1, 1],
                [0, 0, 1, -1, -1],
            ]
        ),
        np.array([[e], [e], [e], [0], [0]])
    )
# [0.0222743, 0.0126026, 0.0096717, 0.0064478, 0.0032239]

# T1 - mg = -m*rw (PFD à m1)
# T2 - mg = m*rw (PFD à m2)
# Jw = T1R - T2R (TMC à la roue)


GRAVITE = 9.81  # g = 9.81 m/s²


def poulie(inertie: float, masse: float, rayon: float) -> typing.List[float]:
    """Résoud l'équation de la poulie."""
    return gauss(
        np.array(
            [
                [1, 0, rayon*masse],
                [0, 1, -rayon*masse],
                [-rayon, rayon, inertie],
            ]
        ),
        np.array([[masse*GRAVITE], [masse*GRAVITE], [0]])
    )
