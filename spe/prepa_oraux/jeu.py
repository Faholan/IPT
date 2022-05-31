"""Les joueurs."""

from random import randint


def gains(n: int, N: int, S: float) -> list[float]:
    """Calcule les gains de chaque joueur."""
    prev_correcte: list[int] = []
    max_prev = 0

    correct = [randint(0, 1) for _ in range(N)]

    for i in range(n):
        prev = 0
        for k in range(N):
            if randint(0, 1) == correct[k]:
                prev += 1

        if prev == max_prev:
            prev_correcte.append(i)
        elif prev > max_prev:
            prev_correcte = [i]
            max_prev = prev

    gain_par = S / len(prev_correcte)

    return [gain_par if i in prev_correcte else 0 for i in range(n)]


def gain_moyen(n: int, N: int, S: float, nb_part: int) -> list[float]:
    """Gain moyen sur un nb de parties."""
    res = [0. for _ in range(n)]
    for _ in range(nb_part):
        for i, e in enumerate(gains(n, N, S)):
            res[i] += e

    return [e / nb_part for e in res]
