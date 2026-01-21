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
        return [start], 1
    
    q = deque([start])
    seen = {start}
    prev = {start: None}
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
            return path, count
        
        for n in curr.get_neighbors():
            if n not in seen:
                seen.add(n)
                prev[n] = curr
                q.append(n)
    
    return None, count

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
    print("8-Puzzle Problem - BFS Solution")
    print("=" * 40)
    print("\nStart State:")
    print(Puzzle8(start_state))
    print("\nGoal State:")
    print(Puzzle8(goal_state))
    print("\n" + "=" * 40)
    
    path, count = bfs(start_state, goal_state)
    
    if path:
        print(f"\nSolution found!")
        print(f"Number of states explored: {count}")
        print(f"Path length (number of moves): {len(path) - 1}")
        print("\nSolution path:")
        for i, state in enumerate(path):
            print(f"\nStep {i}:")
            print(state)
    else:
        print("\nNo solution found!")
        print(f"Number of states explored: {count}")
