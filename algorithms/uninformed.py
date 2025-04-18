# uninformed.py: Store uninformed search algorithms

from models.node import Node
from models.map import Map
from typing import Dict
from algorithms.PathFinder import PathFinder


class DFSPathFinder(PathFinder):
    def __init__(self, map_obj: Map):
        super().__init__(map_obj)
        self.__algorithm_name = "DFS"
        self.map = map_obj
        self.n = map_obj.n
        self.visited = set()
        self.result = None

    def algorithm_name(self) -> str:
        return self.__algorithm_name

    def solve(self) -> Dict:
        start_val = self.map.get_cell(0, 0)
        start_coins = start_val if isinstance(start_val, int) else 0
        start_thief = start_val == "!"
        start_node = Node(0, 0, [(0, 0)], start_coins, start_thief)

        self._dfs(start_node)
        return self.result if self.result else {"path": [], "coins": 0, "stolen": 0}

    def _dfs(self, node) -> bool:
        if (node.x, node.y) == (self.n - 1, self.n - 1):
            self.result = {
                "path": node.path,
                "coins": node.coins,
                "stolen": 0  # No matter if the thief is stolen or not
            }
            return True  # Finding the goal

        self.visited.add((node.x, node.y))

        for dx, dy in [(1, 0), (0, 1)]:
            new_x = node.x + dx
            new_y = node.y + dy

            if self.map.is_valid_move(new_x, new_y) and (new_x, new_y) not in self.visited:
                next_node = node.copy()
                next_node.x = new_x
                next_node.y = new_y
                next_node.path.append((new_x, new_y))

                curr_cell = self.map.get_cell(node.x, node.y)
                next_cell = self.map.get_cell(new_x, new_y)

                if curr_cell == "!":
                    next_node.has_thief = True

                if next_node.has_thief:
                    if next_cell == "!":
                        next_node.has_thief = False  # two thieves cancel each other
                    elif isinstance(next_cell, int):
                        if next_cell > 0:
                            pass
                        else:
                            next_node.coins += next_cell
                            next_node.coins -= abs(next_cell)
                        next_node.has_thief = False
                else:
                    if isinstance(next_cell, int):
                        next_node.coins += next_cell

                if self._dfs(next_node):
                    return True

        self.visited.remove((node.x, node.y))
        return False
