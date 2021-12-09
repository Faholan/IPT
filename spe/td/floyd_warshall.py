"""Algorithme de Floyd-Warshall - 17/11/2021.

Copyright (C) 2021  Faholan <https://github.com/Faholan>
"""
import typing as t

import numpy as np

# Question 1
# Lorsqu'on inclut un sommet de plus dans la liste des sommets possibles,
# Il y a deux candidats pour le chemin minimal :
# Le chemin minimal allant de i à j passant par les k-1 premiers sommets
# Et le chemin minimal allant de i à j passant par le sommet k-1
# Dont la longueur et celle du chemin allant de i à k-1 +
# celle du chemin allant de k-1 à j


# Question 2
def _update_distance(
    base: t.Any,
    step: int,
) -> t.Any:
    """Update the current distance."""
    if step > len(base):
        return base
    final: t.Any = np.ndarray(base.shape)
    for i, column in enumerate(final):
        for j in range(len(final)):
            column[j] = min(
                base[i][j],
                base[i][step - 1] + base[step - 1][j],
            )

    return _update_distance(final, step + 1)


def distance(
    base: t.Any,
) -> t.Any:
    """Renvoie A(n)."""
    return _update_distance(base, 1)


# La complexité de distance est en O(n**3)

# Question 3
# De la même manière, on veut construire le chemin le + court allant de i à j
# Soit ce chemin est le même que celui allant de i à j
# en passant par les k-1 premiers sommets
# Soit ce chemin passe par le point k-1


def _distancepred_update(
    lengths: t.Any,
    preds: t.Any,
    step: int,
) -> t.Tuple[
    t.Any,
    t.Any,
]:
    """Do a step of the distancepred algorithm."""
    if step > len(lengths):
        return lengths, preds

    nextlengths: t.Any = np.ndarray(
        lengths.shape,
    )
    nextpreds: t.Any = np.ndarray(
        preds.shape,
        np.int32,
    )

    for i, column in enumerate(lengths):
        for j in range(len(lengths)):
            if column[j] <= column[step - 1] + lengths[step - 1][j]:
                nextlengths[i][j] = column[j]
                nextpreds[i][j] = preds[i][j]
            else:
                nextlengths[i][j] = column[step - 1] + lengths[step - 1][j]
                nextpreds[i][j] = preds[step - 1, j]
    return _distancepred_update(nextlengths, nextpreds, step + 1)


def _init_preds(
    base: t.Any,
) -> t.Any:
    """Initialize the predecessors."""
    preds: t.Any = np.ndarray(
        base.shape,
        np.int32,
    )
    for i, column in enumerate(preds):
        for j in range(len(preds)):
            if base[i][j] != np.inf:
                column[j] = i
            else:
                column[j] = -1
    return preds


def distancepred(
    base: t.Any,
) -> t.Tuple[
    t.Any,
    t.Any,
]:
    """Get the distances and predecessors."""
    return _distancepred_update(base, _init_preds(base), 1)


# Question 5
# La complexité de _init_preds est en O(n**2)
# La complexité de distancepred est en O(n**3)

# Question 6
def _make_path(
    preds: t.Any,
    i: int,
    j: int,
) -> t.List[int]:
    """Create the shortest path."""
    if i == j:
        return [i]
    base = _make_path(preds, i, preds[i][j])
    base.append(j)
    return base


def chemin(
    base: t.Any,
    i: int,
    j: int,
) -> t.List[int]:
    """Renvoie le chemin le plus court allant de i à j."""
    dist, preds = distancepred(base)
    if dist[i][j] != np.inf:
        return _make_path(preds, i, j)
    return []


dico = {
    "Paris": 0,
    "Marseille": 1,
    "Lyon": 2,
    "Toulouse": 3,
    "Nice": 4,
    "Nantes": 5,
    "Bordeaux": 6,
    "Lille": 7,
    "Strasbourg": 8,
    "Montpellier": 9,
    "Brest": 10,
    "Nancy": 11,
    "Rouen": 12,
    "Orléans": 13,
    "Tours": 14,
    "Dijon": 15,
    "Besançon": 16,
    "Grenoble": 17,
    "Clermont-Ferrand": 18,
    "Rennes": 19,
    "Poitiers": 20,
    "Amiens": 21,
}

