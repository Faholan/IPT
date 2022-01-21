"""TD Marches aléatoires.

Copyright (C) 2021  Faholan <https://github.com/Faholan>
"""
import random
import typing as t
from math import asin, cos, pi, radians, sin, sqrt

RAYON = 6371000


Coords = t.Tuple[float, float, float, float]


# Question 5
def import_rando(filename: str) -> t.List[Coords]:
    """Import the data."""
    result: t.List[Coords] = []
    with open(filename, "r", encoding="utf-8") as file:
        file.readline()
        for line in file:
            lat, long, height, time = line.split(",")
            result.append((float(lat), float(long), float(height), float(time)))

    return result


def plus_haut(coords: t.List[Coords]) -> t.Tuple[float, float]:
    """Get the coordinates of the highest point."""
    cur_lat, cur_long, cur_height, _ = coords[0]

    for lat, long, height, _ in coords:
        if height > cur_height:
            cur_lat, cur_long, cur_height = lat, long, height

    return cur_lat, cur_long


def deniveles(coords: t.List[Coords]) -> t.Tuple[float, float]:
    """Calcule le dénivelé cumulé."""
    neg = pos = 0.
    cur_height = coords[0][2]

    for _, _, height, _ in coords[1:]:
        if height > cur_height:
            pos += height - cur_height
        else:
            neg += cur_height - height

    return pos, neg


def distance(point1: Coords, point2: Coords) -> float:
    """Compute the distance between two points."""
    lat1, long1, height1, _ = point1
    lat2, long2, height2, _ = point2

    lat1 = radians(lat1)
    lat2 = radians(lat2)
    long1 = radians(long1)
    long2 = radians(long2)

    term1 = sin((lat2 - lat1) / 2) ** 2
    term2 = cos(lat1) * cos(lat2) * sin((long2 - long1) / 2) ** 2

    cur_rayon = RAYON + (height1 + height2) / 2

    return 2 * cur_rayon * asin(sqrt(term1 + term2))


def distance_totale(coords: t.List[Coords]) -> float:
    """Compute the total distance."""
    result = 0.
    coord1 = coords[0]
    for coord in coords[1:]:
        result += distance(coord1, coord)
        coord1 = coord
    return result


MU = 0
SIGMA = 1E-8
M = 1E-6
ALPHA = 1E-5

assert MU >= 0 and SIGMA > 0 and M > 0 and ALPHA > 0, "Constants verification"


def vma(v1: t.List[float], a: float, v2: t.List[float]) -> t.List[float]:
    """Vector multiplication addition."""
    assert len(v1) == len(v2)
    return [v1[i] + a * v2[i] for i in range(len(v1))]


def gen_random() -> t.List[float]:
    """Generate random agitation."""
    angle = random.uniform(0, 2 * pi)
    norme = abs(random.gauss(MU, SIGMA))
    return [norme * cos(angle), norme * sin(angle)]


def derive(etat: t.List[float]) -> t.List[float]:
    """Differential equation."""
    v = etat[2:]
    dv = vma(
        vma(
            [0, 0],
            - ALPHA / M,
            v
        ),
        1 / M,
        gen_random()
    )

    return [v[0], v[1], dv[0], dv[1]]


def euler(etat0: t.List[float], dt: float, n: int) -> t.List[t.List[float]]:
    """Solve the thing with euler's method."""
    assert len(etat0) == 4
    result = [etat0]
    etat = etat0
    for _ in range(n):
        etat = vma(etat, dt, derive(etat))
        result.append(etat)

    return result


# Partie III : Marche auto-évitante

Point = t.Tuple[int, int]


def positions_possible(point: Point, atteints: t.List[Point]) -> t.List[Point]:
    """Check which positions can be reached."""
    result: t.List[Point] = []
    x, y = point
    for point2 in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
        if point2 not in atteints:
            result.append(point2)

    return result


def genere_chemin_naif(n: int) -> t.Optional[t.List[Point]]:
    """Generate a random path."""
    result: t.List[Point] = [(0, 0)]
    for _ in range(n):
        possibilites = positions_possible(result[-1], result)
        if not possibilites:
            return None
        result.append(random.choice(possibilites))
    return result


# Question 16
# Ce graphe représente la fréquence à laquelle un chemin n'est pas généré en fonction de n


# Complexité asymptotique attendue : O(n * log n)
def est_cae(chemin: t.List[Point]) -> bool:
    """Check the nature of a path."""
    sortedpath = sorted(chemin)
    for i in range(len(sortedpath) - 1):
        if sortedpath[i] == sortedpath[i + 1]:
            return False

    return True


def rot(p: Point, q: Point, a: t.Literal[0, 1, 2]) -> Point:
    """Rotate a point arount another."""
    delta = q[0] - p[0], q[1] - p[1]
    if a == 0:
        delta = -delta[0], -delta[1]
    elif a == 1:
        delta = -delta[1], delta[0]
    else:
        delta = delta[1], -delta[0]

    return p[0] + delta[0], p[1] + delta[1]


def rotate_path(path: t.List[Point]) -> t.List[Point]:
    """Rotate the path around a randomly chosen point."""
    pivot = random.randint(1, len(path) - 2)
    result = path[: pivot + 1]
    direction: t.Literal[0, 1, 2] = random.randint(0, 2)  # type: ignore

    for i in range(pivot + 1, len(path)):
        result.append(rot(path[pivot], path[i], direction))

    if est_cae(result):
        return result
    return rotate_path(path)


def genere_chemin_pivot(n: int, n_rot: int) -> t.List[Point]:
    """Pivote un chemin."""
    result = [(0, i) for i in range(n)]
    for _ in range(n_rot):
        result = rotate_path(result)

    return result

# Question 23
# Les rotations admissibles sont seulement celles qui n'envoient pas le point après le pivot
# Sur le point avant le pivot. On peut donc déjà éliminer ces rotations.


def rotate_path2(path: t.List[Point]) -> t.List[Point]:
    """Rotate the path, but better."""
    result = path.copy()

    pivot = random.randint(1, len(path) - 2)

    possible_direction: t.List[t.Literal[0, 1, 2]] = [0, 1, 2]
    for x in possible_direction:
        if path[pivot - 1] == rot(path[pivot + 1], path[pivot], x):
            possible_direction.remove(x)
            break

    direction = random.choice(possible_direction)

    for i in range(pivot + 1, len(path)):
        result[i] = rot(path[pivot], path[i], direction)

    if est_cae(result):
        return result
    return rotate_path(path)
