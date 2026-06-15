import os
import shutil
from io import open


def __create_dir(path):
    dir_name = os.path.dirname(path)

    if dir_name != "":
        os.makedirs(dir_name, exist_ok=True)


def save_to_file(file_data, verbose=False, force=False):
    for path, data in file_data.items():
        if data is None:
            continue

        path = os.path.expanduser(path)

        __create_dir(path)

        if os.path.isfile(path) and not force:
            overwrite = input(
                "'{0}' already exists. Overwrite? (Y/n) ".format(path)
            )
            if overwrite != "" and overwrite.lower() != "y":
                continue

        code_block = data.get("code_block")
        if code_block:
            with open(path, "w", encoding="utf8") as f:
                f.write(code_block)
                f.close()
            if verbose:
                print("{0: <50} {1} lines".format(path, len(code_block.splitlines())))
            continue

        source_file = data.get("source_file")
        if source_file:
            shutil.copy(source_file, path)
            if verbose:
                print(f"Copy {source_file} -> {path}")
            continue

        print(f"no data found: {data}")
