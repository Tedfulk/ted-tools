import ast
import json
from pathlib import Path

import typer
from phi.assistant import Assistant
from pydantic import ValidationError
from rich import print_json

from ted_tools.models import Hashtags
from ted_tools.services.api_clients import get_groq_client
from ted_tools.services.llm_tools import TedsFileTool
from ted_tools.utils import (
    clean_dict,
    postprocess_eval_dict,
    preprocess_string_for_eval,
)

ghashtags = typer.Typer()
groq_client = get_groq_client()
hashtags_schema = Hashtags.model_json_schema()


@ghashtags.command(help="Generate 10 hashtags for a video given a topic using Groq.")
def gen_hashtags(user_input: str):
    gen_hashtag = Assistant(
        llm=groq_client,
        system_prompt="Generate 10 hashtags for a video given a topic. They should be relevant and popular.",
    )
    groq_response_hashtag_str = gen_hashtag.run(
        stream=False,
        message=f"Generate 10 hashtags for my topic on {user_input}. Ensure your output matches this JSON schema: {hashtags_schema} and use double quotes for all the keys in the schema.",
    )
    print(groq_response_hashtag_str)
    print(type(groq_response_hashtag_str))
    try:
        metadata_dict = json.loads(groq_response_hashtag_str)
    except json.decoder.JSONDecodeError:
        print(
            "Failed to parse as JSON, attempting Python literal eval with preprocessing."
        )
        try:
            safe_metadata_str = preprocess_string_for_eval(groq_response_hashtag_str)
            temp_dict = ast.literal_eval(safe_metadata_str)
            metadata_dict = postprocess_eval_dict(clean_dict(temp_dict))
            print("metadata_dict 2nd try =  ", metadata_dict)
        except (SyntaxError, ValueError) as e:
            print(f"Error evaluating string as Python dict: {e}")
            print("Problematic string:", groq_response_hashtag_str)
            metadata_dict = None
    print("metadata_dict outside =  ", metadata_dict)
    print(type(metadata_dict))
    if metadata_dict:
        try:
            hashtags_meta_instance = Hashtags(**metadata_dict)
            ft = TedsFileTool(
                base_dir=Path(
                    f"{Path.home()}/repos/personal/youtube/groq/groq_hashtags/"
                ),
                file_name="groq_hashtags.txt",
            )
            ft.save_file(contents=hashtags_meta_instance.model_dump())
            print_json(hashtags_meta_instance.model_dump_json(indent=2))
        except ValidationError as e:
            print("Validation error when creating Hashtags instance:", e.json())
    else:
        print("Failed to prepare metadata for Hashtags model. Skipping save.")


if __name__ == "__main__":
    ghashtags()
