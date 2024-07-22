import base64
import csv
import json
import os
from pathlib import Path

import typer
from phi.assistant import Assistant
from phi.llm.ollama import Ollama

from ted_tools.models import ImageClassification
from ted_tools.utils import convert_webp_to_jpeg, create_file_name
import ollama


ocr = typer.Typer()


@ocr.command(help="Rename images in a directory based on the image content.")
def rename_images(directory_path: str):
    image_schema = {
        "title": "string",
        "description": "string",
        "category": "string",
        "style": "string",
    }
    csv_file_path = os.path.join(directory_path, "image_data.csv")

    if not os.path.exists(directory_path):
        print("Directory not found.")
        return

    if not os.path.exists(csv_file_path):
        with open(csv_file_path, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(
                ["Image Name", "Title", "Description", "Category", "Style"]
            )
        print(f"Created CSV file: {csv_file_path}")

    # Load existing data from CSV to avoid reclassification
    processed_images = set()
    with open(csv_file_path, mode="r", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)
        for row in csvreader:
            if row:
                processed_images.add(row[0])

    for file in os.listdir(directory_path):
        file_path = Path(os.path.join(directory_path, file))
        if file_path.is_file():
            if file.lower().endswith(".webp"):
                if "DALL·E" in file_path:
                    new_file_path = file_path.replace("DALL·E ", "")
                    os.rename(file_path, new_file_path)
                    file_path = new_file_path
                    file = os.path.basename(file_path)
                    print(f"Removed 'DALL·E' from file name: {file_path}")

                jpeg_file_path = convert_webp_to_jpeg(file_path)
                os.remove(file_path)  # Remove WebP file after conversion
                print(f"Converted and removed WebP file: {file_path}")
                file_path = jpeg_file_path
            file_path.suffix.lower() in (".jpg", ".jpeg", ".png")
            if file in processed_images:
                print(f"Skipping {file}, already processed.")
                continue

            img_assistant = Assistant(
                llm=Ollama(model="llava-phi3", format="json"),
                system_prompt=f"You are a master of Image Classification. You are given an image and you must generate a title, description, category, and style for the image.",
            )
            with open(file_path, "rb") as image_file:
                image_bytes = image_file.read()

            try:
                img_assistant_resp = img_assistant.run(
                    message=f"Generate a title, description, category, and style for this image. Follow the schema {image_schema}. Your final output should be in JSON format as a string.",
                    images=[image_bytes],
                    markdown=False,
                    stream=False,
                )
                img_class_dict = json.loads(img_assistant_resp)
                image_classified = ImageClassification(**img_class_dict)

                new_file_name = create_file_name(
                    image_classified.title, file_path.suffix
                )
                if new_file_name:
                    new_file_path = os.path.join(directory_path, new_file_name)
                    os.rename(file_path, new_file_path)
                    print(f"Renamed {file} to {new_file_name}")

                    with open(csv_file_path, "a", newline="") as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(
                            [
                                new_file_name,
                                image_classified.title,
                                image_classified.description,
                                image_classified.category,
                                image_classified.style,
                            ]
                        )
                    print(f"Appended data for {new_file_name} to CSV.")
                else:
                    print(f"Failed to create new file name for {file}")
            except json.JSONDecodeError:
                print(f"Failed to parse JSON response for {file}")
            except Exception as e:
                print(f"Error processing {file}: {str(e)}")


@ocr.command(help="Rename images in a directory based on the image content.")
def rename_images_v2(directory_path: str):
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
    # Remove 'DALL·E' from file names
    for file in os.listdir(directory_path):
        if "DALL·E" in file:
            new_file_name = file.replace("DALL·E ", "")
            os.rename(
                os.path.join(directory_path, file),
                os.path.join(directory_path, new_file_name),
            )
            print(f"Renamed {file} to {new_file_name}")

    # Identify all WebP files in the directory
    webp_files = [
        os.path.join(directory_path, file)
        for file in os.listdir(directory_path)
        if file.lower().endswith(".webp")
    ]
    print(f"Found {len(webp_files)} WebP files: {webp_files}")

    # Convert WebP images to JPEG
    converted_jpg_files = []
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path) and file.lower().endswith(".webp"):
            jpeg_file_path = convert_webp_to_jpeg(file_path)
            converted_jpg_files.append(jpeg_file_path)
    print(f"JPG files: {converted_jpg_files}")

    # Extract file names from converted JPEG paths
    converted_file_names = [path.split("/")[-1] for path in converted_jpg_files]
    print(f"JPG files v2: {converted_file_names}")

    # Process each converted JPEG file
    for file in converted_file_names:
        print(f"Processing {file}")
        file_path = Path(os.path.join(directory_path, file))

        # Skip .DS_Store files
        if file == ".DS_Store":
            print(f"Skipping {file}")
            continue

        print(f"File path: {file_path}")

        # Read image bytes and convert to base64
        image_bytes = file_path.read_bytes()
        base64_string = base64.b64encode(image_bytes).decode("utf-8")
        print(f"Base64 string: {base64_string[:10]}")

        # Use AI model to generate keywords for the image
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
            # Parse AI response and generate new file name
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

            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"Renamed {file} to {new_file_name}")

            # Remove original WebP file
            print(f"Removing {webp_files[0]}")
            os.remove(webp_files[0])
            webp_files.pop(0)
            print(f"WebP files left: {webp_files}")

        except json.JSONDecodeError:
            print(f"Failed to parse JSON response for {file}")
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")


if __name__ == "__main__":
    ocr()
