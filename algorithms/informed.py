# informed.py: Store informed search algorithms
from heapq import heappush, heappop
from models.node import Node
from models.map import Map
from typing import Dict
from config import THIEF, DIRECTION
from algorithms.PathFinder import PathFinder
import itertools

class AStarMaxProfitPathFinder(PathFinder):
    def __init__(self, map_obj: Map):
        super().__init__(map_obj)
        self.__algorithm_name = "A* Max Profit"
        self.map = map_obj
        self.n = map_obj.n
        self._counter = itertools.count()

    def algorithm_name(self) -> str:
        return self.__algorithm_name

    def solve(self) -> Dict:
        start_val = self.map.get_cell(0, 0)
        start_coins = start_val if isinstance(start_val, int) else 0
        start_thief = start_val == THIEF
        start_node = Node(0, 0, [(0, 0)], start_coins, start_thief)

        open_set = []
        heappush(open_set, (-self._f(start_node), next(self._counter), start_node))
        came_from = {}
        g_score = {(0, 0): start_coins}

        while open_set: # pop the node with the highest profit

            # f(n) = g(n) + h(n)
            # g(n) = coins collected
            # h(n) = heuristic (max profit)
            _, _, current = heappop(open_set) 
 
            if (current.x, current.y) == (self.n - 1,self.n - 1):
                return {
                    "path": current.path,
                    "coins": current.coins,
                    "stolen": current.stolen
                }

            for dx, dy in DIRECTION:
                new_x = current.x + dx
                new_y = current.y + dy

                if self.map.is_valid_move(new_x, new_y):
                    next_node = current.copy()
                    next_node.x = new_x
                    next_node.y = new_y
                    next_node.path.append((new_x, new_y))

                    next_cell = self.map.get_cell(new_x, new_y)
                    if current.has_thief:
                        if next_cell == THIEF:
                            next_node.has_thief = False 
                        elif isinstance(next_cell, int):
                            if next_cell > 0:
                                next_node.stolen += next_cell
                            else:
                                next_node.coins += next_cell
                                next_node.stolen += abs(next_cell) 
                            next_node.has_thief = False
                    else:
                        if next_cell == THIEF:
                            next_node.has_thief = True
                        elif isinstance(next_cell, int):
                            next_node.coins += next_cell

                    tentative_g_score = next_node.coins
                    if (new_x, new_y) not in g_score or tentative_g_score > g_score[(new_x, new_y)]:
                        g_score[(new_x, new_y)] = tentative_g_score
                        heuristic = self._heuristic_max_profit(new_x, new_y)
                        f_score = tentative_g_score + heuristic
                        heappush(open_set, (-f_score, next(self._counter), next_node))
                        came_from[(new_x, new_y)] = current

        return {"path": [], "coins": 0, "stolen": 0}

    def _f(self, node: Node) -> int:
        heuristic = self._heuristic_max_profit(node.x, node.y)
        return node.coins + heuristic

    def _heuristic_max_profit(self, x: int, y: int) -> int:
        steps_left = (self.n - 1 - x) + (self.n - 1 - y)
        
        # Find the maximum coin value in the remaining cells
        max_coin = 0
        for i in range(x, self.n):
            for j in range(y, self.n):
                cell = self.map.get_cell(i, j)
                if isinstance(cell, int) and cell > max_coin:
                    max_coin = cell

        return max(0, max_coin * steps_left)
    

class AStarMinLossPathFinder(PathFinder):
    def __init__(self, map_obj: Map):
        super().__init__(map_obj)
        self.__algorithm_name = "A* Min Loss"
        self.map = map_obj
        self.n = map_obj.n
        self._counter = itertools.count()

    def algorithm_name(self) -> str:
        return self.__algorithm_name

    def solve(self) -> Dict:
        start_val = self.map.get_cell(0, 0)
        start_coins = start_val if isinstance(start_val, int) else 0
        start_thief = start_val == THIEF
        start_node = Node(0, 0, [(0, 0)], start_coins, start_thief, 0)

        open_set = []
        heappush(open_set, (self._f(start_node), next(self._counter), start_node))
        came_from = {}
        g_score = {(0, 0): 0} 

        while open_set:
            _, _, current = heappop(open_set)

            if (current.x, current.y) == (self.n - 1, self.n - 1):
                return {
                    "path": current.path,
                    "coins": current.coins,
                    "stolen": current.stolen
                }

            for dx, dy in DIRECTION:
                new_x = current.x + dx
                new_y = current.y + dy

                if self.map.is_valid_move(new_x, new_y):
                    next_node = current.copy()
                    next_node.x = new_x
                    next_node.y = new_y
                    next_node.path.append((new_x, new_y))

                    next_cell = self.map.get_cell(new_x, new_y)
                    if current.has_thief:
                        if next_cell == THIEF:
                            next_node.has_thief = False 
                        elif isinstance(next_cell, int):
                            if next_cell > 0:
                                next_node.stolen += next_cell 
                            else:
                                next_node.coins += next_cell 
                                next_node.stolen += abs(next_cell) 
                            next_node.has_thief = False
                    else:
                        if next_cell == THIEF:
                            next_node.has_thief = True
                        elif isinstance(next_cell, int):
                            next_node.coins += next_cell

                    tentative_g_score = next_node.stolen
                    if (new_x, new_y) not in g_score or tentative_g_score < g_score[(new_x, new_y)]:
                        g_score[(new_x, new_y)] = tentative_g_score
                        heuristic = self._heuristic_min_loss(new_x, new_y)
                        f_score = tentative_g_score + heuristic
                        heappush(open_set, (f_score, next(self._counter), next_node))
                        came_from[(new_x, new_y)] = current

        return {"path": [], "coins": 0, "stolen": 0}

    def _f(self, node: Node) -> int:
        # f(n) = g(n) + h(n)
        # g(n) = stolen coins
        # h(n) = heuristic (min loss)
        heuristic = self._heuristic_min_loss(node.x, node.y)
        return node.stolen + heuristic

    @staticmethod
    def _heuristic_min_loss(x: int, y: int) -> int:
        # Simple admissible heuristic: minimum stolen coins is 0
        return 0
