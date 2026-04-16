# Core AI Lab Coding Roadmap

A foolproof, step-by-step roadmap to mastering the "crux coding" for all your AI Lab assignments (A2 to A14). This focuses exclusively on the logic skeletons you need to memorize. 

---

## Part 1: Blind Search Algorithms
**Assignments covered: Assignment 2 (Q1, Q2), Assignment 5 (Q1)**
*The core logic here revolves around maintaining a "frontier" (a list of nodes to explore next) and an explored set.*

* **BFS (Breadth-First Search):** Uses a Queue (`pop(0)`).
* **DFS (Depth-First Search):** Uses a Stack (`pop()`).
* **IDS (Iterative Deepening Search):** Wraps DFS in a `for limit in range(max_depth):` loop.

### 1. The Search Skeleton (BFS / DFS)
```python
def generic_search(start_state, goal_state):
    frontier = [start_state]           
    explored = set()                   # Keeps track of visited nodes

    while frontier:
        # pop(0) -> BFS
        # pop() -> DFS
        node = frontier.pop(0)         
        
        if is_goal(node):
            return node                # Reconstruct path from goal
            
        explored.add(node)
        
        for neighbor in get_neighbors(node):
            if neighbor not in explored and neighbor not in frontier:
                frontier.append(neighbor)  
                
    return "Failure"
```

---

## Part 2: Heuristic Informed Search
**Assignments covered: Assignment 4 (Q1, Q2), Assignment 6 (Q1, Q2)**
*The logic is identical to blind search, except the frontier is a **Priority Queue** (using the `heapq` module), sorted by cost.*

* **A* Search:** Prioritizes nodes where `f(n) = g(n) + h(n)` (actual cost + heuristic).
* **Greedy Best-First Search:** Prioritizes nodes where `f(n) = h(n)` (only looks at the heuristic).

### 2. The Heuristic Search Skeleton (A*)
```python
import heapq

def a_star_search(start_state):
    # Tuple format: (f_score, state_data)
    frontier = []
    heapq.heappush(frontier, (0 + heuristic(start_state), start_state))
    explored = set()

    while frontier:
        # Always pops the state with the lowest f_score
        f_cost, current = heapq.heappop(frontier)
        
        if is_goal(current):
            return current
            
        explored.add(current)
        
        for neighbor in get_neighbors(current):
            if neighbor not in explored:
                g_cost = get_actual_cost(start_state, neighbor)
                h_cost = heuristic(neighbor)
                
                # Push the combined f(n) cost
                heapq.heappush(frontier, (g_cost + h_cost, neighbor))
```

---

## Part 3: Local Search & Metaheuristics
**Assignments covered: Assignment 7 (Q1, Q2), Assignment 8 (Q1, Q2)**
*We don't keep track of everything seen. We just track a "current state" and strictly evaluate its immediate neighbors. Genetic Algorithm evolves a group.*

* **Steepest Ascent Hill Climbing:** Iterates through all neighbors to pick the absolute best one.
* **Simulated Annealing:** Picks a random neighbor. If it's worse, accept with a calculated probability based on "temperature". 
* **Genetic Algorithm (A8):** Tracks population, uses selection, crossover, and mutation.

### 3a. The Local Search Skeleton (Simulated Annealing)
```python
import math, random

def simulated_annealing(initial_state):
    current = initial_state
    temp = 100.0   # High initial temp
    
    while temp > 0.01:
        neighbor = get_random_neighbor(current)
        delta_E = value(neighbor) - value(current)
        
        if delta_E > 0:
            current = neighbor # It's better, always accept!
        else:
            # It's worse! Calculate probability using temp to maybe accept it anyway
            prob = math.exp(delta_E / temp)
            if random.random() < prob:
                current = neighbor
                
        temp *= 0.99   # Cool down the temperature
        
    return current
```

### 3b. Genetic Algorithm Crux (A8)
```python
def genetic_algorithm(population):
    for generation in range(max_gen):
        new_population = []
        for i in range(len(population)):
            parent1 = select_parent(population) # e.g. tournament selection
            parent2 = select_parent(population)
            
            # Crossover
            child = crossover(parent1, parent2)
            
            # Mutation
            if random.random() < mutation_rate:
                child = mutate(child)
                
            new_population.append(child)
        population = new_population
    return best_individual(population)
```

---

## Part 4: Adversarial Search (Games)
**Assignments covered: Assignment 9 (Q1, Q2)**
*Simulating game trees with two players who play perfectly against each other.*

