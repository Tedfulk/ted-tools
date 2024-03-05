import os
from typing import Optional, List
import typer
from dotenv import load_dotenv
from exa_py import Exa
from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from rich.console import Console
from rich.table import Table

from ted_tools.models import QuestionAnswer
from ted_tools.utils import basic_rag_system_prompt
from phi.tools.wikipedia import WikipediaTools
from phi.tools.arxiv import ArxivTools
from datetime import datetime, timedelta

search = typer.Typer()

load_dotenv()
exa = Exa(os.getenv("EXA_API_KEY"))


def display_results(search_response, qa_with_context=None):
    source_table = Table(title="Sources", padding=(1, 2))
    source_table.add_column("Title", justify="left", style="cyan")
    source_table.add_column("Url", justify="center", style="magenta")
    source_table.add_column("Publish Date", justify="center", style="magenta")
    source_table.add_column("Author", justify="center", style="magenta")
    for result in search_response.results:
        source_table.add_row(
            result.title,
            result.url,
            result.published_date,
            result.author,
        )

    source_console = Console()
    source_console.print(source_table)
    print()

    if qa_with_context:
        qa_table = Table(title="Answer with Context", padding=(1, 2))
        qa_table.add_column("Question", justify="center", style="cyan")
        qa_table.add_column("Answer", justify="center", style="magenta")
        qa_table.add_row(qa_with_context.question, qa_with_context.answer)
        console = Console()
        console.print(qa_table)


@search.command()
def exa(
    user_input: str,
    context: Optional[bool] = typer.Option(
        None, "-c", "--context", help="Flag to fetch context and highlights"
    ),
    include_domains: Optional[List[str]] = typer.Option(
        None, "-i", "--include-domains", help="List of domains to include in the search"
    ),
    exclude_domains: Optional[List[str]] = typer.Option(
        None,
        "-e",
        "--exclude-domains",
        help="List of domains to exclude from the search",
    ),
):
    """
    Query the Exa API for a given user_input.
    """
    search_params = {
        "query": user_input,
        "num_results": 5,
        "use_autoprompt": True,
    }
    if "recent" in user_input or "latest" in user_input:
        search_params["start_published_date"] = (
            datetime.now() - timedelta(days=7)
        ).strftime("%Y-%m-%d")

    if include_domains:
        search_params["include_domains"] = include_domains

    if exclude_domains:
        search_params["exclude_domains"] = exclude_domains

    if context:
        highlights_options = {
            "num_sentences": 7,
            "highlights_per_url": 1,
        }
        search_params["highlights"] = highlights_options
        search_response = exa.search_and_contents(**search_params)
        highlight_info = [sr.highlights[0] for sr in search_response.results]
        user_prompt = f"""Sources: {highlight_info}\n\nQuestion: {user_input}"""
        assistant_with_context = Assistant(
            llm=Ollama(model="dolphin-mixtral:8x7b-v2.7"),
            output_model=QuestionAnswer,
            system_prompt=basic_rag_system_prompt,
            user_prompt=user_prompt,
            debug_mode=False,
        )
        qa_with_context = assistant_with_context.run()
        display_results(search_response, qa_with_context)
    else:
        search_response = exa.search(**search_params)
        display_results(search_response)


@search.command()
def wiki(user_input: str):
    """
    Search Wikipedia for a given user_input.
    """
    wiki_assistant = Assistant(
        llm=Ollama(model="dolphin-mixtral:8x7b-v2.7"),
        tools=[WikipediaTools()],
        use_tools=True,
    )
    wiki_assistant.print_response(message=user_input)


@search.command()
def arxiv(user_input: str):
    """
    Search ArXiv for a given query. Only runs 1 search.
    """
    arxiv_assistant = Assistant(
        llm=Ollama(model="dolphin-mixtral:8x7b-v2.7"),
        tools=[ArxivTools()],
        use_tools=True,
    )
    arxiv_assistant.print_response(message=user_input)


if __name__ == "__main__":
    search()
