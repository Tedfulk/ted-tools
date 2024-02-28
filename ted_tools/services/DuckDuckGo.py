from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from phi.tools.duckduckgo import DuckDuckGo
import typer


def tool_call(model: str = "dolphin-mixtral:8x7b-v2.7-q4_K_M", debug: bool = True):
    print(f"============= Running: {model} =============")
    Assistant(
        llm=Ollama(model=model),
        tools=[DuckDuckGo()],
        show_tool_calls=True,
        debug_mode=debug,
    ).cli_app(user=" Ted 👉 ")
