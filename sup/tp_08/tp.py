"""Tp du 18/01/2021.

Tp sur la manipulation des fichiers
"""
import typing

import matplotlib.pyplot as plt
import numpy as np


def premiers() -> int:
    """Calcule la somme des 1000 premiers nombres entiers."""
    with open(r"fichierEntree\premiers1000.txt", encoding="utf-8") as file:
        total = sum(
            int(line.strip()) for line in file if line.strip()
        )
    return total


def _get_primes(majorant: int) -> typing.List[int]:
    """Get the primes up to majorant."""
    primes = list(range(2, majorant + 1))
    cursor = 0
    while cursor < len(primes):
        prime = primes[cursor]
        for number in primes[cursor + 1:]:
            if not number % prime:
                primes.remove(number)
        cursor += 1
    return primes


def creer_premiers(majorant: int = 10000) -> None:
    """Crée le fichier desPremiers.txt."""
    with open(r"fichierSortie\desPremiers.txt", "w", encoding="utf-8") as file:
        file.write("\n".join([str(i) for i in _get_primes(majorant)]))


def creer_premiers_2(majorant: int = 10000) -> None:
    """Crée le fichier desPremiersPar10.txt."""
    primes = _get_primes(majorant)
    output = []

    lines, rest = divmod(len(primes), 10)
    if rest:
        lines += 1
    for i in range(lines):
        output.append("\t".join([str(j) for j in primes[10 * i: 10 * i + 9]]))

    with open(
        r"fichierSortie\desPremiersPar10.txt",
        "w",
        encoding="utf-8",
    ) as file:
        file.write("\n".join(output))


def ecrit() -> None:
    """Crée quatre fichiers regroupant noms et prénoms des admissibles."""
    candidats = [0] * 4
    series = [[], [], [], []]
    with open(r"fichierEntree\admissibles.txt", encoding="utf-8") as file:
        line = "foo"
        while line:
            line = file.readline().strip()
            if not line:
                continue
            if line.endswith("-"):
                continue
            _, raw_name, __, raw_serie = line.split("\t")
            splitted = raw_name.split(" ")
            first = last = ""
            named = False
            while not named:
                current = splitted.pop(0)
                tested = current.replace("-", "")
                if tested and not tested.isupper():
                    first = current + " "
                    named = True
                else:
                    last += current + " "
            first += " ".join(splitted)
            first = first.strip()
            last = last.strip()
            serie = int(raw_serie) - 1
            candidats[serie] += 1
            series[serie].append(f"{last}\t{first}")
    for i in range(4):
        with open(
            fr"fichierSortie\admissibles{i + 1}.txt",
            "w",
            encoding="utf-8",
        ) as file:
            file.write("\n".join(series[i]))
    print(
        "Candidats par serie :\n1\t2\t3\t4\n" + "\t".join(
            [str(i) for i in candidats]
        )
    )


def puissances() -> None:
    """Exercice 3."""
    coords = np.linspace(-2.5, 2.5, 1000)
    plt.plot(coords, coords, "-")  # x
    coords = np.linspace(-2, 2, 800)
    plt.plot(coords, [i ** 2 for i in coords], "-")  # x²
    coords = np.linspace(-1.5, 1.5, 750)
    plt.plot(coords, [i ** 3 for i in coords], "--")  # x**3
    plt.grid(linestyle=":")
    plt.xlim(-3, 3)
    plt.ylim(-4, 4)
    plt.axhline(color="black")
    plt.axvline(color="black")
    plt.title("Puissances comparées")
    plt.legend(["x", "x²", "x**3"], loc="lower right")
    plt.savefig(r"fichierSortie\puissances.pdf")


def _suite(length: int = 11) -> None:
    """Yield up to length terms."""
    term = -8.41
    for _ in range(length):
        yield term
        term = 63 - term / 2


def graphe(length: int = 11) -> None:
    """Renvoie le graphe discret."""
    plt.plot(list(range(length)), list(_suite(length)))
    plt.grid(linestyle=":")
    plt.axhline(color="black")
    plt.xlim(0, 10)
    plt.ylim(-10, 70)
    plt.xticks([2 * i for i in range(6)])
    plt.yticks([10 * i for i in range(8)])
    plt.savefig(r"fichierSortie\graphe.pdf")
