# uninformed.py: Store uninformed search algorithms
from models.node import Node
from models.map import Map
from typing import List, Dict, Any

class DFSPathFinder:
    def __init__(self, map_obj: Map):
        self.map = map_obj
        self.n = map_obj.n
        self.visited = set()
        self.stack = []
        self.result = None

        def _dfs(self, node) -> Dict:
            if (node.x, node.y) == (self.n - 1, self.n - 1):
                self.result = {
                    "path": node.path,
                    "coins": node.coins,
                    "stolen": 0  # No matter if the thief is stolen or not
                }
                return True # Finding the goal
            
            self.visited.add((node.x, node.y))

            for dx, dy in [(1, 0), (0, 1)]:
                new_x = node.x + dx
                new_y = node.y + dy

                if self.map.is_valid(new_x, new_y) and (new_x, new_y) not in self.visited:
                    next_node = node.copy()
                    next_node.x = new_x
                    next_node.y = new_y
                    next_node.path.append((new_x, new_y))

                    curr_cell = self.map.get_cell(node.x, node.y)
                    next_cell = self.map.get_cell(new_x, new_y)
