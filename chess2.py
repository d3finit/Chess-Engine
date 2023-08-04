import chess
import random
import chess.engine

# Board Representation
board = chess.Board()

# Move Generation
def generate_moves():
    moves = []
    for move in board.legal_moves:
        moves.append(move)
    return moves

# Move Evaluation
def evaluate_move(move):
    # Simple evaluation function: Return a random score between -1 and 1
    score = random.uniform(-1, 1)
    return score

# Search Algorithm
def minimax(depth, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_move(None)

    if maximizing_player:
        max_eval = float("-inf")
        for move in generate_moves():
            board.push(move)
            eval = minimax(depth - 1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for move in generate_moves():
            board.push(move)
            eval = minimax(depth - 1, True)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval

# Main Game Loop
def play_game():
    engine = chess.engine.SimpleEngine.popen_uci(r".\stockfish\stockfish-windows-x86-64-avx2.exe")

    while not board.is_game_over():
        if board.turn == chess.WHITE:
            best_score = float("-inf")
            best_move = None
            for move in generate_moves():
                board.push(move)
                score = minimax(3, False)  # Depth 3 search
                board.pop()
                if score > best_score:
                    best_score = score
                    best_move = move
            board.push(best_move)
        else:
            result = engine.play(board, chess.engine.Limit(time=0.1))

            board.push(result.move)

        print(board)

# Start the game
play_game()
