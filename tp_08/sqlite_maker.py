"""Admissibles database maker.

Create a Sqlite database from the admissibles.txt file
"""
import sqlite3


def main() -> None:
    """Create a sqlite database."""
    conn = sqlite3.connect(r"fichierSortie\admissibles.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS admissibles")
    cursor.execute(
        "CREATE TABLE admissibles ("
        "identifiant INT NOT NULL, "
        "nom TEXT NOT NULL, "
        "prenom TEXT NOT NULL, "
        "admissible BOOLEAN NOT NULL, "
        "serie INT)"
    )
    with open(r"fichierEntree\admissibles.txt", encoding="utf-8") as file:
        line = "foo"
        while line:
            line = file.readline().strip()
            if not line:
                continue
            identifier, raw_name, raw_status, raw_rank = line.split("\t")
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
            status = raw_status == "Admissible"
            rank = int(raw_rank) if status else None
            cursor.execute(
                "INSERT INTO admissibles VALUES (?, ?, ?, ?, ?)",
                (
                    int(identifier),
                    last,
                    first,
                    status,
                    rank,
                ),
            )
    cursor.close()
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
