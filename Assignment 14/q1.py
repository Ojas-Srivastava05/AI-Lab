def solve_forward_chaining(rules, initial_facts, goal):
    inferred_facts = []
    for fact in initial_facts:
        inferred_facts.append(fact)
        
    print("Initial facts:", inferred_facts)
    print("Goal:", goal)
    
    added_fact = True
    while added_fact:
        added_fact = False
        
        for rule in rules:
            premises = rule[0]
            conclusion = rule[1]
            
            if conclusion not in inferred_facts:
                all_premises_true = True
                for premise in premises:
                    if premise not in inferred_facts:
                        all_premises_true = False
                        break
                        
                if all_premises_true:
                    print(f"Rule matches: {premises} -> inferred {conclusion}")
                    inferred_facts.append(conclusion)
                    added_fact = True
                    
                    if conclusion == goal:
                        print("Goal reached successfully.")
                        return True
                        
    print("No more rules match.")
    return goal in inferred_facts

def main():
    print("Part A")
    rules_a = [
        (["P"], "Q"),
        (["L", "M"], "P"),
        (["A", "B"], "L")
    ]
    facts_a = ["A", "B", "M"]
    goal_a = "Q"
    result_a = solve_forward_chaining(rules_a, facts_a, goal_a)
    print("Result for A:", result_a)
    print("")
    
    print("Part B")
    rules_b = [
        (["A"], "B"),
        (["B"], "C"),
        (["C"], "D"),
        (["D", "E"], "F")
    ]
    facts_b = ["A", "E"]
    goal_b = "F"
    result_b = solve_forward_chaining(rules_b, facts_b, goal_b)
    print("Result for B:", result_b)

if __name__ == "__main__":
    main()
