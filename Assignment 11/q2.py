def get_permutations(elements, r):
    if r == 0:
        yield ()
        return
    for i in range(len(elements)):
        for p in get_permutations(elements[:i] + elements[i+1:], r - 1):
            yield (elements[i],) + p

for p in get_permutations(tuple(range(10)), 8):
    s, e, n, d, m, o, r, y = p
    if s == 0 or m == 0:
        continue
    send = s*1000 + e*100 + n*10 + d
    more = m*1000 + o*100 + r*10 + e
    money = m*10000 + o*1000 + n*100 + e*10 + y
    if send + more == money:
        print("SEND + MORE = MONEY")
        print(f"  {send}")
        print(f"+ {more}")
        print("------")
        print(f" {money}")
        print()
        for letter, val in zip("SENDMORY", [s,e,n,d,m,o,r,y]):
            print(f"  {letter} = {val}")
        break
