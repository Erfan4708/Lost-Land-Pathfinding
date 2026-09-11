# PathFinder.py: Base class shared by every search algorithm.

from abc import ABC, abstractmethod
from typing import Dict

from config import THIEF
from models.map import Map
from models.node import Node


class PathFinder(ABC):
    """
    Abstract base class for pathfinding algorithms.

    Subclasses only have to implement `solve()`. The rules of the world
    (how coins are collected and how thieves behave) are implemented here
    once so that every algorithm plays by the same rules.
    """

    algorithm_name = "PathFinder"

    def __init__(self, map_obj: Map):
        self.map = map_obj
        self.n = map_obj.n
        self.goal = (self.n - 1, self.n - 1)

    @abstractmethod
    def solve(self) -> Dict:
        """
        Search the map and return a result dictionary with the keys
        "path", "coins" and "stolen". An empty path means no path was found.
        """

    def start_node(self) -> Node:
        """Node for the top-left corner, where Arian always starts."""
        cell = self.map.get_cell(0, 0)
        coins = 0 if cell == THIEF else cell
        return Node(0, 0, [(0, 0)], coins, cell == THIEF)

    def move(self, node: Node, x: int, y: int) -> Node:
        """
        Return the node reached by stepping from `node` onto the cell (x, y).

        Rules of the world:
          * a numeric cell is added to Arian's coins;
          * stepping on a thief cell makes that thief follow him;
          * a following thief robs the next cell (its value is counted as
            stolen instead of collected) and then leaves.
        """
        next_node = node.copy()
        next_node.x = x
        next_node.y = y
        next_node.path.append((x, y))

        cell = self.map.get_cell(x, y)
        if node.has_thief:
            # The thief robs this cell and disappears afterwards.
            next_node.has_thief = False
            if cell != THIEF:
                if cell > 0:
                    next_node.stolen += cell
                else:
                    next_node.coins += cell
                    next_node.stolen += abs(cell)
        else:
            next_node.has_thief = cell == THIEF
            if cell != THIEF:
                next_node.coins += cell

        return next_node

    def is_goal(self, node: Node) -> bool:
        return (node.x, node.y) == self.goal

    @staticmethod
    def result(node: Node) -> Dict:
        return {"path": node.path, "coins": node.coins, "stolen": node.stolen}

    @staticmethod
    def no_result() -> Dict:
        return {"path": [], "coins": 0, "stolen": 0}
