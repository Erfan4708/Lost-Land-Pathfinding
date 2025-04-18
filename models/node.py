# node model: represents a node in the graph
from typing import List, Dict, Any

class Node:
    def __init__(self, x: int, y: int, path: List[(int, int)], coins: int, has_thief: bool):
        self.x = x
        self.y = y
        self.path = path if path else [(x, y)]
        self.coins = coins
        self.has_thief = has_thief
