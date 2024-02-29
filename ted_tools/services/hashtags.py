import typer
from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from rich import print_json
from pathlib import Path

from ted_tools.models import Hashtags
from ted_tools.services.llm_tools import TedsFileTool

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
