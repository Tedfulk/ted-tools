from api_client import get_openai_client
from ted_tools.models import Description
from ted_tools.utils import write_or_append_with_version

client = get_openai_client()


def create_description(user_input: str):
    """
    Create a new description for a video based on a user input and write it to a text file.

    Args:
        user_input (str)
    """
    resp = client.chat.completions.create(
        model="dolphin-mixtral",
        messages=[
            {
                "role": "user",
                "content": f"Generate a new description for a video about {user_input}.",
            }
        ],
        response_model=Description,
    )

    write_or_append_with_version(
        filename=resp.title.replace(" ", "-"),
        filetype=".txt",
        content=resp.description,
    )
