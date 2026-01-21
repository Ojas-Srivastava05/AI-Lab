"""
8-Puzzle Problem - DFS Solution
Question 2: Find the number of states explored for DFS and compare with BFS
"""

from collections import deque

class Puzzle8:
    def __init__(self, state):
        """
        Initialize the puzzle with a 3x3 state
        state: list of lists representing the puzzle board
        """
        self.state = state
        self.size = 3
    
    def __eq__(self, other):
        """Check if two puzzle states are equal"""
        return self.state == other.state
    
    def __hash__(self):
        """Make puzzle hashable for use in sets"""
        return hash(tuple(tuple(row) for row in self.state))
    
    def __str__(self):
        """String representation of the puzzle"""
        return '\n'.join([' '.join(map(str, row)) for row in self.state])
    
    def find_blank(self):
        """Find the position of the blank tile (represented as 0 or None)"""
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == 0 or self.state[i][j] is None:
                    return (i, j)
        return None
    
    def get_neighbors(self):
        """Generate all possible next states by moving the blank tile"""
        blank_row, blank_col = self.find_blank()
        neighbors = []
        
        # Possible moves: up, down, left, right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in moves:
            new_row = blank_row + dr
            new_col = blank_col + dc
            
            # Check if move is valid
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                # Create a new state by swapping blank with adjacent tile
                new_state = [row[:] for row in self.state]  # Deep copy
                new_state[blank_row][blank_col] = new_state[new_row][new_col]
                new_state[new_row][new_col] = 0
                neighbors.append(Puzzle8(new_state))
        
        return neighbors

def bfs(start_state, goal_state):
    """
    Breadth-First Search to solve 8-puzzle
    Returns: (path, number of states explored, total cost)
    """
    start = Puzzle8(start_state)
    goal = Puzzle8(goal_state)
    
    # If start is already the goal
    if start == goal:
        return [start], 1, 0
    
    # Initialize BFS
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    depth = {start: 0}
    states_explored = 0
    
    while queue:
        current = queue.popleft()
        states_explored += 1
        
        # Check if we reached the goal
        if current == goal:
            # Reconstruct path
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            total_cost = depth[current]  # Cost = depth of goal state
            return path, states_explored, total_cost
        
        # Explore neighbors
        for neighbor in current.get_neighbors():
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                depth[neighbor] = depth[current] + 1
                queue.append(neighbor)
    
    return None, states_explored, float('inf')  # No solution found

def dfs(start_state, goal_state, max_depth=50):
    """
    Depth-First Search to solve 8-puzzle
    Returns: (path, number of states explored, total cost)
    """
    start = Puzzle8(start_state)
    goal = Puzzle8(goal_state)
    
    # If start is already the goal
    if start == goal:
        return [start], 1, 0
    
    # Initialize DFS
    stack = [(start, 0)]  # (state, depth)
    visited = set()
    parent = {start: None}
    depth = {start: 0}
    states_explored = 0
    
    while stack:
        current, current_depth = stack.pop()
        states_explored += 1
        
        # Check if we reached the goal
        if current == goal:
            # Reconstruct path
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            total_cost = depth[current]  # Cost = depth of goal state
            return path, states_explored, total_cost
        
        # Skip if max depth reached
        if current_depth >= max_depth:
            continue
        
        # Only explore if not visited at this depth or at a shallower depth
        if current not in visited:
            visited.add(current)
            
            # Explore neighbors (reverse order for more natural exploration)
            neighbors = current.get_neighbors()
            neighbors.reverse()  # DFS typically explores in reverse order
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    parent[neighbor] = current
                    depth[neighbor] = depth[current] + 1
                    stack.append((neighbor, current_depth + 1))
    
    return None, states_explored, float('inf')  # No solution found

# Define start and goal states
start_state = [
    [7, 2, 4],
    [5, 0, 6],  # 0 represents the blank tile
    [8, 3, 1]
]

goal_state = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

if __name__ == "__main__":
    print("8-Puzzle Problem - DFS Solution and Comparison")
    print("=" * 50)
    print("\nStart State:")
    print(Puzzle8(start_state))
    print("\nGoal State:")
    print(Puzzle8(goal_state))
    print("\n" + "=" * 50)
    
    # Run BFS
    print("\n" + "-" * 50)
    print("BFS (Breadth-First Search):")
    print("-" * 50)
    bfs_path, bfs_states, bfs_cost = bfs(start_state, goal_state)
    
    if bfs_path:
        print(f"Solution found!")
        print(f"Number of states explored: {bfs_states}")
        print(f"Path length (number of moves): {len(bfs_path) - 1}")
        print(f"Total cost (depth): {bfs_cost}")
    else:
        print("No solution found!")
        print(f"Number of states explored: {bfs_states}")
    
    # Run DFS
    print("\n" + "-" * 50)
    print("DFS (Depth-First Search):")
    print("-" * 50)
    dfs_path, dfs_states, dfs_cost = dfs(start_state, goal_state, max_depth=50)
    
    if dfs_path:
        print(f"Solution found!")
        print(f"Number of states explored: {dfs_states}")
        print(f"Path length (number of moves): {len(dfs_path) - 1}")
        print(f"Total cost (depth): {dfs_cost}")
    else:
        print("No solution found!")
        print(f"Number of states explored: {dfs_states}")
    
    # Comparison
    print("\n" + "=" * 50)
    print("COMPARISON: BFS vs DFS")
    print("=" * 50)
    
    if bfs_path and dfs_path:
        print(f"\nStates Explored:")
        print(f"  BFS: {bfs_states} states")
        print(f"  DFS: {dfs_states} states")
        print(f"  Difference: {abs(bfs_states - dfs_states)} states")
        
        print(f"\nPath Cost (Depth):")
        print(f"  BFS: {bfs_cost} (optimal - shortest path)")
        print(f"  DFS: {dfs_cost} (may not be optimal)")
        print(f"  Difference: {abs(bfs_cost - dfs_cost)}")
        
        print(f"\nKey Observations:")
        print(f"  1. BFS explores states level by level, guaranteeing optimal solution")
        print(f"  2. DFS explores deeply first, may find longer paths")
        print(f"  3. BFS typically explores more states but finds shorter paths")
        print(f"  4. DFS may explore fewer states but path cost is usually higher")
        
        if bfs_cost < dfs_cost:
            print(f"\n  → BFS found a more optimal solution (lower cost)")
        elif dfs_cost < bfs_cost:
            print(f"\n  → DFS found a more optimal solution (lower cost)")
        else:
            print(f"\n  → Both found solutions with the same cost")
    else:
        print("\nCannot compare - one or both algorithms did not find a solution")
