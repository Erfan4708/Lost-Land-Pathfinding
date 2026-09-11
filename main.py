from algorithms.informed import (
    AStarMaxProfitPathFinder,
    AStarMinLossPathFinder
)
from algorithms.uninformed import DFSPathFinder
from utils.helpers import run_examples

ALGORITHMS = [
    DFSPathFinder,
    AStarMaxProfitPathFinder,
    AStarMinLossPathFinder,
]

if __name__ == "__main__":
    run_examples(
        input_file="examples/input.txt",
        output_file="examples/output.txt",
        algorithms=ALGORITHMS
    )
