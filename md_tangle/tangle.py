import re
import json
from io import open

TANGLE_CMD = "tangle:"
TANGLE_REGEX = "tangle:+(.*?})"
BLOCK_REGEX = "~{4}|`{3}"
BLOCK_REGEX_START = "^(~{4}|`{3})"


def __contains_code_block_separators(line):
    line = line.lstrip(' ')
    tangle = re.search(BLOCK_REGEX_START, line)
    starts_with_separator = tangle is not None

    tangle = re.findall(BLOCK_REGEX, line)
    only_one_separator = len(tangle) == 1

    return starts_with_separator and only_one_separator


def __get_tangle_options(line):
    tangle = re.search(TANGLE_REGEX, line)

    if tangle is None:
        return None

    match = tangle.group(0)
    json_string = match.replace(TANGLE_CMD, '')
    return json.loads(json_string)

def __add_to_code_blocks(code_blocks, options, line):
    for location in options["dest"]:
        code_blocks[location] = code_blocks.get(location, "") + line


def map_md_to_code_blocks(filename):
    md_file = open(filename, "r", encoding="utf8")
    lines = md_file.readlines()
    options = None
    code_blocks = {}

    for line in lines:
        if __contains_code_block_separators(line):
            options = __get_tangle_options(line)
        elif options is not None:
            __add_to_code_blocks(code_blocks, options, line)

    md_file.close()
    return code_blocks
