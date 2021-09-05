# -*- coding: utf-8 -*-
"""
Created on Sun Apr 03 23:08:38 2016.

@author: herve
"""

# from random import random
import typing as t
# from scipy.integrate import quad
import matplotlib.pyplot as plt
# from math import exp, tan, pi, sqrt


def methode_1(
    func: t.Callable[[float], int],
    a: float,
    b: float,
    n: int,
) -> float:
    """Première méthode de calcul d'une intégrale."""
    integrale = 0
    x = a
    pas = (b-a)/n
    for _ in range(n):
        integrale += func(x)
        x += pas
    return integrale*pas


def methode_2(
    func: t.Callable[[float], float],
    a: float,
    b: float,
    n: int,
) -> float:
    """Deuxième méthode de calcul d'une intégrale."""
    integrale = 0.
    pas = (b - a)/n
    x = a + pas
    for _ in range(n):
        integrale += func(x)
        x += pas
    return integrale*pas


def methode_3(
    func: t.Callable[[float], float],
    a: float,
    b: float,
    n: int,
) -> float:
    """Troisème méthode de calcul d'une intégrale."""
    integrale = 0.
    pas = (b-a)/n
    x = a + pas/2
    for _ in range(n):
        integrale += func(x)
        x += pas
    return integrale*pas


def methode_4(
    func: t.Callable[[float], float],
    a: float,
    b: float,
    n: int,
) -> float:
    """Quatrième méthode de calcul d'une intégrale."""
    integrale = func(a) + func(b)
    pas = (b-a)/n
    x = a + pas
    for _ in range(n-1):
        integrale += 2*func(x)
        x += pas
    return integrale*(b - a)/(2*n)


def methode_5(
    func: t.Callable[[float], float],
    a: float,
    b: float,
    n: int,
) -> float:
    """Cinquième méthode de calcul d'une intégrale."""
    integrale = 0.
    pas = (b - a)/(2*n)
    valgauche = func(a)
    x = a
    for _ in range(n):
        x += pas
        integrale += valgauche + 4*func(x)
        x += pas
        valgauche = func(x)
        integrale += valgauche
    return integrale*pas/3


def graphe(
    func: t.Callable[[float], float],
    a: float,
    b: float,
    n: int,
) -> t.Tuple[t.List[float], t.List[float]]:
    """Affiche le graphe d'une fonction."""
    abscisse = []
    ordonne = []
    x = a
    pas = (b-a)/n
    for _ in range(n+1):
        abscisse.append(x)
        ordonne.append(func(x))
        x += pas
    plt.plot(abscisse, ordonne)
    plt.show()
    return abscisse, ordonne
