import argparse
import logging
from cowgirl_ai.load_files.search import Search

logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d", format="%(levelname)s - %(asctime)s - %(message)s")


def search_files(directory, extension):
    """Search a directory for file extensions and add data to 'loaded_files'."""
    stack = Search()
    stack.search(directory, extension)
    return stack.data

def run():
    """
    Set up argparse and run commands
    """

    parser = argparse.ArgumentParser(description="CLI tool for file management.")
    subparsers = parser.add_subparsers(dest="command")

    search_parser = subparsers.add_parser("search-files", help="Search a directory for file extensions")
    search_parser.add_argument("directory", type=str, help="Directory to search")
    search_parser.add_argument("extension", type=str, help="File extension to search for")

    args = parser.parse_args()

    if args.command == "search-files":
        files = search_files(args.directory, args.extension)
        logging.info(f"Files to load: {files}")

if __name__=="__main__":
    run()
