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

"""
# Assignment 3: Simple Reflex Agents Report

## 1. Vacuum Cleaner Agent

### Problem Statement
A simple reflex agent navigating a three-room environment (A, B, C) to maintain cleanliness.

### Rationality
The rationality of the vacuum agent is defined by its ability to maximize its **Performance Score**.
- **Percepts**: Current Location, Status of Current Room (Clean/Dirty).
- **Actions**: Clean, Move Left, Move Right.
- **Rational Action**: The agent chooses an action that is expected to maximize its future cumulative reward. For a simple reflex agent without state history:
    - If Dirty, it *must* Clean (High Reward for Cleanliness).
    - If Clean, it *must* Move to explore other rooms.

### Performance Cost Definition
We defined the performance metric ($P$) as:
$$ P = \sum (\text{Clean Rooms} \times 10) - (\text{Move Cost} \times 1) - (\text{Cleaning Cost} \times 2) $$

- **Reasoning**:
    - **Cleanliness (+10)**: High reward ensures the primary goal is met.
    - **Cleaning Cost (-2)**: Energy consumption for operation. Prevents cleaning in already clean rooms.
    - **Move Cost (-1)**: Energy consumption for movement. Encourages efficiency.

### Rule Table
| Percept (Location, Status) | Action | Reasoning |
| :--- | :--- | :--- |
| `(Any, Dirty)` | **Clean** | Immediate priority to clean. |
| `(A, Clean)` | **Right** | Only valid move from end room A. |
| `(C, Clean)` | **Left** | Only valid move from end room C. |
| `(B, Clean)` | **Random(Left, Right)** | Since the agent has no memory (Simple Reflex), it doesn't know where it came from. Random/Alternating is the rational choice to ensure eventual coverage of both A and C. |

### Priorities
Yes, strict priorities are encoded:
1. **Cleaning (Dirty)** > **Moving**.
"""