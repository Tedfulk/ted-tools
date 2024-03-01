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
from ted_tools.utils import (
    preprocess_string_for_eval,
    clean_dict,
    clean_for_youtube_metadata,
    postprocess_eval_dict,
)


groq_client = get_groq_client()
all_metadata = typer.Typer()
yt_model_schema = YoutubeMetadata.model_json_schema()


@all_metadata.command(help="Generate all metadata for a YouTube video.")
def gen_metadata(user_input: str):
    assistant = Assistant(
        llm=groq_client,
        system_prompt="Generate all metadata for a YouTube video given a title. Only respond in JSON, No talking.",
    )
    metadata_str = assistant.run(
        stream=False,
        message=f"Generate metadata for my topic on {user_input}. Ensure your output matches this JSON schema: {yt_model_schema} and use double qoutes for all the keys in the shecma.",
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
