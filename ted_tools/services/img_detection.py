import base64
import json
import logging
from pathlib import Path
from typing import List

import ollama
import typer
from tqdm import tqdm

from ted_tools.models import ImageClassification
from ted_tools.utils import convert_webp_to_jpeg

rename_images = typer.Typer()
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


def configure_logging(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    if verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.ERROR)


def _convert_files_to_jpeg(directory_path: Path) -> List[Path]:
    converted_list = []
    for file in directory_path.iterdir():
        if file.is_file() and file.suffix.lower() == ".webp":
            jpeg_file_path = convert_webp_to_jpeg(str(file))
            converted_list.append(Path(jpeg_file_path))
    return converted_list


def _generate_keywords(image_path: Path) -> dict:
    with image_path.open("rb") as img_file:
        base64_string = base64.b64encode(img_file.read()).decode("utf-8")

    response = ollama.chat(
        model="llava-phi3",
        messages=[
            {
                "role": "user",
                "content": "Describe the image as 4 keywords. Output in JSON format. Use the following schema: { keywords: List[str] }.",
                "images": [base64_string],
            },
        ],
    )
    return response


def _process_image(
    directory_path: Path, converted_files: List[Path], webp_files: List[Path]
) -> None:
    for file in tqdm(converted_files, desc="Processing images", unit="image"):
        if file.name == ".DS_Store":
            continue

        try:
            response = _generate_keywords(file)
            resp = (
                response["message"]["content"]
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )
            keywords_dict = json.loads(resp)
            image_classification = ImageClassification(**keywords_dict)
            new_file_name = image_classification.keywords_to_string()
            new_file_path = directory_path / f"{new_file_name}{file.suffix}"

            file.rename(new_file_path)
            logger.info(f"Renamed {file.name} to {new_file_path.name}")

            # Find the corresponding WebP file
            webp_file = next((w for w in webp_files if w.stem == file.stem), None)
            if webp_file:
                webp_file.unlink()
                webp_files.remove(webp_file)
                logger.info(f"Removed original WebP file: {webp_file}")
            else:
                logger.warning(f"No corresponding WebP file found for {file.name}")

        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON response for {file}")
        except Exception as e:
            logger.error(f"Error processing {file}: {str(e)}")

    # Check if there are any remaining WebP files
    for remaining_webp in webp_files:
        logger.warning(f"Unprocessed WebP file: {remaining_webp}")


@rename_images.command(help="Rename image files in a directory based on their content.")
def process_dir(
    directory_path: str,
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
) -> None:
    """
    Rename images in a directory based on their content using AI-generated keywords.

    Args:
        directory_path (str): The path to the directory containing the images.
    """
    dir_path = Path(directory_path)
    configure_logging(verbose)

    webp_files = list(dir_path.glob("*.webp"))
    logger.info(f"Found {len(webp_files)} WebP files")

    converted_jpg_files = _convert_files_to_jpeg(dir_path)
    logger.info(f"Converted {len(converted_jpg_files)} files to JPEG")

    if not converted_jpg_files:
        logger.warning("No JPEG files to process. Exiting.")
        return

    _process_image(dir_path, converted_jpg_files, webp_files)
