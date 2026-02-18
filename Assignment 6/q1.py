
import heapq

network = {
    "Chicago": [("Detroit", 283), ("Cleveland", 345), ("Indianapolis", 182)],
    "Indianapolis": [("Chicago", 182), ("Columbus", 176)],
    "Columbus": [("Indianapolis", 176), ("Cleveland", 144), ("Pittsburgh", 185)],
    "Cleveland": [("Chicago", 345), ("Detroit", 169), ("Buffalo", 189), ("Columbus", 144), ("Pittsburgh", 134)],
    "Detroit": [("Chicago", 283), ("Cleveland", 169), ("Buffalo", 256)],
    "Buffalo": [("Detroit", 256), ("Cleveland", 189), ("Syracuse", 150), ("Pittsburgh", 215)],
    "Pittsburgh": [("Cleveland", 134), ("Buffalo", 215), ("Columbus", 185), ("Philadelphia", 305), ("Baltimore", 247)],
    "Baltimore": [("Pittsburgh", 247), ("Philadelphia", 101)],
    "Philadelphia": [("Baltimore", 101), ("New York", 97), ("Syracuse", 253)],
    "New York": [("Philadelphia", 97), ("Boston", 215), ("Providence", 181)],
    "Providence": [("New York", 181), ("Boston", 50)],
    "Boston": [("Providence", 50), ("Syracuse", 312), ("Portland", 107), ("New York", 215)],
    "Portland": [("Boston", 107)],
    "Syracuse": [("Buffalo", 150), ("Boston", 312), ("Philadelphia", 253)]
}

heuristics = {
    "Boston": 0,
    "Providence": 50,
    "Portland": 107,
    "New York": 215,
    "Philadelphia": 270,
    "Baltimore": 360,
    "Syracuse": 260,
    "Buffalo": 400,
    "Pittsburgh": 470,
    "Cleveland": 550,
    "Columbus": 640,
    "Detroit": 610,
    "Indianapolis": 780,
    "Chicago": 860
}

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

def greedy_best_first_search(graph, start, goal, h):
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
        
        neighbors = graph.get(current, [])
        for next_node, cost in neighbors:
            if next_node not in visited and next_node not in came_from:
                priority = h.get(next_node, float('inf'))
                frontier.put(next_node, priority)
                came_from[next_node] = current
                
    return came_from, explored_nodes

def a_star_search(graph, start, goal, h):
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
        
        neighbors = graph.get(current, [])
        for next_node, cost in neighbors:
            new_cost = cost_so_far[current] + cost
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + h.get(next_node, float('inf'))
                frontier.put(next_node, priority)
                came_from[next_node] = current
                
    return came_from, explored_nodes, cost_so_far

def main():
    start_city = "Chicago"
    goal_city = "Boston"
    
    print(f"Goal: Reach {goal_city} from {start_city}")
    print("-" * 50)
    
    print("Running Greedy Best First Search...")
    came_from_greedy, explored_greedy = greedy_best_first_search(network, start_city, goal_city, heuristics)
    if goal_city in came_from_greedy:
        path_greedy = reconstruct_path(came_from_greedy, start_city, goal_city)
        print(f"Path: {' -> '.join(path_greedy)}")
        cost_greedy = 0
        for i in range(len(path_greedy)-1):
            u, v = path_greedy[i], path_greedy[i+1]
            for neighbor, weight in network[u]:
                if neighbor == v:
                    cost_greedy += weight
                    break
        print(f"Total Cost: {cost_greedy}")
    else:
        print("Path not found.")
    print(f"Explored Nodes: {explored_greedy}")
    print("-" * 50)
    
    print("Running A* Search...")
    came_from_astar, explored_astar, costs_astar = a_star_search(network, start_city, goal_city, heuristics)
    if goal_city in came_from_astar:
        path_astar = reconstruct_path(came_from_astar, start_city, goal_city)
        print(f"Path: {' -> '.join(path_astar)}")
        print(f"Total Cost: {costs_astar[goal_city]}")
    else:
        print("Path not found.")
    print(f"Explored Nodes: {explored_astar}")
    print("-" * 50)

    print("Comparison:")
    print(f"{'Algorithm':<25} | {'Explored Nodes':<15} | {'Path Cost':<10}")
    print("-" * 60)
    
    cost_greedy_val = "N/A"
    if goal_city in came_from_greedy:
        cost_greedy_val = 0
        for i in range(len(path_greedy)-1):
            u, v = path_greedy[i], path_greedy[i+1]
            for neighbor, weight in network[u]:
                if neighbor == v:
                    cost_greedy_val += weight
                    break

    cost_astar_val = costs_astar[goal_city] if goal_city in came_from_astar else "N/A"
    
    print(f"{'Greedy Best First Search':<25} | {explored_greedy:<15} | {cost_greedy_val:<10}")
    print(f"{'A* Search':<25} | {explored_astar:<15} | {cost_astar_val:<10}")

if __name__ == "__main__":
    main()
