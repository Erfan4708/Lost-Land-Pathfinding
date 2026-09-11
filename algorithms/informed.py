# informed.py: Store informed search algorithms

import itertools
from heapq import heappush, heappop
from typing import Dict

from algorithms.PathFinder import PathFinder
from config import DIRECTIONS, THIEF
from models.map import Map
from models.node import Node


class AStarMaxProfitPathFinder(PathFinder):
    """
    A* that looks for the path with the most coins.

    f(n) = g(n) + h(n), where g(n) is the number of coins collected so far
    and h(n) is an optimistic guess of what can still be collected. The
    open set is a max-heap, so the most promising node is expanded first.
    """

    algorithm_name = "A* Max Profit"

    def __init__(self, map_obj: Map):
        super().__init__(map_obj)
        self._counter = itertools.count()

    def solve(self) -> Dict:
        start_node = self.start_node()

        open_set = []
        heappush(open_set, (-self._f(start_node), next(self._counter), start_node))
        best_coins = {(0, 0): start_node.coins}

        while open_set:
            # The counter is only there to break ties without comparing nodes.
            _, _, current = heappop(open_set)

            if self.is_goal(current):
                return self.result(current)

            for dx, dy in DIRECTIONS:
                new_x = current.x + dx
                new_y = current.y + dy

                if not self.map.is_valid_move(new_x, new_y):
                    continue

                next_node = self.move(current, new_x, new_y)
                if (new_x, new_y) not in best_coins or next_node.coins > best_coins[(new_x, new_y)]:
                    best_coins[(new_x, new_y)] = next_node.coins
                    heappush(open_set, (-self._f(next_node), next(self._counter), next_node))

        return self.no_result()

    def _f(self, node: Node) -> int:
        return node.coins + self._heuristic_max_profit(node.x, node.y)

    def _heuristic_max_profit(self, x: int, y: int) -> int:
        """
        Optimistic estimate: assume every remaining step lands on the richest
        cell that is still reachable.
        """
        steps_left = (self.n - 1 - x) + (self.n - 1 - y)

        max_coin = 0
        for i in range(x, self.n):
            for j in range(y, self.n):
                cell = self.map.get_cell(i, j)
                if cell != THIEF and cell > max_coin:
                    max_coin = cell

        return max(0, max_coin * steps_left)


class AStarMinLossPathFinder(PathFinder):
    """
    A* that looks for the path where thieves steal the least.

    f(n) = g(n) + h(n), where g(n) is the amount stolen so far. The
    heuristic is always 0, which is admissible but gives no guidance, so in
    practice this behaves like a uniform cost search on the stolen amount.
    """

    algorithm_name = "A* Min Loss"

    def __init__(self, map_obj: Map):
        super().__init__(map_obj)
        self._counter = itertools.count()

    def solve(self) -> Dict:
        start_node = self.start_node()

        open_set = []
        heappush(open_set, (self._f(start_node), next(self._counter), start_node))
        least_stolen = {(0, 0): 0}

        while open_set:
            _, _, current = heappop(open_set)

            if self.is_goal(current):
                return self.result(current)

            for dx, dy in DIRECTIONS:
                new_x = current.x + dx
                new_y = current.y + dy

                if not self.map.is_valid_move(new_x, new_y):
                    continue

                next_node = self.move(current, new_x, new_y)
                if (new_x, new_y) not in least_stolen or next_node.stolen < least_stolen[(new_x, new_y)]:
                    least_stolen[(new_x, new_y)] = next_node.stolen
                    heappush(open_set, (self._f(next_node), next(self._counter), next_node))

        return self.no_result()

    def _f(self, node: Node) -> int:
        return node.stolen + self._heuristic_min_loss()

    @staticmethod
    def _heuristic_min_loss() -> int:
        # The smallest amount a thief can still steal is always 0.
        return 0
