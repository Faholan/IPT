"""TD analyse de la houle."""
import typing as t

# Partie I
# Question 1
# Pour 20 minutes d'enregistrement
# On effectue 20 * 60 * 2 = 2400 enregistrements.
# à 1 octet / caractère, 8 caractères par ligne, on obtient :
# 8 * 2400 = 19200 octets par 20 minutes d'enregistrement

# Question 2
# En 15 jours, on effectue 15 * 24 * 2 enregistrements
# Soit 30 * 24 * 19200 octets pour le fichier
# Ie 13824000 octets ~ 14 Mo < 1 Go

# Question 3
# Le gain relatif serait de 1 - 7/8 = 12.5 %


# Question 4
def load_file(fp: str = "donnees.txt") -> t.List[float]:
    """Load the data from the data file into memory."""
    with open(fp, encoding="utf-8") as file:
        file.readline()
        return [float(line.strip()) for line in file]


# Partie II
# H1 ~= 9
# H2 ~= 9
# H3 ~= 6


# Question 6
def moyenne(liste_niveaux: t.List[float]) -> float:
    """Calculate the average of liste_niveaux."""
    return sum(liste_niveaux) / len(liste_niveaux)


# Question 7
def integrale_precise(liste_niveaux: t.List[float]) -> float:
    """Calculate ∫η(t)dt."""
    result = 0.0
    for i in range(len(liste_niveaux) - 1):
        result += (liste_niveaux[i] + liste_niveaux[i + 1]) / 4
    return result


def moyenne_precise(liste_niveaux: t.List[float]) -> float:
    """Calculate the average value of η."""
    return integrale_precise(liste_niveaux) / (20 * 60)


# Question 8
def ind_premier_pnd(liste_niveaux: t.List[float]) -> int:
    """Calculate the index of the first PND."""
    moy = moyenne_precise(liste_niveaux)
    for i in range(len(liste_niveaux) - 1):
        if liste_niveaux[i] > moy > liste_niveaux[i + 1]:
            return i
    return -1


# Question 9
def ind_dernier_pnd(liste_niveaux: t.List[float]) -> int:
    """Calculate the index of the last PND."""
    moy = moyenne_precise(liste_niveaux)
    for i in range(len(liste_niveaux) - 1, 0, -1):
        if liste_niveaux[i - 1] > moy > liste_niveaux[i]:
            return i - 1
    return -2


# Question 10
def construction_successeurs(liste_niveaux: t.List[float]) -> t.List[int]:
    """Generate the successors."""
    n = len(liste_niveaux)
    successeurs: t.List[int] = []
    m = moyenne(liste_niveaux)
    for i in range(n - 1):
        if liste_niveaux[i] > m > liste_niveaux[i + 1]:
            successeurs.append(i + 1)
    return successeurs


# Question 11
def decompose_vagues(liste_niveaux: t.List[float]) -> t.List[t.List[float]]:
    """Décompose en vagues."""
    successeurs = construction_successeurs(liste_niveaux)
    result: t.List[t.List[float]] = []
    for i in range(len(successeurs) - 1):
        result.append(liste_niveaux[successeurs[i]: successeurs[i + 1]])
    return result


# Question 12
def proprietes(liste_niveaux: t.List[float]) -> t.List[t.Tuple[float, float]]:
    """Analyse des vagues."""
    vagues = decompose_vagues(liste_niveaux)
    result = [
        (
            max(liste_niveaux[:ind_premier_pnd(liste_niveaux)]) - min(vagues[0]),
            len(vagues[0]) / 2,
        )
    ]
    for i in range(1, len(vagues)):
        result.append((max(vagues[i - 1]) - min(vagues[i]), len(vagues[i]) / 2))
    return result


# Partie III
# Question 13
def hauteur_max(liste_niveaux: t.List[float]) -> float:
    """Calculate the max height."""
    properties = proprietes(liste_niveaux)
    cur_max = 0.0
    for height, _ in properties:
        if height > cur_max:
            cur_max = height
    return cur_max
    # return max(properties)[0]


# Question 14, 15, 16
def tri_rapide(lst: t.List[t.Tuple[float, float]], g: int, d: int) -> None:
    """Implémente le tri rapide."""
    if d - g <= 15:
        tri_insertion(lst, g, d)
        return
    pivot = lst[g][0]
    i = g
    j = d
    while True:
        while i <= d and lst[i][0] < pivot:
            i += 1
        while j >= g and lst[j][0] > pivot:
            j -= 1
        if i > j:
            break
        if i < j:
            lst[i], lst[j] = lst[j], lst[i]
        i += 1
        j -= 1
    if g < j:
        tri_rapide(lst, g, j)
    if i < d:
        tri_rapide(lst, i, d)


def tri_insertion(lst: t.List[t.Tuple[float, float]], g: int, d: int) -> None:
    """Implement the insertion sort."""
    for i in range(g + 1, d + 1):
        j = i - 1
        tmp = lst[i]
        while j >= g and tmp[0] < lst[j][0]:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = tmp


# Question 17
def skewness(liste_hauteurs: t.List[float]) -> float:
    """Implement the skewness algorithm."""
    n = len(liste_hauteurs)
    et3: float = (ecart_type(liste_hauteurs)) ** 3

    moy = moyenne(liste_hauteurs)
    s = 0.0
    for i in range(n):
        s += (liste_hauteurs[i] - moy) ** 3
    s = n / (n - 1) / (n - 2) * s / et3
    return s


# Question 18
# La complexité de la fonction évaluant K sera la même,
# car on effectue là encore un simple parcours de liste.

# Question 20
# C(N) = 2 * C(N/2) + O(N)
# D'où C(N) = O(NlogN)
