"""Sudoku solver by backtracking.

Copyright (C) 2021  Faholan <https://github.com/Faholan>
"""

import tkinter as tk
from tkinter import messagebox
import typing as t
from time import time_ns

Sudoku = t.List[t.List[int]]
History = t.List[t.Tuple[int, int, int]]


def test(grid: Sudoku, i: int, j: int, num: int) -> bool:
    """Check if num can be placed in (i, j)."""
    for k in range(9):
        if num in (grid[i][k], grid[k][j]):
            return False  # Check the row and column

    i0, j0 = 3 * (i // 3), 3 * (j // 3)
    # Coordonnées de la base du carré
    for k in range(3):
        for kk in range(3):
            if grid[i0 + k][j0 + kk] == num:
                return False

    return True


def trouve_zero(grid: Sudoku) -> t.Tuple[int, int]:
    """Return the first empty cell, or -1, -1."""
    for i in range(9):
        for j in range(9):
            if not grid[i][j]:
                return i, j

    return -1, -1


def sudoku(grid: Sudoku) -> Sudoku:
    """Solve the given grid."""
    new_grid = [row.copy() for row in grid]
    history: History = []

    while True:
        i, j = trouve_zero(new_grid)
        if i == -1:
            return new_grid
        insert_val = 0
        for num in range(1, 10):
            if test(new_grid, i, j, num):
                insert_val = num
                break
        if insert_val:
            history.append((insert_val, i, j))
            new_grid[i][j] = insert_val
        else:
            _backtrack(new_grid, history)


def _backtrack(grid: Sudoku, history: History) -> None:
    """Apply the backtracking algorithm."""
    if not history:
        raise ValueError("This Sudoku has no solution !")
    val, i, j = history.pop()
    for new_val in range(val + 1, 10):
        if test(grid, i, j, new_val):
            history.append((new_val, i, j))
            grid[i][j] = new_val
            return

    grid[i][j] = 0
    _backtrack(grid, history)


def timed_sudoku(grid: Sudoku) -> Sudoku:
    """Time the solving of the Sudoku."""
    start = time_ns()
    solution = sudoku(grid)
    print(f"Solving this Sudoku took {(time_ns() - start) / 0x3b9aca00}")
    return solution


def pretty_print(grid: Sudoku) -> None:
    """Print a Sudoku grid, but nicely."""
    print("\n".join(str(row) for row in grid) + "\n")


def voisins(i: int, j: int) -> t.List[t.Tuple[int, int]]:
    """List the neighbours of (i, j)."""
    result: t.List[t.Tuple[int, int]] = []

    if i >= 2:
        if j >= 1:
            result.append((i - 2, j - 1))
        if j <= 7:
            result.append((i - 2, j + 1))

    if j >= 2:
        if i >= 1:
            result.append((i - 1, j - 2))
        if i <= 7:
            result.append((i + 1, j - 2))

    if i <= 6:
        if j >= 1:
            result.append((i + 2, j - 1))
        if j <= 7:
            result.append((i + 2, j + 1))

    if j >= 6:
        if i >= 1:
            result.append((i - 1, j + 2))
        if i <= 7:
            result.append((i + 1, j + 2))

    return result


def test_cavalier(grid: Sudoku, i: int, j: int, num: int) -> bool:
    """Test with cavalryman rule."""
    return test(grid, i, j, num) and all(
        grid[k][l] != num for k, l in voisins(i, j)
    )


def sudoku_cavalier(grid: Sudoku) -> Sudoku:
    """Solve the given grid."""
    new_grid = [row.copy() for row in grid]
    history: History = []

    while True:
        i, j = trouve_zero(new_grid)
        if i == -1:
            return new_grid
        insert_val = 0
        for num in range(1, 10):
            if test_cavalier(new_grid, i, j, num):
                insert_val = num
                break
        if insert_val:
            history.append((insert_val, i, j))
            new_grid[i][j] = insert_val
        else:
            _backtrack_cavalier(new_grid, history)


def _backtrack_cavalier(grid: Sudoku, history: History) -> None:
    """Apply the backtracking algorithm."""
    if not history:
        raise ValueError("This Sudoku has no solution !")
    val, i, j = history.pop()
    for new_val in range(val + 1, 10):
        if test_cavalier(grid, i, j, new_val):
            history.append((new_val, i, j))
            grid[i][j] = new_val
            return

    grid[i][j] = 0
    _backtrack_cavalier(grid, history)


def sudoku_all(grid: Sudoku) -> t.List[Sudoku]:
    """Get all solutions for the given grid."""
    new_grid = copy(grid)

    solutions: t.List[Sudoku] = []
    history: History = []
    try:
        while True:
            i, j = trouve_zero(new_grid)
            if i == -1:
                solutions.append(copy(new_grid))
                low, i, j = history.pop()
                new_grid[i][j] = 0
            else:
                low = 0
            insert_val = 0
            for num in range(low + 1, 10):
                if test(new_grid, i, j, num):
                    insert_val = num
                    break
            if insert_val:
                history.append((insert_val, i, j))
                new_grid[i][j] = insert_val
            else:
                _backtrack(new_grid, history)
    except ValueError:
        return solutions


def copy(entry: Sudoku) -> Sudoku:
    """Copy a sudoku."""
    return [row.copy() for row in entry]


KEYMAPPING = (
    ("&", 1),
    ("<eacute>", 2),
    ('"', 3),
    ("'", 4),
    ("(", 5),
    ("-", 6),
    ("<egrave>", 7),
    ("_", 8),
    ("<ccedilla>", 9),
    ("<agrave>", 0),
    ("<BackSpace>", 0),
)


class Cell:
    """Sudoku cell."""

    def __init__(
        self, master: "Window", frame: tk.Frame, row: int, column: int
    ) -> None:
        """Initialize the cell."""
        self.master = master
        self._row = row
        self._column = column
        self.canvas = tk.Canvas(
            frame,
            height=master.cell_size,
            width=master.cell_size,
            bg=self.color,
        )
        self.value = 0
        self.canvas.grid(row=(row % 3), column=(column % 3))
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<Button-3>", self.click)
        self.isselected = False

    @property
    def color(self) -> str:
        """Get the valid default color."""
        return self.master.default_bg[
            (self._column + self._row) % 2
        ]

    @property
    def line_color(self) -> str:
        """Get the valid line color."""
        return self.master.line_bg[
            (self._column + self._row) % 2
        ]

    def __eq__(self, other: object) -> bool:
        """Implement self == other."""
        return isinstance(other, Cell) and (self._row, self._column) == (
            other._row,
            other._column,
        )

    def update(self, value: int) -> None:
        """Update the value and its display."""
        self.value = value
        self.canvas.delete(tk.ALL)
        if value:
            self.canvas.create_text(
                self.master.cell_size / 2,
                self.master.cell_size / 2,
                text=str(value),
                fill=(
                    self.master.selected_fg
                    if self.isselected
                    else self.master.default_fg
                ),
                font=self.master.font,
            )

    def unselect(self) -> None:
        """Unselect the cell."""
        for k in range(9):
            rowk = self.master.grid[self._row][k]
            rowk.canvas.config(bg=rowk.color)
            columnk = self.master.grid[k][self._column]
            columnk.canvas.config(bg=columnk.color)
        self.isselected = False
        self.update(self.value)

    def click(self, _: t.Any) -> None:
        """Bind the left click."""
        if self == self.master.selected:
            return

        if self.master.selected:
            self.master.selected.unselect()

        for k in range(9):
            rowk = self.master.grid[self._row][k]
            rowk.canvas.config(bg=rowk.line_color)
            columnk = self.master.grid[k][self._column]
            columnk.canvas.config(bg=columnk.line_color)

        self.canvas.config(bg=self.master.selected_bg)
        self.master.selected = self
        self.isselected = True
        self.update(self.value)


class Window:
    """Sudoku window class."""

    cell_size = 50  # Cell size, in bits
    default_bg = ("darkgrey", "lightgrey")
    default_fg = "black"
    selected_bg = "darkblue"
    selected_fg = "white"
    line_bg = ("royalblue", "lightblue")
    font = "arial 15"

    def __init__(self, grid: t.Optional[Sudoku] = None) -> None:
        """Initialize self."""
        self.main = tk.Tk()
        self.main.title("Sudoku displayer")
        self.selected: t.Optional[Cell] = None
        self.grid = self.create_grid()
        self.init_menu()

        for i in range(1, 10):
            button = tk.Button(
                self.main, text=str(i), command=self.updater(i), font=self.font
            )
            button.grid(row=9, column=i - 1, sticky=tk.NSEW)
            self.main.bind(str(i), self.updater(i))

        self.main.bind(str(0), self.updater(0))

        for key, val in KEYMAPPING:
            self.main.bind(key, self.updater(val))

        if grid:
            for i in range(9):
                for j in range(9):
                    self.grid[i][j].update(grid[i][j])

        self.main.resizable(False, False)
        self.main.mainloop()

    def updater(self, value: int) -> t.Callable[..., None]:
        """Define the action of a button, or a key."""

        def callback(_: t.Any = None) -> None:
            """Actual event manager."""
            if self.selected:
                self.selected.update(value)

        return callback

    def init_menu(self) -> None:
        """Initialize the solver menu."""
        menu = tk.Menu(self.main, tearoff=0)

        def popup(event: t.Any) -> None:
            """Popup the menu."""
            menu.post(event.x_root, event.y_root)  # type: ignore

        def reset() -> None:
            """Reset the selected case."""
            if self.selected:
                self.selected.update(0)

        def reset_all() -> None:
            """Reset the sudoku."""
            for i in range(9):
                for j in range(9):
                    self.grid[i][j].update(0)

        menu.add_command(label="Solve Sudoku", command=self.solve)
        menu.add_command(label="Reset selected cell", command=reset)
        menu.add_command(label="Reset Sudoku", command=reset_all)
        self.main.bind("<Button-3>", popup)

    def solve(self) -> None:
        """Solve the Sudoku currently displayed."""
        grid = [[self.grid[i][j].value for j in range(9)] for i in range(9)]
        if not self.isvalid(grid):
            messagebox.showerror(
                "Invalid sudoku",
                "The sudoku cannot be solved, because it isn't valid."
            )
            return

        try:
            solved = sudoku(grid)
        except ValueError:
            messagebox.showerror(
                "Invalid sudoku",
                "This sudoku doesn't have a solution",
            )
        else:
            for i in range(9):
                for j in range(9):
                    self.grid[i][j].update(solved[i][j])

    @staticmethod
    def isvalid(grid: Sudoku) -> bool:
        """Check if a partial grid is valid."""
        for i in range(9):
            for j in range(9):
                if grid[i][j]:
                    val = grid[i][j]
                    grid[i][j] = 0
                    if not test(grid, i, j, val):
                        return False
                    grid[i][j] = val

        return True

    def create_grid(self) -> t.List[t.List["Cell"]]:
        """Create the grid."""
        framelist: t.List[t.List[tk.Frame]] = []
        for i in range(3):
            framelist.append([])
            for j in range(3):
                framelist[-1].append(
                    tk.Frame(
                        self.main,
                        highlightbackground="black",
                        highlightthickness=1,
                    )
                )
                framelist[-1][-1].grid(
                    row=3 * i,
                    column=3 * j,
                    rowspan=3,
                    columnspan=3
                )
        cellist: t.List[t.List[Cell]] = []
        for i in range(9):
            cellist.append([])
            for j in range(9):
                cellist[-1].append(Cell(self, framelist[i//3][j//3], i, j))

        return cellist


# grille facile
EASY = [
    [0, 1, 0, 0, 5, 2, 0, 0, 7],
    [0, 8, 0, 7, 0, 0, 0, 1, 0],
    [9, 0, 2, 0, 6, 1, 5, 0, 0],
    [4, 0, 0, 2, 0, 0, 7, 0, 0],
    [8, 0, 1, 0, 7, 0, 2, 0, 4],
    [0, 0, 7, 0, 0, 5, 0, 0, 9],
    [0, 0, 6, 5, 3, 0, 9, 0, 8],
    [0, 9, 0, 0, 0, 4, 0, 5, 0],
    [2, 0, 0, 9, 8, 0, 0, 7, 0],
]

# grille moyenne
MEDIUM = [
    [0, 6, 0, 0, 0, 0, 9, 8, 5],
    [0, 0, 5, 6, 0, 9, 0, 0, 0],
    [0, 0, 7, 0, 0, 0, 0, 4, 0],
    [0, 2, 0, 9, 0, 0, 0, 0, 8],
    [0, 7, 0, 5, 0, 1, 0, 6, 0],
    [1, 0, 0, 0, 0, 3, 0, 9, 0],
    [0, 1, 0, 0, 0, 0, 4, 0, 0],
    [0, 0, 0, 3, 0, 6, 8, 0, 0],
    [6, 5, 9, 0, 0, 0, 0, 1, 0],
]

# grille difficile
HARD = [
    [0, 0, 0, 3, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 7, 0],
    [2, 0, 8, 0, 9, 0, 0, 5, 0],
    [6, 9, 0, 0, 0, 2, 0, 0, 0],
    [4, 0, 1, 0, 3, 0, 2, 0, 7],
    [0, 0, 0, 9, 0, 0, 0, 1, 5],
    [0, 1, 0, 0, 7, 0, 8, 0, 3],
    [0, 4, 6, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 0, 3, 0, 0, 0],
]


if __name__ == "__main__":
    # pretty_print(timed_sudoku(EASY))
    # pretty_print(timed_sudoku(MEDIUM))
    # pretty_print(timed_sudoku(HARD))
    Window(HARD)
