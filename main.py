# /usr/bin/python3
# ------------------------------------
# Created by: def__init__
# GNU GPL v3.0
# ------------------------------------

# import required libs
import chess, chess.svg, chess.pgn, chess.polyglot, chess.engine
from Console import *
import os
from rich.progress import track, Progress
from rich.prompt import Prompt
import time
from Utils import sort_tuple, convert_to_int, print_board  # local lib for stuff


def get_material(board_to_get):
    board_to_get = convert_to_int(board_to_get)
    num = 0
    for j in range(len(board_to_get)):
        for h in range(len(board_to_get[j])):
            num += int(board_to_get[j][h])
    return num


# TODO: add alpha / beta pruning here and optimize it
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


def new_recurse_material(board, movestack, depth):
    for temp_move in board.legal_moves:
        get_material(board)

        temp_board = chess.Board()
        temp_board.set_fen(board.fen())

        temp_board.push(temp_move)

        if get_material(temp_board) > get_material(board):
            movestack.push([temp_move, 1000])
            movestack = movestack + new_recurse_material(board, movestack, depth - 1)
            print(movestack, depth)

    return movestack


if __name__ == "__main__":
    # PERMVARS
    MATE_SCAN_DEPTH = 4
    MATERIAL_SCAN_DEPTH = 15
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
    print_board(board)

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
        print_board(board)

        start = time.time()

        # begin the engine
        allmoves = []
        blocked_moves = []

        for i in range(1, MATE_SCAN_DEPTH + 1):
            if len(allmoves) >= 1:
                pass
            else:
                allmoves = allmoves + recurse_checkmate(board, allmoves, i)

        # better material recurse with ALPHA BETA PRUNING (its trash rn but it exists)
        allmoves = new_recurse_material(board, allmoves, MATERIAL_SCAN_DEPTH)

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
        print_board(board)
        print(f"Computer move: {move}")
        end = time.time()
        print(f"Computer took: " + str(end - start))

        if board.outcome() is not None:
            print(board.outcome().termination)
            print("gameover")
            print(first_game)
        # print(f"I reccomend the move: {reccomended_moves[0][0]} with a confidence of {reccomended_moves[0][1]}")
