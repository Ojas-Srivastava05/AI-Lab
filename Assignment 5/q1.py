import time

class State:
    def __init__(self, missionaries_left, cannibals_left, boat, parent=None, action=None):
        self.m_left = missionaries_left
        self.c_left = cannibals_left
        self.boat = boat
        self.parent = parent
        self.action = action
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def is_valid(self):
        if self.m_left < 0 or self.c_left < 0 or self.m_left > 3 or self.c_left > 3:
            return False
        
        if self.m_left > 0 and self.m_left < self.c_left:
            return False
        
        m_right = 3 - self.m_left
        c_right = 3 - self.c_left
        if m_right > 0 and m_right < c_right:
            return False
            
        return True

    def is_goal(self):
        return self.m_left == 0 and self.c_left == 0 and self.boat == 0

    def __eq__(self, other):
        return self.m_left == other.m_left and self.c_left == other.c_left and self.boat == other.boat

    def __hash__(self):
        return hash((self.m_left, self.c_left, self.boat))

    def __str__(self):
        return f"Left: ({self.m_left}M, {self.c_left}C, {'B' if self.boat==1 else ' '}) | Right: ({3-self.m_left}M, {3-self.c_left}C, {'B' if self.boat==0 else ' '})"

def get_successors(state):
    successors = []
    moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
    
    for m, c in moves:
        if state.boat == 1:
            new_state = State(state.m_left - m, state.c_left - c, 0, state, f"Move {m}M {c}C to Right")
        else:
            new_state = State(state.m_left + m, state.c_left + c, 1, state, f"Move {m}M {c}C to Left")
            
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
    
    print(f"{'Step':<5} | {'State':<40} | {'Action'}")
    print("-" * 70)
    for i, state in enumerate(path):
        action = state.action if state.action else "Start"
        print(f"{i:<5} | {state} | {action}")

def main():
    initial_state = State(3, 3, 1)
    
    print("--- Problem: Missionaries and Cannibals (3M, 3C) ---")
    
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
