"""TD Python SQL."""

import typing as t


Record = t.List[str]
Table = t.List[Record]


def select_constante(table: Table, indice: int, constante: str) -> t.List[Record]:
    """Select avec une constante."""
    return [record for record in table if record[indice] == constante]


def select_egalite(table: Table, indice1: int, indice2: int) -> t.List[Record]:
    """SELECT avec une égalité d'attributs."""
    return [record for record in table if record[indice1] == record[indice2]]


def project_record(record: Record, liste_indice: t.List[int]) -> Record:
    """Project attributes."""
    return [record[i] for i in liste_indice]


def project(table: Table, liste_indice: t.List[int]) -> Table:
    """Project a table."""
    return [project_record(record, liste_indice) for record in table]


def produit_cartesien(table1: Table, table2: Table) -> Table:
    """Cross join of two tables."""
    return [record1 + record2 for record1 in table1 for record2 in table2]
