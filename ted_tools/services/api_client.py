from openai import OpenAI
import os
import instructor
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


def get_openai_client(
    max_retries: Optional[int] = 3,
):
    api_key = os.getenv("OLLAMA_API_KEY")
    # if api_key is None:
    #     api_key = OpenAI.api_key or os.getenv("OLLAMA_API_KEY")
    client = instructor.patch(
        OpenAI(
            api_key=api_key,
            base_url="http://127.0.0.1:11434/v1",
            max_retries=max_retries,
        ),
        mode=instructor.Mode.JSON,
    )
    return client
