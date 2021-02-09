"""TP du 01/02/2021.

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
import typing

import numpy as np
import matplotlib.pyplot as plt


def dichotomie(
    func: typing.Callable[[float], float],
    inf: float,
    sup: float,
    epsilon: float,
) -> typing.Tuple[float, int]:
    """Recherche dichotomique de zéro."""
    assert inf != sup
    assert epsilon > 0
    if inf > sup:
        inf, sup = sup, inf
    im_1, im_2 = func(inf), func(sup)
    if im_1 * im_2 > 0:
        raise ValueError("f(inf) * f(sup) > 0")
    croissant = im_1 <= im_2
    if im_1 == 0:
        return inf, 0
    if im_2 == 0:
        return sup, 0
    counter = 1
    while sup - inf > epsilon:
        middle = (sup + inf) / 2
        _im = func(middle)
        if _im == 0:
            return middle, counter
        if _im < 0:
            if croissant:
                inf = middle
            else:
                sup = middle
        else:
            if croissant:
                sup = middle
            else:
                inf = middle
        counter += 1
    return (sup + inf) / 2, counter
# Pour f1, on trouve 1.414213562355144, pour une véritable valeur de
# 1.4142135623730951
# Pour f2, epsilon = 10**-3, on trouve -0.0001220703125.
# A 10**-13, on trouve 1.4210854715202004e-14


def prec_newton(
    func: typing.Callable[[float], float],
    dfunc: typing.Callable[[float], float],
    init: float,
    epsilon: float,
) -> typing.Tuple[float, int]:
    """Méthode de Newton."""
    first, second = float("inf"), init
    counter = 0
    while abs(first - second) > epsilon:
        first, second = second, second - func(second) / dfunc(second)
        counter += 1
    return second, counter
# Pour f1, on trouve 1.4142135623730951
# Véritable valeur : 1.4142135623730951
# Pour f2, précision de 10**-3 : 0.0015224388403474445
# Avec une précision de 10 ** -13 : 1.3974558270919528e-13


def iter_newton(
    func: typing.Callable[[float], float],
    dfunc: typing.Callable[[float], float],
    term: float,
    iters: int,
) -> float:
    """Méthode de Newton."""
    assert iters > 0
    for _ in range(iters):
        term = term, term - func(term) / dfunc(term)
    return term
# Cette fonction est relativement proche de la fonction de scipy.otimize.
# La principale différence est que la fonction de scipy implémente
# plusieurs méthodes :
# La méthode de Newton-Raphson (qui nous intéresse), la méthode de Halley
# Et la méthode sécante.
# En réduisant le code source à la partie pertinante, la fonction de scipy est


def scipy_newton(func, x0, fprime, tol=1.48e-8, maxiter=50):
    p0 = 1.0 * x0
    # Newton-Raphson method
    for itr in range(maxiter):
        # first evaluate fval
        fval = func(p0)
        # If fval is 0, a root has been found, then terminate
        if fval == 0:
            return p0
        fder = fprime(p0)
        if fder == 0:
            raise RuntimeError(
                f"Derivative was zero. (value is {p0} "
                f"after {itr + 1} iterations)"
            )
        newton_step = fval / fder
        p = p0 - newton_step
        if abs(p - p0) <= tol:
            return p
        p0 = p

    raise RuntimeError(
        f"Failed to converge after {itr + 1} iterations, value is {p}."
    )
# On voit bien que la méthode employée est la même.


def derive(
    func: typing.Callable[[float], float],
    val: float,
    step: float,
) -> float:
    """Renvoie une valeur approchée de la dérivée."""
    assert step != 0
    return (func(val + step) - func(val)) / step


def derive2(
    func: typing.Callable[[float], float],
    val: float,
    step: float,
) -> float:
    """Renvoie une valeur approchée de la dérivée."""
    assert step != 0
    return (func(val + step) - func(val - step)) / (2 * step)
# Avec un pas de 0.0001, derive atteint une précision de 5 * 10 ** -5,
# contre 2 * 10 ** -9 pour derive2
# derive2 est plus permormant.


def choix_de_h(
    func: typing.Callable[[float], float],
    dfunc: typing.Callable[[float], float],
    val: float,
) -> None:
    """Choix de h."""
    plt.figure()

    xvals = np.linspace(4, 8, 1000)
    yvals = [
        abs(dfunc(val) - derive2(func, val, 10 ** - step)) for step in xvals
    ]

    plt.plot(xvals, yvals)
    plt.show()
# Un choix optimal apparaît être 10 ** -5


def newton_derive(
    func: typing.Callable[[float], float],
    init: float,
    epsilon: float,
) -> typing.Tuple[float, int]:
    """Utilise derive2 pour calculer le zéro."""
    return prec_newton(
        func,
        lambda val: derive2(func, val, 10 ** -5),
        init,
        epsilon,
    )
# A une précision de 10 ** -13, les deux méthodes donnent le même résultat
# en 6 itérations : 1.414213562373095
# Pour 10 ** -9, les deux méthodes donne 1.4142135623730951 en 5 itérations
# Les performances sont identiques.


def secante(
    func: typing.Callable[[float], float],
    first: float,
    second: float,
    epsilon: float,
) -> typing.Tuple[float, int]:
    """Méthode de la sécante."""
    assert epsilon > 0
    assert first != second
    counter = 0
    while abs(first - second) > epsilon:
        first, second = second, first - func(
            first
        ) * (first - second) / (func(first) - func(second))
        counter += 1
    return second, counter
# Pour f1, on trouve 1.4142135623730951
# La valeur réelle : 1.4142135623730951
# Pour f2, précision à 10**-3 : -0.0030578316181607756
# Précision à 10 ** -13 : -2.9600077014861837e-13


def fausse_position(
    func: typing.Callable[[float], float],
    inf: float,
    sup: float,
    epsilon: float,
) -> typing.Tuple[float, int]:
    """Méthode de la fausse position."""
    assert inf != sup
    assert epsilon > 0
    if inf > sup:
        inf, sup = sup, inf
    im_1, im_2 = func(inf), func(sup)
    if im_1 * im_2 > 0:
        raise ValueError("f(inf) * f(sup) > 0")
    croissant = im_1 <= im_2
    middle = sup - func(sup) * (sup - inf) / (func(sup) - func(inf))
    counter = 1
    while func(middle + epsilon) * func(middle - epsilon) > 0:
        if croissant:
            if func(middle) > 0:
                sup = middle
            else:
                inf = middle
        else:
            if func(middle) > 0:
                inf = middle
            else:
                sup = middle
        middle = sup - func(sup) * (sup - inf) / (func(sup) - func(inf))
        counter += 1
    return middle, counter
# Pour f1, on a: 1.4142135623189167
# Vraie valeur : 1.4142135623730951
# Pour f3, on trouve -0.0009999993577245458
# Cependant, cette performance requière 498997 itérations.
# Cette méthode ne semble donc pas très efficace.
