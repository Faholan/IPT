"""TP du 01/03/2021.

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
from math import exp
import typing

import matplotlib.pyplot as plt
import numpy as np

from scipy.integrate import odeint


X = np.linspace(0, 2, 21)


def f(y: float, x: float) -> float:
    """Equation différentielle."""
    return 2 * x * y ** 2


def meth_euler(
    equa: typing.Callable[[float, float], float],
    y0: float,
    coords: np.ndarray,
) -> typing.List[float]:
    """Méthode de résolution d'Euler."""
    final = [y0]
    for i in coords[:-1]:
        final.append(final[-1] + equa(final[-1], i) * (coords[1] - coords[0]))
    return final


def graphe(
    equa: typing.Callable[[float, float], float],
    y0: float,
    coords: np.ndarray,
) -> None:
    """Trace les deux graphes de odeint ainsi que d'Euler."""
    plt.figure()
    plt.plot(coords, meth_euler(equa, y0, coords), label="Euler")
    plt.plot(coords, odeint(equa, y0, coords), label="odeint")
    plt.legend(loc="upper left")
    plt.show()

# Plus il y a de points, plus la méthode d'Euler est proche de odeint
# Un point (sqrt(5)) ou la fonction n'est pas défini est traversé, entraînant des erreurs.


def f2(z: typing.Tuple[float, float], x: float) -> typing.Tuple[float, float]:
    """Equation différentielle d'ordre 2."""
    y, dy = z
    return dy, -dy + y + x ** 2 - 4 * np.sin(x)


def euler_2(
    equa: typing.Callable[
        [typing.Tuple[float, float], float],
        typing.Tuple[float, float]
    ],
    z0: typing.Tuple[float, float],
    coords: np.ndarray,
) -> typing.List[float]:
    """Méthode de résolution d'Euler - 2ème degré."""
    pas = coords[1] - coords[0]
    z = z0
    final = [z0[0]]
    for i in coords[:-1]:
        z2 = equa(z, i)
        z = (z[0] + z[1] * pas, z[1] + z2[1] * pas)
        final.append(z[0])
    return final


def graphe_2(
    equa: typing.Callable[
        [typing.Tuple[float, float], float],
        typing.Tuple[float, float]
    ],
    z0: typing.Tuple[float, float],
    coords: np.ndarray,
) -> None:
    """Graphe - Second ordre."""
    plt.figure()
    plt.plot(coords, euler_2(equa, z0, coords), label="Euler")
    plt.plot(coords, odeint(equa, z0, coords)[:, 0], label="odeint")
    plt.legend(loc="upper left")
    plt.show()


def f_instable(z: typing.Tuple[float, float], _: float) -> typing.Tuple[float, float]:
    """Equation différentielle instable."""
    y, dy = z
    return dy, 6 * y - dy


def graphe_theorie(
    equa: typing.Callable[
        [typing.Tuple[float, float], float],
        typing.Tuple[float, float]
    ],
    z0: typing.Tuple[float, float],
    coords: np.ndarray,
    func_theo: typing.Callable[[float], float]
) -> None:
    """Trace également la fonction théorique."""
    plt.figure()
    plt.plot(coords, euler_2(equa, z0, coords), label="Euler")
    plt.plot(coords, odeint(equa, z0, coords)[:, 0], label="odeint")
    plt.plot(coords, [func_theo(i) for i in coords], label="Théorie")
    plt.legend(loc="upper left")
    plt.show()
# X = np.linspace(0., 10., 101)
# graphe_theorie(f_instable, (2, -6), X, lambda t: 2 * exp(-3*t))
# Le graphe est extrêmement proche de la théorie. Pas de surprise ici.
# Sur [0, 20], la résolution à l'aide de odeint diverge fortement


EPSILON, OMEGA, DY0 = 1, 1, 0


def van_der_pol(z: typing.Tuple[float, float], _: float) -> typing.Tuple[float, float]:
    y, dy = z
    return dy, EPSILON * OMEGA * (1 - y ** 2) * dy - OMEGA ** 2 * y


def graphe_van_der(start: float, end: float, num: int) -> None:
    """Trace le graphe de van der pol."""
    coords = np.linspace(0, 30, 301)
    plt.figure()
    for y0 in np.linspace(start, end, num):
        plt.plot(
            coords,
            odeint(van_der_pol, (y0, DY0), coords)[:, 0],
            label=f"y(0)={y0}",
        )
    plt.legend(loc="upper left")
    plt.show()


def graphe_phase(start: float, end: float, num: int) -> None:
    """Trace le graphe de phases"""
    plt.figure()
    coords = np.linspace(0, 30, 301)
    for y0 in np.linspace(start, end, num):
        result = odeint(van_der_pol, (y0, DY0), coords)
        plt.plot(result[:, 0], result[:, 1], label=f"y0={y0}")
    plt.legend(loc="upper right")
    plt.show()


def chute(start: float, end: float, num: int, v0: float) -> None:
    """Trace les graphes de chute."""
    plt.figure()
    coords = np.linspace(0, 30, 301)
    g = 9.81
    for alpha in np.linspace(start, end, num):
        values = odeint(
            lambda z, t: (v0 * np.cos(alpha), v0 * np.sin(alpha) - g * t),
            (0, 0),
            coords
        )
        values = np.array([i for i in values if i[1] > 0])
        if len(values):
            plt.plot(values[:, 0], values[:, 1])
    plt.show()


def chute_2(
    start: float,
    end: float,
    num: int,
    v0: float,
    alpha: float,
) -> None:
    """Trace le graphe de chute avec des frottements."""
    plt.figure()
    coords = np.linspace(0, 30, 301)
    g = 9.81
    for k in np.linspace(start, end, num):
        def wrapped_x(val, _) -> typing.Tuple[float, float]:
            """Equation différentielle du mouvement en x."""
            _, dx = val
            return dx, -k * dx

        def wrapped_z(val, _) -> typing.Tuple[float, float]:
            """Equation différentielle du mouvement en z."""
            _, dz = val
            return dz, -g - k * dz
        values_x = odeint(
            wrapped_x,
            (0, v0 * np.cos(alpha)),
            coords,
        )
        values_z = odeint(
            wrapped_z,
            (0, v0 * np.sin(alpha)),
            coords,
        )
        values = np.array(
            [
                (values_x[i][0], values_z[i][0]) for i in range(len(values_z))
                if values_z[i][0] > 0
            ]
        )
        if len(values):
            plt.plot(values[:, 0], values[:, 1])
    plt.show()
