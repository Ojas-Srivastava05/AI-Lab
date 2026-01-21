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
        br, bc = self.find_blank()
        neighs = []
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dx, dy in moves:
            nr = br + dx
            nc = bc + dy
            
            if 0 <= nr < self.size and 0 <= nc < self.size:
                new = [row[:] for row in self.state]
                new[br][bc] = new[nr][nc]
                new[nr][nc] = 0
                neighs.append(Puzzle8(new))
        
        return neighs

def bfs(s, g):
    start = Puzzle8(s)
    goal = Puzzle8(g)
    
    if start == goal:
        return [start], 1, 0
    
    q = deque([start])
    seen = {start}
    prev = {start: None}
    d = {start: 0}
    count = 0
    
    while q:
        curr = q.popleft()
        count += 1
        
        if curr == goal:
            path = []
            node = curr
            while node is not None:
                path.append(node)
                node = prev[node]
            path.reverse()
            cost = d[curr]
            return path, count, cost
        
        for n in curr.get_neighbors():
            if n not in seen:
                seen.add(n)
                prev[n] = curr
                d[n] = d[curr] + 1
                q.append(n)
    
    return None, count, float('inf')

def dfs(s, g, max_d=50):
    start = Puzzle8(s)
    goal = Puzzle8(g)
    
    if start == goal:
        return [start], 1, 0
    
    stack = [(start, 0)]
    seen = set()
    prev = {start: None}
    d = {start: 0}
    count = 0
    
    while stack:
        curr, cd = stack.pop()
        count += 1
        
        if curr == goal:
            path = []
            node = curr
            while node is not None:
                path.append(node)
                node = prev[node]
            path.reverse()
            cost = d[curr]
            return path, count, cost
        
        if cd >= max_d:
            continue
        
        if curr not in seen:
            seen.add(curr)
            neighs = curr.get_neighbors()
            neighs.reverse()
            
            for n in neighs:
                if n not in seen:
                    prev[n] = curr
                    d[n] = d[curr] + 1
                    stack.append((n, cd + 1))
    
    return None, count, float('inf')

start_state = [
    [7, 2, 4],
    [5, 0, 6],
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
    
    print("\n" + "-" * 50)
    print("BFS (Breadth-First Search):")
    print("-" * 50)
    bp, bc, bcost = bfs(start_state, goal_state)
    
    if bp:
        print(f"Solution found!")
        print(f"Number of states explored: {bc}")
        print(f"Path length (number of moves): {len(bp) - 1}")
        print(f"Total cost (depth): {bcost}")
    else:
        print("No solution found!")
        print(f"Number of states explored: {bc}")
    
    print("\n" + "-" * 50)
    print("DFS (Depth-First Search):")
    print("-" * 50)
    dp, dc, dcost = dfs(start_state, goal_state, max_d=50)
    
    if dp:
        print(f"Solution found!")
        print(f"Number of states explored: {dc}")
        print(f"Path length (number of moves): {len(dp) - 1}")
        print(f"Total cost (depth): {dcost}")
    else:
        print("No solution found!")
        print(f"Number of states explored: {dc}")
    
    print("\n" + "=" * 50)
    print("COMPARISON: BFS vs DFS")
    print("=" * 50)
    
    if bp and dp:
        print(f"\nStates Explored:")
        print(f"  BFS: {bc} states")
        print(f"  DFS: {dc} states")
        print(f"  Difference: {abs(bc - dc)} states")
        
        print(f"\nPath Cost (Depth):")
        print(f"  BFS: {bcost} (optimal - shortest path)")
        print(f"  DFS: {dcost} (may not be optimal)")
        print(f"  Difference: {abs(bcost - dcost)}")
        
        print(f"\nKey Observations:")
        print(f"  1. BFS explores states level by level, guaranteeing optimal solution")
        print(f"  2. DFS explores deeply first, may find longer paths")
        print(f"  3. BFS typically explores more states but finds shorter paths")
        print(f"  4. DFS may explore fewer states but path cost is usually higher")
        
        if bcost < dcost:
            print(f"\n  → BFS found a more optimal solution (lower cost)")
        elif dcost < bcost:
            print(f"\n  → DFS found a more optimal solution (lower cost)")
        else:
            print(f"\n  → Both found solutions with the same cost")
    else:
        print("\nCannot compare - one or both algorithms did not find a solution")