* **Minimax:** Evaluates all possible leaf combinations recursively.
* **Alpha-Beta Pruning:** Enhances Minimax by passing `alpha` and `beta` values down the tree to prune unnecessary branches and optimize performance.

### 4a. The Minimax Skeleton
```python
def minimax(board, is_maximizing):
    if is_game_over(board):
        return get_score(board)
        
    if is_maximizing:
        best_score = float('-inf')
        for move in get_available_moves(board):
            board.make_move(move)                     # Forward 
            score = minimax(board, False)             # Pass turn 
            board.undo_move(move)                     # Backtrack
            best_score = max(best_score, score)
        return best_score
        
    else: # Minimizing player
        best_score = float('inf')
        for move in get_available_moves(board):
            board.make_move(move)                     # Forward 
            score = minimax(board, True)              # Pass turn
            board.undo_move(move)                     # Backtrack
            best_score = min(best_score, score)
        return best_score
```

### 4b. Alpha-Beta Pruning Skeleton
```python
def alpha_beta(board, is_maximizing, alpha, beta):
    if is_game_over(board):
        return get_score(board)

    if is_maximizing:
        best_score = float('-inf')
        for move in get_available_moves(board):
            board.make_move(move)
            score = alpha_beta(board, False, alpha, beta)
            board.undo_move(move)
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:  # Prune!
                break
        return best_score
    else:  # Minimizing
        best_score = float('inf')
        for move in get_available_moves(board):
            board.make_move(move)
            score = alpha_beta(board,  True, alpha, beta)
            board.undo_move(move)
            best_score = min(best_score, score)
            beta = min(beta, score)
            if beta <= alpha: # Prune!
                break
        return best_score
```

---

## Part 5: Constraint Satisfaction Problems (CSP) & Clustering
**Assignments covered: Assignment 11 (Q1), Assignment 12 (Q1, Q2), Assignment 10 (Q1)**
*Used for constraint-based assignments like graph coloring, soduku, or grouping generic datasets together.*

* **Backtracking (A11):** Used to assign variables, testing if they satisfy constraints.
* **AC-3 (A12):** Trims the 'domains' early, removing fundamentally flawed options before even making variable assignments.
* **K-Means Clustering (A10):** Assigns points to centers, then resets the centers.

### 5a. Backtracking Skeleton (A11)
```python
def backtrack(assignment):
    if is_complete(assignment):
        return assignment
        
    var = select_unassigned_variable(assignment)
    for value in order_domain_values(var, assignment):
        if is_consistent(var, value, assignment):
            assignment.add(var, value)         # Assign 
            
            result = backtrack(assignment)     # Recurse deeper
            if result != "Failure": 
                return result
                
            assignment.remove(var)             # Backtrack if it failed
    return "Failure"
```

### 5b. The Constraint Skeleton (AC-3 Algorithm) (A12)
```python
def ac3(domains, peers):
    # Enqueue ALL arcs (Pairs of connected nodes, like A->B)
    queue = [(X, Y) for X in peers for Y in peers[X]]
    
    while queue:
        X, Y = queue.pop(0)
        
        # If we successfully remove inconsistent pairs from X's domain...
        if revise(domains, X, Y):
            if len(domains[X]) == 0:
                return False   # Domain wiped out, no solution possible
            
            # Since X modified its options, we must re-evaluate all neighbors of X!
            for Z in peers[X]:
                if Z != Y:
                    queue.append((Z, X))
    return True

def revise(domains, X, Y):
    revised = False
    for x in list(domains[X]):
        # Check if there is ANY 'y' that works with our current 'x'
        if not any(is_valid(x, y) for y in domains[Y]):
            domains[X].remove(x) 
            revised = True
    return revised
```

### 5c. K-Means Clustering Core Loop (A10)
```python
def kmeans(data, centers, max_iterations=100):
    for i in range(max_iterations):
        # 1. Assignment Phase
        labels = assign_clusters(data, centers)
        
        # 2. Update Phase (Usually via gradient descent/averaging)
        new_centers = compute_new_centers(data, labels)
        
        # Stop early if the centers didn't actually move
        if has_converged(centers, new_centers):
            break
        centers = new_centers
    return labels, centers
```

---

## Part 6: Logic Inference
**Assignments covered: Assignment 13 (Q1), Assignment 14 (Q1, Q2, Q3)**
*Extracting truths mathematically.*

* **Forward Chaining:** Starts from facts and applies rules to deduce conclusion.
* **Backward Chaining:** Starts from the Goal and works backwards up to the known facts.
* **Propositional Logic Truth Tables:** Loops logic matrices.

