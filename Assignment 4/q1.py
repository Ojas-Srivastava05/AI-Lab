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
    frontier.append((f(node), node))
    
    reached = {problem.initial: node}
    
    nodes_explored_count = 0

    while frontier:
        frontier.sort(key=lambda x: x[0])
        _, node = frontier.pop(0)
        
        nodes_explored_count += 1
        
        if problem.is_goal(node.state):
            return node, nodes_explored_count
        
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.append((f(child), child))
                
    return None, nodes_explored_count


def get_path_string(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return " -> ".join(reversed(path))

def main():
    start_city = "Syracuse"
    goal_city = "Chicago"
    

    problem = Problem(start_city, goal_city, network)

    def f_cost(n):
        return n.path_cost

    result, count = best_first_search(problem, f_cost)
    path = get_path_string(result) if result else "No Path"
    cost = result.path_cost if result else 0
    
    print("\n" + "-" * 60)
    print(f"{'Algorithm':<25} | {'Explored':<10} | {'Cost':<6} | {'Path'}")
    print("-" * 60)
    print(f"{'Best First Search':<25} | {count:<10} | {cost:<6} | {path}")
    print("-" * 60)

if __name__ == "__main__":
    main()
