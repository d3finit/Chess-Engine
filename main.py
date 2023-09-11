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
import chess.gaviota
from rich.progress import track, Progress
from rich.prompt import Prompt
import argparse
import csv

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
            elif temp_board.is_stalemate() or temp_board.is_fifty_moves() or temp_board.is_seventyfive_moves() or temp_board.is_fivefold_repetition():
                pass
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
                    movestack.append([temp_move, get_material(temp_board)])

                else:
                    pathisgood = False

                x3 = new_recurse_material(board, movestack, depth - 1, pathisgood)
                if x3 is not None:
                    movestack = movestack + x3
    else:
        return movestack


def evaluate_board(board):
    score = 0
    r1 = ["a", "b", "c", "d", "e", "f", "g", "h"]
    r2 = ["1", "2", "3", "4", "5", "6", "7", "8"]
    databoard = [
        ["a8", "b8", "c8", "d8", "e8", "f8", "g8"],
        ["a7", "b7", "c7", "d7", "e7", "f7", "g7"],
        ["a6", "b6", "c6", "d6", "e6", "f6", "g6"],
        ["a5", "b5", "c5", "d5", "e5", "f5", "g5"],
        ["a4", "b4", "c4", "d4", "e4", "f4", "g4"],
        ["a3", "b3", "c3", "d3", "e3", "f3", "g3"],
        ["a2", "b2", "c2", "d2", "e2", "f2", "g2"],
        ["a1", "b1", "c1", "d1", "e1", "f1", "g1"],
    ]

    pawn_score_map = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    knight_score_map = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50],
    ]

    bishop_score_map = [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20],
    ]

    rook_score_map = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0]
    ]

    queen_score_map = [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ]

    for i in range(len(pawn_score_map)):
        pawn_score_map[i] = list(reversed(pawn_score_map[i]))
    pawn_score_map = list(reversed(pawn_score_map))

    for i in range(len(knight_score_map)):
        knight_score_map[i] = list(reversed(knight_score_map[i]))
    knight_score_map = list(reversed(knight_score_map))

    for i in range(len(bishop_score_map)):
        bishop_score_map[i] = list(reversed(bishop_score_map[i]))
    bishop_score_map = list(reversed(bishop_score_map))

    for i in range(len(rook_score_map)):
        rook_score_map[i] = list(reversed(rook_score_map[i]))
    rook_score_map = list(reversed(rook_score_map))

    for i in range(len(queen_score_map)):
        queen_score_map[i] = list(reversed(queen_score_map[i]))
    queen_score_map = list(reversed(queen_score_map))


    for i in range(len(databoard)):
        for j in range(len(databoard[i])):
            piece = board.piece_at(chess.parse_square(databoard[i][j]))
            if piece is not None:
                if piece.symbol().lower() == "p":
                    if piece.symbol() == "P":
                        score = score - pawn_score_map[i][j]
                    else:
                        score = score + pawn_score_map[i][j]

                if piece.symbol().lower() == "n":
                    if piece.symbol() == "N":
                        score = score - knight_score_map[i][j]
                    else:
                        score = score + knight_score_map[i][j]

                if piece.symbol().lower() == "b":
                    if piece.symbol() == "B":
                        score = score - bishop_score_map[i][j]
                    else:
                        score = score + bishop_score_map[i][j]

                if piece.symbol().lower() == "r":
                    if piece.symbol() == "R":
                        score = score - rook_score_map[i][j]
                    else:
                        score = score + rook_score_map[i][j]

                if piece.symbol().lower() == "q":
                    if piece.symbol() == "R":
                        score = score - queen_score_map[i][j]
                    else:
                        score = score + queen_score_map[i][j]


    return score

def move_eval_thing(board, movestack):
    for temp_move in board.legal_moves:
        get_material(board)

        temp_board = chess.Board()
        temp_board.set_fen(board.fen())

        temp_board.push(temp_move)
        # print(temp_board)
        # input("")
        x = evaluate_board(temp_board)
        # print(x)
        # print(temp_board)
        # input("")
        if x > evaluate_board(board):
            print(x)
            movestack.append([temp_move, x])

    return movestack


def tablebase_scan(board, movestack):
    try:
        print("loading tablebase")
        with chess.gaviota.open_tablebase("tablebases") as tablebase:
            print("loaded")
            for temp_move in board.legal_moves:
                print(temp_move)
                get_material(board)

                temp_board = chess.Board()
                temp_board.set_fen(board.fen())

                temp_board.push(temp_move)
                # print(temp_board)
                # input("")

                if tablebase.probe_wdl(temp_board) >= tablebase.probe_wdl(board):
                    movestack.append([temp_move, 100000])
    except KeyError:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Just an example",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-matesd", "--mate-scan-depth", help="how far should the model go in checkmate checking?")
    parser.add_argument("-materialsd", "--material-scan-depth",
                        help="how far should the model go in material gain/loss checking?")
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

    running = True
    while running:
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

        x3 = tablebase_scan(board, allmoves)
        if x3 is not None:
            allmoves = allmoves + x3

        x4 = move_eval_thing(board, allmoves)
        if x4 is not None:
            allmoves = allmoves + x4

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
            with open('data.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([board.outcome().termination, board.fen()])

            running = False
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