### 6a. Forward Chaining Skeleton (A14 Q1)
```python
def forward_chaining(rules, known_facts, goal):
    inferred = True
    
    while inferred: # Keep looping as long as we discover new facts
        inferred = False
        
        for preconditions, conclusion in rules:
            if conclusion not in known_facts:
                
                # Check if ALL preconditions are currently facts
                if all(p in known_facts for p in preconditions):
                    known_facts.add(conclusion)
                    inferred = True
                    
                    if conclusion == goal:
                        return True
    return False
```

### 6b. Backward Chaining Skeleton (A14 Q2)
```python
def backward_chaining(goal, rules, known_facts, checking_goals):
    if goal in known_facts:
        return True
    
    # Avoid infinite recursion (A -> B, B -> A)
    if goal in checking_goals:
        return False
        
    checking_goals.add(goal)
    
    # Look at every rule that potentially yields our Goal
    for preconditions, conclusion in rules:
        if conclusion == goal:
            # We must prove ALL preconditions to this rule are true
            all_preconditions_true = True
            for p in preconditions:
                if not backward_chaining(p, rules, known_facts, checking_goals):
                    all_preconditions_true = False
                    break
            
            if all_preconditions_true:
                known_facts.add(goal)
                return True
                
    checking_goals.remove(goal)
    return False
```

---

## Appendix: Exact Data Structure Inputs

If you set your variables up exactly like this before calling the function, your exam code will work seamlessly:

### 1. The Search Skeleton (BFS, DFS, A*)
* **`start_state` / `goal_state`**: Typically represented as a simple `string` (like `"A"`) or a `tuple` of coordinates (like `(0, 0)`).
* **`graph` (the backbone implicitly used by `get_neighbors`)**: Represented as an **Adjacency Dictionary**. 
  * *Example:* `graph = {'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}`
* **`heuristic(node)` / actual costs**: Can be stored in a dictionary mapping points to values.
  * *Example:* `heuristics = {'A': 10, 'B': 8, 'C': 5}`

### 2. Local Search & Genetic Algorithms (Simulated Annealing / TSP)
* **`initial_state` / `current`**: Represented as a **1D List** of items. In problems like the Traveling Salesperson (TSP) or N-Queens, it's just a sequence. 
  * *Example:* `state = [0, 2, 1, 3]` (meaning visit city 0, then 2, then 1, etc.)
* **`population` (Genetic)**: A **List of Lists** (a list of state lists).
  * *Example:* `population = [[0,2,1], [1,0,2], [2,1,0]]`

### 3. Adversarial Search (Minimax / Alpha-Beta)
* **`board`**: For grid games like Tic-Tac-Toe, this is almost always a **1D List of length 9** (or a 2D List).
  * *Example:* `board = ["X", "O", "X", " ", "O", " ", " ", " ", " "]`.
* **`is_maximizing`**: Just a **Boolean** (`True` or `False`).

### 4. Constraint Satisfaction (AC-3 Algorithm)
* **`domains`**: A **Dictionary** mapping a variable to a **List** of its currently allowable values.
  * *Example (Sudoku):* `domains = {(0, 0): [1, 2, 3], (0, 1): [5]}`
* **`peers`**: A **Dictionary** mapping a variable to a **Set** of everything it is connected/restrained by.
  * *Example:* `peers = {(0, 0): set([(0, 1), (0, 2), (1, 0)])}`

### 5. Backtracking (Map Coloring)
* **`assignment`**: A **Dictionary** mapping a completed pairing.
  * *Example:* `assignment = {"WA": "red", "NT": "green"}`

### 6. K-Means Clustering
* **`data` & `centers`**: Both are **Lists of Tuples** (or lists of lists) representing X/Y coordinates.
  * *Example:* `data = [(1.5, 2.0), (3.0, 4.5), (6.1, 7.0)]`

### 7. Logic Inference (Forward / Backward Chaining)
* **`rules`**: A **List of Tuples**. The first element is your List of precedents, the second is your conclusion string.
  * *Example:* `rules = [ (["P"], "Q"), (["L", "M"], "P") ]` ->  (This reads as: If $P$, then $Q$. If $L$ and $M$, then $P$.)
* **`known_facts` / `initial_facts`**: A **List or Set** of single strings.
  * *Example:* `known_facts = ["A", "B", "M"]`
* **`goal`**: A single **String**.
  * *Example:* `goal = "Q"`
