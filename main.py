# /usr/bin/python3
# ------------------------------------
# Created by: def__init__
# GNU GPL v3.0
# ------------------------------------

# import required libs
import chess
import chess.svg
import chess.pgn
import chess.polyglot
import chess.engine
from Console import *
import os
from rich.progress import track, Progress
import random
from rich.prompt import Prompt
import time


# tuple sorter
def sort_tuple(tup):
    tup.sort(key=lambda x: x[1])
    return tup


def convert_to_int(board_to_convert):
    return [
        ['♚♛♜♝♞♟⭘♙♘♗♖♕♔'.index(c) - 6 for c in row.split()]
        for row in board_to_convert.unicode().split('\n')
    ]


def convert_to_anasi(board_to_convert):
    mapped = {
        1: "♟",  # White Pawn
        -1: "♙",  # Black Pawn
        2: "♞",  # White Knight
        -2: "♘",  # Black Knight
        3: "♝",  # White Bishop
        -3: "♗",  # Black Bishop
        4: "♜",  # White Rook
        -4: "♖",  # Black Rook
        5: "♛",  # White Queen
        -5: "♕",  # Black Queen
        6: "♚",  # White King
        -6: "♔"  # Black King
    }
    for j in range(len(board_to_convert)):
        for h in range(len(board_to_convert[j])):
            if board_to_convert[j][h] != 0:
                board_to_convert[j][h] = mapped[board_to_convert[j][h]]
            else:
                board_to_convert[j][h] = "⭘"

    return board_to_convert


def print_good(board_to_convert):
    board_to_convert = convert_to_anasi(convert_to_int(board_to_convert))

    print("  |A|B|C|D|E|F|G|H|")

    for j in range(len(board_to_convert)):
        line = f"|{str(8 - j)}|"
        for h in range(len(board_to_convert[j])):
            line = line + board_to_convert[j][h] + " "

        print(line)


def get_material(board_to_get):
    board_to_get = convert_to_int(board_to_get)

    num = 0

    for j in range(len(board_to_get)):
        for h in range(len(board_to_get[j])):
            num += int(board_to_get[j][h])

    return num


# Move Generation
def generate_moves():
    moves = []
    for move_list in board.legal_moves:
        moves.append(move_list)
    return moves


# Move Evaluation
def evaluate_move():
    # Simple evaluation function: Return a random score between -1 and 1
    eval_score = random.uniform(-1, 1)
    return eval_score


