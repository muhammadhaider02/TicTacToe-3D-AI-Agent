import numpy as np

board = np.zeros((9, 9), dtype=int)
small_board_winners = np.zeros((3, 3), dtype=int)
current_player = 1
last_move = None

def get_board_state():
    return board.copy(), small_board_winners.copy()

def is_legal_move(move):
    global last_move
    big_row, big_col, small_row, small_col = move
    row = big_row * 3 + small_row
    col = big_col * 3 + small_col

    if not (0 <= big_row < 3 and 0 <= big_col < 3 and 0 <= small_row < 3 and 0 <= small_col < 3):
        return False

    if board[row, col] != 0:
        return False

    if small_board_winners[big_row, big_col] != 0:
        return False

    if last_move is None:
        return True

    _, _, last_small_row, last_small_col = last_move
    target_board_row, target_board_col = last_small_row, last_small_col

    if small_board_winners[target_board_row, target_board_col] != 0 or is_small_board_full(target_board_row, target_board_col):
        return True

    return big_row == target_board_row and big_col == target_board_col

def is_small_board_full(big_row, big_col):
    start_row, start_col = big_row * 3, big_col * 3
    return not np.any(board[start_row:start_row + 3, start_col:start_col + 3] == 0)

def check_small_board_winner(big_row, big_col):
    start_row, start_col = big_row * 3, big_col * 3
    small_board = board[start_row:start_row + 3, start_col:start_col + 3]

    for r in range(3):
        if small_board[r, 0] != 0 and small_board[r, 0] == small_board[r, 1] == small_board[r, 2]:
            return small_board[r, 0]

    for c in range(3):
        if small_board[0, c] != 0 and small_board[0, c] == small_board[1, c] == small_board[2, c]:
            return small_board[0, c]

    if small_board[0, 0] != 0 and small_board[0, 0] == small_board[1, 1] == small_board[2, 2]:
        return small_board[0, 0]
    if small_board[0, 2] != 0 and small_board[0, 2] == small_board[1, 1] == small_board[2, 0]:
        return small_board[0, 2]

    return 0

def check_game_winner():
    for r in range(3):
        if small_board_winners[r, 0] != 0 and small_board_winners[r, 0] == small_board_winners[r, 1] == small_board_winners[r, 2]:
            return small_board_winners[r, 0]

    for c in range(3):
        if small_board_winners[0, c] != 0 and small_board_winners[0, c] == small_board_winners[1, c] == small_board_winners[2, c]:
            return small_board_winners[0, c]

    if small_board_winners[0, 0] != 0 and small_board_winners[0, 0] == small_board_winners[1, 1] == small_board_winners[2, 2]:
        return small_board_winners[0, 0]
    if small_board_winners[0, 2] != 0 and small_board_winners[0, 2] == small_board_winners[1, 1] == small_board_winners[2, 0]:
        return small_board_winners[0, 2]

    return 0

def is_board_full():
    return not np.any(board == 0)

def make_move(move):
    global board, small_board_winners, current_player, last_move
    big_row, big_col, small_row, small_col = move
    row = big_row * 3 + small_row
    col = big_col * 3 + small_col

    board[row, col] = current_player
    last_move = move

    winner = check_small_board_winner(big_row, big_col)
    if winner != 0:
        small_board_winners[big_row, big_col] = winner

    current_player = 3 - current_player

def get_valid_moves():
    valid_moves = []
    if last_move is None:
        for big_row in range(3):
            for big_col in range(3):
                if small_board_winners[big_row, big_col] == 0:
                    start_row, start_col = big_row * 3, big_col * 3
                    for r in range(3):
                        for c in range(3):
                            if board[start_row + r, start_col + c] == 0:
                                valid_moves.append((big_row, big_col, r, c))
    else:
        _, _, last_small_row, last_small_col = last_move
        target_board_row, target_board_col = last_small_row, last_small_col
        if small_board_winners[target_board_row, target_board_col] != 0 or is_small_board_full(target_board_row, target_board_col):
            for big_row in range(3):
                for big_col in range(3):
                    if small_board_winners[big_row, big_col] == 0:
                        start_row, start_col = big_row * 3, big_col * 3
                        for r in range(3):
                            for c in range(3):
                                if board[start_row + r, start_col + c] == 0:
                                    valid_moves.append((big_row, big_col, r, c))
        else:
            start_row, start_col = target_board_row * 3, target_board_col * 3
            for r in range(3):
                for c in range(3):
                    if board[start_row + r, start_col + c] == 0:
                        valid_moves.append((target_board_row, target_board_col, r, c))
    return valid_moves

