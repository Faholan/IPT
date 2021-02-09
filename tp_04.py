"""TP du 16/11/2020.

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

from math import log

import numpy as np
import matplotlib.pyplot as plt


def trace_simple() -> None:
    """Tracé simple."""
    plt.figure()

    X = [np.cos(t) for t in range(20)]
    Y = [np.sin(t) for t in range(20)]

    plt.plot(X, Y)

    plt.show()


def trace_simple_2():
    """Tracé simple (2)."""
    plt.figure(figsize=(8, 8))

    X = [np.cos(t) for t in range(20)]
    Y = [np.sin(t) for t in range(20)]

    plt.plot(X, Y)

    plt.show()


def graphe():
    """Tracé de graphe simple."""
    plt.figure()

    X = np.linspace(-np.pi, np.pi, 256)

    C = [np.cos(x) for x in X]
    S = [np.sin(x) for x in X]

    plt.plot(X, C)
    plt.plot(X, S)

    plt.show()


def graphe_2():
    """Tracé de graphe simple (2)."""
    plt.figure()

    X = np.linspace(-np.pi, np.pi, 256)

    C = [np.cos(x) for x in X]
    S = [np.sin(x) for x in X]

    plt.plot(X, C, color="blue", linestyle="-", linewidth=2.5)
    plt.plot(X, S, color="red", linestyle="dashed")

    plt.show()


def graphe_label():
    """Tracé de graphe simple (label)."""
    plt.figure()

    X = np.linspace(-np.pi, np.pi, 256)

    C = [np.cos(x) for x in X]
    S = [np.sin(x) for x in X]

    plt.plot(X, C, color="blue", linestyle="-", label="cos")
    plt.plot(X, S, color="red", linestyle="dashed", label="sin")
    plt.legend(loc="upper left")

    plt.show()


def graphe_marker():
    """Tracé de graphe simple (marker)."""
    plt.figure()

    X = np.linspace(-np.pi, np.pi, 32)

    C = [np.cos(x) for x in X]
    S = [np.sin(x) for x in X]

    plt.plot(X, C, marker="o", linestyle="")
    plt.plot(X, S, marker="s", color="red")

    plt.show()


def graphe_marker_plus():
    """Tracé de graphe simple (marker+)."""
    plt.figure()

    X = np.linspace(-np.pi, np.pi, 32)

    C = [np.cos(x) for x in X]
    S = [np.sin(x) for x in X]

    plt.plot(X, C, marker="o", linestyle="")
    plt.plot(X, S, marker="s", color="red")

    plt.ylim(-1.1, 1.1)

    plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
    plt.yticks([-1, 0, 1])
    plt.grid()
    plt.title("Les fonctions cos et sin")

    plt.show()


def next_suite(mu: float, x: float) -> float:
    """Renvoie le prochain terme de la suite."""
    return mu * x * (1 - x)


def logistique1(mu: float, x0: float, n: int) -> None:
    """Trace le graphe de la figure 1."""
    terms = [x0]
    for _ in range(n):
        terms.append(next_suite(mu, terms[-1]))

    coords = list(range(n + 1))

    plt.figure()

    plt.plot(coords, terms, marker="o")

    plt.ylim(.1, 1)
    plt.xlim(0, n)
    plt.xticks([i for i in range(0, n + 1, 5)])
    plt.yticks([i / 10 for i in range(1, 11)])
    plt.grid()

    plt.title(f"mu = {mu}, x0 = {x0}, n = {n}")

    plt.show()


def logistique2(mu, x0, n):
    """Trace le graphe de la figure 2."""
    terms = [x0]
    for _ in range(n):
        terms.extend([next_suite(mu, terms[-1])] * 2)

    terms.pop()

    plt.figure()

    plt.plot(terms[:-1], terms[1:])

    coords = np.linspace(0, 1, 256)

    images = [next_suite(mu, i) for i in coords]

    plt.plot(coords, images)
    plt.plot(coords, coords)

    plt.ylim(0, 1)
    plt.xlim(0, 1)

    plt.xticks([i / 5 for i in range(6)])
    plt.yticks([i / 5 for i in range(6)])

    plt.title(f"mu = {mu}, x0 = {x0}, n = {n}")

    plt.show()

# a) oui
# b) effectivement
# Quand mu € [1, 2], on a toujours xi < mu pour i > 0
# Si mu € [2, 3], on peut avoir xi > mu
# Pour mu=3.05, on observe que la suite tend à devenir périodique
# pour mu=3.5, La suite diverge sans se stabiliser
# Pour mu=3.86, la divergence est encore plus marquée


def diagramme() -> None:
    """Trace le diagramme des bifurcations."""
    plt.figure(figsize=(8, 8))
    mu = 2.
    while mu <= 4:
        terms = [0.9]
        for _ in range(200):
            terms.append(next_suite(mu, terms[-1]))
        terms = terms[-100:]
        final = [terms[0]]
        for elem in terms[1:]:
            if abs(elem - final[-1]) > 10 ** -3:
                final.append(elem)

        plt.plot([mu] * len(final), final, marker=",", linestyle="")
        mu += 0.002

    plt.title("Diagramme des bifurcations")
    plt.yticks([i / 5 for i in range(6)])
    plt.xticks([2 + i / 2 for i in range(5)])
    plt.ylim(0, 1)
    plt.xlim(2, 4)
    plt.show()


def lyapunov(mu, x0, n):
    """Quantité de lyapunov."""
    total = 0
    x = x0
    for _ in range(n):
        total += log(abs(mu - 2 * mu * x))
        x = next_suite(mu, x)
    return total / n


def lgraphe(x0, n):
    """Graphe de lyapunov."""
    plt.figure()
    mus = np.linspace(3, 4, 256)
    terms = [lyapunov(mu, x0, n) for mu in mus]
    plt.plot(mus, terms)
    plt.show()
# Si l'exposant est négatif, le système se stabilise.
# Au contraire, si l'exposant est positif, les écarts s'amplifient.


def feigenbaum(n):
    """Calcule la constante de Feigenbaum (choisissez n grand).

    n = 10 ** 5 est une bonne valeur
    """
    mus = np.linspace(3.4, 4, 256)
    bifurcs = [3]
    for mu in mus:
        if len(bifurcs) == 6:
            break
