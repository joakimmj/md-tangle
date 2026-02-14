from __future__ import annotations

import os
from io import open
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from io import TextIOWrapper


def __create_dir(path: str) -> None:
    dir_name = os.path.dirname(path)

    if dir_name != "":
        os.makedirs(dir_name, exist_ok=True)


def override_output_dest(
    code_blocks: dict[str, list[str]], output_dest: str
) -> dict[str, list[str]]:
    blocks: dict[str, list[str]] = {}
    common: str = os.path.commonpath(code_blocks.keys())

    for path in code_blocks.keys():
        filename: str = os.path.basename(path)
        dir: str = os.path.dirname(path)

        new_dir: str
        if common == "" or common == path:
            new_dir = output_dest
        else:
            new_dir = dir.replace(common, output_dest)

        blocks[new_dir + "/" + filename] = code_blocks[path]

    return blocks


def save_to_file(
    file_code_blocks: dict[str, list[str]],
    verbose: bool = False,
    force: bool = False,
    block_padding: int = 0,
) -> None:
    for path, code_blocks in file_code_blocks.items():
        path = os.path.expanduser(path)

        block_separator: str = "\n" * block_padding
        value: str = block_separator.join(code_blocks)

        __create_dir(path)

        if os.path.isfile(path) and not force:
            overwrite: str = input(
                "'{0}' already exists. Overwrite? (Y/n) ".format(path)
            )
            if overwrite != "" and overwrite.lower() != "y":
                continue

        f: TextIOWrapper = open(path, "w", encoding="utf8")
        with f:
            f.write(value)

        if verbose:
            print("{0: <50} {1} lines".format(path, len(value.splitlines())))
