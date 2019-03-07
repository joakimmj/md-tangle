# Documentation

This is the documentation, and source code, for `md-tangle`.

## Shebang line
__Python3__
```python tangle:src/py3/md-tangle
#!/usr/bin/env python3
```

__Python2__
```python tangle:src/py2/md-tangle2
#!/usr/bin/env python
```

## Imports
__Python3__
```python tangle:src/py3/md-tangle
import os
import re
import argparse
from typing import Optional, Dict
```

__Python2__
```python tangle:src/py2/md-tangle2
import os
import re
import argparse

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path  # python 2 backport
```

## Regex to fetch the keywords

```python tangle:src/py3/md-tangle
tangle_cmd = "tangle:"
tangle_regex = "tangle:+([^\s]+)"
block_regex = "~{4}|`{3}"
block_regex_start = "^(~{4}|`{3})"
```

Since this script does not support tangling code to multiple files (yet), we need to
add code that is equal in both twice.

```python tangle:src/py2/md-tangle2
tangle_cmd = "tangle:"
tangle_regex = "tangle:+([^\s]+)"
block_regex = "~{4}|`{3}"
block_regex_start = "^(~{4}|`{3})"
```

## Argument parsing

```python tangle:src/py3/md-tangle

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tangle code blocks from Markdown file.")
    parser.add_argument("filename", type=str, help="path to Markdown file")
    parser.add_argument("-v", "--verbose", action='store_true', help="show output")
    parser.add_argument("-f", "--force", action='store_true', help="force overwrite of files")
    return parser.parse_args()
```

```python tangle:src/py2/md-tangle2

def get_args():
    parser = argparse.ArgumentParser(description="Tangle code blocks from Markdown file.")
    parser.add_argument("filename", type=str, help="path to Markdown file")
    parser.add_argument("-v", "--verbose", action='store_true', help="show output")
    parser.add_argument("-f", "--force", action='store_true', help="force overwrite of files")
    return parser.parse_args()
```

## Check if line contains code block separators

```python tangle:src/py3/md-tangle

def contains_code_block_separators(line: str) -> bool:
    line = line.lstrip(' ')
    tangle = re.search(block_regex_start, line)
    starts_with_separator = tangle is not None

    tangle = re.findall(block_regex, line)
    only_one_separator = len(tangle) == 1

    return starts_with_separator and only_one_separator
```

```python tangle:src/py2/md-tangle2

def contains_code_block_separators(line):
    line = line.lstrip(' ')
    tangle = re.search(block_regex_start, line)
    starts_with_separator = tangle is not None

    tangle = re.findall(block_regex, line)
    only_one_separator = len(tangle) == 1

    return starts_with_separator and only_one_separator
```

## Get save location from keyword

```python tangle:src/py3/md-tangle

def get_save_location(line: str) -> Optional[str]:
    tangle = re.search(tangle_regex, line)

    if tangle is None:
        return None

    match = tangle.group(0)
    return match.replace(tangle_cmd, '')
```

```python tangle:src/py2/md-tangle2

def get_save_location(line):
    tangle = re.search(tangle_regex, line)

    if tangle is None:
        return None

    match = tangle.group(0)
    return match.replace(tangle_cmd, '')
```

## Map Markdown to code blocks
```python tangle:src/py3/md-tangle

def map_md_to_code_blocks(filename: str) -> Dict[str, str]:
    md_file = open(filename, "r")
    lines = md_file.readlines()
    extracting_block = False
    current_file = ""
    code_blocks = {}

    for line in lines:
        if contains_code_block_separators(line):
            extracting_block = not extracting_block

            if extracting_block:
                current_file = get_save_location(line)
            elif current_file is not None:
                code_blocks[current_file] += '\n'
        elif extracting_block and current_file is not None:
            code_blocks[current_file] = code_blocks.get(current_file, "") + line

    md_file.close()
    return code_blocks
```

```python tangle:src/py2/md-tangle2

def map_md_to_code_blocks(filename):
    md_file = open(filename, "r")
    lines = md_file.readlines()
    extracting_block = False
    current_file = ""
    code_blocks = {}

    for line in lines:
        if contains_code_block_separators(line):
            extracting_block = not extracting_block

            if extracting_block:
                current_file = get_save_location(line)
            elif current_file is not None:
                code_blocks[current_file] += '\n'
        elif extracting_block and current_file is not None:
            code_blocks[current_file] = code_blocks.get(current_file, "") + line

    md_file.close()
    return code_blocks
```

## Save to file
```python tangle:src/py3/md-tangle

def save_to_file(code_blocks: Dict[str, str], verbose: bool = False, force: bool = False):
    for key, value in code_blocks.items():
        key = os.path.expanduser(key)
        dir_name = os.path.dirname(key)
        if dir_name is not "":
            os.makedirs(dir_name, exist_ok=True)

        if os.path.isfile(key) and not force:
            overwrite = input(f"'{key}' already exists. Overwrite? (Y/n) ")
            if overwrite != "" and overwrite.lower() != "y":
                continue

        with open(key, "w") as f:
            f.write(value)
            f.close()

        if verbose:
            print(f"{key:50} {len(value.splitlines())} lines")
```

```python tangle:src/py2/md-tangle2

def save_to_file(code_blocks, verbose=False, force=False):
    for key, value in code_blocks.items():
        key = os.path.expanduser(key)
        dir_name = os.path.dirname(key)
        if dir_name is not "":
            Path(dir_name).mkdir(exist_ok=True)

        if os.path.isfile(key) and not force:
            overwrite = raw_input("'{0}' already exists. Overwrite? (Y/n) ".format(key))
            if overwrite != "" and overwrite.lower() != "y":
                continue

        with open(key, "w") as f:
            f.write(value)
            f.close()

        if verbose:
            print("{0: <50} {1} lines".format(key, len(value.splitlines())))
```


## Script start
```python tangle:src/py3/md-tangle

if __name__ == "__main__":
    args = get_args()
    blocks = map_md_to_code_blocks(args.filename)
    save_to_file(blocks, args.verbose, args.force)
```

```python tangle:src/py2/md-tangle2

if __name__ == "__main__":
    args = get_args()
    blocks = map_md_to_code_blocks(args.filename)
    save_to_file(blocks, args.verbose, args.force)
```
