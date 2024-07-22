import typer

from ted_tools.services.gsuite import blogger, gmail
from ted_tools.services.img_detection import rename_images
from ted_tools.services.transcript import transcript
from ted_tools.services.youtube import yt

ted = typer.Typer()
ted.add_typer(
    yt,
    name="yt",
    help="Subcommands to generate youtube content.",
)
ted.add_typer(transcript, name="transcript", help="Subcommands to transcribe videos.")
ted.add_typer(
    gmail,
    name="gmail",
    help="Subcommands to interact with gmail.",
)
ted.add_typer(blogger, name="blogger", help="Subcommands to interact with blogger.")
ted.add_typer(
    rename_images,
    name="rename_images",
    help="Subcommands to interact with ollama ocr model to rename images better.",
)
