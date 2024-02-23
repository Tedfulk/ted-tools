from api_client import get_openai_client
from ted_tools.models import Titles, YoutubeMetadata
from ted_tools.utils import write_or_append_with_version

client = get_openai_client()


def create_youtube_metadata(user_input: str):
    """
    Creates metadata for a YouTube video given a users input and writes them to a JSON file.

    Args:
        user_input (str)
    """
    resp = client.chat.completions.create(
        model="dolphin-mixtral",
        messages=[
            {
                "role": "user",
                "content": f"Generate Titles, Description, Hashtags, Transcript, ThumbnailPrompts for a YouTube video about {user_input}. Output should be in json.",
            }
        ],
        response_model=YoutubeMetadata,
    )

    write_or_append_with_version(
        filename=resp.titles[0].replace(" ", "-"),
        filetype=".json",
        content=resp.model_dump_json(indent=2),
    )
