# /usr/bin/python3
# ------------------------------------
# Created by: def__init__
# GNU GPL v3.0
# ------------------------------------

import os
import time

import chess
import chess.engine
import chess.pgn
import chess.polyglot
import chess.svg
from rich.progress import track, Progress
from rich.prompt import Prompt
import argparse

from Console import *
from Utils import sort_tuple, convert_to_int, print_board  # local lib for stuff


def get_material(board_to_get):
    board_to_get = convert_to_int(board_to_get)
    num = 0
    for j in range(len(board_to_get)):
        for h in range(len(board_to_get[j])):
            num += int(board_to_get[j][h])
    return num


# TODO: add alpha / beta pruning here and optimize it

def new_recurse_checkmate(board, movestack, depth):
    if depth > 0:
        for temp_move in board.legal_moves:
            get_material(board)

            temp_board = chess.Board()
            temp_board.set_fen(board.fen())

            temp_board.push(temp_move)

            if temp_board.is_checkmate():
                movestack.append([temp_move, 10000])

            else:
                try:
                    movestack = movestack + new_recurse_checkmate(board, movestack, depth - 1)
                except RecursionError:
                    print("RecursionError " + str(depth))

    return movestack


def new_recurse_material(board, movestack, depth, pathisgood):
    if depth > 0:
        if depth > 2 and pathisgood is not True:
            pass
        elif depth > 2 and pathisgood is True:
            for temp_move in board.legal_moves:
                get_material(board)

                temp_board = chess.Board()
                temp_board.set_fen(board.fen())

                temp_board.push(temp_move)
                # print(temp_board)
                # input("")

                if get_material(temp_board) > get_material(board):
                    pathisgood = True
                    movestack.append([temp_move, 1000])

                else:
                    pathisgood = False

                x3 = new_recurse_material(board, movestack, depth - 1, pathisgood)
                if x3 is not None:
                    movestack = movestack + x3
    else:
        return movestack


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Just an example",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-matesd", "--mate-scan-depth", help="how far should the model go in checkmate checking?")
    parser.add_argument("-materialsd", "--material-scan-depth", help="how far should the model go in material gain/loss checking?")
    parser.add_argument("-sf", "--use-stockfish", action="store_true", help="have the engine play stockfish?")

    args = parser.parse_args()
    config = vars(args)
    print(config)

    
    MATE_SCAN_DEPTH = int(config["mate_scan_depth"])
    MATERIAL_SCAN_DEPTH = int(config["material_scan_depth"])
    USE_STOCKFISH = bool(config["use_stockfish"])
    
    computer_moves = 0

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

    print("MATERIAL_SCAN_DEPTH: " + str(MATERIAL_SCAN_DEPTH))
    print_board(board)

    while True:
        # get user move
        if not USE_STOCKFISH:
            player_move = Prompt.ask("Enter your move (UCI format, enter to have Stockfish16 play.)")
        elif USE_STOCKFISH:
            player_move = ""
            
        try:
            while chess.Move.from_uci(player_move) not in board.legal_moves:
                player_move = Prompt.ask("Enter your move (UCI)")
            first_game.add_variation(chess.Move.from_uci(player_move))
            board.push(chess.Move.from_uci(player_move))
        except Exception as e:
            # print(e)
            result = engine.play(board, chess.engine.Limit(time=0.1))
            board.push(result.move)

        clear()
        if get_material(board) <= -1:
            print(f"Black is up {get_material(board) * -1}")
        elif get_material(board) >= 1:
            print(f"White is up {get_material(board)}")
        else:
            print("Tied in material")

        print("MATERIAL_SCAN_DEPTH: " + str(MATERIAL_SCAN_DEPTH))
        # print("Move: " + str(computer_moves))
        print_board(board)

        start = time.time()

        # begin the engine
        allmoves = []
        blocked_moves = []

        x1 = new_recurse_checkmate(board, allmoves, MATE_SCAN_DEPTH)
        if x1 is not None:
            allmoves = allmoves + x1
        else:
            pass

        x2 = new_recurse_material(board, allmoves, MATERIAL_SCAN_DEPTH, True)
        if x2 is not None:
            allmoves = allmoves + x2

        # check the polygot books for openings
        for i in track(range(len(os.listdir("./polygot_openings/"))), description="Loading polygot_openings..."):
            with chess.polyglot.open_reader("./polygot_openings/" + os.listdir("./polygot_openings/")[i]) as reader:
                for entry in reader.find_all(board):
                    allmoves.append([entry.move, entry.weight])

        reccomended_moves = sort_tuple(allmoves)
        reccomended_moves.reverse()
        try:
            first_game.add_variation(chess.Move.from_uci(str(reccomended_moves[0][0])))
            board.push(chess.Move.from_uci(str(reccomended_moves[0][0])))
        except IndexError:
            # ran out of moves
            print("Ran out of moves")
            result = engine.analyse(board, chess.engine.Limit(time=1))
            print(result["score"].black())
            # x.append(i)
            # y.append(result["score"].black())
            # input("i")
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
        print("MATERIAL_SCAN_DEPTH: " + str(MATERIAL_SCAN_DEPTH))
        print_board(board)
        try:
            move = str(reccomended_moves[0][0])
        except IndexError:
            move = "NONE"
        print(f"Computer move: {move}")
        end = time.time()
        computer_moves += 1
        print(f"Computer took: " + str(end - start) + " Move: " + str(computer_moves))

        if board.outcome() is not None:
            print(board.outcome().termination)
            print("gameover")
            print(first_game)
            raise KeyboardInterrupt
        # print(f"I reccomend the move: {reccomended_moves[0][0]} with a confidence of {reccomended_moves[0][1]}")

"""# plotting the points
plt.plot(x, y)

# naming the x axis
plt.xlabel('Strenght')
# naming the y axis
plt.ylabel('stockfish eval (black pov)')

# giving a title to my graph
plt.title('My first graph!')

# function to show the plot
plt.show()"""
