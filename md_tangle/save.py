import os

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

    if dir_name is not "":
        Path(dir_name).mkdir(exist_ok=True)


def save_to_file(code_blocks, verbose=False, force=False, output_dest=None):
    for path, value in code_blocks.items():
        path = os.path.expanduser(path)

        if output_dest is not None:
            path = output_dest + "/" + os.path.basename(path)

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
