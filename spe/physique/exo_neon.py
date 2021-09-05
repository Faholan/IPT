"""Graphe de l'exo sur les néons.

Copyright (C) 2021  Faholan <https://github.com/Faholan>
"""

from math import exp
import typing as t

import matplotlib.pyplot as plt


def get_points(
    num: int,
    step: float,
    e: float,
    r: float,
    c: float,
    ra: float,
    ua: float,
    ue: float
) -> t.Iterable[t.Tuple[bool, t.List[float], t.List[float]]]:
    """Get the tuple (off, on)."""
    current: t.Tuple[bool, t.List[float], t.List[float]] = (False, [], [])
    initial = True
    t0 = 0.

    tau1 = r * c
    tau2 = c / (1 / r + 1 / ra)
    e2 = e / (1 + r / ra)

    def fun_1(time: float) -> float:
        """First function."""
        return e * (1 - exp(-time / tau1))

    def fun_2(t0: float, time: float) -> float:
        """Second function."""
        return (ua - e2) * exp((t0 - time) / tau2) + e2

    def fun_3(t0: float, time: float) -> float:
        """Third function."""
        return (ue - e) * exp((t0 - time) / tau1) + e

    for i in range(num):
        time = i * step
        if initial:
            u = fun_1(time)
            if u > ua:
                yield current
                current = (True, [u], [time])
                t0 = time
                initial = False
            else:
                current[1].append(u)
                current[2].append(time)
        elif current[0]:
            u = fun_2(t0, time)
            if u < ue:
                yield current
                current = (False, [u], [time])
                t0 = time
            else:
                current[1].append(u)
                current[2].append(time)
        else:
            u = fun_3(t0, time)
            if u > ua:
                yield current
                current = (True, [u], [time])
                t0 = time
            else:
                current[1].append(u)
                current[2].append(time)
    yield current


def graphique(
    num: int,
    step: float,
    e: float,
    ua: float,
    ue: float,
    r: float,
    ra: float,
    c: float,
) -> None:
    """Display the graph."""
    plt.figure()
    for status, points, times in get_points(num, step, e, r, c, ra, ua, ue):
        plt.plot(times, points, color=("green" if status else "red"))

    plt.show()
