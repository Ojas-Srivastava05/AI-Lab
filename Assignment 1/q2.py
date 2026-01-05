from collections import deque,defaultdict

n,m=map(int,input().split())

graph = defaultdict(list)

for _ in range(m):
    u,v=input().split()
    graph[u].append(v)
    graph[v].append(u)

start=input().strip()

def bfs(start):
    q=deque([start])
    visited=set()
    visited.add(start)

    bfsorder=[]

    while q:
        person=q.popleft()
        bfsorder.append(person)

        for neighbour in graph[person]:
            if neighbour not in visited:
                visited.add(neighbour)
                q.append(neighbour)

    return bfsorder

def dfs(start):
    visited=set()
    dfsorder=[]

    def dfsrunner(person):
        visited.add(person)

        for neighbour in graph[person]:
            if neighbour in visited:
                continue

            dfsorder.append(neighbour)
            dfsrunner(neighbour)
    
    dfsrunner(start)
    return dfsorder

bfs_result = bfs(start)
dfs_result = dfs(start)

print("\nBFS Traversal:")
print(" -> ".join(bfs_result))

print("\nDFS Traversal:")
print(" -> ".join(dfs_result))

# ai generated input based on the image
'''
13 20
Raj Priya
Raj Sunil
Priya Aarav
Priya Akash
Priya Neha1
Aarav Neha2
Sunil Akash
Sunil Sneha
Akash Neha1
Neha1 Neha2
Neha1 Rahul
Neha2 Arjun
Rahul Sneha
Rahul Arjun
Sneha Maya
Maya Pooja2
Pooja2 Rahul
Pooja2 Pooja1
Pooja1 Arjun
Neha2 Pooja1
Raj
'''
