"""Exos de révision, piles et classes.

Copyright (C) 2021  Faholan <https://github.com/Faholan>
"""

from queue import Queue, LifoQueue
from math import sqrt
from random import randint
import typing as t


Numeric = t.Union[int, float]


# Question 1
def moyenne(source: t.List[Numeric]) -> float:
    """Calculate the average."""
    somme = 0.
    for i in source:
        somme += i
    return somme / len(source)


def ecart_type(source: t.List[Numeric]) -> float:
    """Calcule l'écart-type."""
    somme = somme2 = 0.
    for i in source:
        somme += i
        somme2 += i ** 2
    return sqrt(somme2 / len(source) - (somme / len(source)) ** 2)


# Question 2
def max_min(source: t.List[Numeric]) -> t.Tuple[Numeric, Numeric]:
    """Fetch the max and min of a list."""
    val_max = val_min = source[0]
    for i in source:
        if i > val_max:
            val_max = i
        elif i < val_min:
            val_min = i
    return val_min, val_max


# Question 3
# Partie a
def occurences(source: t.List[int]) -> t.List[int]:
    """Renvoie la liste des occurences."""
    results = [0] * (max(source) + 1)
    for i in source:
        results[i] += 1
    return results


# Partie b
def occurences2(source: t.Iterable[t.Hashable]) -> t.Dict[t.Hashable, int]:
    """Renvoie le dictionnaire des occurences."""
    results: t.Dict[t.Hashable, int] = {}
    for elem in source:
        results[elem] = results.get(elem, 0) + 1
    return results


# Question 4
def remove_repetitions(source: t.List[t.Any]) -> t.List[t.Any]:
    """Renvoie la liste sans répétitions."""
    results: t.List[t.Any] = []
    for elem in source:
        if elem not in results:
            results.append(elem)
    return results


# Question 5
# Partie a
def pgcd(a: int, b: int) -> int:
    """Renvoie le PGCD de a et de b."""
    x, y = max(a, b), min(a, b)

    while y != 0:
        x, y = y, x % y
    return x


# Partie b
def pgcd_lst(source: t.List[int]) -> int:
    """Renvoie le PGCD d'une liste d'entiers."""
    current = 0
    for i in source:
        current = pgcd(current, i)
    return current


# Partie c
def bezout(a: int, b: int) -> t.Tuple[int, int]:
    """Implement the extended Euler algorithm."""
    r, u, v, r2, u2, v2 = a, 1, 0, b, 0, 1

    while r2 != 0:
        q = r // r2

        rs, us, vs = r, u, v
        r, u, v = r2, u2, v2

        r2, u2, v2 = rs - q * r2, us - q * u2, vs - q * v2

    return u, v


# Piles et classes
# Question 1
def echange(pile: LifoQueue[t.Any]) -> None:
    """Exchange the two first items from a queue."""
    e1 = pile.get()
    e2 = pile.get()
    pile.put(e1)
    pile.put(e2)


# Question 2
def appartient(pile: LifoQueue[t.Any], elem: t.Any) -> int:
    """Return the index of first appearance of an element, or -1 otherwise."""
    index = 0
    while not pile.empty():
        if elem == pile.get():
            return index
        index += 1
    return -1


# Question 3
# Partie a
def reverse(pile: LifoQueue[t.Any]) -> LifoQueue[t.Any]:
    """Reverse a queue."""
    result: LifoQueue[t.Any] = LifoQueue()
    _result: LifoQueue[t.Any] = LifoQueue()
    while not pile.empty():
        elem = pile.get()
        result.put(elem)
        _result.put(elem)

    while not _result.empty():
        pile.put(_result.get())

    return result


# Partie b
def reverse_inplace(pile: LifoQueue[t.Any]) -> None:
    """Reverse a queue in place."""
    buffer: LifoQueue[t.Any] = LifoQueue()
    while not pile.empty():
        buffer.put(pile.get())

    reversedbuffer = reverse(buffer)
    while not reversedbuffer.empty():
        pile.put(reversedbuffer.get())


# Question 4
def shuffle(pile1: LifoQueue[t.Any], pile2: LifoQueue[t.Any]) -> LifoQueue[t.Any]:
    """Shuffle two queues."""
    shuffled: LifoQueue[t.Any] = LifoQueue()
    while not pile1.empty() or not pile2.empty():
        if pile1.empty():
            shuffled.put(pile2.get())
        elif pile2.empty():
            shuffled.put(pile1.get())
        else:
            shuffled.put((pile1 if randint(0, 1) else pile2).get())
    return shuffled


