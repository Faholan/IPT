"""TP du 07/12/2020.

Faire un pendu avec George !
"""
from random import choice
from typing import List

import config_pendu as config


def finished(erreurs: int, mot: str, lettres: List[str]) -> bool:
    """Test whether the game is finished or not."""
    return erreurs >= config.ERREUR_MAX or all(
        chr in lettres for chr in mot
    )


def main() -> None:
    """Programme principal."""
    # Initialisation des variables
    mot = choice(config.MOTS)
    erreurs = 0
    lettres: List[str] = []
    print(
        "Bienvenue dans le jeu du pendu ! Le mot secret comporte "
        f"{len(mot)} lettres"
    )

    while not finished(erreurs, mot, lettres):
        print(f"\nErreurs : {erreurs} / {config.ERREUR_MAX}")
        print(
            "Etat actuel du mot : "
            f"{''.join([ch if ch in lettres else '-' for ch in mot])}"
            "\nLettres essayées : "
            f"{', '.join([ch for ch in lettres if not ch in mot])}"
        )

        lettre = input("Entrez une lettre :")
        if len(lettre) != 1:
            print("Veuillez n'entrer qu'une unique lettre.")
            continue
        if not lettre.isalpha():
            print("Veuillez entrer une lettre.")
            continue
        lettre = lettre.lower()
        if lettre in lettres:
            print("Cette lettre a déjà été entrée.")
            continue
        lettres.append(lettre)
        if lettre in mot:
            print(f"{lettre} appartient bien au mot !")
        else:
            erreurs += 1
            print(f"{lettre} n'appartient pas au mot.")

    if erreurs == config.ERREUR_MAX:
        print(f"Dommage ! Le mot était {mot}. Rejouer ? (o/n)")
    else:
        print(f"Bravo ! Le mot était bien {mot} ! Rejouer ? (o/n)")

    answer = input()
    if answer.lower() in ("o", "y", "continue", "ok"):
        main()  # Limite de récursion : 1000 (on a de la marge)


if __name__ == "__main__":
    main()
