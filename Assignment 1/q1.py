from collections import defaultdict
from collections import deque
n,m=map(int,input().split())
graph = defaultdict(list)

for _ in range(m):
    u,v,w=input().split()
    graph[u].append((v,int(w)))
    graph[v].append((u,int(w)))

start,end=input().split()

def bfs(start,end):
    q=deque()
    visited=set()

    q.append((start,0,[start]))  #Ye unordered_map jo upar banaya tha usse start ke saare neighbour leke unko push kar rhe hain 
    #jaise hum cpp mei start waale ko queue mei daal dete the waise ye kia jaara hai

    all_costs=[] #ye vector banaya hai aisa socho jisme saari costs append kar denge

    while q:  #while(!q.empty()) kia hai 
        city,cost,path=q.popleft()
        if city==end:
            all_costs.append((path,cost))
            continue

        if city in visited:
            continue # agar woh city already visited hai toh path overlap ho jaaega islie aage badh jaao
        
        visited.add(city)

        for neighbour,w in graph[city]:
            if neighbour not in visited:
                q.append((neighbour,cost+w,path+[neighbour]))

    return all_costs


def dfs(start,end): #Ek cheez note karne ke lie ye hai ki dfs bht hi asaan hai likhna python mei as compared to bfs kyunki bfs mei apan koi bhi visited ka set nhi lete the cpp mei but yha hume lena pada dono bfs and dfs ke lie
    visited=set()
    result=[]
    def dfsrunner(city,cost,path):
        if city==end:
            result.append((path.copy(),cost))
            return
        
        visited.add(city)

        for neighbour,w in graph[city]:
            if neighbour in visited:
                continue
            dfsrunner(neighbour,cost+w,path+[neighbour])
        
        visited.remove(city)
    dfsrunner(start,0,[start])
    return result

paths=dfs(start,end)
print("All possible DFS paths and costs:")
for path, cost in paths:
    print(" -> ".join(path), " | Cost =", cost) #ye printing format yaad karle aage bht kaam aaega join waala

results = bfs(start, end)

print("All possible BFS paths and costs:")
for path, cost in results:
    print(" -> ".join(path), " | Cost =", cost)


#This input is AI generated based on the image provided in the assignment
'''
14 20
Chicago Detroit 283
Chicago Cleveland 345
Chicago Indianapolis 182
Indianapolis Columbus 176
Columbus Cleveland 144
Columbus Pittsburgh 185
Cleveland Detroit 169
Cleveland Buffalo 189
Detroit Buffalo 256
Buffalo Syracuse 150
Syracuse Boston 312
Syracuse New_York 254
Boston Providence 50
Boston Portland 107
Providence New_York 181
New_York Philadelphia 97
Philadelphia Baltimore 101
Baltimore Pittsburgh 247
Pittsburgh Buffalo 215
Pittsburgh Philadelphia 305
Syracuse Chicago
'''