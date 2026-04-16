def check_provable(goal, rules, known_facts, checking_goals, indent):
    print(f"{indent}Checking goal: {goal}")
    
    if goal in known_facts:
        print(f"{indent}Goal known as fact.")
        return True
        
    if goal in checking_goals:
        print(f"{indent}Loop detected for goal.")
        return False
        
    checking_goals.append(goal)
    
    for rule in rules:
        premises = rule[0]
        conclusion = rule[1]
        
        if conclusion == goal:
            print(f"{indent}Found rule for {goal} with premises {premises}")
            all_true = True
            
            for premise in premises:
                if not check_provable(premise, rules, known_facts, checking_goals, indent + "  "):
                    print(f"{indent}Premise {premise} failed.")
                    all_true = False
                    break
                    
            if all_true:
                print(f"{indent}Proved {goal} from rule.")
                checking_goals.remove(goal)
                return True
                
    print(f"{indent}Cannot prove {goal}")
    checking_goals.remove(goal)
    return False

def solve_backward_chaining(rules, initial_facts, goal):
    print("Initial facts:", initial_facts)
    print("Goal:", goal)
    
    return check_provable(goal, rules, initial_facts, [], "")

def main():
    print("Part A")
    rules_a = [
        (["P"], "Q"),
        (["R"], "Q"),
        (["A"], "P"),
        (["B"], "R")
    ]
    facts_a = ["A", "B"]
    goal_a = "Q"
    result_a = solve_backward_chaining(rules_a, facts_a, goal_a)
    print("Result for A:", result_a)
    print("")
    
    print("Part B")
    rules_b = [
        (["A"], "B"),
        (["B", "C"], "D"),
        (["E"], "C")
    ]
    facts_b = ["A", "E"]
    goal_b = "D"
    result_b = solve_backward_chaining(rules_b, facts_b, goal_b)
    print("Result for B:", result_b)

if __name__ == "__main__":
    main()
