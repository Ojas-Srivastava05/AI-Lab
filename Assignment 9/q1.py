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


stats = {'nodes_explored': 0}


def minimax(board, is_maximizing, depth=0):
    stats['nodes_explored'] += 1

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


def visualize_tree(board, is_maximizing, depth=0, move_made=None, max_depth=3):
    indent = "  " * depth
    player = "MAX(O)" if is_maximizing else "MIN(X)"

    if move_made is not None:
        pos_label = f"(pos {move_made})"
    else:
        pos_label = "(root)"

    winner = check_winner(board)
    if winner == AI:
        print(f"{indent}└─ {player} {pos_label} → score = {10 - depth}")
        return
    if winner == HUMAN:
        print(f"{indent}└─ {player} {pos_label} → score = {depth - 10}")
        return
    if is_full(board):
        print(f"{indent}└─ {player} {pos_label} → score = 0 (draw)")
        return

    if depth >= max_depth:
        print(f"{indent}└─ {player} {pos_label} → (truncated at depth {max_depth})")
        return

    print(f"{indent}├─ {player} {pos_label}")
    moves = get_available_moves(board)
    for move in moves:
        mark = AI if is_maximizing else HUMAN
        board[move] = mark
        visualize_tree(board, not is_maximizing, depth + 1, move, max_depth)
        board[move] = EMPTY


def play_game():
    board = create_board()
    print("Tic-Tac-Toe: Human (X) vs AI (O)")
    print("Positions are numbered 0-8:")
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
                    print("Invalid move, try again.")
                except ValueError:
                    print("Enter a number 0-8.")
            board[move] = HUMAN
            current = AI
        else:
            print("AI is thinking...")
            stats['nodes_explored'] = 0
            start = time.time()
            score, move = minimax(board, True)
            elapsed = time.time() - start

            board[move] = AI
            print(f"AI plays position {move} (score: {score})")
            print(f"  Nodes explored: {stats['nodes_explored']}")
            print(f"  Time: {elapsed:.4f}s")
            current = HUMAN


def performance_analysis():
    print("=" * 60)
    print("  Min-Max Performance Analysis")
    print("=" * 60)

    board = create_board()
    stats['nodes_explored'] = 0
    start = time.time()
    score, best_move = minimax(board, True)
    elapsed = time.time() - start

    print(f"\n  Empty board analysis:")
    print(f"    Best first move for AI (O): position {best_move}")
    print(f"    Score: {score}")
    print(f"    Nodes explored: {stats['nodes_explored']}")
    print(f"    Time: {elapsed:.4f}s")

    print(f"\n{'─' * 60}")
    print("  Nodes explored from different game states:")
    print(f"  {'Moves played':<16} {'Nodes explored':<18} {'Time (s)':<12} {'Best move'}")
    print(f"  {'-' * 55}")

    test_boards = [
        [],
        [4],
        [4, 0],
        [4, 0, 2],
        [4, 0, 2, 6],
        [4, 0, 2, 6, 1],
        [4, 0, 2, 6, 1, 3],
    ]

    for moves in test_boards:
        b = create_board()
        for i, m in enumerate(moves):
            b[m] = HUMAN if i % 2 == 0 else AI
        is_max = len(moves) % 2 == 1

        stats['nodes_explored'] = 0
        start = time.time()
        sc, mv = minimax(b, is_max)
        elapsed = time.time() - start

        player_label = "O(max)" if is_max else "X(min)"
        print(f"  {len(moves):<16} {stats['nodes_explored']:<18} {elapsed:<12.4f} {mv} [{player_label}]")

    print(f"\n{'─' * 60}")
    print("  Search Tree Visualization (depth-limited to 3):")
    print(f"{'─' * 60}")
    tree_board = create_board()
    tree_board[4] = HUMAN
    tree_board[0] = AI
    print("\n  Board state: X at 4, O at 0")
    print_board(tree_board)
    visualize_tree(tree_board, False, max_depth=3)

    print(f"\n{'─' * 60}")
    print("  OBSERVATIONS:")
    print("  1. From an empty board, minimax explores ~550k nodes since")
    print("     the full game tree of tic-tac-toe has 9! leaf paths.")
    print("  2. As more moves are played, the search space shrinks")
    print("     drastically — fewer empty cells means fewer branches.")
    print("  3. Minimax guarantees optimal play; with perfect play from")
    print("     both sides, tic-tac-toe always results in a draw.")
    print("  4. The tree grows exponentially with branching factor b")
    print("     and depth d giving O(b^d) complexity.")
    print()


def main():
    print("1. Play against AI")
    print("2. Performance analysis")
    choice = input("Choose (1/2): ").strip()

    if choice == '1':
        play_game()
    else:
        performance_analysis()


if __name__ == "__main__":
    main()
