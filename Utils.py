# tuple sorter
def sort_tuple(tup):
    tup.sort(key=lambda x: x[1])
    return tup


# bops the board to be intagers of peive values or something I forgot lol
def convert_to_int(board_to_convert):
    return [
        ['♚♛♜♝♞♟⭘♙♘♗♖♕♔'.index(c) - 6 for c in row.split()]
        for row in board_to_convert.unicode().split('\n')
    ]


# converts the board to ANASI characters
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


# prints a formatted board
def print_board(board_to_convert):
    board_to_convert = convert_to_anasi(convert_to_int(board_to_convert))

    print("  |A|B|C|D|E|F|G|H|")

    for j in range(len(board_to_convert)):
        line = f"|{str(8 - j)}|"
        for h in range(len(board_to_convert[j])):
            line = line + board_to_convert[j][h] + " "

        print(line)
