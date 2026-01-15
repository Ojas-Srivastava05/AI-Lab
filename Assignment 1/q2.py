#defining graph 
connections = {
    "Priya": ["Raj", "Aarav", "Neha", "Akash"],
    "Raj": ["Priya", "Sunil"],
    "Aarav": ["Priya", "Neha", "Arjun"],
    "Akash": ["Priya", "Sunil", "Neha"],
    "Sunil": ["Raj", "Akash", "Sneha"],
    "Neha": ["Priya", "Aarav", "Akash", "Rahul"],
    "Sneha": ["Sunil", "Rahul", "Maya"],
    "Rahul": ["Neha", "Sneha", "Arjun", "Pooja"],
    "Maya": ["Sneha"],
    "Arjun": ["Aarav", "Rahul", "Pooja"],
    "Pooja": ["Rahul", "Arjun"]
}

#BFS
def breadth_first(connections, start_node):
    seen = set()
    q = [start_node]
    traversal = []

    seen.add(start_node)

    while q:
        curr = q.pop(0)
        traversal.append(curr)

        for adjacent in connections[curr]:
            if adjacent not in seen:
                seen.add(adjacent)
                q.append(adjacent)

    return traversal

#DFS
def depth_first(connections, start_node, seen=None, traversal=None):
    if seen is None:
        seen = set()
    if traversal is None:
        traversal = []

    seen.add(start_node)
    traversal.append(start_node)

    for adjacent in connections[start_node]:
        if adjacent not in seen:
            depth_first(connections, adjacent, seen, traversal)

    return traversal

#printing results 
starting_point = "Neha"

bfs_output = breadth_first(connections, starting_point)
dfs_output = depth_first(connections, starting_point)

print("BFS Traversal:")
print(bfs_output)

print("\nDFS Traversal:")
print(dfs_output)