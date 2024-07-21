import argparse
import logging
from cowgirl_ai.load_files.search import Search
from cowgirl_ai.load_files.file_manager import FileManager
# from cowgirl_ai.load_files.vector_manager import VectorManager

logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d", format="%(levelname)s - %(asctime)s - %(message)s")

class CLI:
    """
    CLI 
    ---

    Class for cli related arguments
    """
    def __init__(self):
        self.run()


    def search_files(self, directory, extension):
        """Search a directory for file extensions and add data to 'loaded_files'."""
        stack = Search()
        stack.search(directory, extension)
        return stack.data

    def load_files(self, vector_id, directory, extension):
        """Using the file manager to batch upload loaded files to specific vector."""
        file_manager = FileManager()
        file_manager.batch_upload(vector_id, loaded_files=self.search_files(directory, extension))

    def run(self):
        """
        Set up argparse and run commands
        """

        parser = argparse.ArgumentParser(description="CLI tool for file management.")
        subparsers = parser.add_subparsers(dest="command")

        search_parser = subparsers.add_parser("search-files", help="Search a directory for file extensions")
        search_parser.add_argument("directory", type=str, help="Directory to search")
        search_parser.add_argument("extension", type=str, help="File extension to search for")

        batch_upload_parser = subparsers.add_parser("batch-upload", help="Batch upload loaded files to vector")
        batch_upload_parser.add_argument("vector_id", type=str, help="ID of the vector store you would like to add files to")
        batch_upload_parser.add_argument("directory", type=str, help="Directory to search")
        batch_upload_parser.add_argument("extension", type=str, help="File extension to search for")

        args = parser.parse_args()

        if args.command == "search-files":
            files = self.search_files(args.directory, args.extension)
            logging.info(f"Files to load: {files}")
        elif args.command == "batch-upload":
            self.load_files(args.vector_id, args.directory, args.extension)


if __name__=="__main__":
    CLI()
