import typer
from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from rich import print_json
from pathlib import Path

from ted_tools.models import ImageClassification
from ted_tools.services.llm_tools import TedsFileTool

ocr = typer.Typer()


@ocr.command(help="Detect objects in an image.")
def image(file_path: str):

    gen_imageclassification = Assistant(
        llm=Ollama(model="llava:13b"),
        output_model=ImageClassification,
        system_prompt="You are a master of ImageClassification. You are given an image and you must generate a title, description, category, and style for the image.",
        user_prompt="You are given an image and you must generate a title, description, category, and style for the image.",
    )

    gh = gen_imageclassification.run(stream=True, message=f"{file_path}")
    ft = TedsFileTool(
        base_dir=Path(f"{Path.home()}/repos/personal/youtube/ImageClassification/"),
        file_name="ImageClassification.txt",
    )
    ft.save_file(contents=gh.ImageClassification)
    print_json(gh.model_dump_json(indent=2))


if __name__ == "__main__":
    ocr()
