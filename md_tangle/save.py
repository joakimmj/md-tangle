import os
from io import open

try:
    get_input = raw_input  # fix for Python 2
except NameError:
    get_input = input


def __create_dir(path):
    dir_name = os.path.dirname(path)

    if dir_name != "":
        os.makedirs(dir_name, exist_ok=True)

def override_output_dest(code_blocks, output_dest):
    blocks = {}
    common = os.path.commonpath(code_blocks.keys())

    for path in code_blocks.keys():
        filename = os.path.basename(path)
        dir = os.path.dirname(path)

        if common == "" or common == path:
            new_dir = output_dest
        else:
            new_dir = dir.replace(common, output_dest)

        blocks[new_dir + "/" + filename] = code_blocks[path]

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