invdico = {value: key for key, value in dico.items()}

distances = [
    (0, 2, 465),
    (2, 1, 314),
    (2, 18, 164),
    (15, 2, 194),
    (2, 17, 112),
    (11, 2, 404),
    (11, 15, 214),
    (11, 8, 159),
    (11, 0, 385),
    (1, 4, 199),
    (1, 9, 169),
    (3, 6, 245),
    (3, 9, 247),
    (6, 20, 258),
    (20, 5, 219),
    (20, 18, 319),
    (20, 14, 105),
    (14, 5, 216),
    (14, 13, 117),
    (14, 19, 257),
    (14, 18, 240),
    (13, 0, 132),
    (13, 12, 252),
    (13, 19, 305),
    (13, 5, 335),
    (13, 18, 300),
    (13, 11, 449),
    (21, 0, 145),
    (21, 11, 420),
    (21, 7, 145),
    (21, 12, 120),
    (21, 8, 526),
    (12, 0, 136),
    (12, 19, 311),
    (12, 14, 310),
    (19, 5, 113),
    (19, 10, 242),
    (19, 0, 349),
    (5, 10, 295),
    (5, 6, 347),
    (7, 0, 225),
    (12, 7, 256),
    (11, 7, 418),
    (7, 8, 525),
    (7, 15, 502),
    (7, 2, 691),
    (2, 9, 303),
    (16, 15, 92),
    (16, 2, 255),
    (16, 8, 243),
    (16, 11, 206),
    (16, 0, 410),
    (17, 1, 306),
    (17, 9, 295),
    (0, 3, 679),
    (0, 6, 584),
    (18, 9, 332),
]


def load_adjacence(aretes: t.List[t.Tuple[int, int, int]]) -> t.Any:
    """Generate the adjacence matrix."""
    length = 0
    for i, indexes in enumerate(zip(*aretes)):
        if i != 2:
            length = max(length, *indexes)

    adjacence: t.Any = np.full((length + 1, length + 1), np.inf)
    for i, j, dist in aretes:
        adjacence[i][j] = dist
        adjacence[j][i] = dist
    for i in range(length + 1):
        adjacence[i][i] = 0
    return adjacence


def _make_path_ville(
    preds: t.Any,
    i: int,
    j: int,
) -> t.List[str]:
    """Create the shortest path."""
    if i == j:
        return [invdico[i]]
    base = _make_path_ville(preds, i, preds[i][j])
    base.append(invdico[j])
    return base


# Cache result to speed up program
curaretes: t.Optional[t.Any] = None
curresults: t.Optional[t.Tuple[t.Any, t.Any, t.Any]] = None


def chemin_villes(
    aretes: t.List[t.Tuple[int, int, int]],
    ville1: str,
    ville2: str,
) -> t.Tuple[t.Union[int, float], t.List[str]]:
    """Calculate the shortest path between two cities."""
    global curaretes, curresults
    if aretes == curaretes:
        if curresults:
            adjacence, dist, preds = curresults
        else:
            adjacence = load_adjacence(aretes)
            dist, preds = distancepred(adjacence)
    else:
        adjacence = load_adjacence(aretes)
        dist, preds = distancepred(adjacence)

    curaretes, curresults = aretes, (adjacence, dist, preds)

    if ville1 not in dico:
        raise ValueError(f"{ville1} n'est pas définie")
    if ville2 not in dico:
        raise ValueError(f"{ville2} n'est pas définie")

    if dico[ville1] >= adjacence.shape[0]:
        return np.inf, []

    if dico[ville2] >= adjacence.shape[0]:
        return np.inf, []

    index1 = dico[ville1]
    index2 = dico[ville2]

    if dist[index1][index2] == np.inf:
        return np.inf, []

    return int(dist[index1][index2]), _make_path_ville(preds, index1, index2)


if __name__ == "__main__":
    for v1 in range(len(dico)):
        for v2 in range(v1, len(dico)):
            print(chemin_villes(distances, invdico[v1], invdico[v2]))
