
## Lost Land Pathfinding Project

This project helps a traveler named **Arian** find his way out of a strange land.  
He can move **down or right**, and there are **coins** and **thieves** in the land.

The project uses **search algorithms** to find the best way for Arian to reach the goal.

---

### What the Program Does

The program solves three tasks:

1. **Just get out** – find any path to the end (DFS algorithm).
2. **Get most coins** – find the path with the most coins (A* algorithm).
3. **Lose least coins** – find the path where thieves steal the least (A* algorithm).

---

### Code is Object-Oriented

- All search algorithms inherit from a base class called `PathFinder`.
- The map is handled in a class called `Map`.
- There is a `Node` class to keep track of each step in the path.
- File reading/writing is done with helper classes in the `utils` folder.

---

### Input File Format 
(`examples/input.txt`)

Each map starts with a name like `Example1`, followed by rows of numbers or symbols:

- **Negative numbers** = normal cells (they cost coins to move through)  
- **Positive numbers** = treasure cells (they give coins)  
- **!** = thief cells (they follow Arian and steal from him)

```plaintext
Example1
-3 -2 -2 !
3 -2 3 -2
10 -8 ! 1
-4 -3 -6 !

Example2
-3 ! -2 -2
-3 -2 ! 3
! 10 -8 !
-4 -6 ! -5
```

---

### Output File Format
(`examples/output.txt`)

For each map, the program prints results from **all algorithms**, including:

- Found path
- Final coins Arian has
- How much thieves stole
- Time used
- Memory used

```plaintext
Example1
Date: 2025-04-21 14:30:12

Path found using DFS
path: [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)]
coins: -30
stolen: 0
Time: 0.0012 sec
Memory: 1.4 MB
----------------------------------------

Path found using A Start Max Profit
path: [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (3, 3)]
coins: -6
stolen: 7
Time: 0.0021 sec
Memory: 1.5 MB
----------------------------------------

Path found using A Start Min Profit
path: [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2), (3, 3)]
coins: -9
stolen: 5
Time: 0.0019 sec
Memory: 1.6 MB
----------------------------------------
```


### Project Structure

```
lost-land/
│
├── main.py                    # Runs the program
├── config.py                  # Stores symbols like '!' for thief
│
├── documentation/
│   └── README.md              # This file
│
├── models/
│   ├── map.py                 # Map logic
│   └── node.py                # Node used in search trees
│
├── utils/
│   ├── helper.py              # Time/memory tracking
│   └── parser.py              # Reads maps from file
│
├── algorithms/
│   ├── PathFinder.py          # Base class
│   ├── uninformed.py          # DFS
│   └── informed.py            # A* (max profit and min loss)
│
├── examples/
│   ├── input.txt              # Input maps
│   └── output.txt             # Result output
```
