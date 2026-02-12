import time

class State:
    def __init__(self, g, b, pos, parent=None, action=None):
        self.g = g
        self.b = b
        self.pos = pos
        self.parent = parent
        self.action = action
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def is_valid(self):
        if self.g < 0 or self.b < 0 or self.g > 3 or self.b > 3:
            return False
        
        if self.g > 0 and self.g < self.b:
            return False
        
        gr = 3 - self.g
        br = 3 - self.b
        if gr > 0 and gr < br:
            return False
            
        return True

    def is_goal(self):
        return self.g == 0 and self.b == 0 and self.pos == 0

    def __eq__(self, other):
        return self.g == other.g and self.b == other.b and self.pos == other.pos

    def __hash__(self):
        return hash((self.g, self.b, self.pos))

    def __str__(self):
        return f" L: ({self.g}G, {self.b}B, {'B' if self.pos==1 else ' '}) | R: ({3-self.g}G, {3-self.b}B, {'B' if self.pos==0 else ' '})"

def get_next(u):
    res = []
    # (girls, boys) to move
    steps = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
    
    for dg, db in steps:
        if u.pos == 1:
            v = State(u.g - dg, u.b - db, 0, u, f"Move {dg} Girls, {db} Boys to Right")
        else:
            v = State(u.g + dg, u.b + db, 1, u, f"Move {dg} Girls, {db} Boys to Left")
            
        if v.is_valid():
            res.append(v)
            
    return res

def run_dls(start, limit):
    count = 0
    
    def dfs(u, limit, path):
        nonlocal count
        count += 1
        
        if u.is_goal():
            return u
        
        if limit <= 0:
            return None
        
        for v in get_next(u):
            if v not in path:
                path.add(v)
                res = dfs(v, limit - 1, path)
                if res:
                    return res
                path.remove(v)
        return None

    return dfs(start, limit, {start}), count

def run_ids(start):
    d = 0
    total = 0
    while True:
        res, c = run_dls(start, d)
        total += c
        if res:
            return res, total, d
        d += 1
        if d > 20: 
            return None, total, d

def show_path(node):
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
    root = State(3, 3, 1)
    
    print("--- Problem: 3 Girls and 3 Boys River Crossing ---")
    
    print("\n[1a] Running Depth Limited Search (Limit=3)...")
    t0 = time.time()
    res_dls, c_dls = run_dls(root, 3)
    t1 = time.time()
    
    if res_dls:
        print("Solution found!")
        show_path(res_dls)
    else:
        print("No solution found within depth limit 3.")
    
    print(f"Nodes Explored: {c_dls}")
    print(f"Time Taken: {t1 - t0:.6f} seconds")
    
    print("\n[1b] Running Iterative Deepening Search...")
    t0 = time.time()
    res_ids, c_ids, d_ids = run_ids(root)
    t1 = time.time()
    
    if res_ids:
        print(f"Solution found at depth {d_ids}!")
        show_path(res_ids)
    else:
        print("No solution found.")
        
    print(f"Total Nodes Explored: {c_ids}")
    print(f"Time Taken: {t1 - t0:.6f} seconds")
    
    print("\n--- Comparison ---")
    print(f"{'Algorithm':<25} | {'Explored Nodes':<15} | {'Time (s)':<15} | {'Status'}")
    print("-" * 75)
    print(f"{'DLS (Limit=3)':<25} | {c_dls:<15} | {t1 - t0:.6f}          | {'Failed' if not res_dls else 'Success'}")
    print(f"{'IDS':<25} | {c_ids:<15} | {t1 - t0:.6f}          | {'Success' if res_ids else 'Failed'}")

if __name__ == "__main__":
    main()
