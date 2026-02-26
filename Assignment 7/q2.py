import random
import math
import time


def generate_random_board(n=8):
    return [random.randint(0, n - 1) for _ in range(n)]


def value_function(board):
    n = len(board)
    total_pairs = n * (n - 1) // 2
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:
                conflicts += 1
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return total_pairs - conflicts


def steepest_ascent_hc(board):
    n = len(board)
    max_val = n * (n - 1) // 2
    current = list(board)
    current_val = value_function(current)
    initial_val = current_val
    steps = 0

    while True:
        best_neighbor = None
        best_val = current_val

        for col in range(n):
            original_row = current[col]
            for row in range(n):
                if row == original_row:
                    continue
                current[col] = row
                nv = value_function(current)
                if nv > best_val:
                    best_val = nv
                    best_neighbor = list(current)
                current[col] = original_row

        if best_neighbor is None:
            break

        current = best_neighbor
        current_val = best_val
        steps += 1

    return initial_val, current_val, steps, (current_val == max_val)


def first_choice_hc(board, max_sideways=100):
    n = len(board)
    max_val = n * (n - 1) // 2
    current = list(board)
    current_val = value_function(current)
    initial_val = current_val
    steps = 0
    max_tries_per_step = n * (n - 1)

    while True:
        improved = False
        tried = 0

        while tried < max_tries_per_step:
            col = random.randint(0, n - 1)
            row = random.randint(0, n - 1)
            while row == current[col]:
                row = random.randint(0, n - 1)

            neighbor = list(current)
            neighbor[col] = row
            nv = value_function(neighbor)

            if nv > current_val:
                current = neighbor
                current_val = nv
                steps += 1
                improved = True
                break

            tried += 1

        if not improved:
            break

    return initial_val, current_val, steps, (current_val == max_val)


def random_restart_hc(max_restarts=100):
    total_steps = 0
    restarts = 0
    initial_val_first = None
    final_val = 0

    for _ in range(max_restarts):
        board = generate_random_board()
        init_val, final_val, steps, solved = steepest_ascent_hc(board)

        if initial_val_first is None:
            initial_val_first = init_val

        total_steps += steps
        restarts += 1

        if solved:
            return initial_val_first, final_val, total_steps, True, restarts

    return initial_val_first, final_val, total_steps, False, restarts


def simulated_annealing(board, initial_temp=4.0, cooling_rate=0.995, min_temp=0.001, max_iterations=100000):
    n = len(board)
    max_val = n * (n - 1) // 2
    current = list(board)
    current_val = value_function(current)
    initial_val = current_val
    steps = 0
    temperature = initial_temp

    for iteration in range(max_iterations):
        if current_val == max_val:
            break

        if temperature < min_temp:
            break

        col = random.randint(0, n - 1)
        row = random.randint(0, n - 1)
        while row == current[col]:
            row = random.randint(0, n - 1)

        neighbor = list(current)
        neighbor[col] = row
        nv = value_function(neighbor)
        delta = nv - current_val

        if delta > 0:
            current = neighbor
            current_val = nv
            steps += 1
        else:
            acceptance_prob = math.exp(delta / temperature) if temperature > 0 else 0
            if random.random() < acceptance_prob:
                current = neighbor
                current_val = nv
                steps += 1

        temperature *= cooling_rate

    return initial_val, current_val, steps, (current_val == max_val)


def run_experiment(algorithm_name, algorithm_func, num_trials=50):
    results = []

    for i in range(num_trials):
        board = generate_random_board()

        if algorithm_name == "Random-Restart HC":
            init_val, final_val, steps, solved, restarts = random_restart_hc()
            results.append({
                'trial': i + 1,
                'initial_val': init_val,
                'final_val': final_val,
                'steps': steps,
                'solved': solved,
                'restarts': restarts
            })
        else:
            init_val, final_val, steps, solved = algorithm_func(board)
            results.append({
                'trial': i + 1,
                'initial_val': init_val,
                'final_val': final_val,
                'steps': steps,
                'solved': solved
            })

    return results


def print_results(algorithm_name, results):
    print(f"\n{'=' * 75}")
    print(f"  {algorithm_name}")
    print(f"{'=' * 75}")

    if algorithm_name == "Random-Restart HC":
        print(f"{'Trial':<7} {'Init Val':<9} {'Final Val':<10} {'Steps':<8} {'Restarts':<10} {'Status'}")
        print("-" * 75)
        for r in results:
            status = "SOLVED" if r['solved'] else "FAIL"
            print(f"{r['trial']:<7} {r['initial_val']:<9} {r['final_val']:<10} {r['steps']:<8} {r['restarts']:<10} {status}")
    else:
        print(f"{'Trial':<7} {'Init Val':<9} {'Final Val':<10} {'Steps':<8} {'Status'}")
        print("-" * 75)
        for r in results:
            status = "SOLVED" if r['solved'] else "FAIL"
            print(f"{r['trial']:<7} {r['initial_val']:<9} {r['final_val']:<10} {r['steps']:<8} {status}")


