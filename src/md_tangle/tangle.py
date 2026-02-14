from __future__ import annotations

import re
from io import open
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from io import TextIOWrapper


TANGLE_KEYWORD = "tangle:"
TAGS_KEYWORD = "tags:"
BLOCK_REGEX = "~{4}|`{3}"
BLOCK_REGEX_START = "^(~{4}|`{3})"


def __contains_code_block_separators(line: str) -> bool:
    line = line.lstrip(" ")
    tangle_match = re.search(BLOCK_REGEX_START, line)
    starts_with_separator = tangle_match is not None

    tangle_list = re.findall(BLOCK_REGEX, line)
    only_one_separator = len(tangle_list) == 1

    return starts_with_separator and only_one_separator


def __get_cmd_options(line: str, keyword: str, separator: str) -> list[str] | None:
    command = re.search(keyword + "+([^\\s]+)", line)

    if command is None:
        return None

    match = command.group(0)
    options = match.replace(keyword, "").split(separator)

    if isinstance(options, list) and all(isinstance(option, str) for option in options):
        return options

    return []


def __get_tangle_options(line: str, separator: str) -> dict[str, list[str]] | None:
    locations = __get_cmd_options(line, TANGLE_KEYWORD, separator)

    if locations is None:
        return None

    tags = __get_cmd_options(line, TAGS_KEYWORD, separator)
    return {"locations": locations, "tags": tags or []}


def __should_include_block(
    tags_to_include: list[str], options: dict[str, list[str]]
) -> bool:
    tags = options.get("tags")

    if not tags:
        return True

    if any(tag in tags for tag in tags_to_include):
        return True

    return False


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
