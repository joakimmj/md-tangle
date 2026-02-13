import os
from io import open


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


def save_to_file(file_code_blocks, verbose=False, force=False, block_padding=0):
    for path, code_blocks in file_code_blocks.items():
        path = os.path.expanduser(path)

        block_separator = "\n" * block_padding
        value = block_separator.join(code_blocks)

        __create_dir(path)

        if os.path.isfile(path) and not force:
            overwrite = input(
                "'{0}' already exists. Overwrite? (Y/n) ".format(path)
            )
            if overwrite != "" and overwrite.lower() != "y":
                continue

        with open(path, "w", encoding="utf8") as f:
            f.write(value)
            f.close()

        if verbose:
            print("{0: <50} {1} lines".format(path, len(value.splitlines())))
