# from phi.assistant import Assistant
# from phi.llm.ollama import Ollama
# from phi.tools.duckduckgo import DuckDuckGo
# import typer


# def tool_call(model: str = "dolphin-mixtral:8x7b-v2.7-q4_K_M", debug: bool = False):
#     print(f"============= Running: {model} =============")
#     Assistant(
#         llm=Ollama(model=model),
#         tools=[DuckDuckGo()],
#         # show_tool_calls=True,
#         # debug_mode=debug,
#     ).cli_app(user=" Ted 👉 ", markdown=True)


# if __name__ == "__main__":
#     typer.run(tool_call)

import typer
from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
from phi.llm.ollama import Ollama


# def tool_call(model: str = "mistral", debug: bool = False):
#     print(f"============= Running: {model} =============")
#     a = Assistant(
#         llm=Ollama(model=model),
#         tools=[DuckDuckGo()],
#         description="You are a news assistant that helps users find the latest news.",
#         instructions=[
#             "Given a topic by the user, respond with 2 latest news items about that topic.",
#             "Search for 5 news items and select the top 2 unique items.",
#         ],
#         show_tool_calls=True,
#         # debug_mode=debug,
#         # ).cli_app(user=" Ted 👉 ")
#     )
#     a.print_response(
#         message="Give me news from 3 different countries.",
#         markdown=True,
#     )

#     # if __name__ == "__main__":


# tool_call()
# typer.run(tool_call)

from typing import List, Optional

from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
from pydantic import BaseModel, Field
from rich.pretty import pprint


class NewsItem(BaseModel):
    position: int = Field(..., description="Rank of this news item.")
    title: Optional[str] = Field(None, description="Title of the news item.")
    url: Optional[str] = Field(None, description="Link to the news item.")
    snippet: Optional[str] = Field(None, description="Snippet of the news item.")
    source: Optional[str] = Field(None, description="Source of the news item.")
    publishedDate: Optional[str] = Field(None, description="Date of the news item.")
    score: Optional[str] = Field(None, description="Score of the news item.")


class NewsItems(BaseModel):
    items: List[NewsItem] = Field(..., description="List of news items.")


# news_assistant = Assistant(
#     llm=Ollama(model="dolphin-mixtral"),
#     tools=[DuckDuckGo()],
#     # show_tool_calls=True,
#     output_model=NewsItems,
#     description="You are a news assistant that helps users find the latest news.",
#     instructions=[
#         "Given a topic by the user, respond with 1 latest news items about that topic.",
#         "Make sure you provide only unique news items.",
#         "Use the `duckduckgo_news` tool to get the latest news about a topic. ",
#     ],
#     # Uncomment the line below to run the assistant in debug mode.
#     # Useful when running the first time to see the tool calls.
#     # debug_mode=True,
# )

# # Note: This will take a while to run as it is fetching the latest news.
# latest_news = news_assistant.run("US Stocks")
# print(latest_news.model_dump())


import json
import httpx

from phi.assistant import Assistant


def get_top_hackernews_stories(num_stories: int = 10) -> str:
    """Use this function to get top stories from Hacker News.

    Args:
        num_stories (int): Number of stories to return. Defaults to 10.

    Returns:
        str: JSON string of top stories.
    """

    # Fetch top story IDs
    response = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    story_ids = response.json()

    # Fetch story details
    stories = []
    for story_id in story_ids[:num_stories]:
        story_response = httpx.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        story = story_response.json()
        if "text" in story:
            story.pop("text", None)
        stories.append(story)
    return json.dumps(stories)


assistant = Assistant(
    llm=Ollama(model="dolphin-mixtral"),
    tools=[get_top_hackernews_stories],
    show_tool_calls=True,
)
assistant.print_response("Summarize the top stories on hackernews?", markdown=True)

# from phi.tools.wikipedia import WikipediaTools

# assistant = Assistant(
#     llm=Ollama(model="dolphin-mixtral"), tools=[WikipediaTools()], show_tool_calls=True
# )
# assistant.print_response("Search wikipedia for 'Artificial Intelligence'")

# from phi.tools.arxiv import ArxivTools

# assistant = Assistant(
#     llm=Ollama(model="dolphin-mixtral"),
#     tools=[ArxivTools()],
#     use_tools=True,
#     show_tool_calls=True,
# )
# assistant.print_response("Search arxiv for 'language models'. Only run 1 search.")
