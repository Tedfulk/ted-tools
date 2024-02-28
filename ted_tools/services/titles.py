import typer

from pathlib import Path
from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from ted_tools.models import Titles
from ted_tools.services.llm_tools import TedsFileTool
from rich import print_json


titles = typer.Typer()


@titles.command(help="Generate 3 titles for a video given a topic.")
def gen_titles(user_input: str):
    gen_title = Assistant(
        llm=Ollama(model="dolphin-mixtral:8x7b-v2.7-q4_K_M"),
        output_model=Titles,
        system_prompt="Generate 3 titles for a video given a topic. It should be short, simple, and SEO worthy. Mr. Beast would be proud to use it. ",
    )
    gt = gen_title.run(stream=True, message=f"{user_input}")
    ft = TedsFileTool(
        base_dir=Path(f"{Path.home()}/repos/personal/youtube/titles/"),
        file_name="titles.txt",
    )
    ft.save_file(contents=gt.titles)
    print_json(gt.model_dump_json(indent=2))


if __name__ == "__main__":
    titles()
