import argparse
import sys
from importlib import metadata
from md_tangle.data_processor import override_output_dest, transform_file_data
from md_tangle.save import save_to_file
from md_tangle.tangle import get_tangle_sources


def __get_args():
    parser = argparse.ArgumentParser(
        description="Tangle code blocks from Markdown file."
    )
    parser.add_argument("filename", type=str, help="path to Markdown file", nargs="?")
    parser.add_argument("--version", action="store_true", help="print version")
    parser.add_argument("-v", "--verbose", action="store_true", help="show output")
    parser.add_argument(
        "-f", "--force", action="store_true", help="force overwrite of files"
    )
    parser.add_argument(
        "-d", "--destination", type=str, help="overwrite output destination"
    )
    parser.add_argument(
        "-i",
        "--include",
        type=str,
        default="",
        help="include tagged code blocks (separator=',')",
    )
    parser.add_argument(
        "-s",
        "--separator",
        type=str,
        help="separator for tangle destinations/tags (default=',')",
        default=",",
    )
    parser.add_argument(
        "-p",
        "--block-padding",
        type=int,
        default=0,
        metavar="N",
        help="add N newlines between code blocks when writing to file (default: 0)",
    )
    return parser.parse_args()


def main():
    """Main program entry point"""
    args = __get_args()

    if args.version:
        print(metadata.version(__package__))
        sys.exit(0)

    if args.filename is None:
        sys.stderr.write("The 'filename' argument is required.\n")
        sys.exit(1)

    tangle_sources = get_tangle_sources(args.filename, args.separator)

    tags_to_include = args.include.split(",") if args.include else []
    file_data = transform_file_data(tangle_sources, tags_to_include, args.block_padding)

    if not file_data:
        print("Found no blocks to tangle.")
        return

    if args.destination is not None:
        file_data = override_output_dest(file_data, args.destination)

    save_to_file(file_data, args.verbose, args.force)


if __name__ == "__main__":
    main()
