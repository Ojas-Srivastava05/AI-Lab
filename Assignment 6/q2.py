
import heapq

# Maze Definition
# 0: Empty, 1: Wall, 2: Start, 3: Reward
maze = [
    [2, 0, 0, 0, 1],
    [0, 1, 0, 0, 3],
    [0, 3, 0, 1, 1],
    [0, 1, 0, 0, 1],
    [3, 0, 0, 0, 3]
]

# Heuristic: Manhattan distance to the nearest unvisited reward
def heuristic(position, unvisited_rewards):
    if not unvisited_rewards:
        return 0
    
    min_dist = float('inf')
    x, y = position
    for rx, ry in unvisited_rewards:
        dist = abs(x - rx) + abs(y - ry)
        if dist < min_dist:
            min_dist = dist
    return min_dist

class State:
    def __init__(self, x, y, collected_rewards, parent=None, action=None, g=0):
        self.x = x
        self.y = y
        self.collected_rewards = frozenset(collected_rewards) # Set of (x,y) tuples
        self.parent = parent
        self.action = action
        self.g = g
    
    def __lt__(self, other):
        return self.g < other.g # Placeholder, logic handled in priority queue
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.collected_rewards == other.collected_rewards
    
    def __hash__(self):
        return hash((self.x, self.y, self.collected_rewards))

def get_neighbors(state, maze_grid):
    neighbors = []
    directions = [("L", 0, -1), ("R", 0, 1), ("U", -1, 0), ("D", 1, 0)]
    rows = len(maze_grid)
    cols = len(maze_grid[0])
    
    for action, dx, dy in directions:
        nx, ny = state.x + dx, state.y + dy
        
        if 0 <= nx < rows and 0 <= ny < cols:
            if maze_grid[nx][ny] != 1: # Not a wall
                collected = set(state.collected_rewards)
                if maze_grid[nx][ny] == 3:
                    collected.add((nx, ny))
                
                neighbors.append(State(nx, ny, collected, state, action, state.g + 1))
                
    return neighbors

def solve_maze_astar(maze_grid):
    rows = len(maze_grid)
    cols = len(maze_grid[0])
    
    start_pos = None
    all_rewards = []
    
    for r in range(rows):
        for c in range(cols):
            if maze_grid[r][c] == 2:
                start_pos = (r, c)
            elif maze_grid[r][c] == 3:
                all_rewards.append((r, c))
                
    start_state = State(start_pos[0], start_pos[1], [])
    
    frontier = [] # Priority Queue
    # Priority is f(n) = g(n) + h(n)
    h_start = heuristic(start_pos, all_rewards)
    heapq.heappush(frontier, (h_start, start_state))
    
    came_from = {}
    cost_so_far = {}
    
    came_from[start_state] = None
    cost_so_far[start_state] = 0
    
    print(f"Start Position: {start_pos}")
    print(f"Total Rewards to Collect: {len(all_rewards)}")
    print("-" * 30)
    
    visited_states = set()
    
    while frontier:
        current_f, current_state = heapq.heappop(frontier)
        
        if current_state in visited_states:
            continue
        visited_states.add(current_state)
        
        # Check Goal: All rewards collected
        if len(current_state.collected_rewards) == len(all_rewards):
            print("All rewards collected!")
            return current_state, visited_states
        
        current_pos = (current_state.x, current_state.y)
        remaining_rewards = [r for r in all_rewards if r not in current_state.collected_rewards]
        
        for next_state in get_neighbors(current_state, maze_grid):
            new_cost = cost_so_far[current_state] + 1
            
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                
                # Heuristic for next state
                next_pos = (next_state.x, next_state.y)
                remaining_for_next = [r for r in all_rewards if r not in next_state.collected_rewards]
                h = heuristic(next_pos, remaining_for_next)
                priority = new_cost + h
                
                heapq.heappush(frontier, (priority, next_state))
                came_from[next_state] = current_state
                
    return None, visited_states

def print_path(goal_state):
    path = []
    current = goal_state
    while current:
        path.append(current)
        current = current.parent
    path.reverse()
    
    print("\nNo. | Pos    | Action | Collected")
    print("-" * 35)
    for i, state in enumerate(path):
        action = state.action if state.action else "Start"
        print(f"{i:<3} | ({state.x},{state.y})  | {action:<6} | {len(state.collected_rewards)}")
        
    print(f"\nTotal steps: {len(path)-1}")
    return path

def main():
    print("Finding path to collect all rewards using A* Search...")
    goal_state, visited = solve_maze_astar(maze)
    
    if goal_state:
        path = print_path(goal_state)
        
        print("\nTiles visited on the way (Unique locations visited):")
        unique_visited = set()
        for state in path:
            unique_visited.add((state.x, state.y))
        print(sorted(list(unique_visited)))
        
        print("\nNote on Heuristic:")
        print("Heuristic Cost (h(n)): Manhattan distance to the nearest unvisited reward.")
        print("Evaluation Cost (f(n)): g(n) + h(n), where g(n) is the step count from start.")
        print("Justification: This heuristic is admissible because the agent must travel at least")
        print("the distance to the nearest uncollected reward to make progress.")
        
    else:
        print("Solution not found.")

if __name__ == "__main__":
    main()
