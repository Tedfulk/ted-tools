# from api_client import get_openai_client
# from ted_tools.models import Hashtags
# from ted_tools.utils import write_or_append_with_version

# client = get_openai_client()


# def create_hashtags(user_input: str):
#     """
#     Create 10 Hashtags for a given input using "dolphin-mixtral". Then writes the generated Hashtags to a JSON file.

#     Args:
#         user_input (str)
#     """
#     resp = client.chat.completions.create(
#         model="dolphin-mixtral",
#         messages=[
#             {
#                 "role": "user",
#                 "content": f"Give me ten new hashtags for a video about {user_input}.",
#             }
#         ],
#         response_model=Hashtags,
#     )
#     temp_hashtag_fn = (
#         resp.hashtags[0][1:] + resp.hashtags[1] + resp.hashtags[2]
#     ).replace("#", "-")
#     write_or_append_with_version(
#         filename=temp_hashtag_fn,
#         filetype=".json",
#         content=resp.model_dump_json(indent=2),
#     )


import typer

from phi.assistant import Assistant
from pathlib import Path
from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from ted_tools.services.llm_tools import TedsFileTool
from ted_tools.models import Hashtags
from rich import print_json

hashtags = typer.Typer()


@hashtags.command(help="Generate 10 hashtags for a video given a topic.")
def gen_hashtags(user_input: str):

    gen_hashtags = Assistant(
        llm=Ollama(model="dolphin-mixtral:8x7b-v2.7-q4_K_M"),
        output_model=Hashtags,
        system_prompt="Generate 10 hashtags for a video given a topic.",
    )

    gh = gen_hashtags.run(stream=True, message=f"{user_input}")
    ft = TedsFileTool(
        base_dir=Path(f"{Path.home()}/repos/personal/youtube/hashtags/"),
        file_name="hashtags.txt",
    )
    ft.save_file(contents=gh.hashtags)
    print_json(gh.model_dump_json(indent=2))


if __name__ == "__main__":
    hashtags()
