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

---

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

*\*Note on Signal in Idle: Red for Train (Stop), effectively Green for Road.*

### Justification
- **Obstacle Handling**: If an obstacle (vehicle/animal) is detected between gates, the **Gate must remain OPEN** to allow it to escape, and the **Signal must be RED** to stop the train. Closing the gate would trap the obstacle.
- **Manual Override**: The Station Master's lever is absolute. Use cases include equipment failure or un-sensed danger.

### Multi-source Input
The agent successfully integrates 3 distinct binary inputs to form a truth table of $2^3 = 8$ possible states, mapping each to a safe action set.

---

## Simulation Output
*Please refer to the terminal output of `vacuum_agent.py` and `railway_agent.py` for live simulation logs.*
