from pydantic import BaseModel, Field
from typing import List, Optional


class SearchQuery(BaseModel):
    search_query: str = Field(
        ...,
        description="A restructured search query from the users input to be used to search for relevant information.",
        # description="A restructured search query from the users input to be used to search for relevant information. The search query should be in the form of an answer. Always end with a colon.",
        examples=[
            "Applications of artificial intelligence and machine learning in supply chain management?",
            "Strategies for enhancing cybersecurity in businesses and protecting sensitive data?",
        ],
    )


class QuestionAnswer(BaseModel):
    question: str = Field(
        ...,
        description="A question to be answered based on the provided context.",
        examples=[
            "multifaceted approaches for cyber defense in organizations:",
            "cybersecurity strategies for organizations against potential data breaches and cyber attacks:",
        ],
    )
    answer: str = Field(
        ...,
        description="A answer to be used to answer the question.",
        examples=[
            "Recent research has shed new light on how bats evolved their wings. An international team of researchers used genetic tools to study the embryonic development of bat wings and the genes involved in their formation.",
            "Rome defended Italy from Hannibal by using various strategies. One of the main defenses relied on the Roman manpower base, which consisted of a large army made up of Roman citizens and Italian allies who were obligated to render military service.",
        ],
    )


class ExaSearchResult(BaseModel):
    result_id: str = Field(
        ...,
        description="The ID of the search result.",
    )
    url: str = Field(
        ...,
        description="The URL of the search result.",
    )
    title: str = Field(
        ...,
        description="The title of the search result.",
    )
    score: str = Field(
        ...,
        description="The relevance of the search result.",
    )
    published_date: str = Field(
        ...,
        description="The published date of the search result.",
    )
    author: str = Field(
        ...,
        description="The author of the search result.",
    )
    text: str = Field(
        ...,
        description="The text of the search result.",
    )
    highlights: Optional[List[str]] = Field(
        ...,
        description="The highlights of the search result.",
    )
    highlight_score: Optional[List[float]] = Field(
        ...,
        description="The score of the highlights of the search result.",
    )


class ExaSearchResponse(BaseModel):
    search_results: List[ExaSearchResult] = Field(
        ...,
        description="A list of search results from the Exa search engine.",
    )
    autoprompt_string: str = Field(
        ...,
        description="The autoprompt string to be used to reformat the question.",
    )
