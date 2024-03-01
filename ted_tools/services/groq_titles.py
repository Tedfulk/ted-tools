import ast
import json
from pathlib import Path
from pydantic import ValidationError

import typer
from phi.assistant import Assistant
from rich import print_json

from ted_tools.models import Titles
from ted_tools.services.api_clients import get_groq_client
from ted_tools.services.llm_tools import TedsFileTool
from ted_tools.utils import (
    clean_dict,
    postprocess_eval_dict,
    preprocess_string_for_eval,
)

gtitles = typer.Typer()
groq_client = get_groq_client()
titles_schema = Titles.model_json_schema()


@gtitles.command(help="Generate 3 titles for a video given a topic using Groq.")
def gen_titles(user_input: str):
    gen_title = Assistant(
        llm=groq_client,
        system_prompt="Generate 3 titles for a video given a topic. It should be short, simple, and SEO worthy.",
    )
    groq_response_title_str = gen_title.run(
        stream=False,
        message=f"Generate 3 titles for my topic on {user_input}. Ensure your output matches this JSON schema: {titles_schema} and use double qoutes for all the keys in the shecma.",
    )
    print(groq_response_title_str)
    print(type(groq_response_title_str))
    try:
        metadata_dict = json.loads(groq_response_title_str)
    except json.decoder.JSONDecodeError:
        print(
            "Failed to parse as JSON, attempting Python literal eval with preprocessing."
        )
        try:
            safe_metadata_str = preprocess_string_for_eval(groq_response_title_str)
            temp_dict = ast.literal_eval(safe_metadata_str)
            metadata_dict = postprocess_eval_dict(clean_dict(temp_dict))
            print("metadata_dict 2nd try =  ", metadata_dict)
        except (SyntaxError, ValueError) as e:
            print(f"Error evaluating string as Python dict: {e}")
            print("Problematic string:", groq_response_title_str)
            metadata_dict = None
    print("metadata_dict outside =  ", metadata_dict)
    print(type(metadata_dict))
    if metadata_dict:
        try:
            titles_meta_instance = Titles(**metadata_dict)
            ft = TedsFileTool(
                base_dir=Path(
                    f"{Path.home()}/repos/personal/youtube/groq/groq_titles/"
                ),
                file_name="groq_titles.txt",
            )
            ft.save_file(contents=titles_meta_instance.model_dump())
            print_json(titles_meta_instance.model_dump_json(indent=2))
        except ValidationError as e:
            print("Validation error when creating Titles instance:", e.json())
    else:
        print("Failed to prepare metadata for Titles model. Skipping save.")


if __name__ == "__main__":
    gtitles()
