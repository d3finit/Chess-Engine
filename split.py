import chess.pgn
import os

# Function to split a multi-game PGN into individual games with a maximum number of games per file
def split_pgn_into_individual_games(input_pgn_file, output_directory, max_games_per_file=1000000):
    # Create a directory to store individual game PGNs if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    game_counter = 1
    games_in_current_file = 0

    with open(input_pgn_file, 'r') as pgn_file:
        pgn = chess.pgn.read_game(pgn_file)

        while pgn:
            # Create a new PGN for the current game
            output_pgn_file = os.path.join(output_directory, f'lichess_db_standard_rated_2017-0_{game_counter}.pgn')
            with open(output_pgn_file, 'w') as output_file:
                output_file.write(pgn.headers.__str__() + "\n\n")
                output_file.write(pgn.__str__())

            game_counter += 1
            games_in_current_file += 1

            if games_in_current_file >= max_games_per_file:
                games_in_current_file = 0

            pgn = chess.pgn.read_game(pgn_file)

# Input PGN file containing multiple games
input_pgn_file = 'raw_training_data/lichess_db_standard_rated_2017-01.pgn'

# Output directory to store individual game PGNs
output_directory = 'output'

# Call the function to split the PGN with a maximum of 1 million games per file
split_pgn_into_individual_games(input_pgn_file, output_directory, max_games_per_file=10000000)