def print_summary(all_results):
    print("\n" + "=" * 80)
    print("  COMPARISON SUMMARY")
    print("=" * 80)
    print(f"{'Algorithm':<25} {'Solved':<10} {'Success%':<12} {'Avg Steps':<12} {'Avg Final Val'}")
    print("-" * 80)

    for name, results in all_results.items():
        solved = sum(1 for r in results if r['solved'])
        total = len(results)
        pct = solved / total * 100
        avg_steps = sum(r['steps'] for r in results) / total
        avg_final_val = sum(r['final_val'] for r in results) / total
        print(f"{name:<25} {solved}/{total:<7} {pct:<12.1f} {avg_steps:<12.2f} {avg_final_val:.2f}")

    print()


def main():
    random.seed(42)
    num_trials = 50

    print("=" * 80)
    print("  8-Queens Problem: Hill Climbing Variants Comparison")
    print("  Running each algorithm on 50 random initial boards")
    print("=" * 80)

    all_results = {}

    print("\n Running Steepest-Ascent Hill Climbing...")
    start = time.time()
    results_sa = run_experiment("Steepest-Ascent HC", steepest_ascent_hc, num_trials)
    time_sa = time.time() - start
    print_results("Steepest-Ascent HC", results_sa)
    all_results["Steepest-Ascent HC"] = results_sa

    print("\n Running First-Choice Hill Climbing...")
    start = time.time()
    results_fc = run_experiment("First-Choice HC", first_choice_hc, num_trials)
    time_fc = time.time() - start
    print_results("First-Choice HC", results_fc)
    all_results["First-Choice HC"] = results_fc

    print("\n Running Random-Restart Hill Climbing...")
    start = time.time()
    results_rr = run_experiment("Random-Restart HC", None, num_trials)
    time_rr = time.time() - start
    print_results("Random-Restart HC", results_rr)
    all_results["Random-Restart HC"] = results_rr

    print("\n Running Simulated Annealing...")
    start = time.time()
    results_ann = run_experiment("Simulated Annealing", simulated_annealing, num_trials)
    time_ann = time.time() - start
    print_results("Simulated Annealing", results_ann)
    all_results["Simulated Annealing"] = results_ann

    print_summary(all_results)

    print("=" * 80)
    print("  EXECUTION TIME")
    print("=" * 80)
    print(f"  Steepest-Ascent HC  : {time_sa:.4f} s")
    print(f"  First-Choice HC     : {time_fc:.4f} s")
    print(f"  Random-Restart HC   : {time_rr:.4f} s")
    print(f"  Simulated Annealing : {time_ann:.4f} s")

    print("\n" + "=" * 80)
    print("  ANALYSIS & COMPARISON")
    print("=" * 80)
    print("""
  1. STEEPEST-ASCENT HILL CLIMBING:
     - Evaluates ALL neighbors at each step and picks the one with the highest value.
     - Often gets stuck in local maxima (typically ~14% success rate).
     - Fast per run but frequently fails.

  2. FIRST-CHOICE HILL CLIMBING:
     - Generates random successors until one with a higher value is found.
     - Similar success rate to steepest-ascent but can be faster per step
       since it doesn't evaluate all neighbors.
     - Still susceptible to local maxima.

  3. RANDOM-RESTART HILL CLIMBING:
     - Restarts steepest-ascent HC with new random boards until solved.
     - Near 100% success rate given enough restarts.
     - Total steps are higher but it is very effective.
     - Overcomes local maxima by restarting from different initial states.

  4. SIMULATED ANNEALING:
     - Allows downhill moves with decreasing probability (temperature schedule).
     - Can escape local maxima, leading to higher success rates.
     - The cooling schedule (T = T0 x alpha^t) controls exploration vs exploitation.
     - Generally achieves high success rates with proper tuning.

  KEY INSIGHT:
     Basic hill climbing (steepest-ascent and first-choice) gets stuck in
     local maxima. Random restarts solve this by trying many starting points.
     Simulated annealing solves it by allowing temporary worsening moves.
     Both random-restart and simulated annealing significantly outperform
     basic hill climbing for the 8-Queens problem.
""")


if __name__ == "__main__":
    main()
