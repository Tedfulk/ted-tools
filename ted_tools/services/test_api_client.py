# import asyncio

# from api_client import get_openai_aclient


# async def test_api_client():
#     response = await get_openai_aclient()
#     print(response)


# if __name__ == "__main__":
#     asyncio.run(test_api_client())

from pydantic import BaseModel, Field
from typing import List

from api_client import get_openai_client


class Character(BaseModel):
    name: str
    age: int
    fact: List[str] = Field(..., description="A list of facts about the character")


# enables `response_model` in create call
# client = instructor.patch(
#     OpenAI(
#         base_url="http://localhost:11434/v1",
#         api_key="ollama",  # required, but unused
#     ),
#     mode=instructor.Mode.JSON,
# )

new_client = get_openai_client()

resp = new_client.chat.completions.create(
    model="llama2",
    messages=[
        {
            "role": "user",
            "content": "Tell me about the Harry Potter",
        }
    ],
    response_model=Character,
)
print(resp.model_dump_json(indent=2))
