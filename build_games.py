"""This script helps build all the pico8 games into p8.png files, so they can be easily played inside pico8"""

import os
import glob
import json
from pathlib import Path

PICO8_EXECUTABLE = os.getenv("PICO8")


def build_game(path: Path):
    os.system(f"{PICO8_EXECUTABLE} {path} -export carts/{path.stem}.p8.png")


def get_p8_file_for_game(game_dir: Path) -> str:
    # First, we check json file for game metadata
    json_info_path = None
    if os.path.exists(f"{game_dir}/info.json"):
        json_info_path = f"{game_dir}/info.json"
    else:
        # Just grab any json file, we are going to check that it has what we want anyways
        try:
            json_info_path = next(glob.iglob(f"{game_dir}/*.json"))
        except StopIteration:
            pass

    if json_info_path:
        try:
            with open(json_info_path, "r", encoding="utf-8") as f:
                info = json.load(f)
            source = info.get("source")
            if source and os.path.exists(f"{game_dir}/{source}"):
                return f"{game_dir}/{source}"
        except Exception:
            pass
        print(
            "JSON file not formatted as expected. Attempting to find source p8 file automatically"
        )

    # If there is no json file, we look for a .p8 file named the same as the directory
    p8_files = set(glob.iglob(f"{game_dir}/*.p8"))
    expected_program = f"{game_dir}/{game_dir.name}.p8"
    if expected_program in p8_files:
        # print("found " + expected_program)
        return expected_program
    else:
        # Finally, we just choose any .p8 file that exists
        if len(p8_files) > 0:
            return p8_files.pop()
        else:
            raise FileNotFoundError(f"No valid p8 files found for {game_dir.name}")
    # if game_dir.name in p8_files:
    # return


def build_all_games():
    for directory in Path("./source").iterdir():
        if not directory.is_dir():
            continue
        try:
            program_path = get_p8_file_for_game(directory)
        except FileNotFoundError as e:
            print(e)
            continue
        build_game(Path(program_path))


# for file in os.listdir('./source')

if __name__ == "__main__":
    # get_p8_file_for_game('./source/picosweeper')
    build_all_games()
    # build_game(Path("./source/picosweeper-carsonr/picosweeper.p8"))
