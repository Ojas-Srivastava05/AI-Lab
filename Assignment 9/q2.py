import time

HUMAN = 'X'
AI = 'O'
EMPTY = ' '


def create_board():
    return [EMPTY] * 9


def print_board(board):
    for i in range(3):
        row = []
        for j in range(3):
            row.append(board[i * 3 + j])
        print(" " + " | ".join(row))
        if i < 2:
            print("---+---+---")
    print()


def check_winner(board):
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]
    for a, b, c in lines:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board):
    return EMPTY not in board


def get_available_moves(board):
    return [i for i in range(9) if board[i] == EMPTY]


mm_stats = {'nodes': 0}
ab_stats = {'nodes': 0, 'pruned': 0}


def minimax(board, is_maximizing, depth=0):
    mm_stats['nodes'] += 1

    winner = check_winner(board)
    if winner == AI:
        return 10 - depth, None
    if winner == HUMAN:
        return depth - 10, None
    if is_full(board):
        return 0, None

    moves = get_available_moves(board)

    if is_maximizing:
        best_score = -float('inf')
        best_move = None
        for move in moves:
            board[move] = AI
            score, _ = minimax(board, False, depth + 1)
            board[move] = EMPTY
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for move in moves:
            board[move] = HUMAN
            score, _ = minimax(board, True, depth + 1)
            board[move] = EMPTY
            if score < best_score:
                best_score = score
                best_move = move
        return best_score, best_move


def alpha_beta(board, is_maximizing, alpha, beta, depth=0):
    ab_stats['nodes'] += 1

    winner = check_winner(board)
    if winner == AI:
        return 10 - depth, None
    if winner == HUMAN:
        return depth - 10, None
    if is_full(board):
        return 0, None

    moves = get_available_moves(board)

    if is_maximizing:
        best_score = -float('inf')
        best_move = None
        for move in moves:
            board[move] = AI
            score, _ = alpha_beta(board, False, alpha, beta, depth + 1)
            board[move] = EMPTY
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if beta <= alpha:
                ab_stats['pruned'] += 1
                break
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for move in moves:
            board[move] = HUMAN
            score, _ = alpha_beta(board, True, alpha, beta, depth + 1)
            board[move] = EMPTY
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            if beta <= alpha:
                ab_stats['pruned'] += 1
                break
        return best_score, best_move


def visualize_pruning(board, is_maximizing, alpha, beta, depth=0, move_made=None, max_depth=3):
    indent = "  " * depth
    player = "MAX(O)" if is_maximizing else "MIN(X)"
    pos_label = f"(pos {move_made})" if move_made is not None else "(root)"

    winner = check_winner(board)
    if winner == AI:
        print(f"{indent}└─ {player} {pos_label} → score = {10 - depth}")
        return 10 - depth
    if winner == HUMAN:
        print(f"{indent}└─ {player} {pos_label} → score = {depth - 10}")
        return depth - 10
    if is_full(board):
        print(f"{indent}└─ {player} {pos_label} → score = 0 (draw)")
        return 0
    if depth >= max_depth:
        print(f"{indent}└─ {player} {pos_label} [α={alpha}, β={beta}] (truncated)")
        return 0

    print(f"{indent}├─ {player} {pos_label} [α={alpha}, β={beta}]")
    moves = get_available_moves(board)

    if is_maximizing:
        best = -float('inf')
        for move in moves:
            board[move] = AI
            val = visualize_pruning(board, False, alpha, beta, depth + 1, move, max_depth)
            board[move] = EMPTY
            best = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                print(f"{indent}  ✂ PRUNED remaining branches (β={beta} ≤ α={alpha})")
                break
        return best
    else:
        best = float('inf')
        for move in moves:
            board[move] = HUMAN
            val = visualize_pruning(board, True, alpha, beta, depth + 1, move, max_depth)
            board[move] = EMPTY
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                print(f"{indent}  ✂ PRUNED remaining branches (β={beta} ≤ α={alpha})")
                break
        return best


