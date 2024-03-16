from ted_tools.services.all_yt_metadata import all_metadata
from ted_tools.services.description import description
from ted_tools.services.hashtags import hashtags
from ted_tools.services.thumbnails import thumbnails
from ted_tools.services.titles import titles

from ted_tools.services.transcript import transcript
import typer

yt = typer.Typer()
yt.add_typer(
    thumbnails,
    name="thumb",
    help="Subcommands to generate thumbnails for your content.",
)
yt.add_typer(transcript, name="transcript", help="Subcommands to transcribe videos.")
yt.add_typer(
    description,
    name="description",
    help="Subcommands to generate video descriptions.",
)
yt.add_typer(
    titles, name="titles", help="Subcommands to generate a list of 3 video titles."
)
yt.add_typer(hashtags, name="hashtags", help="Subcommands to generate video hashtags.")
yt.add_typer(
    all_metadata, name="all", help="Subcommands to generate all video metadata."
)

if __name__ == "__main__":
    yt()
