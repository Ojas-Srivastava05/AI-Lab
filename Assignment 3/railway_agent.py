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
