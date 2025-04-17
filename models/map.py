# map model: represents a map of the world

from typing import List, Dict, Any

class Map:
    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.n = len(grid)
    
    def get_cell(self, x: int, y: int) -> int:
        if 0 <= x < self.n and 0 <= y < self.n:
            return self.grid[x][y]
        else:
            raise IndexError("Coordinates out of bounds")
    
    def is_valid_move(self, x: int, y: int) -> bool:
        return 0 <= x < self.n and 0 <= y < self.n