import os


def __should_include_block(tags_to_include, tags):
    if not tags:
        return True

    if any(tag in tags for tag in tags_to_include):
        return True

    return False


def transform_file_data(tangle_sources, tags_to_include, block_padding=0):
    file_data = {}

    for path, code_blocks in tangle_sources.items():
        blocks_to_show = []

        for code_block in code_blocks:
            if __should_include_block(tags_to_include, code_block.get("tags", [])):
                blocks_to_show.append(code_block.get("block", ""))

        block_separator = "\n" * block_padding
        file_data[path] = block_separator.join(blocks_to_show)

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
