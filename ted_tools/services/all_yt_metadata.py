import typer
from phi.assistant import Assistant
from ted_tools.models import YoutubeMetadata
from phi.llm.ollama import Ollama
from rich import print_json
from pathlib import Path
from ted_tools.services.llm_tools import TedsFileTool

all_metadata = typer.Typer()


@all_metadata.command(help="Generate all metadata for a youtube video")
def gen_metadata(user_input: str):
    gen_metadata = Assistant(
        llm=Ollama(model="dolphin-mixtral:8x7b-v2.7-q4_K_M"),
        output_model=YoutubeMetadata,
        system_prompt="Generate all metadata for a youtube video given a topic.",
    )

    gm = gen_metadata.run(stream=True, message=f"{user_input}")
    ft = TedsFileTool(
        base_dir=Path(f"{Path.home()}/repos/personal/youtube/all_yt_metadata/"),
        file_name="all_yt_metadata.txt",
    )
    ft.save_file(contents=gm.model_dump())
    print_json(gm.model_dump_json(indent=2))


if __name__ == "__main__":
    all_metadata()