def heuristic_evaluation():
    score = 0
    for r in range(3):
        for c in range(3):
            if small_board_winners[r, c] == 1:
                score += 10
            elif small_board_winners[r, c] == 2:
                score -= 10
    if small_board_winners[1, 1] == 1:
        score += 5
    elif small_board_winners[1, 1] == 2:
        score -= 5
    for r in range(3):
        for c in range(3):
            if small_board_winners[r, c] != 0:
                continue
            small_board = board[r*3:r*3+3, c*3:c*3+3]
            for i in range(3):
                if np.sum(small_board[i, :] == 1) == 2 and np.sum(small_board[i, :] == 0) == 1:
                    score += 3
                if np.sum(small_board[i, :] == 2) == 2 and np.sum(small_board[i, :] == 0) == 1:
                    score -= 3
                if np.sum(small_board[:, i] == 1) == 2 and np.sum(small_board[:, i] == 0) == 1:
                    score += 3
                if np.sum(small_board[:, i] == 2) == 2 and np.sum(small_board[:, i] == 0) == 1:
                    score -= 3
            if np.sum(small_board.diagonal() == 1) == 2 and np.sum(small_board.diagonal() == 0) == 1:
                score += 3
            if np.sum(small_board.diagonal() == 2) == 2 and np.sum(small_board.diagonal() == 0) == 1:
                score -= 3
            if np.sum(np.fliplr(small_board).diagonal() == 1) == 2 and np.sum(np.fliplr(small_board).diagonal() == 0) == 1:
                score += 3
            if np.sum(np.fliplr(small_board).diagonal() == 2) == 2 and np.sum(np.fliplr(small_board).diagonal() == 0) == 1:
                score -= 3
    return score

def minimax(depth, is_maximizing, alpha, beta):
    winner = check_game_winner()
    if winner == 1:
        return 100 - depth
    if winner == 2:
        return -100 + depth
    if is_board_full() or depth >= 4:
        return heuristic_evaluation()

    valid_moves = get_valid_moves()
    if not valid_moves:
        return heuristic_evaluation()

    if is_maximizing:
        max_eval = float('-inf')
        for move in valid_moves:
            make_move(move)
            eval = minimax(depth + 1, False, alpha, beta)
            undo_move(move)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in valid_moves:
            make_move(move)
            eval = minimax(depth + 1, True, alpha, beta)
            undo_move(move)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def undo_move(move):
    global board, current_player, small_board_winners
    big_row, big_col, small_row, small_col = move
    row = big_row * 3 + small_row
    col = big_col * 3 + small_col
    board[row, col] = 0
    current_player = 3 - current_player
    small_board_winners[big_row, big_col] = check_small_board_winner(big_row, big_col)

def ai_move():
    best_score = float('-inf')
    best_move = None
    for move in get_valid_moves():
        make_move(move)
        score = minimax(0, False, float('-inf'), float('inf'))
        undo_move(move)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def display_board():
    symbols = {0: '.', 1: 'X', 2: 'O'}
    for big_row in range(3):
        for small_row in range(3):
            row = big_row * 3 + small_row
            line = []
            for big_col in range(3):
                start_col = big_col * 3
                for small_col in range(3):
                    col = start_col + small_col
                    line.append(symbols[board[row, col]])
                line.append(' ')
            print(' '.join(line))
        print()
    print("Small Board Winners:")
    for r in range(3):
        print([symbols[small_board_winners[r, c]] for c in range(3)])

