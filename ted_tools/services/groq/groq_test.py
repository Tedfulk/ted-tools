import os

from pathlib import Path

import typer
from phi.assistant import Assistant

from phi.llm.groq import Groq

from rich import print_json

from ted_tools.models import YoutubeMetadata

from ted_tools.services.llm_tools import TedsFileTool
from ted_tools.services.api_clients import get_groq_client
import json

# from dotenv import load_dotenv
# from pydantic import BaseModel
# from typing import List

# load_dotenv()

# groq_client = Groq(
#     model="mixtral-8x7b-32768",
#     api_key=os.getenv("GROQ_API_KEY"),
#     # stream=False,
#     # max_retries=max_retries,
# )

# groq_client = get_groq_client()

# all_metadata = typer.Typer()


# class HealthRecipe(BaseModel):
#     ingredients: List[str]
#     instructions: List[str]


# hr = HealthRecipe.model_json_schema()


# def gen_metadata():
#     gen_metadata = Assistant(
#         llm=groq_client,
#         system_prompt="You are a health coach and you are helping a client with a recipe. Only respond in JSON, No talking.",
#     )
#     gm = gen_metadata.run(
#         stream=False,
#         message=f"Share a quick healthy breakfast recipe. write your output in a json like {hr}",
#     )
#     r = json.loads(gm)
#     health = HealthRecipe(**r["example"])

#     print(health)
#     print()
#     print(health.ingredients)
#     print()
#     print(health.instructions)


# gen_metadata()
groq_client = get_groq_client()
all_metadata = typer.Typer()
yt_model_schema = YoutubeMetadata.model_json_schema()
# print("yt_model_schema = ", yt_model_schema)


def create_new_dict(properties: dict, items: list):
    new_dict = {}
    for item in items:
        if item in properties["properties"]:
            value = properties["properties"][item]["examples"]
            if isinstance(value, list) and (
                item == "description" or item == "transcript"
            ):
                value = "\n".join(value)
            new_dict[item] = value
    return new_dict


@all_metadata.command(help="Generate all metadata for a youtube video.")
def gen_metadata(user_input: str):
    gen_metadata = Assistant(
        llm=groq_client,
        system_prompt="Generate all metadata for a youtube video given a title. Only respond in JSON, No talking.",
        # debug_mode=True,
    )
    gm = gen_metadata.run(
        stream=False,
        message=f"Generate metadata for my topic on {user_input}. Write your output in a JSON schema like this {yt_model_schema}",
    )
    # print("gm = ", gm)
    yt_meta_dict = json.loads(gm)
    temp = create_new_dict(
        yt_meta_dict,
        ["titles", "description", "transcript", "thumbnail_prompts", "hashtags"],
    )
    # print("temp = ", temp)
    # yt_meta_dict = json.loads(gm.replace("'", '"'))
    # print(type(yt_meta_dict))
    # print("yt_meta_dict = ", yt_meta_dict)
    yt_meta = YoutubeMetadata(**temp)
    # print("=======================================")
    # print(yt_meta)
    # print(yt_meta.model_dump_json(indent=2))

    ft = TedsFileTool(
        base_dir=Path(f"{Path.home()}/repos/personal/youtube/all_yt_metadata/"),
        file_name="all_yt_metadata.txt",
    )
    if isinstance(yt_meta, YoutubeMetadata):
        ft.save_file(contents=yt_meta.model_dump())
        print_json(yt_meta.model_dump_json(indent=2))
    # else:
    #     # print(yt_meta)
    #     ft.save_file(contents=yt_meta.model_dump())
    #     print_json(yt_meta.model_dump_json(indent=2))


if __name__ == "__main__":
    all_metadata()
# from pydantic import BaseModel
# from typing import List
# import os
# from dotenv import load_dotenv
# from phi.llm.groq import Groq
# from phi.assistant import Assistant


# load_dotenv()


# class HealthRecipe(BaseModel):
#     ingredients: List[str]
#     instructions: List[str]


# assistant = Assistant(
#     llm=Groq(
#         model="mixtral-8x7b-32768",
#         api_key=os.getenv("GROQ_API_KEY"),
#     ),
#     system_prompt="You help people with their health and fitness goals.",
#     output_model=HealthRecipe,
#     debug_mode=True,
# )
# assistant.print_response("Share a quick healthy breakfast recipe.", markdown=True)
# g = assistant.run(message="Share a quick healthy breakfast recipe.", stream=True)
# print(g)
# print(g.model_dump_json(indent=2))

