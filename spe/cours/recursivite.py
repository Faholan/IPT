"""Cours sur la récursivité."""

import typing as t


Numeric = t.Union[int, float]


def suite(f: t.Callable[[Numeric], Numeric], n: int, u0: Numeric) -> Numeric:
    """Calculate the nth term of the suite."""
    if n:
        return f(suite(f, n - 1, u0))
    return u0


def binome(n: int, p: int) -> int:
    """Calculate p in n."""
    if p > n:
        return 0
    if p:
        return binome(n-1, p) + binome(n-1, p-1)
    return 1


def binaire(n: int) -> t.List[int]:
    """Calculate the binary representation of n."""
    if n == 0:
        return [0]
    if n == 1:
        return [1]
    result = binaire(n // 2)
    result.append(n % 2)
    return result


def base2tobase10(base: t.List[int]) -> int:
    """Convert from base 2 to base 10."""
    if not base:
        return 0
    return base.pop() + (base2tobase10(base) << 1)
