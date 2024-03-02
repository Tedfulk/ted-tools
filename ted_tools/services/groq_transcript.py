import ast
import json
from pathlib import Path
from pydantic import ValidationError

import typer
from phi.assistant import Assistant
from rich import print_json

from ted_tools.models import Transcript
from ted_tools.services.api_clients import get_groq_client
from ted_tools.services.llm_tools import TedsFileTool
from ted_tools.utils import (
    clean_dict,
    postprocess_eval_dict,
    preprocess_string_for_eval,
)

gtranscript = typer.Typer()
groq_client = get_groq_client()
transcript_schema = Transcript.model_json_schema()
print("transcript_schema = ", transcript_schema)


@gtranscript.command(help="Generate a transcript for a video given a topic using Groq.")
def gen_transcript(user_input: str):
    gen_transcript = Assistant(
        llm=groq_client,
        system_prompt="Generate a transcript for a video given a topic.",
    )
    groq_response_transcript_str = gen_transcript.run(
        stream=False,
        message=f"Generate a transcript for my topic on {user_input}. Ensure your output matches this transcript JSON schema: {transcript_schema} and use double quotes for all the keys in the schema.",
    )
    print("groq_response_transcript_str = ", groq_response_transcript_str)
    try:
        metadata_dict = json.loads(groq_response_transcript_str)
    except json.decoder.JSONDecodeError:
        print(
            "Failed to parse as JSON, attempting Python literal eval with preprocessing."
        )
        try:
            safe_metadata_str = preprocess_string_for_eval(groq_response_transcript_str)
            temp_dict = ast.literal_eval(safe_metadata_str)
            metadata_dict = postprocess_eval_dict(clean_dict(temp_dict))
            print("metadata_dict 2nd try =  ", metadata_dict)
        except (SyntaxError, ValueError) as e:
            # print(f"Error evaluating string as Python dict: {e}")
            # print("Problematic string:", groq_response_transcript_str)
            metadata_dict = None
    # print("metadata_dict outside =  ", metadata_dict)
    print(type(metadata_dict))
    if metadata_dict:
        if "properties" in metadata_dict:
            metadata_properties = metadata_dict["properties"]["description"]
        else:
            metadata_properties = metadata_dict
        try:
            transcript_meta_instance = Transcript(**metadata_dict)
            ft = TedsFileTool(
                base_dir=Path(
                    f"{Path.home()}/repos/personal/youtube/groq/groq_transcript/"
                ),
                file_name="groq_transcript.txt",
            )
            ft.save_file(contents=transcript_meta_instance.model_dump())
            print_json(transcript_meta_instance.model_dump_json(indent=2))
        except ValidationError as e:
            print("Validation error when creating Transcript instance:", e.json())
    else:
        print("Failed to prepare metadata for Transcript model. Skipping save.")


if __name__ == "__main__":
    gtranscript()
