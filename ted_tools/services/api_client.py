from openai import OpenAI
import os
import instructor

from dotenv import load_dotenv

load_dotenv()


def get_openai_client():
    api_key = os.getenv("OLLAMA_API_KEY")
    # if api_key is None:
    #     api_key = OpenAI.api_key or os.getenv("OLLAMA_API_KEY")
    print("api_key == ", api_key)
    client = instructor.patch(
        OpenAI(
            api_key=api_key,
            base_url="http://127.0.0.1:11434/v1",
            max_retries=3,
        ),
        mode=instructor.Mode.JSON,
    )
    return client


# client = instructor.patch(
#     OpenAI(
#         base_url="http://127.0.0.1:11434/v1",
#         api_key="ollama",  # required, but unused
#     ),
#     mode=instructor.Mode.JSON,
# )
