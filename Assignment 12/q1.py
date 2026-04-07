def ac3(domains, adj, trace=False):
    queue = []
    for u in adj:
        for v in adj[u]:
            queue.append((u, v))
    
    count = 0
    while queue:
        u, v = queue.pop(0)
        to_remove = [x for x in domains[u] if not any(y != x for y in domains[v])]
        
        if to_remove:
            for x in to_remove:
                domains[u].remove(x)
            if trace and count < 5:
                print(f"Arc ({u}, {v}) revised, domain reduced to {domains[u]}")
                count += 1
            if not domains[u]:
                return False
            for w in adj[u]:
                if w != v:
                    queue.append((w, u))
        elif trace and count < 5:
            print(f"Arc ({u}, {v}) checked, no change")
            count += 1
            
    return True

adj = {
    'P1': ['P2', 'P3', 'P6'],
    'P2': ['P1', 'P3', 'P4'],
    'P3': ['P1', 'P2', 'P5'],
    'P4': ['P2', 'P6'],
    'P5': ['P3', 'P6'],
    'P6': ['P1', 'P4', 'P5']
}

rooms = {'R1', 'R2', 'R3'}
domains = {p: rooms.copy() for p in adj}

print("Tracing the first 5 arc comparisons:")
ac3(domains, adj, trace=True)

print(f"\nProblem Arc-Consistent? {all(domains.values())}")

domains['P1'] = {'R1'}
print("\nAssigning Team P1 to Room R1 and re-running AC-3...")
if ac3(domains, adj):
    print("Arc consistency maintained. Final domains:")
    for p in sorted(domains.keys()):
        print(f"{p}: {domains[p]}")
else:
    print("AC-3 detected a failure.")
