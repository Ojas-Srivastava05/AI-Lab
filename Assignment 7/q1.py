import random


def generate_random_board(n=8):
    return [random.randint(0, n - 1) for _ in range(n)]


def heuristic(board):
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:
                conflicts += 1
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def steepest_ascent_hill_climbing(board):
    n = len(board)
    current = list(board)
    current_h = heuristic(current)
    initial_h = current_h
    steps = 0

    while True:
        best_neighbor = None
        best_h = current_h

        for col in range(n):
            original_row = current[col]
            for row in range(n):
                if row == original_row:
                    continue
                current[col] = row
                neighbor_h = heuristic(current)
                if neighbor_h < best_h:
                    best_h = neighbor_h
                    best_neighbor = list(current)
                current[col] = original_row

        if best_neighbor is None:
            break

        current = best_neighbor
        current_h = best_h
        steps += 1

    final_h = current_h
    solved = (final_h == 0)
    return current, initial_h, final_h, steps, solved


def main():
    num_trials = 50
    results = []

    print("=" * 75)
    print("  8-Queens: Steepest-Ascent Hill Climbing — 50 Random Boards")
    print("=" * 75)
    print(f"{'Trial':<7} {'Initial h':<12} {'Final h':<10} {'Steps':<8} {'Status'}")
    print("-" * 75)

    for i in range(num_trials):
        board = generate_random_board()
        final_board, initial_h, final_h, steps, solved = steepest_ascent_hill_climbing(board)
        status = "SOLVED" if solved else "FAIL"
        results.append({
            'trial': i + 1,
            'initial_h': initial_h,
            'final_h': final_h,
            'steps': steps,
            'solved': solved,
            'final_board': final_board
        })
        print(f"{i + 1:<7} {initial_h:<12} {final_h:<10} {steps:<8} {status}")

    solved_count = sum(1 for r in results if r['solved'])
    failed_count = num_trials - solved_count
    avg_steps_solved = (
        sum(r['steps'] for r in results if r['solved']) / solved_count
        if solved_count > 0 else 0
    )
    avg_steps_failed = (
        sum(r['steps'] for r in results if not r['solved']) / failed_count
        if failed_count > 0 else 0
    )

    print("\n" + "=" * 75)
    print("  SUMMARY")
    print("=" * 75)
    print(f"  Total trials      : {num_trials}")
    print(f"  Solved            : {solved_count} ({solved_count / num_trials * 100:.1f}%)")
    print(f"  Failed            : {failed_count} ({failed_count / num_trials * 100:.1f}%)")
    print(f"  Avg steps (solved): {avg_steps_solved:.2f}")
    print(f"  Avg steps (failed): {avg_steps_failed:.2f}")

    print("\n" + "=" * 75)
    print("  PROOF OF LOCAL MINIMUM")
    print("=" * 75)

    failed_cases = [r for r in results if not r['solved']]
    if failed_cases:
        example = failed_cases[0]
        board = example['final_board']
        h_val = example['final_h']
        n = len(board)

        print(f"\n  Example failed board (Trial {example['trial']}):")
        print(f"  Board : {board}")
        print(f"  h(board) = {h_val} (non-zero, so NOT a solution)")

        all_neighbors_worse_or_equal = True
        neighbor_h_values = []
        for col in range(n):
            original_row = board[col]
            for row in range(n):
                if row == original_row:
                    continue
                board[col] = row
                nh = heuristic(board)
                neighbor_h_values.append(nh)
                if nh < h_val:
                    all_neighbors_worse_or_equal = False
                board[col] = original_row

        print(f"\n  Total neighbors evaluated : {len(neighbor_h_values)}")
        print(f"  Min neighbor h           : {min(neighbor_h_values)}")
        print(f"  Max neighbor h           : {max(neighbor_h_values)}")
        print(f"  Current h                : {h_val}")
        print(f"  All neighbors >= current : {all_neighbors_worse_or_equal}")

        if all_neighbors_worse_or_equal and h_val > 0:
            print("\n  LOCAL MINIMUM CONFIRMED!")
            print(f"  The board is stuck at h = {h_val}. No single-queen move")
            print("  can reduce the number of conflicts. This is a local minimum")
            print("  because the state is NOT a global minimum (h = 0) but no")
            print("  neighbor is strictly better.")
        print()

        print("  Board visualization (Q = queen):")
        for row in range(n):
            line = "  "
            for col in range(n):
                if board[col] == row:
                    line += " Q "
                else:
                    line += " . "
            print(line)
    else:
        print("\n  All trials solved — no local minimum encountered in this run.")
        print("  (This is extremely unlikely; re-run to observe local minima.)")

    print()


if __name__ == "__main__":
    main()
