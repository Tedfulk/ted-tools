from ted_tools.models import (
    Titles,
    ThumbnailPrompts,
    Transcript,
    Description,
    Hashtags,
)
from phi.llm.ollama import Ollama
from phi.task.llm import LLMTask
from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.python import PythonTools
from phi.tools.file import FileTools
from phi.tools.shell import ShellTools
from phi.tools.arxiv import ArxivTools
from phi.tools.wikipedia import WikipediaTools
from pathlib import Path


gen_description_task = LLMTask(
    llm=Ollama(model="dolphin-mixtral:8x7b-v2.7-q4_K_M"),
    output_model=Description,
    system_prompt="Generate a description for a video given a topic. It should be more than 100 words and less than 200 words, and should be simple enough that a high school student could understand.",
)

gen_titles_task = LLMTask(
    llm=Ollama(model="dolphin-mixtral:8x7b-v2.7-q4_K_M"),
    output_model=Titles,
    system_prompt=f"Generate 3 titles for a video given a topic. It should be short, simple, and SEO worthy. Mr. Beast would be proud to use it.",
)

gen_transcript_task = LLMTask(
    llm=Ollama(model="dolphin-mixtral:8x7b-v2.7-q4_K_M"),
    output_model=Transcript,
    system_prompt="Generate a transcript for a video given a topic.",
)

gen_hashtags_task = LLMTask(
    llm=Ollama(model="dolphin-mixtral:8x7b-v2.7-q4_K_M"),
    output_model=Hashtags,
    system_prompt="Generate 10 hashtags for a video given a topic.",
)

gen_thumbnail_prompts_task = LLMTask(
    llm=Ollama(model="dolphin-mixtral:8x7b-v2.7-q4_K_M"),
    output_model=ThumbnailPrompts,
    system_prompt="Generate 3 thumbnail prompts for a video given a topic.",
)
