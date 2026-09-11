# uninformed.py: Store uninformed search algorithms

from typing import Dict

from algorithms.PathFinder import PathFinder
from config import DIRECTIONS
from models.map import Map
from models.node import Node


class DFSPathFinder(PathFinder):
    """
    Depth-first search. It answers the first question of the assignment:
    find *any* way out of the land, without caring about the coins.
    """

    algorithm_name = "DFS"

    def __init__(self, map_obj: Map):
        super().__init__(map_obj)
        self.visited = set()
        self.result_path = None

    def solve(self) -> Dict:
        self._dfs(self.start_node())
        return self.result_path if self.result_path else self.no_result()

    def _dfs(self, node: Node) -> bool:
        if self.is_goal(node):
            self.result_path = self.result(node)
            return True

        self.visited.add((node.x, node.y))

        for dx, dy in DIRECTIONS:
            new_x = node.x + dx
            new_y = node.y + dy

            if self.map.is_valid_move(new_x, new_y) and (new_x, new_y) not in self.visited:
                if self._dfs(self.move(node, new_x, new_y)):
                    return True

        self.visited.remove((node.x, node.y))
        return False
