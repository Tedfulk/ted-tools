from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.python import PythonTools
from phi.tools.file import FileTools
from phi.tools.shell import ShellTools
from phi.tools.arxiv import ArxivTools
from phi.tools.wikipedia import WikipediaTools

# # Assistant with DuckDuckGo tool configuration
# duck_assistant = Assistant(tools=[DuckDuckGo()], show_tool_calls=True)
# # duck_assistant.print_response(
# #     "Whats happening in London? Summarize top stories with sources."
# # )

# # Assistant with PythonTools tool configuration
# assistant = Assistant(tools=[PythonTools()], show_tool_calls=True)
# assistant.print_response(
#     "Write a python script for fibonacci series and display the result till the 10th number"
# )

# # Assistant with FileTools tool configuration
# assistant = Assistant(tools=[FileTools()], show_tool_calls=True)
# assistant.print_response(
#     "What is the most advanced LLM currently? Save the answer to a file."
# )

# # Assistant with ShellTools tool configuration
# assistant = Assistant(tools=[ShellTools()], show_tool_calls=True)
# assistant.print_response("Show me the contents of the current directory")

# # Assistant with ArxivTools tool configuration
# assistant = Assistant(tools=[ArxivTools()], show_tool_calls=True)
# assistant.print_response("Search arxiv for 'language models'")

# # Assistant with WikipediaTools tool configuration
# assistant = Assistant(tools=[WikipediaTools()], show_tool_calls=True)
# assistant.print_response("Search wikipedia for 'Artificial Intelligence'")


from phi.tools import Toolkit
from pathlib import Path
from typing import Optional, List
from phi.utils.log import logger


class TedsFileTool(Toolkit):

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        file_name: Optional[str] = None,
        save_files: Optional[bool] = True,
        read_files: Optional[bool] = True,
        list_files: Optional[bool] = True,
    ):
        super().__init__(name="teds_file_tools")

        self.base_dir: Path = base_dir or Path.cwd()
        self.file_name = file_name

        if save_files:
            self.register(self.save_file, sanitize_arguments=False)
        if read_files:
            self.register(self.read_file)
        if list_files:
            self.register(self.list_files)

    def save_file(
        self,
        contents: str | List[str] | dict,
        overwrite: Optional[bool] = False,
    ) -> str:
        """Appends the contents to the predefined file and returns the file name if successful. Handles strings, lists of strings, and dictionaries.

        :param contents: The contents to save. Can be a string, a list of strings, or a dictionary.
        :param overwrite: Overwrite the file if it already exists. Defaults to False to append by default.
        :return: The file name if successful, otherwise returns an error message.
        """
        if not self.file_name:
            return "No file name specified."

        try:
            file_path = self.base_dir.joinpath(self.file_name)
            logger.debug(f"Checking and preparing directory and file: {file_path}")
            file_path.parent.mkdir(parents=True, exist_ok=True)

            mode = "w" if overwrite else "a"

            with file_path.open(mode, encoding="utf-8") as file:
                if isinstance(contents, dict):
                    for key, value in contents.items():
                        file.write(f"{key}:\n")  # header
                        if isinstance(value, str):
                            file.write(f"{value}\n\n")
                        elif isinstance(value, list) and all(
                            isinstance(item, str) for item in value
                        ):
                            for item in value:
                                file.write(
                                    f"{item}\n"
                                )  # Write each string in the list followed by a newline
                            file.write(
                                "\n"
                            )  # Add an extra newline for spacing after the list
                elif isinstance(contents, list):
                    for item in contents:
                        file.write(f"{item}\n")
                else:
                    file.write(f"{contents}\n")
                # Add a final newline to the end of the file
                file.write("\n")
            logger.info(f"Content appended to: {file_path}")
            return str(self.file_name)
        except Exception as e:
            logger.error(f"Error appending to file: {e}")
            return f"Error appending to file: {e}"

    def read_file(self, file_name: str) -> str:
        """Reads the contents of the file `file_name` and returns the contents if successful.

        :param file_name: The name of the file to read.
        :return: The contents of the file if successful, otherwise returns an error message.
        """
        try:
            logger.info(f"Reading file: {file_name}")
            file_path = self.base_dir.joinpath(file_name)
            contents = file_path.read_text()
            return str(contents)
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return f"Error reading file: {e}"

    def list_files(self) -> List[str]:
        """Returns a list of files in the base directory

        :return: The contents of the file if successful, otherwise returns an error message.
        """
        try:
            logger.info(f"Reading files in : {self.base_dir}")
            return [str(file_path) for file_path in self.base_dir.iterdir()]
        except Exception as e:
            logger.error(f"Error reading files: {e}")
            return [f"Error reading files: {e}"]
