# node model: represents a node in the search tree

from typing import List, Tuple


class Node:
    """
    One state of the search: where Arian stands, how he got there, how many
    coins he holds, how many were stolen from him and whether a thief is
    currently following him.
    """

    def __init__(
        self,
        x: int,
        y: int,
        path: List[Tuple[int, int]],
        coins: int,
        has_thief: bool,
        stolen: int = 0,
    ):
        self.x = x
        self.y = y
        self.path = path if path else [(x, y)]
        self.coins = coins
        self.has_thief = has_thief
        self.stolen = stolen

    def copy(self) -> 'Node':
        return Node(
            self.x,
            self.y,
            self.path.copy(),
            self.coins,
            self.has_thief,
            self.stolen
        )

    def __repr__(self) -> str:
        return (
            f"Node(x={self.x}, y={self.y}, path={self.path}, "
            f"coins={self.coins}, stolen={self.stolen}, "
            f"has_thief={self.has_thief})"
        )
