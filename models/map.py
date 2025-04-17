# map model: represents a map of the world

from typing import List, Dict, Any

class Map:
    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.n = len(grid)