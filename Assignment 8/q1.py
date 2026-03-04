# Q1. Use the local beam search to solve the TSP problem.
# Give a comparative analysis of the algorithm when the beam width k=3, 5, 10.
# Does the convergence depend on the value of k?

import random
import time


# Distance matrix for 8 cities (A through H)
DISTANCE_MATRIX = [
    [0,  10, 15, 20, 25, 30, 35, 40],   # City 0 (A)
    [12,  0, 35, 15, 20, 25, 30, 45],   # City 1 (B)
    [25, 30,  0, 10, 40, 20, 15, 35],   # City 2 (C)
    [18, 25, 12,  0, 15, 30, 20, 10],   # City 3 (D)
    [22, 18, 28, 20,  0, 15, 25, 30],   # City 4 (E)
    [35, 22, 18, 28, 12,  0, 40, 20],   # City 5 (F)
    [30, 35, 22, 18, 28, 32,  0, 15],   # City 6 (G)
    [40, 28, 35, 22, 18, 25, 12,  0],   # City 7 (H)
]

CITY_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
NUM_CITIES = len(DISTANCE_MATRIX)


def tour_cost(tour):
    """Calculate the total cost of a tour (round trip)."""
    cost = 0
    for i in range(len(tour)):
        cost += DISTANCE_MATRIX[tour[i]][tour[(i + 1) % len(tour)]]
    return cost


def generate_random_tour():
    """Generate a random permutation of cities as a tour."""
    tour = list(range(NUM_CITIES))
    random.shuffle(tour)
    return tour


def get_neighbors(tour):
    """Generate all neighbors of a tour by swapping every pair of cities."""
    neighbors = []
    n = len(tour)
    for i in range(n):
        for j in range(i + 1, n):
            neighbor = list(tour)
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors


def local_beam_search(k, max_iterations=1000):
    """
    Local Beam Search for TSP.

    Parameters:
        k: beam width (number of states to keep at each step)
        max_iterations: maximum number of iterations

    Returns:
        best_tour, best_cost, iterations, cost_history
    """
    # Step 1: Generate k random initial states
    current_states = [generate_random_tour() for _ in range(k)]
    current_costs = [tour_cost(s) for s in current_states]

    best_idx = current_costs.index(min(current_costs))
    best_tour = list(current_states[best_idx])
    best_cost = current_costs[best_idx]

    cost_history = [best_cost]

    for iteration in range(max_iterations):
        # Step 2: Generate all successors of all k states
        all_successors = []
        for state in current_states:
            neighbors = get_neighbors(state)
            for neighbor in neighbors:
                all_successors.append(neighbor)

        # Step 3: Evaluate all successors
        successor_costs = [tour_cost(s) for s in all_successors]

        # Step 4: Select the k best successors
        paired = list(zip(successor_costs, all_successors))
        paired.sort(key=lambda x: x[0])
        top_k = paired[:k]

        new_costs = [p[0] for p in top_k]
        new_states = [p[1] for p in top_k]

        # Track the global best
        if new_costs[0] < best_cost:
            best_cost = new_costs[0]
            best_tour = list(new_states[0])

        cost_history.append(best_cost)

        # Check for convergence (no improvement)
        if new_costs[0] >= min(current_costs):
            # No improvement found — converged
            break

        current_states = new_states
        current_costs = new_costs

    return best_tour, best_cost, iteration + 1, cost_history


def tour_to_string(tour):
    """Convert a tour (list of indices) to a readable city-name string."""
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

        random.seed(42)  # Reset seed for fair comparison across k values

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

    # Comparative Analysis
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
    print("  1. Larger beam width (k) generally produces BETTER (lower) average costs")
    print("     because more states are explored in parallel, reducing the chance of")
    print("     getting stuck in a local minimum.")
    print("  2. Larger k requires MORE computation per iteration (more neighbors to")
    print("     evaluate), leading to higher wall-clock time.")
    print("  3. Convergence DOES depend on k:")
    print("     - Small k (e.g., 3) converges FASTER (fewer iterations) but to a")
    print("       WORSE solution (higher cost) — it behaves closer to hill climbing.")
    print("     - Large k (e.g., 10) may take more iterations but converges to a")
    print("       BETTER solution — it behaves closer to a parallel breadth search.")
    print("  4. As k increases, the variance across trials tends to DECREASE,")
    print("     indicating more consistent (reliable) results.")
    print()


if __name__ == "__main__":
    main()
