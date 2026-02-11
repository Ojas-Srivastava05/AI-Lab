import time

class State:
    def __init__(self, girls_left, boys_left, boat, parent=None, action=None):
        self.g_left = girls_left
        self.b_left = boys_left
        self.boat = boat
        self.parent = parent
        self.action = action
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def is_valid(self):
        if self.g_left < 0 or self.b_left < 0 or self.g_left > 3 or self.b_left > 3:
            return False
        
        if self.g_left > 0 and self.g_left < self.b_left:
            return False
        
        g_right = 3 - self.g_left
        b_right = 3 - self.b_left
        if g_right > 0 and g_right < b_right:
            return False
            
        return True

    def is_goal(self):
        return self.g_left == 0 and self.b_left == 0 and self.boat == 0

    def __eq__(self, other):
        return self.g_left == other.g_left and self.b_left == other.b_left and self.boat == other.boat

    def __hash__(self):
        return hash((self.g_left, self.b_left, self.boat))

    def __str__(self):
        return f"Left: ({self.g_left}G, {self.b_left}B, {'Boat' if self.boat==1 else '    '}) | Right: ({3-self.g_left}G, {3-self.b_left}B, {'Boat' if self.boat==0 else '    '})"

def get_successors(state):
    successors = []
    moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
    
    for g, b in moves:
        if state.boat == 1:
            new_state = State(state.g_left - g, state.b_left - b, 0, state, f"Move {g} Girls, {b} Boys to Right")
        else:
            new_state = State(state.g_left + g, state.b_left + b, 1, state, f"Move {g} Girls, {b} Boys to Left")
            
        if new_state.is_valid():
            successors.append(new_state)
            
    return successors

def dls(start_state, limit):
    nodes_explored = 0
    
    def recursive_dls(node, limit, path_visited):
        nonlocal nodes_explored
        nodes_explored += 1
        
        if node.is_goal():
            return node
        
        if limit <= 0:
            return None
        
        for succ in get_successors(node):
            if succ not in path_visited:
                path_visited.add(succ)
                result = recursive_dls(succ, limit - 1, path_visited)
                if result is not None:
                    return result
                path_visited.remove(succ)
        return None

    return recursive_dls(start_state, limit, {start_state}), nodes_explored

def ids(start_state):
    depth = 0
    total_nodes_explored = 0
    while True:
        result, nodes = dls(start_state, depth)
        total_nodes_explored += nodes
        if result:
            return result, total_nodes_explored, depth
        depth += 1
        if depth > 20: 
            return None, total_nodes_explored, depth

def print_solution(node):
    path = []
    while node:
        path.append(node)
        node = node.parent
    path.reverse()
    
    print(f"{'Step':<5} | {'State':<45} | {'Action'}")
    print("-" * 80)
    for i, state in enumerate(path):
        action = state.action if state.action else "Start"
        print(f"{i:<5} | {state} | {action}")

def main():
    initial_state = State(3, 3, 1)
    
    print("--- Problem: 3 Girls and 3 Boys River Crossing ---")
    
    print("\n[1a] Running Depth Limited Search (Limit=3)...")
    start_time = time.time()
    result_dls, nodes_dls = dls(initial_state, 3)
    end_time = time.time()
    
    if result_dls:
        print("Solution found!")
        print_solution(result_dls)
    else:
        print("No solution found within depth limit 3.")
    
    print(f"Nodes Explored: {nodes_dls}")
    print(f"Time Taken: {end_time - start_time:.6f} seconds")
    
    print("\n[1b] Running Iterative Deepening Search...")
    start_time = time.time()
    result_ids, nodes_ids, depth_ids = ids(initial_state)
    end_time = time.time()
    
    if result_ids:
        print(f"Solution found at depth {depth_ids}!")
        print_solution(result_ids)
    else:
        print("No solution found.")
        
    print(f"Total Nodes Explored: {nodes_ids}")
    print(f"Time Taken: {end_time - start_time:.6f} seconds")
    
    print("\n--- Comparison ---")
    print(f"{'Algorithm':<25} | {'Explored Nodes':<15} | {'Time (s)':<15} | {'Status'}")
    print("-" * 75)
    print(f"{'DLS (Limit=3)':<25} | {nodes_dls:<15} | {end_time - start_time:.6f}          | {'Failed' if not result_dls else 'Success'}")
    print(f"{'IDS':<25} | {nodes_ids:<15} | {end_time - start_time:.6f}          | {'Success' if result_ids else 'Failed'}")

if __name__ == "__main__":
    main()
