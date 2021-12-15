"""Exposé sur la cryptographie."""

import hashlib
from random import randint
import typing as t

ALPHABET = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ ")


def cesar(message: str, decalage: int) -> str:
    """Implémentation du chiffre de César.

    :param message: Message à encrypter
    :type message: str
    :param decalage: Clé secrète
    :type decalage: int
    :return: Message crypté
    :rtype: str
    """
    return "".join(
        ALPHABET[(ALPHABET.index(letter) + decalage) % len(ALPHABET)]
        if letter in ALPHABET
        else letter
        for letter in message.upper()
    )


def cesar_decrypt(message: str, decalage: int) -> str:
    """Décryptage du chiffre de César.

    :param message: Message à décrypter
    :type message: str
    :param decalage: Clé secrète
    :type decalage: int
    :return: Message décrypté
    :rtype: str
    """
    return cesar(message, -decalage)


def vigenere(message: str, key: str) -> str:
    """Chiffre de Vigenère.

    :param message: Message à encrypter
    :type message: str
    :param key: Clé secrète
    :type key: str
    :return: Message crypté
    :rtype: str
    """
    result = ""
    key = key.upper()
    for i, letter in enumerate(message.upper()):
        result += (
            ALPHABET[
                (ALPHABET.index(letter) + ALPHABET.index(key[i % len(key)]))
                % len(ALPHABET)
            ]
            if letter in ALPHABET
            else letter
        )
    return result


def vigenere_decrypt(message: str, key: str) -> str:
    """Décryptage du chiffre de Vigenère.

    :param message: Message à décrypter
    :type message: str
    :param key: Clé secrète
    :type key: str
    :return: Message décrypté
    :rtype: str
    """
    key = key.upper()
    result = ""
    for i, letter in enumerate(message.upper()):
        result += ALPHABET[
            (ALPHABET.index(letter) - ALPHABET.index(key[i % len(key)])) % len(ALPHABET)
        ]
    return result


def sha256(message: str) -> str:
    """Hash a message."""
    return hashlib.sha256(bytes(message, encoding="utf-8")).hexdigest()


def mod_inverse(value: int, modulus: int) -> int:
    """Return the modular inverse of value."""
    x1, x2, y1, y2 = 0, 1, 1, 0

    curmod = modulus
    while curmod:
        q, r = divmod(value, curmod)

        x = x2 - q * x1
        y = y2 - q * y1
        value, curmod, x2, x1, y2, y1 = curmod, r, x1, x, y1, y

    return x2 % modulus


class Curve:
    """Implement an elliptic curve, y² = x³ + ax + b."""

    __slots__ = ("a", "b", "field", "basepoint", "order", "name")

    def __init__(
        self,
        a: int,
        b: int,
        field: int,
        basepoint: t.Tuple[int, int],
        order: int,
        name: t.Optional[str] = None,
    ) -> None:
        """Initialize an elliptic curve."""
        self.a = a
        self.b = b
        self.field = field
        # The prime order of the field on which to do computations
        self.basepoint = Point(*basepoint, self)
        self.order = order
        # The order of the basepoint
        self.name = name

    def __contains__(self, point: "Point") -> bool:
        """Check if the point is on the curve."""
        return (
            point.infinity
            or (point.x ** 3 + self.a * point.x + self.b - point.y ** 2) % self.field
            == 0
        )

    def __repr__(self) -> str:
        """Return the canonical of self."""
        return f"<{str(self)}>"

    def __str__(self) -> str:
        """Return the string representation of self."""
        if self.name:
            return f"Curve {self.name}"
        return f"Curve y² = x³ + {self.a}x + {self.b}"


