from pydantic import BaseModel, Field


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
