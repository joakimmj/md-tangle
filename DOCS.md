# Documentation
This is the documentation, and source code, for `md-tangle`.

`md-tangle` is the original script, and written in Python 3. Since some still swear to
Python 2, I have also added the source code for `md-tangle2`.

## Shebang line
This is just setting the environment to execute the script with.

__md-tangle__
```python tangle:src/py3/md-tangle
#!/usr/bin/env python3
```

__md-tangle2__
```python tangle:src/py2/md-tangle2
#!/usr/bin/env python
```

## Imports
```python tangle:src/py3/md-tangle,src/py2/md-tangle2
import os
import re
import argparse
```

__md-tangle2__

`os.makedirs` does not support creating paths if already exists in Python 2. So for 
`md-tangle2` we use `Path` from `pathlib2` (Python 2 backport for `pathlib`).

```python tangle:src/py2/md-tangle2
from pathlib2 import Path  # python 2 backport
```

## Regex to fetch the keywords
These are the different Regex's for finding code blocks, and the tangle keyword.

```python tangle:src/py3/md-tangle,src/py2/md-tangle2
TANGLE_CMD = "tangle:"
TANGLE_REGEX = "tangle:+([^\s]+)"
BLOCK_REGEX = "~{4}|`{3}"
BLOCK_REGEX_START = "^(~{4}|`{3})"
```

## Argument parsing
Setup for all arguments

```python tangle:src/py3/md-tangle,src/py2/md-tangle2
def __get_args():
    parser = argparse.ArgumentParser(description="Tangle code blocks from Markdown file.")
    parser.add_argument("filename", type=str, help="path to Markdown file")
    parser.add_argument("-v", "--verbose", action='store_true', help="show output")
    parser.add_argument("-f", "--force", action='store_true', help="force overwrite of files")
    parser.add_argument("-s", "--separator", type=str, help="separator for tangle destinations (default=',')", default=",")
    return parser.parse_args()
```

## Check if line contains code block separators
This function check if the line starts with one of the code block separators, and
it checks that it is only one on that line. So ```this``` is not read as a code block.

```python tangle:src/py3/md-tangle,src/py2/md-tangle2
def __contains_code_block_separators(line):
    line = line.lstrip(' ')
    tangle = re.search(BLOCK_REGEX_START, line)
    starts_with_separator = tangle is not None

    tangle = re.findall(BLOCK_REGEX, line)
    only_one_separator = len(tangle) == 1

    return starts_with_separator and only_one_separator
```

## Get save location from keyword
If the line includes one code block separator, this function will try to extract the tangle keyword.

```python tangle:src/py3/md-tangle,src/py2/md-tangle2
def __get_save_locations(line, separator):
    tangle = re.search(TANGLE_REGEX, line)

    if tangle is None:
        return None

    match = tangle.group(0)
    locations = match.replace(TANGLE_CMD, '')
    return locations.split(separator)
```

## Map Markdown to code blocks
These functions simply add the lines in the code blocks to it's destinations. The format on this
data model is:
```python
code_blocks = {
    "path/filename": "text from code block",
    "path/filename2": "text from code block",
}
```

__implementation__
```python tangle:src/py3/md-tangle,src/py2/md-tangle2
def __add_to_code_blocks(code_blocks, locations, line):
    for location in locations:
        code_blocks[location] = code_blocks.get(location, "") + line

def __map_md_to_code_blocks(filename, separator):
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

## Save to file

### Create save destination
It's a small difference in the creation of the destination for saving, as mentioned above.

__md-tangle__
```python tangle:src/py3/md-tangle
def __create_destination(dir_name):
    os.makedirs(dir_name, exist_ok=True)
```

__md-tangle2__
```python tangle:src/py2/md-tangle2
def __create_destination(dir_name):
    Path(dir_name).mkdir(exist_ok=True)
```

### Overwrite
Prompt user for checking if one should overwrite existing files.

__md-tangle__
```python tangle:src/py3/md-tangle
def __get_input(filename):
    return input(f"'{filename}' already exists. Overwrite? (Y/n) ")
```

__md-tangle2__
```python tangle:src/py2/md-tangle2
def __get_input(filename):
    return raw_input("'{0}' already exists. Overwrite? (Y/n) ".format(filename))
```

### Print result
__md-tangle__
```python tangle:src/py3/md-tangle
def __print_out(key, value):
    print(f"{key:50} {len(value.splitlines())} lines")
```

__md-tangle2__
```python tangle:src/py2/md-tangle2
def __print_out(key, value):
    print("{0: <50} {1} lines".format(key, len(value.splitlines())))
```

### Save function
This function writes the code blocks to it's destinations.

```python tangle:src/py3/md-tangle,src/py2/md-tangle2
def __save_to_file(code_blocks, verbose=False, force=False):
    for key, value in code_blocks.items():
        key = os.path.expanduser(key)
        dir_name = os.path.dirname(key)
        if dir_name is not "":
            __create_destination(dir_name)

        if os.path.isfile(key) and not force:
            overwrite = __get_input(key)
            if overwrite != "" and overwrite.lower() != "y":
                continue

        with open(key, "w") as f:
            f.write(value)
            f.close()

        if verbose:
            __print_out(key, value)
```

## Script start
```python tangle:src/py3/md-tangle,src/py2/md-tangle2
if __name__ == "__main__":
    args = __get_args()
    blocks = __map_md_to_code_blocks(args.filename, args.separator)
    __save_to_file(blocks, args.verbose, args.force)
```
