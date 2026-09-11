# map model: represents a map of the world

from typing import Any, List


class Map:
    """
    A square grid of cells. Each cell is either a number of coins or the
    thief marker. The class only knows about the grid itself; the rules of
    the game live in the pathfinding algorithms.
    """

    def __init__(self, grid: List[List[Any]]):
        if not grid or any(len(row) != len(grid) for row in grid):
            raise ValueError("The map must be a non-empty square grid")
        self.grid = grid
        self.n = len(grid)

    def get_cell(self, x: int, y: int) -> Any:
        if not self.is_valid_move(x, y):
            raise IndexError("Coordinates out of bounds")
        return self.grid[x][y]

    def is_valid_move(self, x: int, y: int) -> bool:
        return 0 <= x < self.n and 0 <= y < self.n
