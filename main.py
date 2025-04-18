from models.map import Map
from algorithms.PathFinder import PathFinder
from algorithms.uninformed import DFSPathFinder

if __name__ == "__main__":
    test_map = [
        [-3, -2, -2, "!"],
        [ 3, -2,  3, -2],
        [10, -8, "!", 1],
        [-4, -3, -6, "!"]
    ]

    map_obj = Map(test_map)

    algorithms: list[tuple[str, type[PathFinder]]] = [
        ("DFS", DFSPathFinder),
    ]

    for name, AlgoClass in algorithms:
        solver: PathFinder = AlgoClass(map_obj)
        result = solver.solve()

        if result:
            print("Path found using", name)
            print("path:", result["path"])
            print("coins:", result["coins"])
            print("stolen", result["stolen"])
        else:
            print("No path found using", name)
