import re
from io import open

TANGLE_KEYWORD = "tangle:"
TAGS_KEYWORD = "tags:"
BLOCK_REGEX = "~{4}|`{3}"
BLOCK_REGEX_START = "^(~{4}|`{3})"


def __contains_code_block_separators(line):
    line = line.lstrip(' ')
    tangle = re.search(BLOCK_REGEX_START, line)
    starts_with_separator = tangle is not None

    tangle = re.findall(BLOCK_REGEX, line)
    only_one_separator = len(tangle) == 1

    return starts_with_separator and only_one_separator


def __get_cmd_options(line, keyword, separator):
    command = re.search(keyword + "+([^\\s]+)", line)

    if command is None:
        return None

    match = command.group(0)
    options = match.replace(keyword, '').split(separator)

    if isinstance(options, list) and all(isinstance(option, str) for option in options):
        return options

    return []


def __get_tangle_options(line, separator):
    locations = __get_cmd_options(line, TANGLE_KEYWORD, separator)

    if locations is None:
        return None

    tags = __get_cmd_options(line, TAGS_KEYWORD, separator)
    return {
        "locations": locations,
        "tags": tags or []
    }


def __should_include_block(tags_to_include, options):
    tags = options.get("tags")

    if not tags:
        return True

    if any(tag in tags for tag in tags_to_include):
        return True

    return False


def __add_to_code_blocks(code_blocks, options, line):
    for location in options.get("locations"):
        code_blocks[location] = code_blocks.get(location, "") + line


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
