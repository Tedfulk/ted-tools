import json
import ast
from pathlib import Path
from pydantic import ValidationError
import typer
from phi.assistant import Assistant
from rich import print_json

from ted_tools.models import YoutubeMetadata
from ted_tools.services.api_clients import get_groq_client
from ted_tools.services.llm_tools import TedsFileTool

# Initialize Typer CLI and Groq client
groq_client = get_groq_client()
all_metadata = typer.Typer()
yt_model_schema = YoutubeMetadata.model_json_schema()

# Unique placeholder for single quotes in strings
UNIQUE_PLACEHOLDER = "__UNIQUE_SINGLE_QUOTE__"


def preprocess_string_for_eval(input_str):
    """
    Temporarily replaces single quotes in strings with a unique placeholder.
    """
    return input_str.replace("'", UNIQUE_PLACEHOLDER)


def postprocess_eval_dict(eval_dict):
    """
    Recursively reverts placeholders back to single quotes in the resulting dictionary.
    """
    if isinstance(eval_dict, dict):
        return {k: postprocess_eval_dict(v) for k, v in eval_dict.items()}
    elif isinstance(eval_dict, list):
        return [postprocess_eval_dict(v) for v in eval_dict]
    elif isinstance(eval_dict, str):
        return eval_dict.replace(UNIQUE_PLACEHOLDER, "'")
    else:
        return eval_dict


def clean_dict(data):
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            # Correctly handle and clean keys by removing backslashes
            cleaned_key = key.replace("\\_", "_")
            if isinstance(value, list):
                new_dict[cleaned_key] = [
                    clean_dict(v) if isinstance(v, (dict, list)) else v for v in value
                ]
            else:
                new_dict[cleaned_key] = (
                    clean_dict(value) if isinstance(value, dict) else value
                )
        return new_dict
    elif isinstance(data, list):
        return [clean_dict(item) for item in data]
    return data


def clean_for_youtube_metadata(data):
    """
    Cleans the data to match the YoutubeMetadata model expectations.
    """
    cleaned_data = {}

    # Fields that should be lists of strings
    list_fields = ["titles", "thumbnail_prompts", "hashtags"]
    # Fields that should be single strings
    string_fields = ["description", "transcript"]

    for key, value in data.items():
        if key in list_fields:
            # Ensure the value is a list of strings
            if isinstance(value, list) and all(isinstance(item, str) for item in value):
                cleaned_data[key] = value
            elif isinstance(value, dict):
                # Example handling if the dictionary has a specific structure you expect
                # This is just a placeholder logic; adjust according to your actual data structure
                cleaned_data[key] = value.get("examples", [])
            else:
                # Fallback or error handling
                cleaned_data[key] = []
        elif key in string_fields:
            # Ensure the value is a string
            if isinstance(value, str):
                cleaned_data[key] = value
            elif isinstance(value, dict):
                # If the dictionary has a 'description' or similar field, use it
                cleaned_data[key] = value.get("examples", "")
            else:
                # Fallback or error handling
                cleaned_data[key] = ""
        else:
            # Handle any other fields as needed
            cleaned_data[key] = value

    return cleaned_data


@all_metadata.command(help="Generate all metadata for a YouTube video.")
def gen_metadata(user_input: str):
    assistant = Assistant(
        llm=groq_client,
        system_prompt="Generate all metadata for a YouTube video given a title. Only respond in JSON, No talking.",
    )
    metadata_str = assistant.run(
        stream=False,
        message=f"Generate metadata for my topic on {user_input}. Ensure your output matches this JSON schema: {yt_model_schema}",
    )
    try:
        metadata_dict = json.loads(metadata_str)
    except json.decoder.JSONDecodeError:
        print(
            "Failed to parse as JSON, attempting Python literal eval with preprocessing."
        )
        try:
            safe_metadata_str = preprocess_string_for_eval(metadata_str)
            temp_dict = ast.literal_eval(safe_metadata_str)
            metadata_dict = postprocess_eval_dict(clean_dict(temp_dict))
        except (SyntaxError, ValueError) as e:
            print(f"Error evaluating string as Python dict: {e}")
            print("Problematic string:", metadata_str)
            metadata_dict = None

    if metadata_dict:
        # Assuming `metadata_dict` is structured with a 'properties' key based on your provided output
        metadata_properties = metadata_dict.get("properties", {})

        # Clean and prepare the dictionary to match the expected model schema
        cleaned_metadata_properties = clean_for_youtube_metadata(metadata_properties)

        # Now, `cleaned_metadata_properties` should have the correct structure and cleaned keys/values
        try:
            yt_meta_instance = YoutubeMetadata(**cleaned_metadata_properties)
            # Proceed with saving the data or any other operations
            ft = TedsFileTool(
                base_dir=Path(f"{Path.home()}/repos/personal/youtube/all_yt_metadata/"),
                file_name="all_yt_metadata.txt",
            )
            ft.save_file(contents=yt_meta_instance.model_dump())
            print_json(yt_meta_instance.model_dump_json(indent=2))
        except ValidationError as e:
            print("Validation error when creating YoutubeMetadata instance:", e.json())
    else:
        print("Failed to prepare metadata for YoutubeMetadata model. Skipping save.")


if __name__ == "__main__":
    all_metadata()
