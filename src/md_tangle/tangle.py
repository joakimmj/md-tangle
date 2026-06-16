import re
from io import open
from pathlib import Path


TANGLE_KEYWORD = "tangle:"
TAGS_KEYWORD = "tags:"
BLOCK_REGEX = "~{4}|`{3}"
BLOCK_REGEX_START = "^(~{4}|`{3})"
COPY_KEYWORD = "TANGLE_CP:"


def __make_absolute(input_path: str, source_file: str) -> str:
    path = Path(input_path).expanduser()
    base_path = Path(source_file).resolve().parent

    if path.drive and not path.is_absolute():
        resolved_path = path.resolve()
    else:
        resolved_path = (base_path / path).resolve()

    return str(resolved_path)


def __contains_code_block_separators(line):
    line = line.lstrip(" ")
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
    options = match.replace(keyword, "").split(separator)

    if isinstance(options, list) and all(isinstance(option, str) for option in options):
        return options

    return []


def __get_tangle_options(line, separator):
    locations = __get_cmd_options(line, TANGLE_KEYWORD, separator)

    if locations is None:
        return None

    tags = __get_cmd_options(line, TAGS_KEYWORD, separator)
    return {"locations": locations, "tags": tags or []}


def __get_copy_source(line, separator):
    copy_source_list = __get_cmd_options(line, COPY_KEYWORD, separator)
    if copy_source_list is None:
        return None
    return copy_source_list[0]


def __add_tangle_item(source_file, sources, options, item_type, value):
    if options is None or not value:
        return

    for location in options.get("locations", []):
        absolute_path = __make_absolute(location, source_file)
        tangle_content = sources.get(absolute_path, [])
        tangle_content.append({
            item_type: value,
            "tags": options.get("tags", [])
        })
        sources[absolute_path] = tangle_content


def get_tangle_sources(filename, separator):
    md_file = open(filename, "r", encoding="utf8")
    lines = md_file.readlines()
    options = None
    sources = {}
    current_block = ""

    for line in lines:
        copy_source = __get_copy_source(line, separator)
        if __contains_code_block_separators(line):
            __add_tangle_item(filename, sources, options, "block", current_block)
            current_block = ""
            options = __get_tangle_options(line, separator)
        elif options is not None:
            current_block = current_block + line
        elif copy_source is not None:
            copy_options = __get_tangle_options(line, separator)
            absolute_src = __make_absolute(copy_source, filename)
            __add_tangle_item(filename, sources, copy_options, "source", absolute_src)

    __add_tangle_item(filename, sources, options, "block", current_block)

    md_file.close()
    return sources
