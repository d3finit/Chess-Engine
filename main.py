# /usr/bin/python3
# ------------------------------------
# Created by: def__init__
# GNU GPL v3.0
# ------------------------------------

import os
import time

import chess, chess.engine, chess.pgn, chess.polyglot, chess.svg, chess.gaviota
from rich.progress import track, Progress
from rich.prompt import Prompt
import argparse, csv
from contextlib import contextmanager
import threading
import _thread
import time
import sys
from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Footer, Header, RichLog, Button, Static, Input, Label, Pretty, DataTable
from textual.validation import Function, Number, ValidationResult, Validator
from textual import on
from rich.text import Text
import asyncio

from Console import *
from Utils import sort_tuple, convert_to_int, print_board, get_material  # local lib for stuff


class TimeoutException(Exception):
    def __init__(self, msg=''):
        self.msg = msg


@contextmanager
def time_limit(seconds, msg=''):
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutException("Timed out for operation {}".format(msg))
    finally:
        # if the action ends in specified time, timer is canceled
        timer.cancel()


def is_piece_hang(board, move):
    ori_material = get_material(board)
    board.push(move)
    with_move_material = get_material(board)

    for m1 in board.legal_moves:
        temp_board = board
        temp_board.push(m1)
        tb_material = get_material(temp_board)
        for m2 in temp_board.legal_moves:
            tb2 = temp_board
            tb2.push(m2)
            tb2_material = get_material(tb2)

            if ori_material - with_move_material <= tb2_material:
                return False


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
                    movestack.append([temp_move, get_material(temp_board) * 100])

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
            # print(x)
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


class MyApp(App):
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="j", action="down", description="Scroll down", show=False),
    ]

    CSS_PATH = "horizontal_layout.css"

    def compose(self) -> ComposeResult:
        yield Footer()
        yield Header(show_clock=True, name="App")
        yield Horizontal(
            VerticalScroll(
                Static("Standard Buttons", classes="header"),
                Button("Play"),
                RichLog(id="InputLog"),
                Input(
                    placeholder="Enter a move...",
                    validators=[
                        Move(),
                    ],
                ),
                DataTable()
            )
        )

    def on_key(self, event: events.Key) -> None:
        # self.query_one("#ButtonLog").write(event)
        ROWS = [
            ("A", "B", "C", "D", "E", "F", "G"),
            (" ", " ", " ", " ", " ", " ", " "),
            ("♙", "♙", "♙", "♙", "♙", "♙", "♙"),
        ]
        table = self.query_one(DataTable)
        table.add_columns(*ROWS[0])


        for number, row in enumerate(ROWS[1:], start=1):
            label = Text(str(number), style="#B0FC38 italic")
            table.add_row(*row, label=label)
            table.update_cell_at((0, 0), "")
        pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        global play_btn_press, user_move
        l = event.button.label
        self.query_one("#InputLog").write(str(l))
        play_btn_press = True

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.query_one("#InputLog").write(event.value)


class Move(Validator):
    def validate(self, value: str) -> ValidationResult:
        if self.is_move(value):
            return self.success()
        else:
            return self.failure("That's not a move :/")

    @staticmethod
    def is_move(value: str) -> bool:
        return (len(value) == 4) == True


global play_btn_press, user_move

if __name__ == "__main__":
    global play_btn_press, user_move
    parser = argparse.ArgumentParser(description="Just an example",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-matesd", "--mate-scan-depth", help="how far should the model go in checkmate checking?")
    parser.add_argument("-materialsd", "--material-scan-depth",
                        help="how far should the model go in material gain/loss checking?")
    parser.add_argument("-sf", "--use-stockfish", action="store_true", help="have the engine play stockfish?")
    parser.add_argument("-ui", "--expemental-ui", action="store_true", help="enable expemental ui?")

    args = parser.parse_args()
    config = vars(args)
    print(config)

    MATE_SCAN_DEPTH = int(config["mate_scan_depth"])
    MATERIAL_SCAN_DEPTH = int(config["material_scan_depth"])
    USE_STOCKFISH = bool(config["use_stockfish"])
    EXPERMENTAL_UI_ENABLE = bool(config["expemental_ui"])

    if (EXPERMENTAL_UI_ENABLE):
        app = MyApp()
        asyncio.run(app.run_async())

    computer_moves = 0
    engine = chess.engine.SimpleEngine.popen_uci(r".\stockfish\stockfish-windows-x86-64-avx2.exe")

    pgn = open("CurrentGame.pgn")
    first_game = chess.pgn.read_game(pgn)
    board = first_game.board()
    for move in first_game.mainline_moves():
        board.push(move)

    running = True
    while running:
        print_board(board)

        # get user move
        if USE_STOCKFISH:
            result = engine.play(board, chess.engine.Limit(time=0.1))
            board.push(result.move)

        elif not USE_STOCKFISH:
            player_move = Prompt.ask("Enter your move (UCI format, enter to have Stockfish16 play.)")

            while chess.Move.from_uci(player_move) not in board.legal_moves:
                player_move = Prompt.ask("Enter your move (UCI)")
            first_game.add_variation(chess.Move.from_uci(player_move))
            board.push(chess.Move.from_uci(player_move))

        print_board(board)

        while play_btn_press is not True:
            pass

        play_btn_press = False

        start = time.time()

        # begin the engine
        allmoves = []
        blocked_moves = []
        try:
            with time_limit(5, 'sleep'):
                x1 = new_recurse_checkmate(board, allmoves, MATE_SCAN_DEPTH)
                if x1 is not None:
                    allmoves = allmoves + x1

                x2 = new_recurse_material(board, allmoves, MATERIAL_SCAN_DEPTH, True)
                if x2 is not None:
                    allmoves = allmoves + x2

                x3 = tablebase_scan(board, allmoves)
                if x3 is not None:
                    allmoves = allmoves + x3

                x4 = move_eval_thing(board, allmoves)
                if x4 is not None:
                    allmoves = allmoves + x4
        except TimeoutException:
            print("TIMES UP")

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
            print("Ran out of moves")
            result = engine.analyse(board, chess.engine.Limit(time=1))
            print(result["score"].black())

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
                        print(move.uci())
                        print_board(board)
                        print(move.uci())
                        break
                else:
                    for move2 in reccomended_moves:
                        if not is_piece_hang(board, reccomended_moves[i][0]):
                            move = str(reccomended_moves[0][0])
                            first_game.add_variation(chess.Move.from_uci(str(reccomended_moves[0][0])))
                            board.push(chess.Move.from_uci(str(reccomended_moves[0][0])))
                            print_board(board)
                            print(move)
                            break

        print_board(board)
        # print(move.uci())

        if (len(reccomended_moves) >= 1):
            move = str(reccomended_moves[0][0])
        else:
            move = "NONE"

        print(f"Computer move: {move}")
        end = time.time()
        computer_moves += 1
        print(f"Computer took: " + str(end - start))

        if board.outcome() is not None:
            print(board.outcome().termination)
            print("385: game over.")
            # print(first_game)
            with open('data.csv', 'a', newline='\n') as file:
                writer = csv.writer(file)
                writer.writerow([board.outcome().termination, board.fen()])

            running = False
            try:
                os.system("python3 .\main.py -matesd 1 -materialsd 1 -sf")
            except KeyboardInterrupt:
                sys.exit()
