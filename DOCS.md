# Documentation
This is the documentation, and source code, for `md-tangle`.

## Packaging

Still include an `__init__.py` (empty) to mark the directory as a package.
This is done for clarity, robustness, and compatibility with the Python ecosystem. 

### \_\_init__.py
```python tangle:src/md_tangle/__init__.py

```

### \_\_main__.py
```python tangle:src/md_tangle/__main__.py
from . import main
main.main()
```

## Entry point

__Imports__
```python tangle:src/md_tangle/main.py
import argparse
import sys
from importlib import metadata
from md_tangle.save import override_output_dest, save_to_file
from md_tangle.tangle import map_md_to_code_blocks
```

### Argument parsing
Setup for all arguments

```python tangle:src/md_tangle/main.py
def __get_args():
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
    return parser.parse_args()
```

### main.py
```python tangle:src/md_tangle/main.py
def main():
    """Main program entry point"""
    args = __get_args()

    if args.version:
        print(metadata.version(__package__))
        sys.exit(0)

    if args.filename is None:
        sys.stderr.write("The 'filename' argument is required.\n")
        sys.exit(1)

    tags_to_include = args.include.split(",") if args.include else []
    blocks = map_md_to_code_blocks(args.filename, args.separator, tags_to_include)

    if not blocks:
        print("Found no blocks to tangle.")
        return

    if args.destination is not None:
        blocks = override_output_dest(blocks, args.destination)

    save_to_file(blocks, args.verbose, args.force)


if __name__ == "__main__":
    main()
```

## Tangling

__Imports__
```python tangle:src/md_tangle/tangle.py
import re
from io import open
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
def __contains_code_block_separators(line):
    line = line.lstrip(" ")
    tangle = re.search(BLOCK_REGEX_START, line)
    starts_with_separator = tangle is not None

    tangle = re.findall(BLOCK_REGEX, line)
    only_one_separator = len(tangle) == 1

    return starts_with_separator and only_one_separator
```

### Get tangle options from keyword
This function will try to extract the tangle options.

Extract options after keyword
```python tangle:src/md_tangle/tangle.py
def __get_cmd_options(line, keyword, separator):
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
def __get_tangle_options(line, separator):
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
def __should_include_block(tags_to_include, options):
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
    "path/filename": "text from code block",
    "path/filename2": "text from code block",
}
```

__implementation__
```python tangle:src/md_tangle/tangle.py
def __add_to_code_blocks(code_blocks, options, line):
    for location in options.get("locations"):
        code_blocks[location] = code_blocks.get(location, "") + line
```

Add code blocks if has `tangle` location and include tags provided when running
the `md-tangle` command.
```python tangle:src/md_tangle/tangle.py
def map_md_to_code_blocks(filename, separator, tags_to_include):
    md_file = open(filename, "r", encoding="utf8")
    lines = md_file.readlines()
    options = None
    code_blocks = {}

    for line in lines:
        if __contains_code_block_separators(line):
            options = __get_tangle_options(line, separator)
        elif options is not None and __should_include_block(tags_to_include, options):
            __add_to_code_blocks(code_blocks, options, line)

    md_file.close()
    return code_blocks
```

## Saving

__Imports__

`os.makedirs` does not support creating paths if they already exists in Python 2. So we need use `Path` from
`pathlib`/`pathlib2` (backport for Python 2).

```python tangle:src/md_tangle/save.py
import os
from io import open
```

### Create directory
Creates directory if not existing

```python tangle:src/md_tangle/save.py
def __create_dir(path):
    dir_name = os.path.dirname(path)

    if dir_name != "":
        os.makedirs(dir_name, exist_ok=True)
```

### Override output destination
This function changes save path to be the overridden path.

```python tangle:src/md_tangle/save.py
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

```

### Saving to file
This function writes the code blocks to it's destinations.

```python tangle:src/md_tangle/save.py
def save_to_file(code_blocks, verbose=False, force=False):
    for path, value in code_blocks.items():
        path = os.path.expanduser(path)

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

```
