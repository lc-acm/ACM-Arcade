"""This script helps build all the pico8 games into p8.png files, so they can be easily played inside pico8"""
import os
from pathlib import Path

PICO8_EXECUTABLE = os.getenv("PICO8")

def build_game(path: Path):
    os.system(f"{PICO8_EXECUTABLE} {path} -export carts/{path.stem}.p8.png")

if __name__ == '__main__':
    build_game(Path("./source/picosweeper-carsonr/picosweeper.p8"))