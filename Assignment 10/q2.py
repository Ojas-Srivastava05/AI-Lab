def is_goal(state):
    loc, dirt_A, dirt_B = state
    return dirt_A == 'Clean' and dirt_B == 'Clean'

def get_actions(state):
    # In any state, agent can Move Left, Move Right, or Suck
    return ['Left', 'Right', 'Suck']

def get_results(state, action):
    loc, dirt_A, dirt_B = state
    
    if action == 'Left':
        return set([('A', dirt_A, dirt_B)])
        
    if action == 'Right':
        return set([('B', dirt_A, dirt_B)])
        
    if action == 'Suck':
        results = set()
        if loc == 'A':
            if dirt_A == 'Dirty':
                # Normal: cleans A
                results.add(('A', 'Clean', dirt_B))
                # Erratic: also cleans B
                results.add(('A', 'Clean', 'Clean'))
            else:
                # loc is Clean
                # Normal: stays clean
                results.add(('A', 'Clean', dirt_B))
                # Erratic: deposits dirt
                results.add(('A', 'Dirty', dirt_B))
        elif loc == 'B':
            if dirt_B == 'Dirty':
                # Normal: cleans B
                results.add(('B', dirt_A, 'Clean'))
                # Erratic: also cleans A
                results.add(('B', 'Clean', 'Clean'))
            else:
                # loc is Clean
                # Normal: stays clean
                results.add(('B', dirt_A, 'Clean'))
                # Erratic: deposits dirt
                results.add(('B', dirt_A, 'Dirty'))
        return results

def and_search(states, path):
    plan = {}
    for s in states:
        subplan = or_search(s, path)
        if subplan == 'failure':
            return 'failure'
        plan[s] = subplan
    return plan

def or_search(state, path):
    if is_goal(state):
        return []
    
    if state in path:
        return 'failure'
        
    for action in get_actions(state):
        results = get_results(state, action)
        
        # Don't try an action if it only leads to the exact same state (to avoid simple loops)
        if len(results) == 1 and state in results:
            continue
            
        plan = and_search(results, path + [state])
        if plan != 'failure':
            return [action, plan]
            
    return 'failure'

def print_plan(plan, indent=""):
    if not plan:
        print(indent + "-> NoOp (Goal reached)")
        return
        
    if plan == 'failure':
        print(indent + "-> Failure")
        return
        
    action = plan[0]
    subplans = plan[1]
    
    print(indent + f"-> Action: {action}")
    for state, subplan in subplans.items():
        print(indent + f"  If resulting state is {state}:")
        print_plan(subplan, indent + "    ")

def main():
    print("Erratic Vacuum Agent AND-OR Graph Search\n")
    
    # Generate all possible non-goal initial states to test
    locations = ['A', 'B']
    statuses = ['Clean', 'Dirty']
    
    for loc in locations:
        for da in statuses:
            for db in statuses:
                state = (loc, da, db)
                if not is_goal(state):
                    print(f"Finding plan for initial state: {state}")
                    plan = or_search(state, [])
                    print_plan(plan)
                    print("-" * 50)

if __name__ == '__main__':
    main()
