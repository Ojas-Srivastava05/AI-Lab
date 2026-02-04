import random

RULES = {
    ('A', 1): 'Clean',
    ('A', 0): 'Right',
    ('B', 1): 'Clean',
    ('B', 0): 'Random',
    ('C', 1): 'Clean',
    ('C', 0): 'Left'
}

def get_action(location, status):
    if location == 'B' and status == 0:
        return random.choice(['Left', 'Right'])
    return RULES[(location, status)]

def main():
    loc = input("Start Location (A, B, C): ").strip().upper()
    
    print("Enter 1 for Dirty, 0 for Clean")
    state = {
        'A': int(input("Status A: ")),
        'B': int(input("Status B: ")),
        'C': int(input("Status C: "))
    }
    
    steps = int(input("How many steps? "))
    
    print(f"\nSTARTING at {loc} with state {state}\n")
    
    for i in range(steps):
        is_dirty = state[loc]
        print(f"Step {i+1} | Percept: ({loc}, {is_dirty})")

        action = get_action(loc, is_dirty)
        print(f"  -> Action: {action}")

        if action == 'Clean':
            state[loc] = 0
        elif action == 'Right':
            if loc == 'A': loc = 'B'
            elif loc == 'B': loc = 'C'
        elif action == 'Left':
            if loc == 'B': loc = 'A'
            elif loc == 'C': loc = 'B'
        
        print(f"  -> New Location: {loc} | State: {state}")

        for room in state:
            if state[room] == 0 and random.random() < 0.2:
                state[room] = 1
                print(f"     (Randomly: {room} became dirty)")
        
        print("-" * 30)

if __name__ == "__main__":
    main()