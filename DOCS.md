# Documentation
This is the documentation, and source code, for `md-tangle`.

## Packaging

Still include an `__init__.py` (empty) to mark the directory as a package.
This is done for clarity, robustness, and compatibility with the Python ecosystem. 

### \_\_init__.py
```python tangle:src/md_tangle/__init__.py
# Marking directory as package
```

### \_\_main__.py
```python tangle:src/md_tangle/__main__.py
from . import main
main.main()
```

## Entry point

__Imports__
```python tangle:src/md_tangle/main.py
from __future__ import annotations

import argparse
import sys
from importlib import metadata
from typing import TYPE_CHECKING

from md_tangle.save import override_output_dest, save_to_file
from md_tangle.tangle import map_md_to_code_blocks

if TYPE_CHECKING:
    from argparse import Namespace
```

### Argument parsing
Setup for all arguments

```python tangle:src/md_tangle/main.py
def __get_args() -> Namespace:
    parser = argparse.ArgumentParser(
        description="Tangle code blocks from Markdown file."
    )
    parser.add_argument("filename", type=str, help="path to Markdown file", nargs="?")
    parser.add_argument("--version", action="store_true", help="print version")
    parser.add_argument("-v", "--verbose", action="store_true", help="show output")
    parser.add_argument(
        "-f", "--force", action="store_true", help="force overwrite of files"
    )
    parser.add_argument(
        "-d", "--destination", type=str, help="overwrite output destination"
    )
    parser.add_argument(
        "-i",
        "--include",
        type=str,
        default="",
        help="include tagged code blocks (separator=',')",
    )
    parser.add_argument(
        "-s",
        "--separator",
        type=str,
        help="separator for tangle destinations/tags (default=',')",
        default=",",
    )
    parser.add_argument(
        "-p",
        "--block-padding",
        type=int,
        default=0,
        metavar="N",
        help="add N newlines between code blocks when writing to file (default: 0)",
    )
    return parser.parse_args()
```

### main.py
```python tangle:src/md_tangle/main.py
def main() -> None:
    """Main program entry point"""
    args = __get_args()

    if args.version:
        print(metadata.version(__package__))
        sys.exit(0)

    if args.filename is None:
        sys.stderr.write("The 'filename' argument is required.\n")
        sys.exit(1)

    tags_to_include: list[str] = args.include.split(",") if args.include else []
    blocks: dict[str, list[str]] = map_md_to_code_blocks(
        args.filename, args.separator, tags_to_include
    )

    if not blocks:
        print("Found no blocks to tangle.")
        return

    if args.destination is not None:
        blocks = override_output_dest(blocks, args.destination)

    save_to_file(blocks, args.verbose, args.force, args.block_padding)


if __name__ == "__main__":
    main()
```

## Tangling

__Imports__
```python tangle:src/md_tangle/tangle.py
from __future__ import annotations

import re
from io import open
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from io import TextIOWrapper
```

### Regex to fetch the keywords
These are the different Regex's for finding code blocks, and the tangle keyword.

```python tangle:src/md_tangle/tangle.py
TANGLE_KEYWORD = "tangle:"
TAGS_KEYWORD = "tags:"
BLOCK_REGEX = "~{4}|`{3}"
BLOCK_REGEX_START = "^(~{4}|`{3})"
```

### Check if line contains code block separators
This function check if the line starts with one of the code block separators, and
it checks that it is only one on that line. So ```this``` is not read as a code block.

```python tangle:src/md_tangle/tangle.py
def __contains_code_block_separators(line: str) -> bool:
    line = line.lstrip(" ")
    tangle_match = re.search(BLOCK_REGEX_START, line)
    starts_with_separator = tangle_match is not None

    tangle_list = re.findall(BLOCK_REGEX, line)
    only_one_separator = len(tangle_list) == 1

    return starts_with_separator and only_one_separator
```

### Get tangle options from keyword
This function will try to extract the tangle options.

Extract options after keyword
```python tangle:src/md_tangle/tangle.py
def __get_cmd_options(line: str, keyword: str, separator: str) -> list[str] | None:
    command = re.search(keyword + "+([^\\s]+)", line)

    if command is None:
        return None

    match = command.group(0)
    options = match.replace(keyword, "").split(separator)

    if isinstance(options, list) and all(isinstance(option, str) for option in options):
        return options

    return []
```

Return options if `tangle` keyword exists
```python tangle:src/md_tangle/tangle.py
def __get_tangle_options(line: str, separator: str) -> dict[str, list[str]] | None:
    locations = __get_cmd_options(line, TANGLE_KEYWORD, separator)

    if locations is None:
        return None

    tags = __get_cmd_options(line, TAGS_KEYWORD, separator)
    return {"locations": locations, "tags": tags or []}
```

### Check if codeblock should be included
If the code block is tagged, at least one of the tags should be included as
with the `-i`/`--include` argument.

```python tangle:src/md_tangle/tangle.py
def __should_include_block(
    tags_to_include: list[str], options: dict[str, list[str]]
) -> bool:
    tags = options.get("tags")

    if not tags:
        return True

    if any(tag in tags for tag in tags_to_include):
        return True

    return False
```

### Map Markdown to code blocks
These functions simply add the lines in the code blocks to it's destinations. The format on this
data model is:
```python
code_blocks = {
    "path/filename": ["text from code block 1", "text from code block 2"],
    "path/filename2": ["text from code block"],
}
```

__implementation__
```python tangle:src/md_tangle/tangle.py
def __add_codeblock(
    code_blocks: dict[str, list[str]],
    options: dict[str, list[str]] | None,
    current_block: str,
) -> None:
    if options is None or not current_block:
        return

    for location in options.get("locations", []):
        location_blocks = code_blocks.get(location, [])
        location_blocks.append(current_block)
        code_blocks[location] = location_blocks
```

Add code blocks if has `tangle` location and include tags provided when running
the `md-tangle` command.
```python tangle:src/md_tangle/tangle.py
def map_md_to_code_blocks(
    filename: str, separator: str, tags_to_include: list[str]
) -> dict[str, list[str]]:
    md_file: TextIOWrapper = open(filename, "r", encoding="utf8")
    lines: list[str] = md_file.readlines()
    options: dict[str, list[str]] | None = None
    code_blocks: dict[str, list[str]] = {}
    current_block = ""

    for line in lines:
        if __contains_code_block_separators(line):
            __add_codeblock(code_blocks, options, current_block)
            current_block = ""
            options = __get_tangle_options(line, separator)
        elif options is not None and __should_include_block(tags_to_include, options):
            current_block = current_block + line

    __add_codeblock(code_blocks, options, current_block)

    md_file.close()
    return code_blocks
```

## Saving

__Imports__

`os.makedirs` does not support creating paths if they already exists in Python 2. So we need use `Path` from
`pathlib`/`pathlib2` (backport for Python 2).

```python tangle:src/md_tangle/save.py
from __future__ import annotations

import os
from io import open
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from io import TextIOWrapper
```

### Create directory
Creates directory if not existing

```python tangle:src/md_tangle/save.py
def __create_dir(path: str) -> None:
    dir_name = os.path.dirname(path)

    if dir_name != "":
        os.makedirs(dir_name, exist_ok=True)
```

### Override output destination
This function changes save path to be the overridden path.

```python tangle:src/md_tangle/save.py
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
```

### Saving to file
This function writes the code blocks to it's destinations.

```python tangle:src/md_tangle/save.py
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
```
