# Lost Land Pathfinding

A small university project about classical search algorithms.

A traveller named **Arian** is stranded in a square land. He starts in the
top-left cell, has to reach the bottom-right one, and can only walk **down or
right**. Some cells hold coins, others hold thieves. The project implements
three search strategies that answer three different questions about the same
map, and compares their results, runtime and memory usage side by side.

This was written as a course assignment, so the focus is on the search
algorithms themselves rather than on tooling, packaging or a user interface.

## Rules of the world

The land is an `n x n` grid. Each cell is either a number or a `!`:

| Cell            | Meaning                                         |
| --------------- | ----------------------------------------------- |
| Positive number | Treasure — Arian collects that many coins.      |
| Negative number | A costly cell — that many coins are subtracted. |
| `0`             | An empty cell.                                  |
| `!`             | A thief — he starts following Arian.            |

A thief that follows Arian robs the **next** cell he walks onto and then
leaves: the value of that cell is recorded as *stolen* instead of being
collected. If the next cell holds another thief, the two cancel out and nobody
follows Arian any more.

## What the program does

For every map in the input file it runs three algorithms:

1. **DFS** — *just get out*. A depth-first search that returns the first path
   it finds, without caring about coins.
2. **A\* Max Profit** — *collect as much as possible*. `g(n)` is the number of
   coins collected so far and the heuristic assumes every remaining step lands
   on the richest cell still ahead.
3. **A\* Min Loss** — *lose as little as possible*. `g(n)` is the amount stolen
   so far, with an admissible heuristic of `0`.

Each run reports the path, the final coins, the amount stolen, the execution
time and the peak memory usage (measured with `tracemalloc`).

## Tech stack

- Python 3.8 or newer
- Standard library only — `heapq`, `tracemalloc`, `abc`, `typing`. There are no
  third-party dependencies and nothing to install.

## Project structure

```
.
├── main.py                 # Entry point: runs every algorithm on every example
├── config.py               # The thief marker and the allowed movement directions
│
├── algorithms/
│   ├── PathFinder.py       # Abstract base class + the shared rules of the world
│   ├── uninformed.py       # DFS
│   └── informed.py         # A* Max Profit and A* Min Loss
│
├── models/
│   ├── map.py              # The grid and its bounds checks
│   └── node.py             # One state of the search (position, path, coins, stolen)
│
├── utils/
│   ├── parser.py           # Reads the maps from the input file
│   └── helpers.py          # Runs the algorithms and formats the report
│
├── examples/
│   ├── input.txt           # Ten example maps
│   └── output.txt          # Result of the last run
│
└── documentation/
    └── README.md           # Notes on how the algorithms work
```

## Getting started

Prerequisites: a Python 3.8+ interpreter. Nothing else.

```bash
git clone https://github.com/Erfan4708/Lost-Land-Pathfinding.git
cd Lost-Land-Pathfinding
python main.py
```

The script must be run from the project root, because the input and output
paths in `main.py` are relative to it. Results are printed to the console and
written to `examples/output.txt`, overwriting the previous run.

## Configuration

There are no environment variables and no configuration files. The only
settings are the two constants in `config.py`:

- `THIEF` — the character that marks a thief in the input files (`"!"`).
- `DIRECTIONS` — the moves Arian is allowed to make (`down` and `right`).

The input and output paths are passed to `run_examples()` in `main.py`.

## Usage

### Input format

Each map starts with a line naming it (`Example1`, `Example2`, ...), followed
by its rows. Cells are separated by spaces, and maps are separated by a blank
line:

```
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

Grids have to be square; `Map` raises a `ValueError` otherwise.

### Output format

```
Example1
2025-04-21 23:21:30

Path found using DFS
path: [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)]
coins: -3
stolen: 0
Execution time: 0.000073 sec, Memory peak: 0.003311 MB
----------------------------------------
Path found using A* Max Profit
path: [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (3, 3)]
coins: 2
stolen: 1
Execution time: 0.000193 sec, Memory peak: 0.003098 MB
----------------------------------------
Path found using A* Min Loss
path: [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)]
coins: -3
stolen: 0
Execution time: 0.000121 sec, Memory peak: 0.001846 MB
----------------------------------------
```

The line under the map name is the timestamp of the run.

### Adding a map

Append it to `examples/input.txt` under a new `ExampleN` heading and run
`python main.py` again.

### Adding an algorithm

Subclass `PathFinder`, set the `algorithm_name` class attribute, implement
`solve()` and add the class to the `ALGORITHMS` list in `main.py`. The base
class provides `start_node()`, `move()`, `is_goal()` and the result helpers, so
a new algorithm does not have to reimplement the rules of the world.

## Testing

There is no automated test suite — this was a course project and none was
written at the time.

The ten maps in `examples/input.txt` serve as a manual check. Between them they
cover a thief on the starting cell (Examples 4 and 6), a thief on the goal cell
(Example 1), two thieves in a row (Example 3), a grid of zeros with a single
thief (Example 8), a grid with no thieves at all (Example 10) and one 5x5 map
(Example 3) next to the 4x4 ones.

`examples/output.txt` is the committed result of the last run, so re-running
`python main.py` and looking at the diff is an easy way to see whether a change
affected any result.

## Technical notes

- All three algorithms inherit from `PathFinder`, which owns the rules of the
  world in `move()`. Keeping the coin and thief bookkeeping in one place is
  what makes the three results comparable: the algorithms differ only in the
  order they expand nodes, never in how they score them.
- A search state is a `Node`: position, the path taken to get there, the coins
  collected, the amount stolen and whether a thief is currently following.
  Nodes are copied on every move, which is simple to reason about and fine for
  maps of this size.
- The A\* implementations push `(priority, counter, node)` tuples onto a
  `heapq`. The counter breaks ties so that two nodes with the same priority are
  never compared to each other. Max Profit negates the priority to turn the
  min-heap into a max-heap.

## Limitations

These are known and were left as they are; the project is kept as the course
assignment it was.

- **A\* Min Loss has no real heuristic.** `h(n)` is always `0`, which is
  admissible but gives no guidance, so it effectively degrades to a uniform
  cost search over the stolen amount.
- **The visited tables ignore the thief state.** Both A\* variants remember the
  best value seen per coordinate, not per (coordinate, "is a thief following")
  pair. A cell reached in two different thief states keeps only one of them, so
  the returned path is not guaranteed to be optimal on every map.
- **The max-profit heuristic is recomputed from scratch.** It scans the whole
  remaining sub-grid on every expansion, which is fine for the small maps here
  but wasteful on larger ones.
- **DFS is recursive**, so a very large map could hit Python's recursion limit.
- Because movement is restricted to down and right, every square map has a
  path; the "No path found" branch exists for completeness but is never
  reached with the current rules.
