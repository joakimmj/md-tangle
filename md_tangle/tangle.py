import re

TANGLE_CMD = "tangle:"
TANGLE_REGEX = "tangle:+([^\s]+)"
BLOCK_REGEX = "~{4}|`{3}"
BLOCK_REGEX_START = "^(~{4}|`{3})"


def __contains_code_block_separators(line):
    line = line.lstrip(' ')
    tangle = re.search(BLOCK_REGEX_START, line)
    starts_with_separator = tangle is not None

    tangle = re.findall(BLOCK_REGEX, line)
    only_one_separator = len(tangle) == 1

    return starts_with_separator and only_one_separator


def __get_save_locations(line, separator):
    tangle = re.search(TANGLE_REGEX, line)

    if tangle is None:
        return None

    match = tangle.group(0)
    locations = match.replace(TANGLE_CMD, '')
    return locations.split(separator)


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
