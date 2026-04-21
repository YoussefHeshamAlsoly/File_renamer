import os
import re
import sys
from pathlib import Path


def get_dir_number(part, fallback):
    try:
        # Extract leading number from a directory name (e.g. "2. Intro", "2 Intro", "2.Intro" → 2)
        match = re.match(r"^(\d+)", part)
        return int(match.group(1)) if match else fallback
    except (ValueError, IndexError):
        return fallback


def all_dir_file(main_dir_path, file_type=".pdf", levels=2, verbose=False):
    for counter, full_path in enumerate(main_dir_path.rglob(f"*{file_type}"), start=1):
        if verbose:
            print(full_path)

        parts = full_path.parts

        # collect numbers from ancestor directories based on the requested levels. parts[-1] is the file, 
        # parts[-2] is parent, parts[-3] is grandparent, etc
        dir_numbers = []
        for i in range(levels, 0, -1):
            part = parts[-(i + 1)]  # walk up from parent by level
            dir_numbers.append(get_dir_number(part, fallback=counter))

        prefix = ".".join(str(n) for n in dir_numbers)
        new_name = full_path.with_name(f"{prefix}.{full_path.name}")
        full_path.rename(new_name)

    print("Done.")


if __name__ == "__main__":

    # root directory to search for files
    main_dir_path_input = input(f"Path [N=exit, Enter={os.getcwd()}]: ")

    if main_dir_path_input.lower() == "n":
        sys.exit("Exiting...")
    elif main_dir_path_input == "":
        main_dir_path = Path(os.getcwd())
    else:
        main_dir_path = Path(main_dir_path_input)
        if not main_dir_path.exists():
            raise NotADirectoryError("No such directory exists")

    # file extension to target for renaming (e.g. .pdf, .mp4)
    file_type = input("File extension [Enter=.pdf]: ") or ".pdf"
    if not file_type.startswith("."):
        raise ValueError("File extension must start with a dot '.'")

    # number of ancestor directory parent levels to include in the prefix
    levels_input = input("Directory parent levels [Enter=1]: ") or "1"
    if not levels_input.isdigit() or int(levels_input) < 1:
        raise ValueError("Parent levels must be a positive integer")
    levels = int(levels_input)

    verbose = input("Show renamed files? [Y=Yes, Enter=no]: ").lower() == "y"

    all_dir_file(main_dir_path, file_type, levels, verbose)