def get_peers():
    peers = {}
    for r in range(9):
        for c in range(9):
            s = set()
            for i in range(9):
                if i != c: s.add((r, i))
                if i != r: s.add((i, c))
            start_r, start_c = 3 * (r // 3), 3 * (c // 3)
            for i in range(start_r, start_r + 3):
                for j in range(start_c, start_c + 3):
                    if (i, j) != (r, c):
                        s.add((i, j))
            peers[(r, c)] = s
    return peers

def ac3(domains, peers):
    q = [(u, v) for u in peers for v in peers[u]]
    removed = 0
    while q:
        u, v = q.pop(0)
        to_del = [x for x in domains[u] if not any(y != x for y in domains[v])]
        if to_del:
            for x in to_del:
                domains[u].remove(x)
                removed += 1
            if not domains[u]:
                return False, removed
            for w in peers[u]:
                if w != v:
                    q.append((w, u))
    return True, removed

grid = "0000060000590000082000080000450000000030000000060030500000007000000000000000050002"
domains = {}
for r in range(9):
    for c in range(9):
        val = int(grid[r*9 + c])
        domains[(r, c)] = [val] if val != 0 else list(range(1, 10))

peers = get_peers()
success, total_removed = ac3(domains, peers)

print(f"Total values removed from domains: {total_removed}")
print("\nDomain Sizes:")
for r in range(9):
    if r % 3 == 0 and r != 0:
        print("-" * 21)
    row_vals = []
    for c in range(9):
        if c % 3 == 0 and c != 0:
            row_vals.append("|")
        row_vals.append(str(len(domains[(r, c)])))
    print(" ".join(row_vals))

is_solved = all(len(d) == 1 for d in domains.values())
is_failed = any(len(d) == 0 for d in domains.values())

print("\nFinal Result:")
if is_failed:
    print("AC-3 detected a failure (puzzle unsolvable).")
elif is_solved:
    print("AC-3 solved the puzzle completely.")
else:
    print("AC-3 thinned the possibilities but some domains still have multiple values.")
