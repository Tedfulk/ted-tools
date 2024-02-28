import typer

from pathlib import Path
from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from ted_tools.models import Transcript
from ted_tools.services.llm_tools import TedsFileTool
from rich import print_json

transcript = typer.Typer()


@transcript.command(help="Generate 3 transcripts for a video given a topic.")
def gen_transcripts(user_input: str):

    gen_transcripts = Assistant(
        llm=Ollama(model="dolphin-mixtral:8x7b-v2.7-q4_K_M"),
        output_model=Transcript,
        system_prompt="Generate a transcript for a video given a topic.",
    )
    gt = gen_transcripts.run(stream=True, message=f"{user_input}")
    ft = TedsFileTool(
        base_dir=Path(f"{Path.home()}/repos/personal/youtube/transcripts/"),
        file_name="transcripts.txt",
    )
    ft.save_file(contents=gt.transcript)
    print_json(gt.model_dump_json(indent=2))


if __name__ == "__main__":
    transcript()
