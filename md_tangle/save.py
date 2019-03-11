import os

try:
    get_input = raw_input  # fix for Python 2
except NameError:
    get_input = input

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path  # Python 2 backport


def save_to_file(code_blocks, verbose=False, force=False):
    for key, value in code_blocks.items():
        key = os.path.expanduser(key)
        dir_name = os.path.dirname(key)
        if dir_name is not "":
            Path(dir_name).mkdir(exist_ok=True)

        if os.path.isfile(key) and not force:
            overwrite = get_input("'{0}' already exists. Overwrite? (Y/n) ".format(key))
            if overwrite != "" and overwrite.lower() != "y":
                continue

        with open(key, "w") as f:
            f.write(value)
            f.close()

        if verbose:
            print("{0: <50} {1} lines".format(key, len(value.splitlines())))
