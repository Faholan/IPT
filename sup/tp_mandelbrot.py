"""All the work done on 28/09/2020 in IPT class.

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

import math

import numpy as np
import matplotlib.pyplot as plt


def graphe_tangente(f, fprime, x0: float, size: float = 10.0) -> None:
    """Display a function and its tangent."""

    coordx = np.linspace(x0 - size, x0 + size, 100)

    plt.figure()

    plt.plot(coordx, [f(x) for x in coordx], label="f", color="blue")

    plt.plot(
        coordx,
        [f(x0) + (x - x0) * fprime(x0) for x in coordx],
        label="f'",
        color="red"
    )

    plt.legend(loc="upper left")

    plt.show()


def graphe_ellipse(coef_x: float = 1.0, coef_y: float = 1.0) -> None:
    """Display (x/coef_x)² + (y/coef_y)² = 1."""
    theta = np.linspace(0, 2 * math.pi, 100)

    plt.figure()

    plt.plot(coef_x * np.cos(theta), coef_y * np.sin(theta))

    plt.show()


def graphe_polaire(
    base: float,
    thetamin: float = -10 * math.pi,
    thetamax: float = 0,
    points: int = 1000,
) -> None:
    """Display r = base^theta."""
    theta = np.linspace(thetamin, thetamax, points)

    plt.figure()

    plt.plot(
        [math.cos(t) * base ** t for t in theta],
        [math.sin(t) * base ** t for t in theta]
    )

    plt.show()


def suite(f, x0: float, n: int) -> list:
    """Return [x0, x1, ..., xn]."""
    result = [x0]
    for _ in range(n):
        result.append(f(result[-1]))
    return result


def graphe_suite(f, a: float, b: float, x0: float, n: int) -> None:
    """Plot the graphe."""
    base_points = suite(f, x0, n)
    points_plot = [(x0, x0)]
    for i in range(1, len(base_points)):
        points_plot.append((base_points[i - 1], base_points[i]))
        points_plot.append((base_points[i], base_points[i]))

    graphe_space = np.linspace(a, b, 100)

    plt.figure()

    plt.plot(*zip(*points_plot), color="red")
    plt.plot(graphe_space, graphe_space, color="blue")
    plt.plot(graphe_space, [f(x) for x in graphe_space], color="green")

    plt.show()


def _mandelbrot(base: complex, n: int):
    """Yield the Mandlebrot suite."""
    yield base
    current = base
    for _ in range(n):
        current = current ** 2 + base
        yield current


def inf2(base: complex, p: int) -> bool:
    """inf2 function."""
    for value in _mandelbrot(base, p):
        if abs(value) > 2:
            return False
    return True


def mandelbrot(
        n: int, p: int, size: float = 2.0, pointsize: float = 0.05) -> None:
    """Display Mandelbrot."""
    base = np.linspace(-size, size, n)
    points = []
    for real in base:
        for imaginary in base:
            if inf2(complex(real, imaginary), p):
                points.append((real, imaginary))

    plt.figure()

    plt.scatter(*zip(*points), s=pointsize, color="black")
    plt.show()