def human_vs_human():
    global board, small_board_winners, current_player, last_move
    board = np.zeros((9, 9), dtype=int)
    small_board_winners = np.zeros((3, 3), dtype=int)
    current_player = 1
    last_move = None

    while True:
        display_board()
        player = 'X' if current_player == 1 else 'O'
        print(f"Player {player}'s turn")
        if last_move:
            _, _, last_small_row, last_small_col = last_move
            target_board = (last_small_row, last_small_col)
            if small_board_winners[target_board[0], target_board[1]] == 0 and not is_small_board_full(target_board[0], target_board[1]):
                print(f"Must play in board ({target_board[0]}, {target_board[1]})")
                try:
                    small_row = int(input("Enter small board row (0-2): "))
                    small_col = int(input("Enter small board col (0-2): "))
                    move = (target_board[0], target_board[1], small_row, small_col)
                except ValueError:
                    print("Invalid input. Enter numbers between 0 and 2.")
                    continue
            else:
                print("Can play in any available board")
                try:
                    big_row = int(input("Enter big board row (0-2): "))
                    big_col = int(input("Enter big board col (0-2): "))
                    small_row = int(input("Enter small board row (0-2): "))
                    small_col = int(input("Enter small board col (0-2): "))
                    move = (big_row, big_col, small_row, small_col)
                except ValueError:
                    print("Invalid input. Enter numbers between 0 and 2.")
                    continue
        else:
            try:
                big_row = int(input("Enter big board row (0-2): "))
                big_col = int(input("Enter big board col (0-2): "))
                small_row = int(input("Enter small board row (0-2): "))
                small_col = int(input("Enter small board col (0-2): "))
                move = (big_row, big_col, small_row, small_col)
            except ValueError:
                print("Invalid input. Enter numbers between 0 and 2.")
                continue

        if not is_legal_move(move):
            print("Illegal move. Try again.")
            continue
        make_move(move)

        winner = check_game_winner()
        if winner != 0:
            display_board()
            print(f"Player {'X' if winner == 1 else 'O'} wins!")
            break
        if is_board_full():
            display_board()
            print("It's a draw!")
            break

def human_vs_ai():
    global board, small_board_winners, current_player, last_move
    board = np.zeros((9, 9), dtype=int)
    small_board_winners = np.zeros((3, 3), dtype=int)
    current_player = 1
    last_move = None

    while True:
        display_board()
        if current_player == 1:
            print("AI (X) is thinking...")
            move = ai_move()
            print(f"AI plays: big board ({move[0]}, {move[1]}), small board ({move[2]}, {move[3]})")
            make_move(move)
        else:
            print("Human (O)'s turn")
            if last_move:
                _, _, last_small_row, last_small_col = last_move
                target_board = (last_small_row, last_small_col)
                if small_board_winners[target_board[0], target_board[1]] == 0 and not is_small_board_full(target_board[0], target_board[1]):
                    print(f"Must play in board ({target_board[0]}, {target_board[1]})")
                    try:
                        small_row = int(input("Enter small board row (0-2): "))
                        small_col = int(input("Enter small board col (0-2): "))
                        move = (target_board[0], target_board[1], small_row, small_col)
                    except ValueError:
                        print("Invalid input. Enter numbers between 0 and 2.")
                        continue
                else:
                    print("Can play in any available board")
                    try:
                        big_row = int(input("Enter big board row (0-2): "))
                        big_col = int(input("Enter big board col (0-2): "))
                        small_row = int(input("Enter small board row (0-2): "))
                        small_col = int(input("Enter small board col (0-2): "))
                        move = (big_row, big_col, small_row, small_col)
                    except ValueError:
                        print("Invalid input. Enter numbers between 0 and 2.")
                        continue
            else:
                try:
                    big_row = int(input("Enter big board row (0-2): "))
                    big_col = int(input("Enter big board col (0-2): "))
                    small_row = int(input("Enter small board row (0-2): "))
                    small_col = int(input("Enter small board col (0-2): "))
                    move = (big_row, big_col, small_row, small_col)
                except ValueError:
                    print("Invalid input. Enter numbers between 0 and 2.")
                    continue

            if not is_legal_move(move):
                print("Illegal move. Try again.")
                continue
            make_move(move)

        winner = check_game_winner()
        if winner != 0:
            display_board()
            print(f"{'AI (X)' if winner == 1 else 'Human (O)'} wins!")
            break
        if is_board_full():
            display_board()
            print("It's a draw!")
            break

def play_game():
    print("Starting 3D Tic-Tac-Toe...")
    while True:
        try:
            mode = int(input("Enter 1 for Human vs Human, 2 for Human vs AI: "))
            print(f"Selected mode: {mode}")
            if mode == 1:
                print("Starting Human vs Human mode...")
                human_vs_human()
                break
            elif mode == 2:
                print("Starting Human vs AI mode...")
                human_vs_ai()
                break
            else:
                print("Invalid choice. Enter 1 or 2.")
        except ValueError:
            print("Invalid input. Enter a number (1 or 2).")
    print("Game ended.")

play_game()