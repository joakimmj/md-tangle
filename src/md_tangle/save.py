import os
from io import open


def __create_dir(path):
    dir_name = os.path.dirname(path)

    if dir_name != "":
        os.makedirs(dir_name, exist_ok=True)


def save_to_file(file_data, verbose=False, force=False):
    for path, file_body in file_data.items():
        path = os.path.expanduser(path)

        __create_dir(path)

        if os.path.isfile(path) and not force:
            overwrite = input(
                "'{0}' already exists. Overwrite? (Y/n) ".format(path)
            )
            if overwrite != "" and overwrite.lower() != "y":
                continue

        with open(path, "w", encoding="utf8") as f:
            f.write(file_body)
            f.close()

        if verbose:
            print("{0: <50} {1} lines".format(path, len(file_body.splitlines())))