class Point:
    """A point on an elliptic curve."""

    __slots__ = ("x", "y", "curve")

    infinity = False

    def __init__(self, x: int, y: int, curve: Curve) -> None:
        """Initialize a Point.

        :param x: The x coordinate of the point
        :type x: int
        :param y: The y coordinate of the point
        :type y: int
        :param curve: The elliptic curve on which the point is situated
        :type curve: Curve
        :raises ValueError: The point isn't on the given curve
        """
        self.x = x % curve.field
        self.y = y % curve.field
        self.curve = curve

        if self not in curve:
            raise ValueError(f"({x}, {y}) is not on the curve {curve}!")

    def __eq__(self, other: object) -> bool:
        """Check if two points are equal."""
        if not isinstance(other, Point):
            return False

        if other.infinity:
            return False
        return (self.x, self.y, self.curve) == (other.x, other.y, other.curve)

    def __sub__(self, other: "Point") -> "Point":
        """Substract two points."""
        return self + (-other)

    def __ne__(self, other: object) -> bool:
        """Implement self != other."""
        if not isinstance(other, Point):
            return True
        if other.infinity:
            return True
        return (self.x, self.y, self.curve) != (other.x, other.y, other.curve)

    def __neg__(self) -> "Point":
        """Negate a point."""
        return Point(self.x, -self.y, self.curve)

    def __add__(self, other: "Point") -> "Point":
        """Add two points."""
        if other.infinity:
            return self

        if self == other:
            return self.double()

        if self.x == other.x:
            return Infinity(self.curve)

        lamb = (other.y - self.y) * mod_inverse(other.x - self.x, self.curve.field)

        xres = lamb ** 2 - self.x - other.x
        return Point(
            xres,
            lamb * (self.x - xres) - self.y,
            self.curve,
        )

    def __mul__(self, other: int) -> t.Union["Point", "Infinity"]:
        """Multiply a point by a scalar."""
        res: t.Union[Point, Infinity] = Infinity(self.curve)
        other = other % self.curve.field

        current = self

        while other:
            if other & 1:
                res += current
            current = current.double()
            other >>= 1
        return res

    __rmul__ = __mul__

    def double(self) -> "Point":
        """Double a Point."""
        if self.y == 0:
            return Infinity(self.curve)

        lamb = (
            (3 * self.x ** 2 + self.curve.a)
            * mod_inverse(2 * self.y, self.curve.field)
            % self.curve.field
        )

        xres = (lamb ** 2 - 2 * self.x) % self.curve.field
        return Point(
            xres,
            lamb * (self.x - xres) - self.y,
            self.curve,
        )

    def __repr__(self) -> str:
        """Return the canonical of self."""
        return f"<{str(self)}>"

    def __str__(self) -> str:
        """Return the string representation of self."""
        return f"Point({self.x}, {self.y}) on {self.curve}"


class Infinity(Point):
    """Represent the infinity point on a curve."""

    __slots__ = ()

    infinity = True

    def __init__(self, curve: Curve) -> None:
        """Initialize self."""
        super().__init__(0, 0, curve)

    def __add__(self, other: Point) -> Point:
        """Implement self + other."""
        return other

    def __eq__(self, other: object) -> bool:
        """Implement self == other."""
        return isinstance(other, Infinity)

    def __ne__(self, other: object) -> bool:
        """Implement self != other."""
        return not isinstance(other, Infinity)

    def __neg__(self) -> "Infinity":
        """Implement -self."""
        return self

    def __mul__(self, _: int) -> "Infinity":
        """Implement other * self."""
        return self

    __rmul__ = __mul__

    def double(self) -> "Infinity":
        """Double self."""
        return self

    def __str__(self) -> str:
        """Return the string representation of self."""
        return f"Infinity point on {self.curve}"


SECP256K1 = Curve(
    0,
    7,
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    (
        0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
        0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    ),
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    "secp256k1"
)


def gen_private(curve: Curve = SECP256K1) -> t.Tuple[Point, int]:
    """Generate a public key / private key tuple."""
    k = randint(1, curve.order - 1)
    return k * curve.basepoint, k


def load_ecdh(point: Point, private: int) -> int:
    """Generate the shared secret."""
    return (private * point).x


def sign_ecdsa(
    message: str, private: int, curve: Curve = SECP256K1
) -> t.Tuple[int, int]:
    """Sign a message with ECDSA."""
    hashed = int(sha256(message), base=16)
    nonce = randint(1, curve.order - 1)

    point = nonce * curve.basepoint
    if (point.x % curve.order) == 0:
        return sign_ecdsa(message, private, curve)

    term = (
        mod_inverse(nonce, curve.order) * (hashed + private * point.x)
    ) % curve.order

    if term == 0:
        return sign_ecdsa(message, private, curve)

    return point.x, term


def verify_ecdsa(message: str, public: Point, signature: t.Tuple[int, int]) -> bool:
    """Verify an ECDSA signature."""
    x, y = signature
    if not (1 <= x < public.curve.order and 1 <= y < public.curve.order):
        return False

    hashed = int(sha256(message), base=16)

    w = mod_inverse(y, public.curve.order)

    point = ((hashed * w) % public.curve.order) * public.curve.basepoint + (
        (x * w) % public.curve.order
    ) * public
    return x == point.x % public.curve.order
