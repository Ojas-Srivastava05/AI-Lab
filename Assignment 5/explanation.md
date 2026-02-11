# 3 Girls and 3 Boys: Concept and Implementation Guide

This document explains the solution for the **3 Girls and 3 Boys** river crossing problem implemented in `q1.py`.

## 1. Problem Statement
Three girls and three boys are on one side of a river, along with a boat that can hold one or two people. You need to get everyone to the other side.
**Constraint**: At no point can the girls be outnumbered by the boys on either side (unless there are zero girls on that place).

## 2. State Representation
We represent the "world" as a state `State` with three variables:
- `g_left`: Number of Girls on the left bank.
- `b_left`: Number of Boys on the left bank.
- `boat`: Position of the boat (1 = Left, 0 = Right).

**Initial State**: `(3, 3, 1)` - 3 Girls, 3 Boys, Boat on Left.
**Goal State**: `(0, 0, 0)` - 0 Girls, 0 Boys, Boat on Right.

## 3. The Rules (Constraints)
The `is_valid()` method checks if a state is allowed. A state is **invalid** if:
1.  **Out of bounds**: Any number is less than 0 or greater than 3.
2.  **Girls outnumbered on Left**: `g_left > 0` AND `g_left < b_left`.
3.  **Girls outnumbered on Right**: `g_right > 0` AND `g_right < b_right` (where `g_right = 3 - g_left`).

## 4. Generating Moves
The `get_successors()` function calculates all possible next states.
The boat can carry:
- 1 Girl `(1, 0)`
- 2 Girls `(2, 0)`
- 1 Boy `(0, 1)`
- 2 Boys `(0, 2)`
- 1 Girl, 1 Boy `(1, 1)`

If the boat is on the **Left**, we **subtract** these numbers from the left side.
If the boat is on the **Right**, we **add** these numbers to the left side.

## 5. Algorithms Used

### A. Depth Limited Search (DLS)
**Concept**: This is a standard Depth First Search (DFS) but it stops if it reaches a specific depth limit.
- **Why use it?** DFS can get stuck in infinite loops or go too deep. A limit prevents this.
- **In our code**: We call `dls(start_state, limit=3)`.
- **Result**: **Failed**.
- **Reason**: The minimum number of steps to solve this problem is **11**. A limit of 3 is too shallow to find the solution.

### B. Iterative Deepening Search (IDS)
**Concept**: This algorithm repeatedly runs DLS with increasing limits:
- Run DLS with Limit = 0
- Run DLS with Limit = 1
- ...
- Run DLS with Limit = 11 (Solution Found!)

- **Why use it?** It combines the benefits of BFS (optimality) with the memory efficiency of DFS.
- **In our code**: The `ids()` function has a `while True` loop that increments `depth` until a solution is returned.

## 6. Code Walkthrough (`q1.py`)

1.  **`State` Class**:
    -   Stores the current counts (Girls, Boys, Boat).
    -   `parent`: Stores the previous state so we can reconstruct the path later.
    -   `action`: String description of the move (e.g., "Move 1G 1B to Right").

2.  **`dls(start_state, limit)`**:
    -   Uses a helper function `recursive_dls`.
    -   Keeps track of variables to prevent infinite loops.
    -   Returns the goal state if found, otherwise `None`.

3.  **`ids(start_state)`**:
    -   Starts depth at 0.
    -   Calls `dls` with the current depth.
    -   If `dls` returns a result, we are done.
    -   If not, increment depth and try again.

4.  **`main()`**:
    -   Runs DLS(3) and prints "No solution found" (as expected).
    -   Runs IDS, which eventually tries depth 11, finds the solution, and prints the step-by-step path.

## 7. Solution Path
The algorithm finds the following optimal 11-step solution:
1.  Move 2 Boys to Right
2.  Move 1 Boy back to Left
3.  Move 2 Boys to Right
4.  Move 1 Boy back to Left
5.  Move 2 Girls to Right
6.  Move 1 Girl and 1 Boy back to Left
7.  Move 2 Girls to Right
8.  Move 1 Boy back to Left
9.  Move 2 Boys to Right
10. Move 1 Boy back to Left
11. Move 2 Boys to Right -> **Goal Reached**
