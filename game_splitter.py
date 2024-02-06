import os
import re

# Define the output directory and the desired number of games per file
output_dir = "output_directory"  # Change to your desired output directory
games_per_file = 1000  # Adjust as needed

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

current_game = ""
game_count = 0
file_count = 0

with open("lichess_db_standard_rated_2023-08.pgn", "r", encoding="utf-8") as pgn_file:
    for line in pgn_file:
        current_game += line

        if line.startswith("1. "): 
            game_count += 1

            if game_count == games_per_file:
                file_count += 1
                output_file = os.path.join(output_dir, f"smaller_games_{file_count}.pgn")

                with open(output_file, "w", encoding="utf-8") as output:
                    output.write(current_game)

                # Reset variables
                current_game = ""
                game_count = 0

if current_game.strip():
    file_count += 1
    output_file = os.path.join(output_dir, f"smaller_games_{file_count}.pgn")

    with open(output_file, "w", encoding="utf-8") as output:
        output.write(current_game)

print(f"Split into {file_count} smaller PGN files.")