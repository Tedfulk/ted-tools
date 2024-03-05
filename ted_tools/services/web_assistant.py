import json
import os
from typing import List, Optional

import httpx
import typer
from dotenv import load_dotenv
from exa_py import Exa
from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from phi.tools.arxiv import ArxivTools
from phi.tools.wikipedia import WikipediaTools
from pydantic import BaseModel, Field
from rich import print, print_json
from rich.pretty import pprint
from ted_tools.utils import basic_rag_system_prompt
from ted_tools.models import SearchQuery, QuestionAnswer


load_dotenv()

exa = Exa(os.getenv("EXA_API_KEY"))


def gen_search_query(user_input: str):
    search_query_assistant = Assistant(
        # llm=Ollama(model="mistral"),
        llm=Ollama(model="dolphin-mixtral:8x7b-v2.7"),
        output_model=SearchQuery,
        system_prompt="You are a helpful assistant that generates search queries based on user input. Only generate one search query.",
        # debug_mode=True,
    )
    # search_query_assistant.print_response(message=f"{user_input}")
    search_query_response = search_query_assistant.run(message=f"{user_input}")
    # print(search_query_response.model_dump_json(indent=2))
    # Parameters for our Highlights search
    highlights_options = {
        "num_sentences": 7,  # how long our highlights should be
        "highlights_per_url": 1,  # just get the best highlight for each URL
    }

    search_response = exa.search_and_contents(
        search_query_response.search_query,
        highlights=highlights_options,
        num_results=5,
        use_autoprompt=False,
    )
    pprint("search resuts = ", search_response.results)
    info = [sr.highlights[0] for sr in search_response.results]

    user_prompt = f"""Sources: {info}

    Question: {search_query_response.search_query}"""

    with_context_assistant = Assistant(
        # llm=Ollama(model="mistral"),
        llm=Ollama(model="dolphin-mixtral:8x7b-v2.7"),
        output_model=QuestionAnswer,
        system_prompt=basic_rag_system_prompt,
        user_prompt=user_prompt,
        # debug_mode=True,
    )
    pprint(with_context_assistant.run())
    # with_context_response = with_context_assistant.run()
    # print(with_context_response.model_dump_json(indent=2))


# gen_search_query("What's the latest tech news?")
gen_search_query(
    "In an era of increasing digital threats, what multifaceted approaches are organizations adopting to fortify their cyber defenses and safeguard confidential information from potential breaches and cyber attacks?"
)
