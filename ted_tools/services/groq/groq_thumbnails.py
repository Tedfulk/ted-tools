import ast
import json
from pathlib import Path
from pydantic import ValidationError

import typer
from phi.assistant import Assistant
from rich import print_json

from ted_tools.models import ThumbnailPrompts
from ted_tools.services.api_clients import get_groq_client
from ted_tools.services.llm_tools import TedsFileTool
from ted_tools.utils import (
    clean_dict,
    postprocess_eval_dict,
)

gthumbnails = typer.Typer()
groq_client = get_groq_client()
thumbnails_schema = ThumbnailPrompts.model_json_schema()


@gthumbnails.command(
    help="Generate 3 thumbnail prompts for a video given a topic using Groq."
)
def gen_thumbnail_prompts(user_input: str):
    gen_thumbnail_prompt = Assistant(
        llm=groq_client,
        system_prompt="Generate 3 thumbnail prompts for a video given a topic. They should be creative and engaging.",
    )
    groq_response_thumbnail_str = gen_thumbnail_prompt.run(
        stream=False,
        message=f'Generate 3 thumbnail prompts for my topic on {user_input}. Ensure your output matches this JSON schema: {thumbnails_schema} and use double quotes for all the keys in the schema. Do not add any backslahes to the keys such as "thumbnail\_prompts" should be "thumbnail_prompts".',
    )
    print(groq_response_thumbnail_str)
    print(type(groq_response_thumbnail_str))
    try:
        metadata_dict = json.loads(groq_response_thumbnail_str)
    except json.decoder.JSONDecodeError:
        print(
            "Failed to parse as JSON, attempting Python literal eval with preprocessing."
        )
        try:
            temp_dict = ast.literal_eval(groq_response_thumbnail_str)
            metadata_dict = postprocess_eval_dict(clean_dict(temp_dict))
            print("metadata_dict 2nd try =  ", metadata_dict)
        except (SyntaxError, ValueError) as e:
            print(f"Error evaluating string as Python dict: {e}")
            print("Problematic string:", groq_response_thumbnail_str)
            metadata_dict = None
    print("metadata_dict outside =  ", metadata_dict)
    print(type(metadata_dict))
    if metadata_dict:
        try:
            thumbnails_meta_instance = ThumbnailPrompts(**metadata_dict)
            ft = TedsFileTool(
                base_dir=Path(
                    f"{Path.home()}/repos/personal/youtube/groq/groq_thumbnail_prompts/"
                ),
                file_name="groq_thumbnail_prompts.txt",
            )
            ft.save_file(contents=thumbnails_meta_instance.model_dump())
            print_json(thumbnails_meta_instance.model_dump_json(indent=2))
        except ValidationError as e:
            print("Validation error when creating ThumbnailPrompts instance:", e.json())
    else:
        print("Failed to prepare metadata for ThumbnailPrompts model. Skipping save.")


if __name__ == "__main__":
    gthumbnails()
