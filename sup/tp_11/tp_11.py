"""All the work done on 15/03/2021 in IPT class.

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

from math import exp, pi, sqrt, tan
from random import uniform
import typing as t

from scipy.integrate import quad

from enonce import methode_5


def func(x: float) -> float:
    """Process the function studied."""
    return exp(-x**2/2)
# Avec quad, on obtient 0.855624391892149
# Avec la méthode 1, on obtient 0.8621260519038276
# Avec la méthode 2, on obtient 0.849010407227582
# Avec la méthode 3, on obtient 0.8556524738354515
# Avec la méthode 4, on obtient 0.8555682295657049
# Avec la méthode 5, on obtient 0.8556243924122028
# Les 5 méthodes donnent bien environ le même résultat


def rang_necessaire(
    fun: t.Callable[[float], float],
    a: float,
    b: float,
    err: float,
    methode: t.Callable[[t.Callable[[float], float], float, float, int], float]
) -> int:
    """Détermine le rang nécessaire pour atteindre l'erreur requise."""
    ref = quad(fun, a, b)[0]
    diff = rang = 100000
    while diff > 0:
        if rang != 0:
            while abs(methode(fun, a, b, rang) - ref) >= err:
                rang += diff
            rang -= diff
        diff //= 10
        rang += diff
    return rang + 1
# Pour la méthode du point milieu à 10**-8 près, il faut aller au rang 1590.
# Pour la méthode du point milieu à 10**-10 près, il faut pousser au rang 15895.
# Pour la méthode des trapèzes à 10**-8 près, il faut pousser au rang 2249.
# Pour la méthode des trapèzes à 10**-10 près, il faut pousser au rang 22481
# Pour la méthode de Simpson à 10**-8 près, il faut pousser au rang 15
# Pour la méthode de Simpson à 10**-10 près, il faut pousser au rang 46
# Pour la méthode de Simpson à 10**-12 près, il faut pousser au rang 144


def φ(x: float) -> float:
    """Calcule la fonction φ."""
    return methode_5(func, 0, x, 100)


def φ_tan(y: float) -> float:
    """Calcule φ avec le changement de variable t = tan(y)."""
    return exp(-tan(y)**2/2)*(1 + tan(y)**2)

# On trouve 2.5066282746133557
# Valeur théorique : 2.5066282746310002
# Le résultat est extrêmement proche.


def monte_carlo(
    fun: t.Callable[[float], float],
    a: float,
    b: float,
    n: int,
) -> float:
    """Méthode de Monte-Carlo, version 1."""
    total = 0.
    for _ in range(n):
        total += fun(uniform(a, b))
    return (b - a) * total / n


def rang_necessaire_m(
    fun: t.Callable[[float], float],
    a: float,
    b: float,
    err: float,
) -> int:
    """Nombre de tirages nécessaires pour la méthode de Monte-Carlo."""
    n = 1
    value = monte_carlo(fun, a, b, n)
    ref = quad(fun, a, b)[0]
    while abs(ref - value) > err:
        n += 1
        value = monte_carlo(fun, a, b, n)
    return n


def rang_necessaire_moyenne(
    fun: t.Callable[[float], float],
    a: float,
    b: float,
    err: float,
    essais: int,
) -> float:
    """Nombre nécessaires de tirages en moyenne."""
    total = 0
    for _ in range(essais):
        total += rang_necessaire_m(fun, a, b, err)
    return total / essais
# Il faut en moyenne 164 tirages pour parvenir à trouver une valeur.


def π(essais: int) -> float:
    """Détermine une valeur approchée de pi."""
    total = 0
    for _ in range(essais):
        if uniform(0, 1)**2 + uniform(0, 1)**2 <= 1:
            total += 1
    return 4 * total / essais  # La surface vaut environ π/4 (1/4 de cercle)
# On obtient 3.14 pour π(1000)


def boule(essais: int) -> float:
    """Détermine une valeur approchée du volume d'une boule."""
    total = 0
    for _ in range(essais):
        if uniform(0, 1)**2 + uniform(0, 1)**2 + uniform(0, 1)**2 <= 1:
            total += 1
    return 8 * total / essais
# On obtient 4.344
# Valeur théorique : 4.1887902047863905


def suite(a1: float, fun: t.Callable[[float], float], n: int):
    """Yield la suite."""
    a = 0.
    b = a1
    for _ in range(n):
        yield b
        a, b = b, b + (fun(a) * fun(b) - fun(b) ** 2) / b
    yield 1


def calc(a1: float, fun: t.Callable[[float], float], n: int) -> float:
    """Optimisation de la division."""
    a = 0
    total = 0
    for x in suite(a1, fun, n):
        total += (x - a) * fun(a)
        a = x
    return total


def approximation(essais: int, fun, n: int) -> float:
    """Optimisation de la division."""
    a, b = 0., 1.
    c_a, c_b = calc(a, fun, n), calc(b, fun, n)
    obj = pi/4
    for _ in range(essais):
        m = (a + b)/2
        if calc(m, fun, n) >= obj:
            pass
