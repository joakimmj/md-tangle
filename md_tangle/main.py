import argparse
import sys
import md_tangle
from md_tangle.save import save_to_file
from md_tangle.tangle import map_md_to_code_blocks


def __get_args():
    parser = argparse.ArgumentParser(description="Tangle code blocks from Markdown file.")
    parser.add_argument("filename", type=str, help="path to Markdown file", nargs='?')
    parser.add_argument("--version", action='store_true', help="print version")
    parser.add_argument("-v", "--verbose", action='store_true', help="show output")
    parser.add_argument("-f", "--force", action='store_true', help="force overwrite of files")
    parser.add_argument("-s", "--separator", type=str, help="separator for tangle destinations (default=',')",
                        default=",")
    return parser.parse_args()


def main():
    """Main program entry point"""
    args = __get_args()

    if args.version:
        print(md_tangle.__version__)
        sys.exit(0)

    if args.filename is None:
        sys.stderr.write("The 'filename' argument is required.\n")
        sys.exit(1)

    blocks = map_md_to_code_blocks(args.filename, args.separator)
    save_to_file(blocks, args.verbose, args.force)


if __name__ == '__main__':
    main()
