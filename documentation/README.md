# Algorithm notes

Notes on how the three searches are implemented. The general description of
the project, the file formats and how to run it are in the [root
README](../README.md).

## The state space

A state is a `Node` (`models/node.py`):

| Field       | Meaning                                            |
| ----------- | -------------------------------------------------- |
| `x`, `y`    | Where Arian stands.                                 |
| `path`      | The cells he walked through to get there.           |
| `coins`     | Coins he currently holds.                           |
| `stolen`    | Coins a thief took from him along the way.          |
| `has_thief` | Whether a thief is following him right now.         |

The start state is the top-left cell, the goal state is the bottom-right one.
Because the only moves are down and right, the state space is a directed
acyclic graph: from `(x, y)` you can reach `(x + 1, y)` and `(x, y + 1)` and
never come back.

`PathFinder.move()` (`algorithms/PathFinder.py`) is the transition function. It
is the single place where the rules of the world are implemented:

```
if a thief is following:
    the thief takes this cell and leaves
    positive cell -> stolen += value      (the coins never reach Arian)
    negative cell -> coins  += value      (he pays the cell)
                     stolen += |value|    (and the loss is recorded)
    thief cell    -> the two thieves cancel out
otherwise:
    thief cell    -> the thief starts following him
    any number    -> coins += value
```

Nodes are immutable in practice: `move()` copies the current node instead of
mutating it, so a node that is still sitting in the open set is never modified
by another branch of the search.

## DFS — find any way out

`algorithms/uninformed.py`. A plain recursive depth-first search with a
`visited` set, trying *down* before *right*. It stops at the first path it
finds and does not look at coins at all, so on a grid where every path is
valid it always returns the "all the way down, then all the way right" path.
The coins and stolen amounts it reports are simply what that path happens to
yield.

`visited` is unwound on backtracking (`visited.remove(...)`), which matters for
maps where a branch can dead-end — not possible with the current movement
rules, but the search is written to handle it.

## A\* Max Profit — collect as much as possible

`algorithms/informed.py`. `f(n) = g(n) + h(n)` with:

- `g(n)` = coins collected so far.
- `h(n)` = `max_coin * steps_left`, where `steps_left` is the Manhattan
  distance to the goal and `max_coin` is the largest value in the sub-grid
  that is still reachable. This never underestimates what can still be
  collected, which is the admissibility condition for a maximisation search.

`heapq` is a min-heap, so the priority is pushed negated to pop the most
promising node first. A node is only pushed if it reaches its cell with more
coins than any node seen there before (`best_coins`).

## A\* Min Loss — lose as little as possible

Same structure, but `g(n)` is the amount stolen so far and `h(n)` is always
`0`, because a thief can always steal nothing from here on. The heuristic is
admissible but carries no information, so this search behaves like a uniform
cost search. It is kept as an A\* to keep the three algorithms comparable.

A node is only pushed if it reaches its cell with less stolen than any node
seen there before (`least_stolen`).

## Why the results can differ from the true optimum

`best_coins` and `least_stolen` are keyed on the coordinates alone. The real
state also includes `has_thief`: arriving at a cell with a thief in tow is not
the same situation as arriving without one, even though the coordinates match.
Keeping one entry per coordinate can therefore discard a state that would have
led to a better final result. Keying those tables on
`(x, y, has_thief)` would fix it; it was left as it is because the maps in
`examples/input.txt` are small and the assignment was about writing the
searches, not about squeezing out the last coin.
