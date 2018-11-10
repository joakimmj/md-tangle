#!/usr/bin/env python3

import re
import argparse
from typing import Optional, Dict

tangle_cmd = "tangle:"
tangle_regex = "tangle:+([^\s]+)"
block_regex = "~{4}|`{3}"
block_regex_start = "^(~{4}|`{3})"


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tangle code blocks from Markdown file.")
    parser.add_argument("filename", type=str, help="path to Markdown file")
    parser.add_argument("--verbose", action='store_true', help="show output")
    return parser.parse_args()


def contains_code_block_separators(line: str) -> bool:
    line = line.lstrip(' ')
    tangle = re.search(block_regex_start, line)
    starts_with_separator = tangle is not None

    tangle = re.findall(block_regex, line)
    only_one_separator = len(tangle) == 1

    return starts_with_separator and only_one_separator


def get_save_location(line: str) -> Optional[str]:
    tangle = re.search(tangle_regex, line)

    if tangle is None:
        return None

    match = tangle.group(0)
    return match.replace(tangle_cmd, '')


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


def save_to_file(code_blocks: Dict[str, str], verbose: bool):
    for key, value in code_blocks.items():
        if verbose:
            print(f"{key:50} {len(value.splitlines())} lines")
        new_file = open(key, 'w')
        new_file.write(value)
        new_file.close()


if __name__ == "__main__":
    args = get_args()
    blocks = map_md_to_code_blocks(args.filename)
    save_to_file(blocks, args.verbose)