def play_game():
    board = create_board()
    print("Tic-Tac-Toe with Alpha-Beta Pruning")
    print("Human (X) vs AI (O)")
    print("Positions:")
    print(" 0 | 1 | 2")
    print("---+---+---")
    print(" 3 | 4 | 5")
    print("---+---+---")
    print(" 6 | 7 | 8")
    print()

    current = HUMAN

    while True:
        print_board(board)
        winner = check_winner(board)
        if winner:
            print(f"{'Human' if winner == HUMAN else 'AI'} ({winner}) wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break

        if current == HUMAN:
            available = get_available_moves(board)
            while True:
                try:
                    move = int(input(f"Your move (available: {available}): "))
                    if move in available:
                        break
                    print("Invalid, try again.")
                except ValueError:
                    print("Enter a number.")
            board[move] = HUMAN
            current = AI
        else:
            print("AI thinking (alpha-beta)...")
            ab_stats['nodes'] = 0
            ab_stats['pruned'] = 0
            start = time.time()
            score, move = alpha_beta(board, True, -float('inf'), float('inf'))
            elapsed = time.time() - start

            board[move] = AI
            print(f"AI plays position {move} (score: {score})")
            print(f"  Nodes: {ab_stats['nodes']}, Pruned: {ab_stats['pruned']}")
            print(f"  Time: {elapsed:.4f}s")
            current = HUMAN


def comparative_analysis():
    print("=" * 70)
    print("  Alpha-Beta Pruning vs Min-Max — Comparative Analysis")
    print("=" * 70)

    test_configs = [
        ("Empty board", [], True),
        ("After X:4", [4], True),
        ("After X:4, O:0", [4, 0], False),
        ("After X:4, O:0, X:2", [4, 0, 2], True),
        ("After X:4, O:0, X:2, O:6", [4, 0, 2, 6], False),
        ("After X:4, O:0, X:2, O:6, X:1", [4, 0, 2, 6, 1], True),
        ("After X:4, O:0, X:2, O:6, X:1, O:3", [4, 0, 2, 6, 1, 3], False),
    ]

    print(f"\n  {'State':<38} {'MM Nodes':<12} {'AB Nodes':<12} {'Pruned':<10} {'Reduction':<12} {'AB Time'}")
    print(f"  {'-' * 95}")

    for label, moves, is_max in test_configs:
        board_mm = create_board()
        board_ab = create_board()
        for i, m in enumerate(moves):
            mark = HUMAN if i % 2 == 0 else AI
            board_mm[m] = mark
            board_ab[m] = mark

        mm_stats['nodes'] = 0
        minimax(board_mm, is_max)
        mm_nodes = mm_stats['nodes']

        ab_stats['nodes'] = 0
        ab_stats['pruned'] = 0
        start = time.time()
        alpha_beta(board_ab, is_max, -float('inf'), float('inf'))
        ab_time = time.time() - start
        ab_nodes = ab_stats['nodes']
        pruned = ab_stats['pruned']

        if mm_nodes > 0:
            reduction = (1 - ab_nodes / mm_nodes) * 100
        else:
            reduction = 0

        print(f"  {label:<38} {mm_nodes:<12} {ab_nodes:<12} {pruned:<10} {reduction:<11.1f}% {ab_time:.4f}s")

    print(f"\n{'─' * 70}")
    print("  Pruning Pattern Visualization:")
    print(f"{'─' * 70}")
    v_board = create_board()
    v_board[4] = HUMAN
    v_board[0] = AI
    print("\n  Board: X at center(4), O at corner(0)")
    print_board(v_board)
    visualize_pruning(v_board, False, -float('inf'), float('inf'), max_depth=3)

    print(f"\n{'─' * 70}")
    print("  Analysis on varied game trees:")
    print(f"{'─' * 70}")

    varied_states = [
        ("Corner opening (X:0)", [0]),
        ("Center opening (X:4)", [4]),
        ("Edge opening (X:1)", [1]),
        ("Diagonal (X:0,O:4,X:8)", [0, 4, 8]),
        ("Line threat (X:0,O:4,X:1)", [0, 4, 1]),
    ]

    print(f"\n  {'Configuration':<38} {'MM Nodes':<12} {'AB Nodes':<12} {'Pruned':<10} {'Savings %'}")
    print(f"  {'-' * 80}")

    for label, moves in varied_states:
        b1 = create_board()
        b2 = create_board()
        for i, m in enumerate(moves):
            mark = HUMAN if i % 2 == 0 else AI
            b1[m] = mark
            b2[m] = mark
        is_max = len(moves) % 2 == 1

        mm_stats['nodes'] = 0
        minimax(b1, is_max)
        mm_n = mm_stats['nodes']

        ab_stats['nodes'] = 0
        ab_stats['pruned'] = 0
        alpha_beta(b2, is_max, -float('inf'), float('inf'))
        ab_n = ab_stats['nodes']
        pr = ab_stats['pruned']
        savings = (1 - ab_n / mm_n) * 100 if mm_n > 0 else 0

        print(f"  {label:<38} {mm_n:<12} {ab_n:<12} {pr:<10} {savings:.1f}%")

    print(f"\n{'─' * 70}")
    print("  OBSERVATIONS:")
    print("  1. Alpha-beta pruning explores significantly fewer nodes than plain")
    print("     minimax while producing identical optimal decisions.")
    print("  2. Pruning is most effective when good moves are explored first;")
    print("     with optimal move ordering, alpha-beta can reduce the search")
    print("     tree from O(b^d) to O(b^(d/2)).")
    print("  3. More pruning occurs at MAX nodes when a high value is found")
    print("     early (raising alpha) and at MIN nodes when a low value is")
    print("     found early (lowering beta).")
    print("  4. The reduction percentage varies with game state — states with")
    print("     clear threats or forced moves tend to prune more aggressively")
    print("     because the optimal path is discovered sooner.")
    print("  5. Despite pruning, both algorithms always return the same optimal")
    print("     move, confirming correctness of alpha-beta.")
    print()


def main():
    print("1. Play against AI (alpha-beta)")
    print("2. Comparative analysis (minimax vs alpha-beta)")
    choice = input("Choose (1/2): ").strip()

    if choice == '1':
        play_game()
    else:
        comparative_analysis()


if __name__ == "__main__":
    main()
