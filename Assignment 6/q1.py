import heapq

cities = [
    "Baltimore", "Boston", "Buffalo", "Chicago", "Cleveland", "Columbus", 
    "Detroit", "Indianapolis", "New York", "Philadelphia", "Pittsburgh", 
    "Portland", "Providence", "Syracuse"
]

city_to_index = {city: i for i, city in enumerate(cities)}

adj_matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 101, 247, 0, 0, 0],   
    [0, 0, 0, 0, 0, 0, 0, 0, 215, 0, 0, 107, 50, 312], 
    [0, 0, 0, 0, 189, 0, 256, 0, 0, 0, 215, 0, 0, 150],
    [0, 0, 0, 0, 345, 0, 283, 182, 0, 0, 0, 0, 0, 0],   
    [0, 0, 189, 345, 0, 144, 169, 0, 0, 0, 134, 0, 0, 0], 
    [0, 0, 0, 0, 144, 0, 0, 176, 0, 0, 185, 0, 0, 0],   
    [0, 0, 256, 283, 169, 0, 0, 0, 0, 0, 0, 0, 0, 0],   
    [0, 0, 0, 182, 0, 176, 0, 0, 0, 0, 0, 0, 0, 0],     
    [0, 215, 0, 0, 0, 0, 0, 0, 0, 97, 0, 0, 181, 0],    
    [101, 0, 0, 0, 0, 0, 0, 0, 97, 0, 0, 0, 0, 253],    
    [247, 0, 215, 0, 134, 185, 0, 0, 0, 305, 0, 0, 0, 0], 
    [0, 107, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],       
    [0, 50, 0, 0, 0, 0, 0, 0, 181, 0, 0, 0, 0, 0],      
    [0, 312, 150, 0, 0, 0, 0, 0, 0, 253, 0, 0, 0, 0]    
]

heuristics = [360, 0, 400, 860, 550, 640, 610, 780, 215, 270, 470, 107, 50, 260]

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def greedy_best_first_search(adj, start, goal, h):
    frontier = PriorityQueue()
    frontier.put(start, h[start])
    came_from = {}
    came_from[start] = None
    explored_nodes = 0
    visited = set()

    while not frontier.empty():
        current = frontier.get()
        explored_nodes += 1
        
        if current == goal:
            break
        
        if current in visited:
            continue
        visited.add(current)
        
        for neighbor_idx, cost in enumerate(adj[current]):
            if cost > 0: 
                if neighbor_idx not in visited and neighbor_idx not in came_from:
                    priority = h[neighbor_idx]
                    frontier.put(neighbor_idx, priority)
                    came_from[neighbor_idx] = current
                
    return came_from, explored_nodes

def a_star_search(adj, start, goal, h):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    explored_nodes = 0
    
    while not frontier.empty():
        current = frontier.get()
        explored_nodes += 1
        
        if current == goal:
            break
        
        for neighbor_idx, cost in enumerate(adj[current]):
            if cost > 0: 
                new_cost = cost_so_far[current] + cost
                if neighbor_idx not in cost_so_far or new_cost < cost_so_far[neighbor_idx]:
                    cost_so_far[neighbor_idx] = new_cost
                    priority = new_cost + h[neighbor_idx]
                    frontier.put(neighbor_idx, priority)
                    came_from[neighbor_idx] = current
                
    return came_from, explored_nodes, cost_so_far

def main():
    start_city_name = "Chicago"
    goal_city_name = "Boston"
    
    start_index = city_to_index[start_city_name]
    goal_index = city_to_index[goal_city_name]
    
    print(f"Goal: Reach {goal_city_name} from {start_city_name}")
    print("-" * 50)
    
    print("Running Greedy Best First Search...")
    came_from_greedy, explored_greedy = greedy_best_first_search(adj_matrix, start_index, goal_index, heuristics)
    if goal_index in came_from_greedy:
        path_indices = reconstruct_path(came_from_greedy, start_index, goal_index)
        path_names = [cities[i] for i in path_indices]
        print(f"Path: {' -> '.join(path_names)}")
        
        cost_greedy = 0
        for i in range(len(path_indices)-1):
            u, v = path_indices[i], path_indices[i+1]
            cost_greedy += adj_matrix[u][v]
            
        print(f"Total Cost: {cost_greedy}")
    else:
        print("Path not found.")
    print(f"Explored Nodes: {explored_greedy}")
    print("-" * 50)
    
    print("Running A* Search...")
    came_from_astar, explored_astar, costs_astar = a_star_search(adj_matrix, start_index, goal_index, heuristics)
    if goal_index in came_from_astar:
        path_indices_astar = reconstruct_path(came_from_astar, start_index, goal_index)
        path_names_astar = [cities[i] for i in path_indices_astar]
        print(f"Path: {' -> '.join(path_names_astar)}")
        print(f"Total Cost: {costs_astar[goal_index]}")
    else:
        print("Path not found.")
    print(f"Explored Nodes: {explored_astar}")
    print("-" * 50)

    print("Comparison:")
    print(f"{'Algorithm':<25} | {'Explored Nodes':<15} | {'Path Cost':<10}")
    print("-" * 60)
    
    cost_greedy_val = "N/A"
    if goal_index in came_from_greedy:
        cost_greedy_val = 0
        current_greedy_path = reconstruct_path(came_from_greedy, start_index, goal_index)
        for i in range(len(current_greedy_path)-1):
            u, v = current_greedy_path[i], current_greedy_path[i+1]
            cost_greedy_val += adj_matrix[u][v]

    cost_astar_val = costs_astar[goal_index] if goal_index in came_from_astar else "N/A"
    
    print(f"{'Greedy Best First Search':<25} | {explored_greedy:<15} | {cost_greedy_val:<10}")
    print(f"{'A* Search':<25} | {explored_astar:<15} | {cost_astar_val:<10}")

if __name__ == "__main__":
    main()
