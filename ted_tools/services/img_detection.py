import base64
import json
import os
from pathlib import Path

import typer

from ted_tools.models import ImageClassification
from ted_tools.utils import convert_webp_to_jpeg
import ollama


ocr = typer.Typer()


def remove_dalle_from_filenames(directory_path: str):
    for file in os.listdir(directory_path):
        if "DALL·E" in file:
            new_file_name = file.replace("DALL·E ", "")
            os.rename(
                os.path.join(directory_path, file),
                os.path.join(directory_path, new_file_name),
            )


def convert_files_to_jpeg_list(directory_path: str, converted_list: list):
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path) and file.lower().endswith(".webp"):
            jpeg_file_path = convert_webp_to_jpeg(file_path)
            converted_list.append(jpeg_file_path)


def process_image(directory_path: str, converted_file_names: list, webp_files: list):
    for file in converted_file_names:
        file_path = Path(os.path.join(directory_path, file))

        if file == ".DS_Store":
            continue

        image_bytes = file_path.read_bytes()
        base64_string = base64.b64encode(image_bytes).decode("utf-8")

        response = ollama.chat(
            model="llava-phi3",
            messages=[
                {
                    "role": "user",
                    "content": f"Describe the image as 4 keywords. Output in JSON format. Use the following schema: {{ keywords: List[str] }}.",
                    "images": [base64_string],
                },
            ],
        )

        try:
            resp = (
                response["message"]["content"]
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )
            keywords_dict = json.loads(resp)
            image_classification = ImageClassification(**keywords_dict)
            new_file_name = image_classification.keywords_to_string()
            new_file_path = (
                os.path.join(directory_path, new_file_name) + file_path.suffix
            )

            os.rename(file_path, new_file_path)

            os.remove(webp_files[0])
            webp_files.pop(0)

        except json.JSONDecodeError:
            print(f"Failed to parse JSON response for {file}")
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")


@ocr.command(help="Rename webp image types in a directory based on the image content.")
def rename_images(directory_path: str):
    """
    Rename images in a directory based on their content using AI-generated keywords.

    This function performs the following steps:
    1. Removes 'DALL·E' from file names if present.
    2. Converts WebP images to JPEG format.
    3. Uses an AI model to generate keywords for each image.
    4. Renames the images based on these keywords.
    5. Removes the original WebP files after conversion.

    Args:
        directory_path (str): The path to the directory containing the images.
    """
    remove_dalle_from_filenames(directory_path)

    webp_files = [
        os.path.join(directory_path, file)
        for file in os.listdir(directory_path)
        if file.lower().endswith(".webp")
    ]

    converted_jpg_files = []
    convert_files_to_jpeg_list(directory_path, converted_jpg_files)

    converted_file_names = [path.split("/")[-1] for path in converted_jpg_files]

    process_image(directory_path, converted_file_names, webp_files)


if __name__ == "__main__":
    ocr()
