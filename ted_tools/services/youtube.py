from ted_tools.services.all_yt_metadata import all_metadata
from ted_tools.services.description import description
from ted_tools.services.hashtags import hashtags
from ted_tools.services.thumbnails import thumbnails
from ted_tools.services.titles import titles

from ted_tools.services.transcript import transcript
import typer

app = typer.Typer()
app.add_typer(
    thumbnails,
    name="thumb",
    help="Subcommands to generate thumbnails for your content.",
)
app.add_typer(transcript, name="transcript", help="Subcommands to transcribe videos.")
app.add_typer(
    description,
    name="description",
    help="Subcommands to generate video descriptions.",
)
app.add_typer(
    titles, name="titles", help="Subcommands to generate a list of 3 video titles."
)
app.add_typer(hashtags, name="hashtags", help="Subcommands to generate video hashtags.")
app.add_typer(
    all_metadata, name="all", help="Subcommands to generate all video metadata."
)

if __name__ == "__main__":
    app()
