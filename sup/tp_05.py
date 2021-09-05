"""TP du 23/11/2020.

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
from math import floor, log, sqrt
import typing


def troots(a: float, b: float, c: float) -> typing.Tuple[float]:
    """Renvoie les racines du trinôme."""
    delta = b ** 2 - 4 * a * c
    if delta < 0:
        return ()
    if delta == 0:
        return (-b / (2 * a),)
    return (-b - sqrt(delta)) / (2 * a), (-b + sqrt(delta)) / (2 * a)
# La fonction renvoie un singleton pour (1, 6, 9)
# Et None pour (.1, .6, .9)


def troots_2(a: float, b: float, c: float) -> typing.Tuple[float]:
    """Renvoie les racines du trinôme (en mieux)."""
    coef = max((-floor(log(i, 10)) for i in (a, b, c)))
    return troots(*(i * 10 ** coef for i in (a, b, c)))
# troots renvoie -0.5000000000000004 pour ces valeurs
# delta = (1 + 2**-50)**2 - 4*(0.25 + 2**-51)
# delta = 1 + 2**-49 + 2**-100 - 1 - 2**-49
# delta = 2 ** -100 = (2 ** -50) ** 2
# x1 = (-1 - 2 ** -50 - 2 ** -50)/2 = -1/2 - 2**-50
# x2 = (-1 - 2** -50 + 2 ** -50)/2 = -1/2
# L'écart entre les deux racines théoriques et la racine unique calculée
# Est due au stockage de 2 ** -100, arrondi en 0
# u_n = 2 ** (n-1) * 2 * sin(pi/2**n)


def approx_pi(n: int) -> typing.List[typing.Tuple[float]]:
    """Approxime pi (n récursions)."""
    assert isinstance(n, int) and n >= 0
    terms = [(2 * sqrt(2), 4)]
    for _ in range(n):
        u, v = terms[-1]
        v = (2 * u * v) / (u + v)
        terms.append((sqrt(u * v), v))
    return terms
# Il devient inutile de poursuivre l'itération à partir du rang 26.
# a2 = floor(10 ** 200 * u2) <= 10 ** 200 * u2
# b2 = ceil(10 ** 2 * u2) >= 10 ** 200 * u2


def _floor(x: int, y: int) -> int:
    return x // y


def _ceil(x: int, y: int) -> int:
    return x // y + (1 if x % y else 0)


def g(a: float, x: float) -> float:
    """Calcule g_a(x)."""
    return (x + a / x) / 2
# Supposons par l'absurde que n n'existe pas.
# Soit N le point en lequel le minimum de rn est atteint.
# rN+1 = floor((rN + a / rN) / 2)
# On a rN > sqrt(a)
# rN+1 < floor(rN + sqrt(a) / 2)
# rN+1 < floor(rN)
# rN+1 < rN
# Il existe donc n tel que rn <= sqrt(a)


def _fsqrt(a: int) -> int:
    r = 10 ** ((len(str(a)) + 1) // 2)
    sqr = r ** 2
    while sqr > a:
        r = (sqr + a) // (2 * r)
        sqr = r ** 2
    return r


def _csqrt(a: int) -> int:
    r = _fsqrt(a)
    if r ** 2 == a:
        return r
    return r + 1


def _encadr(a, b, c, d):
    _b = _floor(2 * a * b, a + b)
    _d = _ceil(2 * c * d, c + d)
    return (_fsqrt(a * _b), _b, _csqrt(c * _d), _d)


def encadr():
    """Renvoie un encadrement de 10**200 * pi."""
    a = _fsqrt(8 * 10 ** 400)
    b = 4 * 10 ** 200
    c = _csqrt(8 * 10 ** 400)
    d = 4 * 10 ** 200
    n = 2

    _a, _b, _c, _d = _encadr(a, b, c, d)
    while (a, b, c, d) != (_a, _b, _c, _d):
        n += 1
        a, b, c, d = _a, _b, _c, _d
        _a, _b, _c, _d = _encadr(a, b, c, d)
    return n, a, d
# Cet encadrement fournit 196 décimales exactes en 335 itérations