# Question 5
def depile(pile: LifoQueue[t.Any], k: int) -> None:
    """Dépile les k premiers éléments."""
    result = []
    for _ in range(k):
        if not pile.empty():
            result.append(pile.get())

    return result


# Question 6
def depile_elem(pile: LifoQueue[t.Any], elem: t.Any) -> None:
    """Dépile jusqu'à un élément."""
    result = []
    while not pile.empty():
        result.append(pile.get())
        if result[-1] == elem:
            return result


# Question 7
class Quaternion:
    """Généralise les nombres complexes."""

    __slots__ = ("a", "b", "c", "d")

    def __init__(self, a: Numeric = 0, b: Numeric = 0, c: Numeric = 0, d: Numeric = 0) -> None:
        """Initialize self."""
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    @property
    def re(self) -> Numeric:
        """Get the real part."""
        return self.a

    @property
    def im(self) -> t.Tuple[Numeric, Numeric, Numeric]:
        """Get the imaginary type as a tuple (b, c, d)."""
        return self.b, self.c, self.d

    def __str__(self) -> str:
        """Implement str(self)."""
        return f"{self.a} + {self.b}i + {self.c}j + {self.d}k"

    def __eq__(self, other) -> bool:
        """Implement self == other."""
        if isinstance(other, (int, float)):
            other = Quaternion(other)
        if not isinstance(other, Quaternion):
            return False
        return (self.a, self.b, self.c, self.d) == (other.a, other.b, other.c, other.d)

    def __hash__(self):
        """Implement hash(self)."""
        return hash((self.a, self.b, self.c, self.d))

    def __add__(self, other):
        """Implement self + other."""
        if isinstance(other, (int, float)):
            other = Quaternion(other)
        if not isinstance(other, Quaternion):
            return NotImplemented
        return Quaternion(
            self.a + other.a,
            self.b + other.b,
            self.c + other.c,
            self.d + other.d,
        )

    def __abs__(self) -> float:
        """Implement abs(self)."""
        return sqrt(self.a ** 2 + self.b ** 2 + self.c ** 2 + self.d ** 2)

    def __mul__(self, other):
        """Implement self * other."""
        if isinstance(other, (int, float)):
            other = Quaternion(other)
        if not isinstance(other, Quaternion):
            return NotImplemented

        return Quaternion(
            self.a * other.a - self.b * other.b - self.c * other.c - self.d * other.d,
            self.a * other.b + self.b * other.a + self.c * other.d - self.d * other.c,
            self.a * other.c - self.b * other.d + self.c * other.a + self.d * other.b,
            self.a * other.d + self.b * other.c - self.c * other.b + self.d * other.a,
        )

    def __div__(self, other):
        """Implement self / other."""
        if isinstance(other, (int, float)):
            other = Quaternion(other)
        if not isinstance(other, Quaternion):
            raise TypeError()

        return self * other.inv()

    def conj(self):
        """Return self's conjugate."""
        return Quaternion(
            self.a,
            -self.b,
            -self.c,
            -self.d,
        )

    def inv(self):
        """Return self's inverse."""
        mod = self.a ** 2 + self.b ** 2 + self.c ** 2 + self.d ** 2
        if mod == 0:
            raise ZeroDivisionError()
        return Quaternion(self.a/mod, -self.b/mod, -self.c/mod, -self.d/mod)


def auto_int(q: Quaternion, u: Quaternion) -> Quaternion:
    """Implémente l'automorphisme."""
    return q * u * q.inv()


# Question 8
# Partie a
def queue_to_list(file: Queue[t.Any]) -> t.List[t.Any]:
    """Empty a queue into a list."""
    result = []
    while not file.empty():
        result.append(file.get())
    return result


def copy_queue(file: Queue[t.Any]) -> t.List[t.Any]:
    """Get a copy of a queue's elements."""
    result = []
    for _ in range(file.qsize()):
        elem = file.get()
        result.append(elem)
        file.put(elem)
    return result


def list_to_queue(source: t.List[t.Any]) -> Queue[t.Any]:
    """Copy a list into a queue."""
    result: Queue[t.Any] = Queue()
    for elem in source:
        result.put(elem)
    return result


def inqueue(source: Queue[t.Any], elem: t.Any):
    """Test if elem is in source."""
    while not source.empty():
        if source.get() == elem:
            return True
    return False


# Partie b
def josephus(n: int, k: int) -> int:
    """Résoud le problème de Joséphus."""
    famille: Queue[int] = Queue()
    for i in range(n):
        famille.put(i + 1)
    while not famille.empty():
        for _ in range(k - 1):
            famille.put(famille.get())
        result = famille.get()
    return result
