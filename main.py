# main.py: Main script to run the app

from models.map import Map
from algorithms.uninformed import DFSPathFinder

if __name__ == "__main__":
    test_map = [
        [-3, -2, -2, "!"],
        [ 3, -2,  3, -2],
        [10, -8, "!", 1],
        [-4, -3, -6, "!"]
    ]

    map_obj = Map(test_map)
    dfs_solver = DFSPathFinder(map_obj)
    result = dfs_solver.solve()

    if result:
        print(f"Path found by {dfs_solver.get_name()}:")
        print("Path:", result["path"])
        print("Coins:", result["coins"])
        print("Stolen:", result["stolen"])
    else:
        print("No path found.")
