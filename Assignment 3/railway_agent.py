def railway_agent(train, obstacle, emergency):
    action = {'Signal': 'RED', 'Gate': 'OPEN', 'Hooter': 'OFF'}
    
    if emergency or obstacle:
        action['Signal'] = 'RED'
        action['Gate'] = 'OPEN' 
        action['Hooter'] = 'ON'
    elif train:
        action['Signal'] = 'GREEN'
        action['Gate'] = 'CLOSED'
        action['Hooter'] = 'ON'
    else:
        # Default safe state
        action['Signal'] = 'RED'
        action['Gate'] = 'OPEN'
        action['Hooter'] = 'OFF'

    return action

def main():
    print("Railway Crossing Simulation")
    print("Train | Obstacle | Emergency || Signal | Gate | Hooter")
    print("-" * 60)
    
    cases = [
        (False, False, False),
        (False, False, True),
        (False, True, False),
        (False, True, True),
        (True, False, False),
        (True, False, True),
        (True, True, False),
        (True, True, True),
    ]

    for t, o, e in cases:
        res = railway_agent(t, o, e)
        print(f"{str(t):<5} | {str(o):<8} | {str(e):<9} || {res['Signal']:<6} | {res['Gate']:<6} | {res['Hooter']}")

if __name__ == "__main__":
    main()

r"""
## 2. Railway Level Crossing Agent

### Problem Statement
A safety-critical reflex agent for a railway crossing managing a Gate, Signal, and Hooter based on sensors.

### Rule Set & Priorities
The agent must balance Safety (preventing accidents) vs Efficiency (minimizing delay).
**Priorities:**
1.  **Emergency / Obstacle (Critical Safety)**: Overrides all other states.
2.  **Train Approaching (Normal Safety)**: Standard operation.
3.  **Idle (Efficiency)**: Open flow for road traffic.

### Rule Table (Logic)

| Train Detected | Obstacle Detected | Manual Emergency | **Signal** | **Gate** | **Hooter** | **Status** |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| F | F | F | **RED*** | **OPEN** | OFF | **Idle** (Road open) |
| F | F | T | **RED** | **OPEN** | ON | **Emergency** |
| F | T | F | **RED** | **OPEN** | ON | **Obstacle Escape** |
| F | T | T | **RED** | **OPEN** | ON | **Emergency** |
| T | F | F | **GREEN** | **CLOSED** | ON | **Train Passage** |
| T | F | T | **RED** | **OPEN** | ON | **Emergency Stop** |
| T | T | F | **RED** | **OPEN** | ON | **Collision Aversion** |
| T | T | T | **RED** | **OPEN** | ON | **Severe Emergency** |

*\Note on Signal in Idle: Red for Train (Stop), effectively Green for Road.*

### Justification
- **Obstacle Handling**: If an obstacle (vehicle/animal) is detected between gates, the **Gate must remain OPEN** to allow it to escape, and the **Signal must be RED** to stop the train. Closing the gate would trap the obstacle.
- **Manual Override**: The Station Master's lever is absolute. Use cases include equipment failure or un-sensed danger.

### Multi-source Input
The agent successfully integrates 3 distinct binary inputs to form a truth table of $2^3 = 8$ possible states, mapping each to a safe action set.
"""
