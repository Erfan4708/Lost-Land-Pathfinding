# helpers.py: Store helper functions for the project.

import tracemalloc
from time import perf_counter
from datetime import datetime
from typing import List, Tuple, Type

from models.map import Map
from algorithms.PathFinder import PathFinder
from utils.parser import MapParser

def run_examples(
    input_file: str,
    output_file: str,
    algorithms: List[Tuple[str, Type[PathFinder]]]
):
    examples = MapParser.parse_examples_from_file(input_file)

    with open(output_file, 'w', encoding='utf-8') as out_f:
        for example_name, grid in examples:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            header = f"{example_name}\n{date_str}\n\n"
            print(header, end='')
            out_f.write(header)

            map_obj = Map(grid)

            for algo_name, AlgoClass in algorithms:
                solver: PathFinder = AlgoClass(map_obj)

                tracemalloc.start()
                t0 = perf_counter()
                result = solver.solve()
                t1 = perf_counter()
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                elapsed = t1 - t0
                peak_mb = peak / (1024 * 1024)

                if result:
                    block = (
                        f"Path found using {algo_name}\n"
                        f"path: {result['path']}\n"
                        f"coins: {result['coins']}\n"
                        f"stolen {result['stolen']}\n"
                        f"Execution time: {elapsed:.6f} sec, "
                        f"Memory peak: {peak_mb:.6f} MB\n"
                        + "-"*40 + "\n"
                    )
                else:
                    block = (
                        f"No path found using {algo_name}\n"
                        + "-"*40 + "\n"
                    )

                print(block, end='')
                out_f.write(block)

            print()
            out_f.write("\n")
