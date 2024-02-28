import typer

from pathlib import Path
from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from ted_tools.models import Description
from ted_tools.services.llm_tools import TedsFileTool
from rich import print_json

description = typer.Typer()


@description.command(help="Generate a description for a video given a topic.")
def gen_description(user_input: str):

    gen_description = Assistant(
        llm=Ollama(model="dolphin-mixtral:8x7b-v2.7-q4_K_M"),
        output_model=Description,
        system_prompt="Generate a description for a video given a topic. It should be more than 100 words and less than 200 words, and should be simple enough that a high school student could understand.",
    )
    gd = gen_description.run(stream=True, message=f"{user_input}")
    ft = TedsFileTool(
        base_dir=Path(f"{Path.home()}/repos/personal/youtube/descriptions/"),
        file_name="descriptions.txt",
    )
    ft.save_file(contents=gd.description)
    print_json(gd.model_dump_json(indent=2))


if __name__ == "__main__":
    description()
