import typer

from pathlib import Path
from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from ted_tools.models import ThumbnailPrompts
from ted_tools.services.llm_tools import TedsFileTool
from rich import print_json

thumbnails = typer.Typer()


@thumbnails.command(help="Generate 3 thumbnail prompts for a video given a topic.")
def gen_thumbnail_prompts(user_input: str):

    gen_thumbnail_prompts = Assistant(
        llm=Ollama(model="dolphin-mixtral:8x7b-v2.7-q4_K_M"),
        output_model=ThumbnailPrompts,
        system_prompt="Generate 3 thumbnail prompts for a video given a topic.",
    )
    gt = gen_thumbnail_prompts.run(stream=True, message=f"{user_input}")
    ft = TedsFileTool(
        base_dir=Path(f"{Path.home()}/repos/personal/youtube/thumbnail_prompts/"),
        file_name="thumbnail_prompts.txt",
    )
    ft.save_file(contents=gt.thumbnail_prompts)
    print_json(gt.model_dump_json(indent=2))


if __name__ == "__main__":
    thumbnails()
