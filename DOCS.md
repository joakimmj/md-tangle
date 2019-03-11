# Documentation
This is the documentation, and source code, for `md-tangle`.

`md-tangle` is supported by both Python 2 and Python 3.
 
Since some still swear to Python 2, I had to do some adaptations. 

I would prefer to use:
* `Typings` (introduced in Python 3.5)
* `os.makedirs(dir, exist_ok=True)` instead of `Path(dir).mkdir(exist_ok=True)`
* `f"{filename:50} {lines} lines"` instead of `"{0: <50} {1} lines".format(filename, lines)`

## Packaging

### \_\_init__.py
```python tangle:md_tangle/__init__.py
__title__ = 'md-tangle'
__version__ = '1.2.0'
__author__ = 'Joakim Myrvoll Johansen'
__author_email__ = 'joakimmyrvoll@gmail.com'
__license__ = 'MIT'
```

### \_\_main__.py
```python tangle:md_tangle/__main__.py
from . import main
main.main()
```

## Entry point

__Imports__
```python tangle:md_tangle/main.py
import argparse
import sys
import md_tangle
from md_tangle.save import save_to_file
from md_tangle.tangle import map_md_to_code_blocks
```

### Argument parsing
Setup for all arguments

```python tangle:md_tangle/main.py
def __get_args():
    parser = argparse.ArgumentParser(description="Tangle code blocks from Markdown file.")
    parser.add_argument("filename", type=str, help="path to Markdown file", nargs='?')
    parser.add_argument("--version", action='store_true', help="print version")
    parser.add_argument("-v", "--verbose", action='store_true', help="show output")
    parser.add_argument("-f", "--force", action='store_true', help="force overwrite of files")
    parser.add_argument("-s", "--separator", type=str, help="separator for tangle destinations (default=',')", default=",")
    return parser.parse_args()
```

### main.py
```python tangle:md_tangle/main.py
def main():
    """Main program entry point"""
    args = __get_args()

    if args.version:
        print(md_tangle.__version__)
        sys.exit(0)

    if args.filename is None:
        sys.stderr.write("The 'filename' argument is required.\n")
        sys.exit(1)

    blocks = map_md_to_code_blocks(args.filename, args.separator)
    save_to_file(blocks, args.verbose, args.force)


if __name__ == '__main__':
    main()
```

## Tangling

__Imports__
```python tangle:md_tangle/tangle.py
import re
```

### Regex to fetch the keywords
These are the different Regex's for finding code blocks, and the tangle keyword.

```python tangle:md_tangle/tangle.py
TANGLE_CMD = "tangle:"
TANGLE_REGEX = "tangle:+([^\s]+)"
BLOCK_REGEX = "~{4}|`{3}"
BLOCK_REGEX_START = "^(~{4}|`{3})"
```

### Check if line contains code block separators
This function check if the line starts with one of the code block separators, and
it checks that it is only one on that line. So ```this``` is not read as a code block.

```python tangle:md_tangle/tangle.py
def __contains_code_block_separators(line):
    line = line.lstrip(' ')
    tangle = re.search(BLOCK_REGEX_START, line)
    starts_with_separator = tangle is not None

    tangle = re.findall(BLOCK_REGEX, line)
    only_one_separator = len(tangle) == 1

    return starts_with_separator and only_one_separator
```

### Get save location from keyword
If the line includes one code block separator, this function will try to extract the tangle keyword.

```python tangle:md_tangle/tangle.py
def __get_save_locations(line, separator):
    tangle = re.search(TANGLE_REGEX, line)

    if tangle is None:
        return None

    match = tangle.group(0)
    locations = match.replace(TANGLE_CMD, '')
    return locations.split(separator)
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
```python tangle:md_tangle/tangle.py
def __add_to_code_blocks(code_blocks, locations, line):
    for location in locations:
        code_blocks[location] = code_blocks.get(location, "") + line


def map_md_to_code_blocks(filename, separator):
    md_file = open(filename, "r")
    lines = md_file.readlines()
    locations = None
    code_blocks = {}

    for line in lines:
        if __contains_code_block_separators(line):
            locations = __get_save_locations(line, separator)
        elif locations is not None:
            __add_to_code_blocks(code_blocks, locations, line)

    md_file.close()
    return code_blocks
```

## Saving

__Imports__
`os.makedirs` does not support creating paths if already exists in Python 2. So we need use `Path` from
`pathlib2` (Python 2 backport for `pathlib`).

```python tangle:md_tangle/save.py
import os

try:
    get_input = raw_input  # fix for Python 2
except NameError:
    get_input = input

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path  # Python 2 backport
```

### Saving to file
This function writes the code blocks to it's destinations.

```python tangle:md_tangle/save.py
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

```
