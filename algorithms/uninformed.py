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
        