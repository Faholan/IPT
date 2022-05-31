"""Sujet d'algèbre linéaire."""

import numpy as np
from random import randint
import typing as t


def gen_j(n: int) -> t.Any:
    """Generate Jn."""
    return np.array([
        [
            1 if j == n - i - 1 else 0
            for j in range(n)
        ]
        for i in range(n)
    ])


def rand_matrix(n: int, p: int) -> t.Any:
    """Generate a random nxp matrix."""
    return np.array([
        [
            randint(0, 99)
            for _ in range(p)
        ]
        for _ in range(n)
    ])


def centro(a: t.Any) -> t.Any:
    """Calcule la centro-transposée de A."""
    return np.array([
        [
            a[-i - 1][-j - 1]
            for j in range(len(a[-i - 1]))
        ]
        for i in range(len(a))
    ])


def test_jn(n: int) -> None:
    """Test the hypothesis."""
    a = rand_matrix(n, n)
    b = centro(a)
    j = gen_j(n)
    assert np.all(j @ a @ j == b)


def decompose(m: t.Any) -> t.Tuple[t.Any, t.Any, t.Any, t.Any]:
    """Decompose."""
    s = (m + np.transpose(m)) / 2
    a = (m - np.transpose(m)) / 2
    return (s + centro(s)) / 2, (s - centro(s)) / 2, (a + centro(a)) / 2, (a - centro(a)) / 2


def gen_q(n: int) -> t.Any:
    """Gen Qn."""
    id_mat = np.zeros((n, n), int)
    for i in range(n):
        id_mat[i][i] = 1

    j = gen_j(n)
    return np.block([[id_mat, -j], [j, id_mat]])