# Search Algorithm
def minimax(depth, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_move()

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


def recurse_checkmate(board, movestack, limit):
    with Progress() as progress:
        d1 = progress.add_task(f"Mate in X, depth {limit} checking...", total=board.legal_moves.count())
        for temp_move in board.legal_moves:
            if len(movestack) >= 1:
                pass

            else:
                temp_board = chess.Board(fen=board.fen())

                temp_board.push(temp_move)

                progress.update(d1, advance=1)

                movestack = movestack + recurse_checkmate_2(temp_board, movestack, limit - 1, temp_move, progress)

    return movestack


def recurse_checkmate_2(board, movestack, limit, move, progress):
    if limit == 0:
        if board.is_checkmate():
            movestack.append([move, 10000])
    else:
        if limit == 1 or limit == 2:
            pass
        else:
            d1 = progress.add_task(f"Mate in X, depth {limit} checking...", total=board.legal_moves.count())

        if len(movestack) >= 1:
            pass

        else:
            for temp_move in board.legal_moves:
                temp_board = chess.Board()
                temp_board.set_fen(board.fen())

                temp_board.push(temp_move)

                if limit == 1 or limit == 2:
                    pass
                else:
                    progress.update(d1, advance=1)

                    recurse_checkmate_2(temp_board, movestack, limit - 1, move, progress)
    return movestack


def recurse_material(board, movestack, limit, full_board, blocked_moves):
    with Progress() as progress:
        d1 = progress.add_task(f"Depth {limit} checking...", total=board.legal_moves.count())
        for temp_move in board.legal_moves:
            if len(movestack) >= 1:
                pass

            else:
                temp_board = chess.Board(fen=board.fen())

                temp_board.push(temp_move)

                if get_material(temp_board) <= get_material(board):
                    blocked_moves.append(move)

                progress.update(d1, advance=1)
                temp = recurse_material_2(temp_board, movestack, limit - 1, temp_move, progress, full_board,
                                          blocked_moves)
                movestack, blocked_moves = movestack + temp[0], blocked_moves + temp[1]

    return movestack, blocked_moves


def recurse_material_2(board, movestack, limit, move, progress, full_board, blocked_moves):
    if limit == 0:
        if get_material(full_board) <= get_material(board):
            allmoves.append([move, 1000])
    else:
        if limit == 1 or limit == 2:
            pass
        else:
            d1 = progress.add_task(f"Depth {limit} checking...", total=board.legal_moves.count())

        if len(movestack) >= 1:
            pass

        else:
            for temp_move in board.legal_moves:
                temp_board = chess.Board()
                temp_board.set_fen(board.fen())

                temp_board.push(temp_move)

                if get_material(temp_board) <= get_material(board):
                    blocked_moves.append(move)

                if limit == 1 or limit == 2:
                    pass
                else:
                    progress.update(d1, advance=1)

                    recurse_material_2(temp_board, movestack, limit - 1, move, progress, full_board, blocked_moves)
    return movestack, blocked_moves


if __name__ == "__main__":
    # PERMVARS
    MATE_SCAN_DEPTH = 4
    MATERIAL_SCAN_DEPTH = 5
    MINIMAX_DEPTH = 3

    # load stonksfish
    engine = chess.engine.SimpleEngine.popen_uci(r".\stockfish\stockfish-windows-x86-64-avx2.exe")
    # open the game
    pgn = open("CurrentGame.pgn")
    first_game = chess.pgn.read_game(pgn)
    board = first_game.board()
    for move in first_game.mainline_moves():
        board.push(move)

    clear()

    if get_material(board) <= -1:
        print(f"Black is up {get_material(board) * -1}")
    elif get_material(board) >= 1:
        print(f"White is up {get_material(board)}")
    else:
        print("Tied in material")
    print_good(board)

    while True:
        # get user move
        move = Prompt.ask("Enter your move (UCI format, enter to have Stockfish16 play.)")
        # move = ""
        try:
            while chess.Move.from_uci(move) not in board.legal_moves:
                move = Prompt.ask("Enter your move (UCI)")
            first_game.add_variation(chess.Move.from_uci(move))
            board.push(chess.Move.from_uci(move))
        except:
            result = engine.play(board, chess.engine.Limit(time=0.1))
            board.push(result.move)

        clear()
        if get_material(board) <= -1:
            print(f"Black is up {get_material(board) * -1}")
        elif get_material(board) >= 1:
            print(f"White is up {get_material(board)}")
        else:
            print("Tied in material")
        print_good(board)

        start = time.time()

        # begin the engine
        allmoves = []
        blocked_moves = []

        best_score = float("-inf")
        best_move = None
        for move in track(generate_moves(), description="Minimax scanning..."):
            board.push(move)
            score = minimax(MINIMAX_DEPTH, False)  # Depth 3 search
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move

        allmoves.append([best_move, 100000])

        for i in range(1, MATE_SCAN_DEPTH + 1):
            if len(allmoves) >= 1:
                pass
            else:
                allmoves = allmoves + recurse_checkmate(board, allmoves, i)

        for i in range(1, MATERIAL_SCAN_DEPTH + 1):
            if len(allmoves) >= 1:
                pass
            else:
                temp = recurse_material(board, allmoves, i, board, blocked_moves)
                allmoves, blocked_moves = allmoves + temp[0], blocked_moves + temp[1]

        # check the polygot books for openings
        for i in track(range(len(os.listdir("./polygot_openings/"))), description="Loading polygot_openings..."):
            with chess.polyglot.open_reader("./polygot_openings/" + os.listdir("./polygot_openings/")[i]) as reader:
                for entry in reader.find_all(board):
                    allmoves.append([entry.move, entry.weight])

        reccomended_moves = sort_tuple(allmoves)
        reccomended_moves.reverse()

        first_game.add_variation(chess.Move.from_uci(str(reccomended_moves[0][0])))
        board.push(chess.Move.from_uci(str(reccomended_moves[0][0])))
        clear()
        print(board)
        # print(f"I reccomend the move: {reccomended_moves[0][0]} with a confidence of {reccomended_moves[0][1]}")

        # engine move
        reccomended_moves = sort_tuple(allmoves)
        reccomended_moves.reverse()
        if board.legal_moves.count() == 0:
            if len(reccomended_moves) < 0:
                for move in board.legal_moves:
                    if move in blocked_moves:
                        pass

                    else:
                        first_game.add_variation(move)
                        board.push(move)
                        move = move.uci()
                        break
                else:
                    move = str(reccomended_moves[0][0])
                    first_game.add_variation(chess.Move.from_uci(str(reccomended_moves[0][0])))
                    board.push(chess.Move.from_uci(str(reccomended_moves[0][0])))

        clear()

        if get_material(board) <= -1:
            print(f"Black is up {get_material(board) * -1}")
        elif get_material(board) >= 1:
            print(f"White is up {get_material(board)}")
        else:
            print("Tied in material")
        print_good(board)
        print(f"Computer move: {move}")
        end = time.time()
        print(f"Computer took: " + str(end - start))

        if board.outcome() is not None:
            print(board.outcome().termination)
            print("gameover")
            print(first_game)
        # print(f"I reccomend the move: {reccomended_moves[0][0]} with a confidence of {reccomended_moves[0][1]}")
