import random

class VacuumEnvironment:
    def __init__(self):
        # 3 Rooms: A, B, C. 0 = Clean, 1 = Dirty
        self.location_map = ['A', 'B', 'C']
        self.state = {
            'A': random.choice([0, 1]),
            'B': random.choice([0, 1]),
            'C': random.choice([0, 1])
        }
        self.agent_location = random.choice(['A', 'B', 'C'])
        self.performance_score = 0
        self.step_count = 0

    def get_percept(self):
        # Percept: [Location, Status]
        return (self.agent_location, 'Dirty' if self.state[self.agent_location] == 1 else 'Clean')

    def execute_action(self, action):
        self.step_count += 1
        # Performance Cost Definition:
        # +10 for each Clean room at end of step (Maintenance)
        # -1 for each Move (Energy Cost)
        # -2 for Suck execution (Energy Cost) 
        
        cost = 0
        if action == 'Suck':
            self.state[self.agent_location] = 0 # Make Clean
            cost = -2
            print(f"Action: SUCK in {self.agent_location}")
        elif action == 'Right':
            cost = -1
            print(f"Action: MOVE RIGHT from {self.agent_location}")
            if self.agent_location == 'A': self.agent_location = 'B'
            elif self.agent_location == 'B': self.agent_location = 'C'
            # C -> Right stays in C (Wall)
        elif action == 'Left':
            cost = -1
            print(f"Action: MOVE LEFT from {self.agent_location}")
            if self.agent_location == 'C': self.agent_location = 'B'
            elif self.agent_location == 'B': self.agent_location = 'A'
            # A -> Left stays in A (Wall)
        elif action == 'NoOp':
            print("Action: NoOp")
            cost = 0

        # Reward for purely being clean
        clean_bonus = sum(10 for room in ['A', 'B', 'C'] if self.state[room] == 0)
        self.performance_score += (cost + clean_bonus)
        
        return self.get_percept()

def simple_reflex_agent(percept):
    # Rule Table stored effectively as logic here.
    # Rules:
    # 1. If Dirty -> Suck
    # 2. If Clean and A -> Right
    # 3. If Clean and C -> Left
    # 4. If Clean and B -> Random(Left, Right) [Simple Reflex cannot know history]
    
    location, status = percept
    
    if status == 'Dirty':
        return 'Suck'
    
    if location == 'A':
        return 'Right'
    elif location == 'C':
        return 'Left'
    elif location == 'B':
        return random.choice(['Left', 'Right'])
    
    return 'NoOp'

def run_vacuum_simulation(steps=15):
    env = VacuumEnvironment()
    print("--- Starting Vacuum Simulation (3 Rooms: A, B, C) ---")
    print("Rationality: Maximize cleanliness (reward) while minimizing movement/action energy (cost).")
    print("Performance Metric: Score = Sum(+10 per clean room) - 1(Move) - 2(Suck)")
    print("-" * 50)
    
    # 1. Definition of Rule Table (Dictionary format for Display)
    rule_table = {
        ('Any', 'Dirty'): 'Suck',
        ('A', 'Clean'): 'Right',
        ('C', 'Clean'): 'Left',
        ('B', 'Clean'): 'Random(Left, Right)'
    }
    print(f"Agent Rule Table: {rule_table}")
    print("-" * 50)

    print(f"Initial State: {env.state}, Agent at: {env.agent_location}")
    
    current_percept = env.get_percept()
    
    for i in range(steps):
        print(f"\nStep {i+1}:")
        print(f"Percept: {current_percept}")
        
        action = simple_reflex_agent(current_percept)
        current_percept = env.execute_action(action)
        
        print(f"New State: {env.state}")
        print(f"Current Performance Score: {env.performance_score}")

    print("-" * 50)
    print(f"Final Score: {env.performance_score}")
    print("Simulation Complete.")

if __name__ == "__main__":
    run_vacuum_simulation()
