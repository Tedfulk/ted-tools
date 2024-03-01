import ast
import json
from pathlib import Path

import typer
from phi.assistant import Assistant
from pydantic import ValidationError
from rich import print_json

from ted_tools.models import Description
from ted_tools.services.api_clients import get_groq_client
from ted_tools.services.llm_tools import TedsFileTool
from ted_tools.utils import (
    clean_dict,
    postprocess_eval_dict,
    preprocess_string_for_eval,
)

gdescription = typer.Typer()
groq_client = get_groq_client()
description_schema = Description.model_json_schema()


@gdescription.command(
    help="Generate a description for a video given a topic using Groq."
)
def gen_description(user_input: str):
    gen_description = Assistant(
        llm=groq_client,
        system_prompt="Generate a description for a video given a topic. It should be engaging, informative, and SEO worthy.",
    )
    groq_response_description_str = gen_description.run(
        stream=False,
        message=f"Generate a description for my topic on {user_input}. Ensure your output matches this JSON schema: {description_schema} and use double quotes for all the keys in the schema.",
    )
    print(groq_response_description_str)
    print(type(groq_response_description_str))
    try:
        metadata_dict = json.loads(groq_response_description_str)
    except json.decoder.JSONDecodeError:
        print(
            "Failed to parse as JSON, attempting Python literal eval with preprocessing."
        )
        try:
            safe_metadata_str = preprocess_string_for_eval(
                groq_response_description_str
            )
            temp_dict = ast.literal_eval(safe_metadata_str)
            metadata_dict = postprocess_eval_dict(clean_dict(temp_dict))
            print("metadata_dict 2nd try =  ", metadata_dict)
        except (SyntaxError, ValueError) as e:
            print(f"Error evaluating string as Python dict: {e}")
            print("Problematic string:", groq_response_description_str)
            metadata_dict = None
    print("metadata_dict outside =  ", metadata_dict)
    print(type(metadata_dict))
    if metadata_dict:
        if "properties" in metadata_dict:
            metadata_properties = metadata_dict["properties"]["description"]
        else:
            metadata_properties = metadata_dict

        try:
            description_meta_instance = Description(**metadata_properties)
            ft = TedsFileTool(
                base_dir=Path(
                    f"{Path.home()}/repos/personal/youtube/groq/groq_description/"
                ),
                file_name="groq_description.txt",
            )
            ft.save_file(contents=description_meta_instance.model_dump())
            print_json(description_meta_instance.model_dump_json(indent=2))
        except ValidationError as e:
            print("Validation error when creating Description instance:", e.json())
    else:
        print("Failed to prepare metadata for Description model. Skipping save.")


if __name__ == "__main__":
    gdescription()
