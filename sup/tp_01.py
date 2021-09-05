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
from math import log
from time import time


def heure_to_sec(hours: int, minutes: int, seconds: int) -> int:
    """Convert time in hours, minutes and seconds to a number of seconds."""
    return hours * 3600 + minutes * 60 + seconds


def sec_to_hours(seconds: int) -> str:
    """Convert a time in seconds to hh:mm:ss format."""
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f"{hours}:{minutes}:{seconds}"


def duree(h1: int, m1: int, s1: int, h2: int, m2: int, s2: int) -> str:
    """Calculate the time delta between the two times."""
    seconds = s2 - s1
    minutes = 0
    if seconds < 0:
        seconds += 60
        minutes = -1
    minutes += m2 - m1

    hours = 0
    if minutes < 0:
        minutes += 60
        hours = -1
    hours += h2 - h1

    return f"{hours}:{minutes}:{seconds}"


def entiers(start: int, end: int) -> None:
    """Print the integers between start and end."""
    print("-".join(str(i) for i in range(start, end + 1)))


def entiers_not_7(start: int, end: int) -> None:
    """Print the integers between start and end that are not a multiple of 7."""
    print("-".join([i for i in range(start, end + 1) if i % 7 != 0]))


def talkhys_1(total: int = 10) -> None:
    """Display the first Talkhys formula."""
    for i in range(1, total + 1):
        print(
            f"{' ' * (total - i)}{'1' * i} x {'1' * i}{' ' * (total - i)} "
            f"= {' ' * (total - i)}{int('1' * i) ** 2}"
        )
# On ne peut pas utiliser le formattage :> (il requière un entier fixé)


def talkhys_2() -> None:
    """Display the second Talkhys formula."""
    for i in range(1, 10):
        num = int("".join([str(j) for j in range(1, i + 1)]))
        print(
            f"8 x {num:<9} + {i} = {8 * num + i}"
        )


def rotr_13(string: str) -> str:
    """Shift the message by 13 places in the alphabet."""
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    shifted = ""
    for car in string:
        if car in alphabet:
            shifted += alphabet[(alphabet.index(car) + 13) % 26]
        else:
            shifted += car
    return shifted
# On peut décoder le ROTR13 en réappliquant le ROTR13 au message
# En effet, comme l'alphabet compte 26 lettres, décaler 2 fois de 13 caractères
# revient à renvoyer le message original.
# `gurer vf ab fcbba` se décode donc en `there is no spoon`


def isqrt(number: int) -> int:
    """Return the integer square root of a number."""
    root = 0
    while root ** 2 <= number:
        root += 1
    return root - 1


def isqrt_2(number: int) -> int:
    """Return the integer square root of a number (with additions)."""
    root = 0
    square = 0
    while square <= number:
        square += root + root + 1
        root += 1
    return root - 1


def universe(string: str) -> int:
    """Return the smallest power of two containing the string."""
    i = 0
    while string not in str(2 ** i):
        i += 1
    return i
# 2**21226 is the smallest power of two containing `24072004`


def premier(integer: int) -> bool:
    """Return true if the number is primary, false otherwise."""
    k = 2
    while k ** 2 <= integer:
        if integer % k == 0:
            return False
        k += 1
    return True


def print_first_primary(total: int = 1000) -> float:
    """Print the specified number of first primary numbers."""
    start = time()
    count = 0
    number = 2
    primary = []
    while count < total:
        if premier(number):
            count += 1
            primary.append(str(number))
        number += 1
    print("\n".join(primary))
    return time() - start
# Cette méthode est suffisamment efficace (temps de calcul de 0.1 secondes)
# Cependant, ce n'est pas vraiment optimal


def check_written_as_sum_primary(maximum: int = 1000) -> bool:
    """Check if the even numbers from 4 to maximum can be written as a sum of two primary number."""
    for i in range(4, maximum + 1, 2):
        wrong = True
        for first in range(2, int(i / 2) + 1):
            if not premier(first):
                continue
            if not premier(i - first):
                continue
            wrong = False
            break
        if wrong:
            return False
    return True
# Cette fonction renvoit bien `True`, comme attendu


def find_odd_number():
    """Return the first odd number that's not a sum of a power of two and a primary number."""
    odd = 3
    while True:
        power = 0
        test = False
        while 2 ** power < odd:
            if premier(odd - 2 ** power):
                test = True
                break
            power += 1
        if not test:
            return odd
        odd += 2
# 127 ne s'écrit pas comme somme d'une puissance de 2 et d'un nombre premier.
# Donc la conjecture énoncée en 4 est fausse


def lookandsay(term: str) -> str:
    """Send the next term of Conway's suite."""
    next_term = ""
    current_char = term[0]
    count = 0
    for char in term:
        if char == current_char:
            count += 1
        else:
            next_term += str(count) + current_char
            count = 1
            current_char = char
    return next_term + str(count) + current_char


def first_terms(number: int) -> list:
    """Return the first terms of Conway's suite."""
    terms = ["1"]
    for _ in range(number - 1):
        terms.append(lookandsay(terms[-1]))
    return terms
# 1
# 11
# 21
# 1211
# 111221
# 312211
# 13112221
# 1113213211
# 31131211131221
# 13211311123113112211
# 11131221133112132113212221
# 3113112221232112111312211312113211
# 1321132132111213122112311311222113111221131221
# 11131221131211131231121113112221121321132132211331222113112211
# 311311222113111231131112132112311321322112111312211312111322212311322113212221
# 132113213221133112132113311211131221121321131211132221123113112221131112311332111213211322211312113211
# 11131221131211132221232112111312212321123113112221121113122113111231133221121321132132211331121321231231121113122113322113111221131221
# 31131122211311123113321112131221123113112211121312211213211321322112311311222113311213212322211211131221131211132221232112111312111213111213211231131122212322211331222113112211
# 1321132132211331121321231231121113112221121321132122311211131122211211131221131211132221121321132132212321121113121112133221123113112221131112311332111213122112311311123112111331121113122112132113213211121332212311322113212221
# 11131221131211132221232112111312111213111213211231132132211211131221131211221321123113213221123113112221131112311332211211131221131211132211121312211231131112311211232221121321132132211331121321231231121113112221121321133112132112312321123113112221121113122113121113123112112322111213211322211312113211


def constant_value(index: int) -> float:
    """Return the value of un+1 / un for a value of n."""
    terms = first_terms(index + 1)
    return len(terms[index]) / len(terms[index - 1])
# On trouve une valeur d'environ 1.3 pour cette constante pour n=40, 50 et 60
# On trouve en effet 1.295 pour 21, 1.285 pour 22, 1.33 pour 23 et 1.30 pour 24
# Il y a bien un deficit de caractères pour le 22ème terme


def shadok(integer: int) -> str:
    """Convert a number to Shadok."""
    shadok_alphabet = ["ga", "bu", "zo", "meu"]
    converted = []
    current = integer
    power = int(log(integer, 4))
    while power >= 0:
        converted.append(
            shadok_alphabet[
                current // 4 ** power
            ]
        )
        current %= 4 ** power
        power -= 1
    return "-".join(converted)


def shadok_to_int(shad: str) -> int:
    """Convert a shadok number to int."""
    return int(
        shad.replace(
            "-", "",
        ).replace(
            "ga", "0",
        ).replace(
            "bu", "1",
        ).replace(
            "zo", "2",
        ).replace(
            "meu", "3",
        ),
        base=4,
    )
