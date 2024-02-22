from api_client import get_openai_client
from ted_tools.models import ThumbnailPrompts
from ted_tools.utils import (
    write_or_append_with_version,
    get_first_5_to_10_words_from_text,
)

client = get_openai_client()


def create_thumbnail_prompts(user_input: str):
    """
    Creates 3 thumbnail prompts based on user input and writes them to a JSON file.

    Args:
        user_input (str)
    """
    resp = client.chat.completions.create(
        model="dolphin-mixtral",
        messages=[
            {
                "role": "user",
                "content": f"Give me three new thumbnail prompts for that would embody {user_input}.",
            }
        ],
        response_model=ThumbnailPrompts,
    )

    write_or_append_with_version(
        filename=get_first_5_to_10_words_from_text(resp.thumbnail_prompts[0]),
        filetype=".json",
        content=resp.model_dump_json(indent=2),
    )
