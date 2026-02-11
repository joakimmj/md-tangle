import argparse
import sys
from importlib import metadata
from md_tangle.save import override_output_dest, save_to_file
from md_tangle.tangle import map_md_to_code_blocks


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

    tags_to_include = args.include.split(",") if args.include else []
    blocks = map_md_to_code_blocks(args.filename, args.separator, tags_to_include)

    if not blocks:
        print("Found no blocks to tangle.")
        return

    if args.destination is not None:
        blocks = override_output_dest(blocks, args.destination)

    save_to_file(blocks, args.verbose, args.force)


if __name__ == "__main__":
    main()
