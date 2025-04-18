# node model: represents a node in the graph
from typing import List, Dict, Any

class Node:
    def __init__(self, x: int, y: int, path: List[(int, int)], coins: int, has_thief: bool):
        self.x = x
        self.y = y
        self.path = path if path else [(x, y)]
        self.coins = coins
        self.has_thief = has_thief

    def __repr__(self) -> str:
        return f"Node(x={self.x}, y={self.y}, path={self.path}, coins={self.coins}, has_thief={self.has_thief})"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "path": self.path,
            "coins": self.coins,
            "has_thief": self.has_thief
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        self.x = data.get("x", 0)
        self.y = data.get("y", 0)
        self.path = data.get("path", [(self.x, self.y)])
        self.coins = data.get("coins", 0)
        self.has_thief = data.get("has_thief", False)
        