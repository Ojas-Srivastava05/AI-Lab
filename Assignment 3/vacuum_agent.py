import random

class VacuumEnvironment:
    def __init__(self):
        self.location_condition = {
            'A': random.randint(0, 1),
            'B': random.randint(0, 1),
            'C': random.randint(0, 1)
        }
        self.agent_loc = random.choice(['A', 'B', 'C'])
        self.score = 0

    def get_percept(self):
        return (self.agent_loc, self.location_condition[self.agent_loc])

    def step(self, action):
        cost = 0
        if action == 'Clean':
            cost = -2
            print(f"Action: CLEAN at {self.agent_loc}")
            self.location_condition[self.agent_loc] = 0
        elif action == 'Right':
            cost = -1
            print(f"Action: RIGHT from {self.agent_loc}")
            if self.agent_loc == 'A': 
                self.agent_loc = 'B'
            elif self.agent_loc == 'B': 
                self.agent_loc = 'C'
        elif action == 'Left':
            cost = -1
            print(f"Action: LEFT from {self.agent_loc}")
            if self.agent_loc == 'B': 
                self.agent_loc = 'A'
            elif self.agent_loc == 'C': 
                self.agent_loc = 'B'
        else:
            print("Action: NoOp")


        clean_score = 0
        for loc in ['A', 'B', 'C']:
            if self.location_condition[loc] == 0:
                clean_score += 10
        
        self.score += (cost + clean_score)

def simple_reflex_agent(percept):
    loc, status = percept
    if status == 1:
        return 'Clean'
    
    if loc == 'A':
        return 'Right'
    elif loc == 'C':
        return 'Left'
    elif loc == 'B':
        return random.choice(['Left', 'Right'])
    return 'NoOp'

def main():
    env = VacuumEnvironment()
    print("Initial State:", env.location_condition)
    print("Agent Location:", env.agent_loc)
    
    steps = 15
    for i in range(steps):
        print(f"\nStep {i+1}")
        percept = env.get_percept()
        action = simple_reflex_agent(percept)
        env.step(action)
        print("Current State:", env.location_condition)
        print("Score:", env.score)
    
    print("\nFinal Score:", env.score)

if __name__ == "__main__":
    main()
