def get_clause_as_sorted_tuple(clause_list):
    return tuple(sorted(clause_list))

def compute_negation(literal):
    if literal.startswith("~"):
        return literal[1:]
    return "~" + literal

def resolve_clauses(first_clause, second_clause):
    new_clauses = []
    
    for literal in first_clause:
        negated = compute_negation(literal)
        
        if negated in second_clause:
            combined = list(first_clause)
            combined.remove(literal)
            
            second_clause_list = list(second_clause)
            second_clause_list.remove(negated)
            
            for item in second_clause_list:
                if item not in combined:
                    combined.append(item)
                    
            is_tautology = False
            for item in combined:
                if compute_negation(item) in combined:
                    is_tautology = True
                    break
                    
            if not is_tautology:
                new_clauses.append(get_clause_as_sorted_tuple(combined))
                
    return new_clauses

def solve_resolution(initial_clauses, goal):
    negated_goal = compute_negation(goal)
    clauses = []
    
    for clause in initial_clauses:
        clauses.append(get_clause_as_sorted_tuple(clause))
        
    clauses.append(get_clause_as_sorted_tuple([negated_goal]))
    
    print("Initial clauses:", clauses)
    print("Negated goal:", negated_goal)
    
    generated_clauses = []
    
    while True:
        added_new_clause = False
        
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                new_resolvents = resolve_clauses(clauses[i], clauses[j])
                
                for resolvent in new_resolvents:
                    if resolvent not in clauses and resolvent not in generated_clauses:
                        print(f"Resolving {list(clauses[i])} and {list(clauses[j])} -> {list(resolvent)}")
                        
                        if len(resolvent) == 0:
                            print("Empty clause found. Contradiction reached!")
                            return True
                            
                        generated_clauses.append(resolvent)
                        added_new_clause = True
                        
        for clause in generated_clauses:
            if clause not in clauses:
                clauses.append(clause)
                
        if not added_new_clause:
            print("No new clauses generated. Cannot prove goal.")
            return False

def main():
    print("Part A")
    clauses_a = [
        ["P", "Q"],
        ["~P", "R"],
        ["~Q", "S"],
        ["~R", "S"]
    ]
    goal_a = "S"
    result_a = solve_resolution(clauses_a, goal_a)
    print("Result for A:", result_a)
    print("")
    
    print("Part B")
    clauses_b = [
        ["~P", "Q"],
        ["~Q", "R"],
        ["~S", "~R"],
        ["P"]
    ]
    goal_b = "S"
    result_b = solve_resolution(clauses_b, goal_b)
    print("Result for B:", result_b)
    print("")
    
    print("Part B (Negated Goal)")
    goal_b_negated = "~S"
    result_b_negated = solve_resolution(clauses_b, goal_b_negated)
    print("Result for B Negated:", result_b_negated)

if __name__ == "__main__":
    main()
