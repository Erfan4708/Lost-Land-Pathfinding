# helpers.py: Store helper functions for the project.

import tracemalloc
from datetime import datetime
from time import perf_counter
from typing import List, Type

from algorithms.PathFinder import PathFinder
from models.map import Map
from utils.parser import MapParser

SEPARATOR = "-" * 40


def run_examples(
    input_file: str,
    output_file: str,
    algorithms: List[Type[PathFinder]]
):
    """
    Run every algorithm on every map of the input file and write the results
    both to the console and to the output file.
    """
    examples = MapParser.parse_examples_from_file(input_file)

    with open(output_file, 'w', encoding='utf-8') as out_f:

        def emit(text: str) -> None:
            print(text, end='')
            out_f.write(text)

        for example_name, grid in examples:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            emit(f"{example_name}\n{date_str}\n\n")

            map_obj = Map(grid)

            for algorithm in algorithms:
                solver = algorithm(map_obj)

                tracemalloc.start()
                start_time = perf_counter()
                result = solver.solve()
                elapsed = perf_counter() - start_time
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                peak_mb = peak / (1024 * 1024)

                if result["path"]:
                    emit(
                        f"Path found using {solver.algorithm_name}\n"
                        f"path: {result['path']}\n"
                        f"coins: {result['coins']}\n"
                        f"stolen: {result['stolen']}\n"
                        f"Execution time: {elapsed:.6f} sec, "
                        f"Memory peak: {peak_mb:.6f} MB\n"
                        f"{SEPARATOR}\n"
                    )
                else:
                    emit(
                        f"No path found using {solver.algorithm_name}\n"
                        f"{SEPARATOR}\n"
                    )

            emit("\n")
