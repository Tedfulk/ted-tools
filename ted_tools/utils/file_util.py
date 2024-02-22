import os
import random


def get_first_5_to_10_words_from_text(text):
    words = text.split()
    num_words_to_extract = random.randint(5, 10)
    num_words_to_extract = min(num_words_to_extract, len(words))
    first_words = words[:num_words_to_extract]
    return "-".join(first_words)


def write_or_append_with_version(filename: str, filetype: str, content: str):
    """
    Writes content to a file in a directory named after the filename within the user's
    ~/.repos/personal/youtube/ directory. If the file already exists, appends a version
    number to the filename and writes the content to this new file inside the same-named directory.

    Parameters:
    - filename: The name of the file where the content should be written.
    - filetype: The type of the file (e.g., '.txt', '.py').
    - content: The content to write to the file.
    """
    base_directory = os.path.expanduser("~/repos/personal/youtube/")
    base_filename, _ = os.path.splitext(filename)
    # Create a directory named after the base_filename within the base_directory
    directory = os.path.join(base_directory, base_filename)

    if not os.path.exists(directory):
        os.makedirs(directory)

    # The file will be placed inside the directory with the same name as the base_filename
    filepath = os.path.join(directory, f"{base_filename}{filetype}")
    if not os.path.exists(filepath):
        with open(filepath, "w") as file:
            print(f"Writing script to {directory}/{base_filename}{filetype}")
            file.write(content)
    else:
        version = 1
        new_filepath = os.path.join(directory, f"{base_filename}_v{version}{filetype}")
        while os.path.exists(new_filepath):
            version += 1
            new_filepath = os.path.join(
                directory, f"{base_filename}_v{version}{filetype}"
            )

        with open(new_filepath, "w") as file:
            file.write(content)
