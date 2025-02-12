import os
from io import open

try:
    get_input = raw_input  # fix for Python 2
except NameError:
    get_input = input

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path  # Python 2 backport


def __create_dir(path):
    dir_name = os.path.dirname(path)

    if dir_name != "":
        Path(dir_name).mkdir(exist_ok=True)

def override_output_dest(code_blocks, output_dest):
    blocks = {}
    common_root = os.path.commonpath(blocks.keys())

    for path in code_blocks.keys():
        new_path = path.replace(common_root, output_dest)
        blocks[new_path] = code_blocks[path]

    return blocks

def save_to_file(code_blocks, verbose=False, force=False):
    for path, value in code_blocks.items():
        path = os.path.expanduser(path)

        __create_dir(path)

        if os.path.isfile(path) and not force:
            overwrite = get_input("'{0}' already exists. Overwrite? (Y/n) ".format(path))
            if overwrite != "" and overwrite.lower() != "y":
                continue

        with open(path, "w", encoding="utf8") as f:
            f.write(value)
            f.close()

        if verbose:
            print("{0: <50} {1} lines".format(path, len(value.splitlines())))
