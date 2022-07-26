"""Troisième partie des exos."""

import math
from random import randint
from typing import List, Union

import matplotlib.pyplot as plt

EPSILON = 1e-8
Number = Union[int, float]


def distance(t: Number, x: Number) -> float:
    """Calculate the distance."""

    return math.sqrt((x - 0.5) ** 2 + math.exp(-2 * t * x))


def phi(t: Number, x: Number) -> float:
    """Dérivée de distance²."""
    return 2 * x - 1 - 2 * t * math.exp(-2 * t * x)


def zero(t: Number, epsilon: Number) -> float:
    """Find the minimum."""

    a, b = 0.5, 1.0

    while b - a > epsilon:
        x = (b + a) / 2

        if phi(t, x) < 0:
            a = x
        else:
            b = x

    return (a + b) / 2


def plot_til(k_max: int) -> None:
    """Plot the thingy."""

    x_coord: List[int] = []
    y_coord: List[float] = []

    for k in range(k_max):
        x_coord.append(k + 1)
        y_coord.append(zero(k + 1, EPSILON))

    plt.plot(x_coord, y_coord)
    plt.show()


def partial_sum(n_max: int) -> float:
    """Calculate the sum of un - l."""

    return sum(zero(k + 1, EPSILON) - 0.5 for k in range(n_max))


# Exercice 986
def jeu(n: int, q: int) -> bool:
    """Simulation du jeu."""
    depart = n
    pont = arrivee = 0

    while True:
        jet = randint(1, 6)

        if jet in {1, 6}:
            q -= 1
            if q == 0:
                return False
        elif jet in {2, 5}:
            if depart != 0:
                depart -= 1
                pont += 1
        else:
            if pont != 0:
                pont -= 1
                arrivee += 1
                if arrivee == n:
                    return True


def simulate(n: int, q: int, repet: int) -> float:
    """Evaluate pn,q."""

    return sum(jeu(n, q) for _ in range(repet)) / repet
