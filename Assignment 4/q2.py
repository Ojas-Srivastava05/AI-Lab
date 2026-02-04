import heapq
import random

class Node:
    def __init__(self, r, c, g=0, h=0, parent=None, action=None):
        self.r = r
        self.c = c
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent
        self.action = action

    def __lt__(self, other):
        return self.f < other.f

def get_manhattan_distance(r1, c1, r2, c2):
    return abs(r1 - r2) + abs(c1 - c2)

def print_grid(rows, cols, obstacles, start, end, path_map=None):
    print("-" * (cols * 3 + 2))
    for r in range(rows):
        line = "|"
        for c in range(cols):
            if (r, c) == start:
                symbol = "S "
            elif (r, c) == end:
                symbol = "E "
            elif (r, c) in obstacles:
                symbol = "# "
            elif path_map and (r, c) in path_map:
                symbol = path_map[(r, c)] + " "
            else:
                symbol = ". "
            line += " " + symbol
        line += "|"
        print(line)
    print("-" * (cols * 3 + 2))

def main():
    try:
        print("Enter Grid Dimensions (rows cols): ")
        rows, cols = map(int, input().split())
        
        print("Enter Start Coordinates (r c): ")
        start_r, start_c = map(int, input().split())
        start = (start_r, start_c)
        
        print("Enter End Coordinates (r c): ")
        end_r, end_c = map(int, input().split())
        end = (end_r, end_c)
        
        print("Enter Number of Obstacles: ")
        num_obstacles = int(input())
    except ValueError:
        print("Invalid input format.")
        return

    obstacles = set()
    possible_locs = [(r, c) for r in range(rows) for c in range(cols) 
                     if (r, c) != start and (r, c) != end]
    
    if num_obstacles > len(possible_locs):
        print("Too many obstacles for grid size!")
        num_obstacles = len(possible_locs)
        
    for pos in random.sample(possible_locs, num_obstacles):
        obstacles.add(pos)

    print("\nInitial Grid Layout:")
    print("S: Start, E: Exit, #: Wall/Obstacle, .: Empty")
    print_grid(rows, cols, obstacles, start, end)

    print("\nJustification for Evaluation Function:")
    print("We use f(n) = g(n) + h(n) (A* Search).")
    print("- g(n): Actual cost from start. We assume uniform cost (1) per step.")
    print("- h(n): Manhattan distance. Since movement is restricted to 4 directions (up, down, left, right),")
    print("  Manhattan distance is an admissible heuristic (never overestimates).")
    print("  This guarantees the optimal (shortest) path for evacuation.")
    
    open_list = []
    start_node = Node(start[0], start[1], g=0, h=get_manhattan_distance(start[0], start[1], end[0], end[1]))
    heapq.heappush(open_list, start_node)
    
    visited = {}
    visited[start] = 0
    
    final_node = None
    
    moves = [(-1, 0, '↑'), (1, 0, '↓'), (0, -1, '←'), (0, 1, '→')]

    nodes_expanded = 0

    while open_list:
        current = heapq.heappop(open_list)
        nodes_expanded += 1
        
        if (current.r, current.c) == end:
            final_node = current
            break
        
        for dr, dc, arrow in moves:
            nr, nc = current.r + dr, current.c + dc
            
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in obstacles:
                new_g = current.g + 1
                
                if (nr, nc) not in visited or new_g < visited[(nr, nc)]:
                    visited[(nr, nc)] = new_g
                    h = get_manhattan_distance(nr, nc, end[0], end[1])
                    child = Node(nr, nc, g=new_g, h=h, parent=current, action=arrow)
                    heapq.heappush(open_list, child)

    if final_node:
        print(f"\nGoal Reached! Path Length: {final_node.g}")
        print(f"Nodes Expanded: {nodes_expanded}")
        
        path_map = {}
        curr = final_node
        while curr.parent:
            path_map[(curr.parent.r, curr.parent.c)] = curr.action
            curr = curr.parent
        
        print("\nEvacuation Plan (Follow Arrows):")
        print_grid(rows, cols, obstacles, start, end, path_map)
    else:
        print("\nNo path found! Evacuation path blocked.")

if __name__ == "__main__":
    main()
