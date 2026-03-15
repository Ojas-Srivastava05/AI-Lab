import random
import time

DISTANCE_MATRIX = [
    [0,  10, 15, 20, 25, 30, 35, 40],
    [12,  0, 35, 15, 20, 25, 30, 45],
    [25, 30,  0, 10, 40, 20, 15, 35],
    [18, 25, 12,  0, 15, 30, 20, 10],
    [22, 18, 28, 20,  0, 15, 25, 30],
    [35, 22, 18, 28, 12,  0, 40, 20],
    [30, 35, 22, 18, 28, 32,  0, 15],
    [40, 28, 35, 22, 18, 25, 12,  0],
]

CITY_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
NUM_CITIES = len(DISTANCE_MATRIX)


def tour_cost(tour):
    cost = 0
    for i in range(len(tour)):
        cost += DISTANCE_MATRIX[tour[i]][tour[(i + 1) % len(tour)]]
    return cost


def generate_random_tour():
    tour = list(range(NUM_CITIES))
    random.shuffle(tour)
    return tour


def get_neighbors(tour):
    neighbors = []
    n = len(tour)
    for i in range(n):
        for j in range(i + 1, n):
            neighbor = list(tour)
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors


def local_beam_search(k, max_iterations=1000):
    current_states = [generate_random_tour() for _ in range(k)]
    current_costs = [tour_cost(s) for s in current_states]

    best_idx = current_costs.index(min(current_costs))
    best_tour = list(current_states[best_idx])
    best_cost = current_costs[best_idx]
    cost_history = [best_cost]

    for iteration in range(max_iterations):
        all_successors = []
        for state in current_states:
            for neighbor in get_neighbors(state):
                all_successors.append(neighbor)

        successor_costs = [tour_cost(s) for s in all_successors]

        paired = list(zip(successor_costs, all_successors))
        paired.sort(key=lambda x: x[0])
        top_k = paired[:k]

        new_costs = [p[0] for p in top_k]
        new_states = [p[1] for p in top_k]

        if new_costs[0] < best_cost:
            best_cost = new_costs[0]
            best_tour = list(new_states[0])

        cost_history.append(best_cost)

        if new_costs[0] >= min(current_costs):
            break

        current_states = new_states
        current_costs = new_costs

    return best_tour, best_cost, iteration + 1, cost_history


def tour_to_string(tour):
    return " -> ".join(CITY_NAMES[c] for c in tour) + " -> " + CITY_NAMES[tour[0]]


def main():
    beam_widths = [3, 5, 10]
    num_trials = 20

    print("=" * 80)
    print("  TSP — Local Beam Search (Comparative Analysis)")
    print("=" * 80)

    all_results = {}

    for k in beam_widths:
        print(f"\n{'─' * 80}")
        print(f"  Beam Width k = {k}")
        print(f"{'─' * 80}")
        print(f"  {'Trial':<8} {'Best Cost':<12} {'Iterations':<14} {'Best Tour'}")
        print(f"  {'-' * 72}")

        trial_costs = []
        trial_iterations = []
        best_overall_tour = None
        best_overall_cost = float('inf')

        random.seed(42)
        start_time = time.time()

        for t in range(num_trials):
            best_tour, best_cost, iterations, cost_history = local_beam_search(k)
            trial_costs.append(best_cost)
            trial_iterations.append(iterations)

            if best_cost < best_overall_cost:
                best_overall_cost = best_cost
                best_overall_tour = best_tour

            print(f"  {t + 1:<8} {best_cost:<12} {iterations:<14} {tour_to_string(best_tour)}")

        elapsed = time.time() - start_time

        avg_cost = sum(trial_costs) / num_trials
        min_cost = min(trial_costs)
        max_cost = max(trial_costs)
        avg_iters = sum(trial_iterations) / num_trials

        all_results[k] = {
            'avg_cost': avg_cost,
            'min_cost': min_cost,
            'max_cost': max_cost,
            'avg_iters': avg_iters,
            'best_tour': best_overall_tour,
            'best_cost': best_overall_cost,
            'time': elapsed,
            'trial_costs': trial_costs,
        }

        print(f"\n  Summary for k = {k}:")
        print(f"    Avg cost       : {avg_cost:.2f}")
        print(f"    Best cost      : {min_cost}")
        print(f"    Worst cost     : {max_cost}")
        print(f"    Avg iterations : {avg_iters:.2f}")
        print(f"    Time elapsed   : {elapsed:.4f}s")
        print(f"    Best tour      : {tour_to_string(best_overall_tour)}")

    print("\n" + "=" * 80)
    print("  COMPARATIVE ANALYSIS")
    print("=" * 80)
    print(f"\n  {'Beam Width (k)':<18} {'Avg Cost':<12} {'Best Cost':<12} {'Worst Cost':<13} {'Avg Iters':<12} {'Time (s)'}")
    print(f"  {'-' * 75}")

    for k in beam_widths:
        r = all_results[k]
        print(f"  {k:<18} {r['avg_cost']:<12.2f} {r['min_cost']:<12} {r['max_cost']:<13} {r['avg_iters']:<12.2f} {r['time']:.4f}")

    print(f"\n  {'─' * 75}")
    print("  OBSERVATIONS:")
    print("  1. Larger beam width generally produces better average costs since more")
    print("     states are explored in parallel, reducing the risk of local minima.")
    print("  2. Larger k is more expensive per iteration (more neighbors to evaluate),")
    print("     so wall-clock time goes up.")
    print("  3. Convergence depends on k — small k converges quickly but to worse")
    print("     solutions (closer to hill climbing), while large k converges to better")
    print("     solutions but takes longer (closer to parallel breadth search).")
    print("  4. Variance across trials decreases as k increases, giving more")
    print("     consistent results.")
    print()


if __name__ == "__main__":
    main()
