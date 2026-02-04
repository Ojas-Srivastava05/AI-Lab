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

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost < other.path_cost

    def __repr__(self):
        return f"Node({self.state}, cost={self.path_cost})"

class Problem:
    def __init__(self, initial, goal, graph):
        self.initial = initial
        self.goal = goal
        self.graph = graph

    def is_goal(self, state):
        return state == self.goal

    def actions(self, state):
        return [neighbor for neighbor, cost in self.graph.get(state, [])]

    def result(self, state, action):
        return action

    def action_cost(self, s, action, s_prime):
        for neighbor, cost in self.graph.get(s, []):
            if neighbor == s_prime:
                return cost
        return float('inf')

def expand(problem, node):
    s = node.state
    for action in problem.actions(s):
        s_prime = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s_prime)
        yield Node(state=s_prime, parent=node, action=action, path_cost=cost)

def best_first_search(problem, f):
    node = Node(state=problem.initial)
    frontier = []
    heapq.heappush(frontier, (f(node), node))
    
    reached = {problem.initial: node}
    
    nodes_explored_count = 0

    while frontier:
        _, node = heapq.heappop(frontier)
        
        nodes_explored_count += 1
        
        if problem.is_goal(node.state):
            print(f"Goal Reached! Total nodes expanded: {nodes_explored_count}")
            return node, nodes_explored_count
        
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                heapq.heappush(frontier, (f(child), child))
                
    return None, nodes_explored_count

def compute_heuristic_table(graph, goal):
    h = {}
    pq = [(0, goal)]
    visited = set()

    print("Computing Heuristic Table (getting min costs from Goal)...")
    
    while pq:
        cost, u = heapq.heappop(pq)
        
        if u in visited:
            continue
        visited.add(u)
        h[u] = cost
        
        for v, edge_cost in graph.get(u, []):
            if v not in visited:
                heapq.heappush(pq, (cost + edge_cost, v))
                
    return h

def print_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    print(" -> ".join(reversed(path)))

def main():
    start_city = "Syracuse"
    goal_city = "Chicago"
    
    heuristic_table = compute_heuristic_table(network, goal_city)
    
    print("\nPrecomputed Heuristic Table (h values):")
    for city, val in sorted(heuristic_table.items()):
        print(f"  h({city}) = {val}")
    print("-" * 40)

    problem = Problem(start_city, goal_city, network)

    print("\nRunning Greedy Best First Search (f = h)...")
    def f_greedy(n):
        return heuristic_table.get(n.state, float('inf'))
        
    result_greedy, count_greedy = best_first_search(problem, f_greedy)
    if result_greedy:
        print("Path found:")
        print_path(result_greedy)
        print(f"Total Cost: {result_greedy.path_cost}")
    else:
        print("Failure")

    print("-" * 40)

    print("\nRunning A* Search (f = g + h)...")
    def f_astar(n):
        return n.path_cost + heuristic_table.get(n.state, float('inf'))

    result_astar, count_astar = best_first_search(problem, f_astar)
    if result_astar:
        print("Path found:")
        print_path(result_astar)
        print(f"Total Cost: {result_astar.path_cost}")
    else:
        print("Failure")
    
    print("-" * 40)
    print("Comparison of Nodes Expanded:")
    print(f"Greedy Best First Search: {count_greedy}")
    print(f"A* Search:                {count_astar}")
    print("Note: Since we used a perfect heuristic (actual shortest path distance),")
    print("both algorithms find the optimal path very efficiently.")

if __name__ == "__main__":
    main()
