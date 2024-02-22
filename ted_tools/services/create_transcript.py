from ted_tools.utils import (
    write_or_append_with_version,
    get_first_5_to_10_words_from_text,
)
import asyncio
from ollama import AsyncClient


async def create_transcript(user_input: str):
    """
    Creates a text transcript based on a given user input and writes it to a text file.

    Args:
        user_input (str)
    """
    message = {
        "role": "user",
        "content": f"Generate a text script about {user_input}, no chapter heardings, just a continuous script.",
    }
    response = await AsyncClient().chat(model="dolphin-mixtral", messages=[message])

    write_or_append_with_version(
        filename=get_first_5_to_10_words_from_text(response["message"]["content"]),
        filetype=".txt",
        content=response["message"]["content"],
    )


# asyncio.run(chat(user_input=content))
