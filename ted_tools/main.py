from ted_tools.services.youtube import yt
from ted_tools.services.gsuite import gmail, blogger

from ted_tools.services.transcript import transcript
from ted_tools.services.img_detection import ocr
import typer

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
    ocr,
    name="ocr",
    help="Subcommands to interact with ollama ocr model to rename images better.",
)

# if __name__ == "__main__":
#     ted()
