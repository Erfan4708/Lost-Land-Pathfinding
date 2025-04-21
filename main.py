from algorithms.PathFinder import PathFinder
from algorithms.uninformed import DFSPathFinder
from algorithms.informed import (
    AStarMaxProfitPathFinder,
    AStarMinLossPathFinder
)
from utils.helpers import run_examples

if __name__ == "__main__":
    algorithms = [
        ("DFS", DFSPathFinder),
        ("A* Max Profit", AStarMaxProfitPathFinder),
        ("A* Min Loss", AStarMinLossPathFinder),
    ]

    run_examples(
        input_file="examples/input.txt",
        output_file="examples/output.txt",
        algorithms=algorithms
    )
