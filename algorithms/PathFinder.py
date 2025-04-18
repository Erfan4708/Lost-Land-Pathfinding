from models.map import Map
from abc import ABC, abstractmethod

class PathFinder(ABC):
    """
    Abstract base class for pathfinding algorithms.
    """

    def __init__(self, map_obj: Map):
        self.__algorithm_name = "PathFinder"
        self.map = map_obj

    @property
    def algorithm_name(self) -> str:
        """
        Returns the name of the algorithm.
        """
        return self.__algorithm_name

    @abstractmethod
    def solve(self) -> dict:
        """
        Abstract method to solve the pathfinding problem.
        This method should be implemented by subclasses.
        """
        pass
