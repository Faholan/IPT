"""Exercice de Centrale - 07/06/2022."""
from functools import cache
from math import sqrt
import random
import typing as t

import numpy as np
from matplotlib import pyplot as plt


# n°969
@cache
def calc_m(n: int) -> int:
    """Calculate the value of Mn."""
    if n in (0, 1):
        return 1

    return calc_m(n - 1) + sum(calc_m(k) * calc_m(n - k - 2) for k in range(n - 2))


# n°967


def calc_an(n: int) -> float:
    """Calculate the value of an."""
    if n == 0:
        return 1.0

    a = b = 1

    for k in range(n):
        a *= 2 * k + 1
        b *= 2 * (k + 1)

    return a / b


def calc_an_2(n: int) -> float:
    """Calculate the value of 1 / (n * an²)."""
    return 1 / (n * calc_an(n) ** 2)


# On remarque que cette valeur tend vers pi


def plot_an(n_max: int) -> None:
    """Plot the graphe of an."""
    plt.plot(
        tuple(range(n_max)),
        tuple(calc_an(n) for n in range(n_max)),
        color="red",
        ls="",
        marker="+",
    )

    x_range = np.arange(0, n_max, n_max / 1000)

    plt.plot(x_range, tuple(1 / sqrt(2 * x + 1) for x in x_range), color="green")
    plt.show()


# n° 987


def calculate_pi(n: int, p: t.Callable[[int], float]) -> float:
    """Calculate pin."""
    pi_tot = 0
    for _ in range(1000):
        x = 0
        for k in range(n):
            if p(k) >= random.random():
                x += 1
        if x % 2 == 0:
            pi_tot += 1

    return pi_tot / 1000


def proba_1(n: int) -> float:
    """First probability law."""
    return 1 / (2 * (n + 1) ** 2)


def proba_2(n: int) -> float:
    """The Second Law."""
    return 1 / (2 * (n + 1))


def proba_3(n: int) -> float:
    """Third probability law."""
    return 1 / (2 * sqrt(n + 1))


def plot_pi_100() -> None:
    """Plot the pi function."""

    x_range = tuple(range(1, 101))

    colors = ("red", "green", "blue")

    for proba, color in zip((proba_1, proba_2, proba_3), colors):
        plt.plot(
            x_range,
            tuple(calculate_pi(n, proba) for n in x_range),
            color=color,
            marker="+",
        )

    plt.show()


def plot_pi(n_max: int) -> None:
    """Plot the pi function."""

    plt.plot(
        tuple(range(1, n_max + 1)),
        tuple(calculate_pi(n + 1, proba_1) for n in range(n_max)),
    )

    plt.show()
