import json
import base64
import os
from pathlib import Path
import csv

import typer
from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from rich import print_json

from ted_tools.models import ImageClassification

# from ted_tools.services.llm_tools import TedsFileTool
from ted_tools.utils import convert_webp_to_jpg, create_file_name

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
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            convert_webp_to_jpg(file_path)

    # Find JPG and PNG files not in the CSV and encode them as base64
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path) and (
            file.lower().endswith(".jpg") or file.lower().endswith(".png")
        ):
            if file in processed_images:
                print(f"Skipping {file}, already processed.")
                continue
            elif file not in processed_images:
                file_ext = file.split(".")[-1]
                img_assistant = Assistant(
                    llm=Ollama(model="llava:13b", format="json"),
                    system_prompt=f"You are a master of Image Classification. You are given an image and you must generate a title, description, category, and style for the image.",
                )
                with open(file_path, "rb") as image_file:
                    b64 = base64.b64encode(image_file.read()).decode()

                img_assistant_resp = img_assistant.run(
                    message=f"Generate a title, description, category, and style for this image. Follow the schema {image_schema}. Your final output should be in JSON format as a string.",
                    images=[b64],
                    markdown=False,
                    stream=False,
                )
                img_class_dict = json.loads(img_assistant_resp)
                image_classified = ImageClassification(**img_class_dict)
                new_file_name = create_file_name(image_classified.title, file_ext)

                if new_file_name:
                    os.rename(
                        os.path.join(directory_path, file),
                        os.path.join(directory_path, new_file_name),
                    )
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
                for file in os.listdir(directory_path):
                    file_path = os.path.join(directory_path, file)
                    if os.path.isfile(file_path) and file.lower().endswith(".webp"):
                        os.remove(file_path)


if __name__ == "__main__":
    ocr()
