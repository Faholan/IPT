"""Exos Python Centrale - 31/05."""
from functools import cache

import numpy as np
from numpy import linalg as alg

# Numéro 899


def pgcd(a: int, b: int) -> int:
    """Calculate the GCD."""
    if b > a:
        # pylint: disable=arguments-out-of-order
        return pgcd(b, a)

    if b < 0:
        return pgcd(abs(a), abs(b))

    if b == 0:
        return a

    r = a % b
    if r == 0:
        return b

    return pgcd(b, r)


@cache
def phi(n: int) -> int:
    """Calculate the phi function."""
    if n <= 0:
        return 0
    if n == 1:
        return 1

    if n % 2:
        return phi(n // 2) + phi((n + 1) // 2)

    return phi(n // 2)


def test_vals_phi() -> None:
    """Test the PGCD for different values of n."""
    print(tuple(pgcd(phi(i), phi(i + 1)) for i in range(100)))


def inv_phi(a: int, b: int) -> int:
    """Inverse the phi function."""
    if (a, b) == (0, 1):
        return 0

    if a < b:
        n = inv_phi(a, b - a)
        return 2 * n

    n = inv_phi(a - b, b)
    return 2 * n + 1


def test_inv_phi() -> None:
    """Test phi's inverse function."""
    for i in range(1000):
        assert i == inv_phi(phi(i), phi(i + 1))


# Exercice 934


MAT_A = np.array(
    [
        [0, 2, 1, -1],
        [2, 0, 0, 0],
        [1, 0, 0, -1],
        [-1, 0, -1, 1],
    ],
    dtype=int,
)


VALS, VECTS = alg.eig(MAT_A)


def verifunitaire(mat) -> None:
    """Vérification de l'unicité des vecteurs."""
    for i in range(len(mat[0])):
        x = mat[:, i]
        print(np.dot(x, x))
        # Passed


V = np.array(
    [
        [1],
        [1],
        [1],
        [1],
    ]
)


def verif2(mat) -> None:
    """Vérifie les valeurs propres de A + U1VT."""
    for i in range(len(mat[0])):
        vector = mat[:, i]
        column = np.reshape(vector, (len(vector), 1))

        mat_b = MAT_A + np.dot(column, np.transpose(V))

        print(alg.eigvals(mat_b))