# print(type(assistant))
# print(assistant.model_dump())
# {
#     "llm": {
#         "model": "mixtral-8x7b-32768",
#         "name": "Groq",
#         "metrics": {},
#         "response_format": None,
#         "tools": None,
#         "tool_choice": None,
#         "run_tools": True,
#         "show_tool_calls": None,
#         "functions": None,
#         "function_call_limit": 20,
#         "function_call_stack": None,
#         "system_prompt": None,
#         "instructions": None,
#     },
#     "introduction": None,
#     "name": None,
#     "assistant_data": None,
#     "run_id": "eddd5ed9-e57d-4f57-b530-d9befa02acce",
#     "run_name": None,
#     "run_data": None,
#     "user_id": None,
#     "user_data": None,
#     "memory": {"chat_history": [], "llm_messages": [], "references": []},
#     "add_chat_history_to_messages": False,
#     "add_chat_history_to_prompt": False,
#     "num_history_messages": 6,
#     "knowledge_base": None,
#     "add_references_to_prompt": False,
#     "storage": None,
#     "db_row": None,
#     "tools": None,
#     "use_tools": False,
#     "show_tool_calls": False,
#     "tool_call_limit": None,
#     "tool_choice": None,
#     "update_knowledge_base": False,
#     "read_tool_call_history": False,
#     "format_messages": True,
#     "system_prompt": None,
#     "system_prompt_function": None,
#     "build_default_system_prompt": True,
#     "description": "You help people with their health and fitness goals.",
#     "instructions": None,
#     "extra_instructions": None,
#     "add_to_system_prompt": None,
#     "add_knowledge_base_instructions": True,
#     "prevent_hallucinations": False,
#     "prevent_prompt_injection": False,
#     "limit_tool_access": False,
#     "add_datetime_to_instructions": False,
#     "markdown": False,
#     "user_prompt": None,
#     "user_prompt_function": None,
#     "build_default_user_prompt": True,
#     "references_function": None,
#     "references_format": "json",
#     "chat_history_function": None,
#     "output_model": "__main__.HealthRecipe",
#     "parse_output": True,
#     "output": None,
#     "tasks": None,
#     "task_data": None,
#     "debug_mode": True,
#     "monitoring": False,
# }


{
    "properties": {
        "titles": {
            "description": "List of 3 titles about the video",
            "examples": [
                "JavaScript and React: A Comprehensive Guide",
                "Mastering React with JavaScript: Best Practices",
                "Building Modern Web Apps with JavaScript and React",
            ],
            "items": {"type": "string"},
            "maxItems": 3,
            "minItems": 3,
            "title": "Titles",
            "type": "array",
        },
        "description": {
            "description": "An SEO driven description for the video that will be used on YouTube. This should be 50 words.",
            "title": "Description",
            "type": "string",
        },
        "transcript": {
            "description": "The transcript for the video that will have an introduction, supporting sections of conversation, and a conclusion.",
            "title": "Transcript",
            "type": "string",
        },
        "thumbnail_prompts": {
            "description": "List of 3 prompts for the thumbnail for this video",
            "examples": [
                "Illustrate JavaScript and React working together in a dynamic web application.",
                "Showcase a modern web app built with JavaScript and React.",
                "Highlight the power of JavaScript and React with a visually appealing thumbnail.",
            ],
            "items": {"type": "string"},
            "maxItems": 3,
            "minItems": 3,
            "title": "Thumbnail Prompts",
            "type": "array",
        },
        "hashtags": {
            "description": "List of 10 hashtags for this video",
            "examples": [
                "#JavaScriptTutorial",
                "#ReactTutorial",
                "#WebDevelopment",
                "#CodingTips",
                "#ProgrammingBlog",
                "#WebAppDevelopment",
                "#FrontEndDevelopment",
                "#CodingCommunity",
                "#TechEducation",
                "#CodingTutorials",
            ],
            "items": {"type": "string"},
            "maxItems": 10,
            "minItems": 10,
            "title": "Hashtags",
            "type": "array",
        },
    },
    "required": [
        "titles",
        "description",
        "transcript",
        "thumbnail_prompts",
        "hashtags",
    ],
    "title": "YoutubeMetadata",
    "type": "object",
}
