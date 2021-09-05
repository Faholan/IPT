"""Jeu de Nim.

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
from random import randint


def ia_turn(batons: int, difficult: bool) -> int:
    """Tour de l'ordinateur."""
    if difficult:
        if batons % 5 == 1:
            return 1
        return (batons - 1) % 5
    return randint(1, min(4, batons))


def print_state(player: str, allumettes: int) -> None:
    """Affiche l'état actuel."""
    print(f"\n***{player}. Allumettes disponibles :{'|' * allumettes}")


def main() -> None:
    """Programme principal."""
    print(
        "Un ensemble de 20 allumettes sont disposées devant vous.\n"
        "A chaque étape vous pouvez retirer entre 1 et 4 allumettes\n"
        "Le joueur qui prend le dernier bâton a perdu\n"
        "Vous jouez contre l'ordinateur et vous jouez en premier"
    )
    difficult = input(
        "\nChoisissez le niveau de difficulté :\n"
        "0: facile\n1: difficile (valeur par défaut)"
    )
    difficult = difficult != "0"
    print(f"\nNiveau de difficulté : {'difficile' if difficult else 'facile'}")

    allumettes = 20
    while allumettes:
        print_state("Votre tour", allumettes)

        move = 0
        while move > 4 or move < 1 or move > allumettes:
            move = input(
                "\nCombien d'allumettes souhaitez-vous retirer ? "
                "(entre 1 et 4) "
            )
            move = int(move) if move.isdigit() else 0
        allumettes -= move
        print(f"Vous prenez {move} allumette{'s' if allumettes > 1 else ''}.")
        if not allumettes:
            print("Vous avez perdu !")
            continue
        if allumettes == 1:
            print(
                "Vous avez gagné ! L'ordinateur prend forcément "
                "la dernière allumette."
            )
            allumettes = 0
            continue
        print_state("Tour de l'ordinateur", allumettes)
        move = ia_turn(allumettes, difficult)
        allumettes -= move
        print(
            f"L'ordinateur prend {move} allumette"
            f"{'s' if allumettes > 1 else ''}."
        )
        if allumettes == 1:
            print(
                "Vous avez perdu : vous prenez forcément la dernière allumette"
            )
            allumettes -= 1
        if allumettes == 0:
            print("Vous avez gagné !")

    print("Voulez-vous rejouer ? (o/n)")
    answer = input()
    if answer.lower() in ("o", "y", "continue", "ok"):
        main()  # Limite de récursion : 1000 (on a de la marge)


if __name__ == "__main__":
    main()
