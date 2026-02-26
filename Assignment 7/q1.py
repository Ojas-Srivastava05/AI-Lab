import random


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


def steepest_ascent_hill_climbing(board):
    n = len(board)
    max_value = n * (n - 1) // 2
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
                neighbor_val = value_function(current)
                if neighbor_val > best_val:
                    best_val = neighbor_val
                    best_neighbor = list(current)
                current[col] = original_row

        if best_neighbor is None:
            break

        current = best_neighbor
        current_val = best_val
        steps += 1

    final_val = current_val
    solved = (final_val == max_value)
    return current, initial_val, final_val, steps, solved


def main():
    num_trials = 50
    results = []

    print("=" * 75)
    print("  8-Queens: Steepest-Ascent Hill Climbing — 50 Random Boards")
    print("=" * 75)
    print(f"{'Trial':<7} {'Init Value':<12} {'Final Value':<12} {'Steps':<8} {'Status'}")
    print("-" * 75)

    for i in range(num_trials):
        board = generate_random_board()
        final_board, initial_val, final_val, steps, solved = steepest_ascent_hill_climbing(board)
        status = "SOLVED" if solved else "FAIL"
        results.append({
            'trial': i + 1,
            'initial_val': initial_val,
            'final_val': final_val,
            'steps': steps,
            'solved': solved,
            'final_board': final_board
        })
        print(f"{i + 1:<7} {initial_val:<12} {final_val:<12} {steps:<8} {status}")

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
        val = example['final_val']
        n = len(board)
        max_val = n * (n - 1) // 2

        print(f"\n  Example failed board (Trial {example['trial']}):")
        print(f"  Board : {board}")
        print(f"  Value = {val} (Total pairs is {max_val}, so NOT a solution)")

        all_neighbors_worse_or_equal = True
        neighbor_values = []
        for col in range(n):
            original_row = board[col]
            for row in range(n):
                if row == original_row:
                    continue
                board[col] = row
                nv = value_function(board)
                neighbor_values.append(nv)
                if nv > val:
                    all_neighbors_worse_or_equal = False
                board[col] = original_row

        print(f"\n  Total neighbors evaluated : {len(neighbor_values)}")
        print(f"  Max neighbor value       : {max(neighbor_values)}")
        print(f"  Current value            : {val}")
        print(f"  All neighbors <= current : {all_neighbors_worse_or_equal}")

        if all_neighbors_worse_or_equal and val < max_val:
            print("\n  LOCAL MAXIMUM CONFIRMED!")
            print(f"  The board is stuck at value = {val}. No single-queen move")
            print("  can increase the number of non-attacking pairs. This is a local maximum")
            print("  because the state is NOT a global maximum (28) but no")
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

    print()


if __name__ == "__main__":
    main()
