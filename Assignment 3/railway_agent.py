import random

class RailwayCrossingEnvironment:
    def __init__(self):
        self.inputs = {
            'Train_Detected': False,
            'Obstacle_Detected': False,
            'Emergency_Manual': False
        }
    
    def set_inputs(self, train, obstacle, emergency):
        self.inputs['Train_Detected'] = train
        self.inputs['Obstacle_Detected'] = obstacle
        self.inputs['Emergency_Manual'] = emergency
        return self.inputs

def railway_reflex_agent(percepts):
    train = percepts['Train_Detected']
    obstacle = percepts['Obstacle_Detected']
    emergency = percepts['Emergency_Manual']
    
    action = {
        'Gate': 'Unknown',
        'Hooter': 'Unknown',
        'Signal': 'Unknown'
    }
    
    if emergency or obstacle:
        action['Signal'] = 'RED'
        action['Hooter'] = 'ON'
        action['Gate'] = 'OPEN' 
        
    elif train:
        action['Signal'] = 'GREEN'
        action['Hooter'] = 'ON'
        action['Gate'] = 'CLOSED'
        
    else:
        action['Signal'] = 'RED'
        action['Hooter'] = 'OFF'
        action['Gate'] = 'OPEN'
        
    return action

def run_railway_simulation():
    env = RailwayCrossingEnvironment()
    print("--- Railway Level Crossing Agent Simulation ---")
    print("Goal: Maximize safety (no accidents) and efficiency (min delay).")
    print("Priorities: Emergency > Obstacle > Train Traffic > Idle")
    print("-" * 60)
    print(f"{'Train':<10} | {'Obstacle':<10} | {'Emergency':<10} || {'Signal':<10} | {'Gate':<10} | {'Hooter':<10}")
    print("-" * 60)
    
    scenarios = [
        (False, False, False),
        (False, False, True),
        (False, True, False),
        (False, True, True),
        (True, False, False),
        (True, False, True),
        (True, True, False),
        (True, True, True),
    ]
    
    for t, o, e in scenarios:
        percepts = env.set_inputs(t, o, e)
        action = railway_reflex_agent(percepts)
        
        t_str = str(t)
        o_str = str(o)
        e_str = str(e)
        
        print(f"{t_str:<10} | {o_str:<10} | {e_str:<10} || {action['Signal']:<10} | {action['Gate']:<10} | {action['Hooter']:<10}")

    print("-" * 60)
    print("Rationale for Conflicts:")
    print("1. If Obstacle is True, Signal is RED regardless of Train presence to prevent collision.")
    print("2. Gate is OPEN when Obstacle detected to allow vehicle to exit the box.")
    print("3. Emergency Manual overrides everything to Safe State (Red/Open/On).")

if __name__ == "__main__":
    run_railway_simulation()
