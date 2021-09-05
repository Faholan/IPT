from typing import Iterable, List, Tuple


def gauss(table: List[Iterable[int]]) -> List[Tuple[int]]:
    """Implement the Gauss algorithm."""
    for row in table:
        if len(row) != len(table[0]):
            raise ValueError("All rows must be of equal length.")
        for elem in row:
            if not isinstance(elem, int):
                raise TypeError("All elements must be integers.")
    return __gauss__(table)


def __gauss__(table: list) -> list:
    if len(table) == 1:
        return table
    i = 0
    while i < len(table[0]) and not table[0][i]:
        i += 1
    if not table[0][i]:
        return [table[0]] + __gauss__(table[1:])
    return [table[0]] + __gauss__(
        [
            tuple(
                row[j]
                - table[0][j] * (row[i] / table[0][i])
                for j in range(len(table[0]))
            ) for row in table[1:]
        ]
    )
