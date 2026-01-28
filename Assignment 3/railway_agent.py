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
    # Percepts: dict with boolean values
    train = percepts['Train_Detected']
    obstacle = percepts['Obstacle_Detected']
    emergency = percepts['Emergency_Manual']
    
    # Actuators default state (Safe-fail: Red, Open, Hooter On is panic mode)
    # Let's define safe defaults clearly.
    action = {
        'Gate': 'Unknown',
        'Hooter': 'Unknown',
        'Signal': 'Unknown'
    }
    
    # Priority Rule Implementation
    # 1. Critical Safety: Emergency Manual Override OR Obstacle on Track
    if emergency or obstacle:
        # If train is coming or not, we MUST stopping train if possible (Signal Red)
        # And we must Open gate to let obstacle escape if possible? 
        # Actually standard procedure for Obstacle: Signal RED, Gate OPEN (to let exit), Hooter ON
        action['Signal'] = 'RED'
        action['Hooter'] = 'ON'
        action['Gate'] = 'OPEN' 
        # Rationale: If stuck, raising gate allows escape. Red signal stops train.
        
    # 2. Normal Operation: Train Aproaching, No Obstacles, No Emergency
    elif train:
        action['Signal'] = 'GREEN' # Safe for train to proceed (after gate closed)
        action['Hooter'] = 'ON'    # Warn traffic
        action['Gate'] = 'CLOSED'  # Stop road traffic
        
    # 3. Idle: No Train, No Obstacle
    else:
        action['Signal'] = 'RED'   # Railway signal usually red if block not claimed, or Green?
                                   # Let's say RED for train (Stop), allowing Road Traffic.
        action['Hooter'] = 'OFF'
        action['Gate'] = 'OPEN'    # Road traffic allowed
        
    return action

def run_railway_simulation():
    env = RailwayCrossingEnvironment()
    print("--- Railway Level Crossing Agent Simulation ---")
    print("Goal: Maximize safety (no accidents) and efficiency (min delay).")
    print("Priorities: Emergency > Obstacle > Train Traffic > Idle")
    print("-" * 60)
    print(f"{'Train':<10} | {'Obstacle':<10} | {'Emergency':<10} || {'Signal':<10} | {'Gate':<10} | {'Hooter':<10}")
    print("-" * 60)
    
    # Truth Table Simulation (All 8 combinations)
    scenarios = [
        (False, False, False),
        (False, False, True),
        (False, True, False),
        (False, True, True), # emergency + obstacle
        (True, False, False), # Normal, Train coming
        (True, False, True),  # Train + Emergency
        (True, True, False),  # Train + Obstacle (Critical!)
        (True, True, True),   # Max Chaos
    ]
    
    for t, o, e in scenarios:
        percepts = env.set_inputs(t, o, e)
        action = railway_reflex_agent(percepts)
        
        # Formatting output
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
