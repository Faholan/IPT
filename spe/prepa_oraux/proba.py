"""Problème Python marche aléatoire - 24/05."""

from random import random


# Partie 1
def simul_exp(p: float, k: int) -> int:
    """Simulate the first experiment."""
    pos = 0

    while pos < k:
        if random() <= p:
            pos += 1
        pos += 1

    return 1 if pos == k else 0


def simul_100(p: float, k: int) -> tuple[float, float]:
    """Proportion of success."""
    return sum(simul_exp(p, k) for _ in range(100)) / 100, 1 / (p + 1)
