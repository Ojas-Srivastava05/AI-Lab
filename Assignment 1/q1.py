#defining Queue
class Queue:
    def __init__(self):
        self.elements = []

    def add(self, element):
       
        self.elements = self.elements + [element]

    def remove(self):
      
        if self.check_empty():
            return None

        first = self.elements[0]
        self.elements = self.elements[1:]
        return first

    def check_empty(self):
        return len(self.elements) == 0
    
#BFS
def find_all_bfs_routes(network, origin, destination):
        queue = Queue()
        queue.add((origin, [origin], 0))
        all_routes = []

        while not queue.check_empty():
            node, route, distance = queue.remove()

            if node == destination:
                all_routes.append((route, distance))
                continue

            for next_node, edge_weight in network[node]:
                if next_node not in route:
                    queue.add((next_node, route + [next_node], distance + edge_weight))

        return all_routes

#DFS
def find_all_dfs_routes(network, origin, destination, route=None, distance=0, all_routes=None):
    if route is None:
        route = [origin]
    if all_routes is None:
        all_routes = []

    if origin == destination:
        all_routes.append((route, distance))
        return all_routes

    for next_node, edge_weight in network[origin]:
        if next_node not in route:
            find_all_dfs_routes(
                network,
                next_node,
                destination,
                route + [next_node],
                distance + edge_weight,
                all_routes
            )

    return all_routes

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

origin = "Syracuse"
destination = "Chicago"


breadth_first_routes = find_all_bfs_routes(network, origin, destination)
depth_first_routes = find_all_dfs_routes(network, origin, destination)

print("BFS Routes:")
for route, distance in breadth_first_routes:
    print(route, "Distance:", distance)

print("\nDFS Routes:")
for route, distance in depth_first_routes:
    print(route, "Distance:", distance)