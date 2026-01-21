from collections import deque

class Puzzle8:
    def __init__(self, state):
        self.state = state
        self.size = 3
    
    def __eq__(self, other):
        return self.state == other.state
    
    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.state))
    
    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.state])
    
    def find_blank(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] == 0 or self.state[i][j] is None:
                    return (i, j)
        return None
    
    def get_neighbors(self):
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
    start = Puzzle8(start_state)
    goal = Puzzle8(goal_state)
    
    # If start is already the goal
    if start == goal:
        return [start], 1
    
    # Initialize BFS
    queue = deque([start])
    visited = {start}
    parent = {start: None}
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
            return path, states_explored
        
        # Explore neighbors
        for neighbor in current.get_neighbors():
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    return None, states_explored  # No solution found

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
    print("8-Puzzle Problem - BFS Solution")
    print("=" * 40)
    print("\nStart State:")
    print(Puzzle8(start_state))
    print("\nGoal State:")
    print(Puzzle8(goal_state))
    print("\n" + "=" * 40)
    
    path, states_explored = bfs(start_state, goal_state)
    
    if path:
        print(f"\nSolution found!")
        print(f"Number of states explored: {states_explored}")
        print(f"Path length (number of moves): {len(path) - 1}")
        print("\nSolution path:")
        for i, state in enumerate(path):
            print(f"\nStep {i}:")
            print(state)
    else:
        print("\nNo solution found!")
        print(f"Number of states explored: {states_explored}")
