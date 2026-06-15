import os


def __valid_tags(tags_to_include, tags):
    if not tags:
        return True

    if any(tag in tags for tag in tags_to_include):
        return True

    return False


def __transform_tangle_source(tangle_source, tags_to_include, block_padding):
    blocks_to_show = []
    files_to_copy = []

    for source in tangle_source:
        if not __valid_tags(tags_to_include, source.get("tags", [])):
            continue

        code_block = source.get("block")
        if code_block is not None:
            blocks_to_show.append(code_block)

        file_to_copy = source.get("source")
        if file_to_copy is not None:
            files_to_copy.append(file_to_copy)

    if blocks_to_show and files_to_copy:
        print("warning: both tangling and copying to same file. Defaults to tangle")

    if blocks_to_show:
        block_separator = "\n" * block_padding
        return {"code_block": block_separator.join(blocks_to_show)}

    if files_to_copy:
        if len(files_to_copy) > 1:
            print("multiple files copied to same dest. only copy first")

        return {"source_file": files_to_copy[0]}

    return None


def transform_file_data(tangle_sources, tags_to_include, block_padding=0):
    file_data = {}

    for path, tangle_source in tangle_sources.items():
        file_data[path] = __transform_tangle_source(
            tangle_source,
            tags_to_include,
            block_padding
        )

    return file_data


def override_output_dest(file_data, output_dest):
    blocks = {}
    common = os.path.commonpath(file_data.keys())

    for path in file_data.keys():
        filename = os.path.basename(path)
        dir = os.path.dirname(path)

        if common == "" or common == path:
            new_dir = output_dest
        else:
            new_dir = dir.replace(common, output_dest)

        blocks[new_dir + "/" + filename] = file_data[path]

    return blocks
