"""TD rayons."""

import math
import typing as t

import numpy as np

Point = t.Any  # np.ndarray 3x1
Vector = t.Any  # np.ndarray 3x1
Rayon = t.Tuple[Point, Vector]
Sphere = t.Tuple[Point, float]


def vec(a: Point, b: Point) -> Vector:
    """Return the vector from a to b."""
    return b - a


def ps(v1: Vector, v2: Vector) -> float:
    """Return the scalar product of v1 and v2."""
    return np.inner(v1, v2)  # type: ignore


def norme(v: Vector) -> float:
    """Return the norm of v."""
    return math.sqrt(ps(v, v))


def unitaire(v: Vector) -> Vector:
    """Return the unit vector of v."""
    return v / norme(v)


# Question 5
# La fonction pt renvoie le point du rayon situé à distance t de son origine.
# La fonction dir renvoie la direction du rayon.
# La fonction ra renvoie le rayon AB.


def pt(rayon: Rayon, pos: float) -> Point:
    """Return the point of the rayon at distance t from its origin."""
    assert pos >= 0
    return rayon[0] + rayon[1] * pos


def dir_(a: Point, b: Point) -> Vector:
    """Return the direction of the rayon from a to b."""
    return unitaire(vec(a, b))


def ra(a: Point, b: Point) -> Rayon:
    """Return the rayon from a to b."""
    return a, dir_(a, b)


def sp(a: Point, b: Point) -> Sphere:
    """Return the sphere from a to b."""
    return a, norme(vec(a, b))


# Question 7
# M = A + tu € Sphere <=> ||CM|| == r
# ||CA + tu||² = r²
# ||CA||² + ||tu||² + 2CA.tu = r²
# t² - r² + 2t(u.CA) + ||CA||² = 0


def intersection(rayon: Rayon, sphere: Sphere) -> t.Optional[t.Tuple[Point, float]]:
    """Renvoie le premier point de la sphère frappé par le rayon.

    :param rayon: rayon considéré
    :type rayon: Rayon
    :param sphere: Sphère éclairée
    :type sphere: Sphere
    :return: Point d'intersection, s'il existe
    :rtype: Optional[Tuple[Point, float]]
    """
    ca = vec(sphere[0], rayon[0])
    b = 2 * ps(rayon[1], ca)
    c = ps(ca, ca) - sphere[1] ** 2
    delta = b ** 2 - 4 * c
    if delta < 0:
        return None
    pos = (-b - math.sqrt(delta)) / 2
    if pos >= 0:
        return pt(rayon, pos), pos
    return None


Couleur = t.Any  # np.array
NOIR: Couleur = np.array([0.0, 0.0, 0.0])  # type: ignore
BLANC: Couleur = np.array([1.0, 1.0, 1.0])  # type: ignore

# Condition: Si S et C sont dans deux demi-espaces différents selon Pp
# ==> PC.PS <= 0


def au_dessus(sphere: Sphere, point: Point, src: Point) -> bool:
    """Vérifie si la source est au-dessus de l'horizon au niveau du point.

    :param sphere: Sphère à considérer
    :type sphere: Sphere
    :param point: Point d'où l'on observe
    :type point: Point
    :param src: Source lumineuse
    :type src: Point
    :return: Si la source est au-dessus de l'horizon
    :rtype: bool
    """
    return ps(vec(point, sphere[0]), vec(point, src)) <= 0


def visible(obj: t.List[Sphere], j: int, point: Point, src: Point) -> bool:
    """Check if the source is visible.

    :param obj: list of all spheres in play
    :type obj: List[Sphere]
    :param j: Index of the sphere on which the point is
    :type j: int
    :param point: Point of interest
    :type point: Point
    :param src: Source lumineuse
    :type src: Point
    :return: Whethere the source is visible or not
    :rtype: bool
    """
    if not au_dessus(obj[j], point, src):
        return False
    length = norme(vec(src, point))
    rayon = ra(src, point)
    for i in range(len(obj)):
        sphere = obj[i]
        if i != j:
            inter = intersection(rayon, sphere)
            if inter:
                if inter[1] < length:
                    return False
    return True


def couleur_diffusee(
    rayon: Rayon, incident: Couleur, normal: Vector, coeffs: Couleur
) -> Couleur:
    """Calcul de la couleur diffusée."""
    cosθ = ps(-rayon[1], normal)
    return cosθ * incident * coeffs


def rayon_reflechi(sphere: Sphere, point: Point, src: Point) -> Rayon:
    """Calcul du rayon réfléchi."""
    u = dir_(src, point)
    center, _ = sphere
    normal = dir_(center, point)
    v = ps(-u, normal) * normal
    w = u + 2 * v
    return point, w


DELTA: float = 100.0  # Whatever, we don't care
N: int = 10
OBJET: t.List[Sphere] = []
KDOBJ: t.List[Couleur] = []
SOURCE: t.List[Point] = []
COLSRC: t.List[Couleur] = []


def grille(i: int, j: int) -> Point:
    """Return the point associated with this grid."""
    unite = DELTA / N
    x = (i - N / 2) * unite
    y = (j - N / 2) * unite
    return np.array([x + unite / 2, y - unite / 2, 0])  # type: ignore


def rayon_ecran(omega: Point, i: int, j: int) -> Rayon:
    """Trouve le rayon issu de oméga passant par le point de l'écran."""
    point = grille(i, j)
    return omega, dir_(omega, point)


def interception(rayon: Rayon) -> t.Optional[t.Tuple[Point, int]]:
    """Trouve le premier point d'interception."""
    i_min: t.Optional[int] = None
    point_min: t.Optional[Point] = None
    for i in range(len(OBJET)):
        inter = intersection(rayon, OBJET[i])
        if inter:
            point, _ = inter
            if point_min is None or point[2] > point_min[2]:
                i_min, point_min = i, point
    if i_min:
        return point_min, i_min
    return None


def couleur_diffusion(point: Point, j: int) -> Couleur:
    """Calcule la couleur diffusée."""
    result: Couleur = np.copy(NOIR)  # type: ignore
    for i in range(len(SOURCE)):
        if visible(OBJET, j, point, SOURCE[i]):
            rayon = ra(SOURCE[i], point)
            result += couleur_diffusee(
                rayon,
                COLSRC[i],
                dir_(OBJET[j][0], point),
                KDOBJ[j]
            )
    return result


Image = t.Any  # np.array N * N * 3


def lancer(omega: Point, fond: Couleur) -> Image:
    """Génération de l'image par lancer."""
    im: Image = np.zeros((N, N, 3))  # type: ignore
    for i in range(N):
        for j in range(N):
            rayon = rayon_ecran(omega, i, j)
            intercepte = interception(rayon)
            if intercepte:
                point, indice = intercepte
                im[i, j] = couleur_diffusion(point, indice)
            else:
                im[i, j] = np.copy(fond)  # type: ignore
    return im
