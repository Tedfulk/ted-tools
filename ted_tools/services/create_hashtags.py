from api_client import get_openai_client
from ted_tools.models import Hashtags
from ted_tools.utils import write_or_append_with_version

client = get_openai_client()


def create_hashtags(user_input: str):
    """
    Create 10 Hashtags for a given input using "dolphin-mixtral". Then writes the generated Hashtags to a JSON file.

    Args:
        user_input (str)
    """
    resp = client.chat.completions.create(
        model="dolphin-mixtral",
        messages=[
            {
                "role": "user",
                "content": f"Give me ten new hashtags for a video about {user_input}.",
            }
        ],
        response_model=Hashtags,
    )
    temp_hashtag_fn = (
        resp.hashtags[0][1:] + resp.hashtags[1] + resp.hashtags[2]
    ).replace("#", "-")
    write_or_append_with_version(
        filename=temp_hashtag_fn,
        filetype=".json",
        content=resp.model_dump_json(indent=2),
    )
