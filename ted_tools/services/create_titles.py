from api_client import get_openai_client
from ted_tools.models import Titles, YoutubeMetadata
from ted_tools.utils import write_or_append_with_version

client = get_openai_client()


def create_titles(user_input: str):
    """
    Creates 3 new titles for a given user input and writes them to a JSON file.

    Args:
        user_input (str)
    """
    resp = client.chat.completions.create(
        model="dolphin-mixtral",
        messages=[
            {
                "role": "user",
                "content": f"Give me three new titles for a {user_input}.",
            }
        ],
        response_model=Titles,
    )

    write_or_append_with_version(
        filename=resp.titles[0].replace(" ", "-"),
        filetype=".json",
        content=resp.model_dump_json(indent=2),
    )
