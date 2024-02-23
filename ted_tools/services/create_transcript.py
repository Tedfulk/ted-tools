from ted_tools.utils import (
    write_or_append_with_version,
    get_first_5_to_10_words_from_text,
)
import asyncio
from ollama import AsyncClient

# schema = {
#     "script": "string",
# }


# async def create_transcript(user_input: str):
#     """
#     Creates a text transcript based on a given user input and writes it to a text file.

#     Args:
#         user_input (str)
#     """
#     message = {
#         "role": "user",
#         "content": f"Generate a 50 word text script about {user_input}, Output format is JSON and the schema looks like {schema}",
#     }
#     response = await AsyncClient().chat(
#         model="dolphin-mixtral", messages=[message], format="json"
#     )
# for resp in response:
# print(response["message"]["content"])
# write_or_append_with_version(
#     filename=get_first_5_to_10_words_from_text(response["message"]["content"]),
#     filetype=".txt",
#     content=response["message"]["content"],
# )


# content = "Five surprising names for a pet pelican."

# asyncio.run(create_transcript(user_input=content))
from api_client import get_openai_client
from ted_tools.models import Transcript

from ted_tools.utils import write_or_append_with_version

client = get_openai_client()

user_input = "Five surprising names for a pet pelican."


def create_transcript(user_input: str):
    """
    Create a new Transcript for a video based on a user input and write it to a text file.

    Args:
        user_input (str)
    """
    resp = client.chat.completions.create(
        model="dolphin-mixtral",
        messages=[
            {
                "role": "user",
                "content": f"Generate a text script about {user_input}",
            }
        ],
        response_model=Transcript,
    )

    write_or_append_with_version(
        filename=get_first_5_to_10_words_from_text(resp.title),
        filetype=".txt",
        content=resp.transcript,
    )
