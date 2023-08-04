import os
from glob import glob

subfolders = [ f.path for f in os.scandir("./test/") if f.is_dir() ]

for folder in subfolders:
    os.rename(("test/" + folder.split("./test/")[1] + "/" + folder.split("./test/")[1] + ".pgn"), ("full_games/" + folder.split("./test/")[1] + ".pgn"))
