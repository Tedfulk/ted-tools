import llm
from ted_tools.utils import (
    write_or_append_with_version,
    get_first_5_to_10_words_from_text,
)


def generate_llm_metadata(user_input: str):
    model = llm.get_model("dolphin-mixtral:8x7b-v2.7")
    response = model.prompt(
        user_input,
        stream=True,
        system="""## Instructions Main objective is to generate three Titles, a Transcript, A Description,  a List of 10 tags, and three Thumbnail prompt options. Please replace (Content Summary) with a brief summary of the users provided topic or content for each section. ### Title: Generate three distinct catchy titles for the following content (Content Summary).1. Option 1: (Content Summary) 2. Option 2: (Content Summary) 3. Option 3: (Content Summary) ### Transcript: Include a detailed transcript of the content, capturing key dialogues, actions, and important moments to provide a comprehensive overview for readers. The tone and writing style should be informal while semi-professional. ### Description: Write a concise and informative description that encapsulates the main points and themes of the content (Content Summary). ### Tags: List relevant 10 tags that cover the key topics, themes, or genres present in the content (Content Summary). ### Thumbnail Prompt Options: Create three distinct thumbnail prompt options for the content. Each option should offer a unique angle or highlight a different aspect of the content, ensuring creativity and relevance to the title, description, and tags provided. 1. Option 1: (Content Summary) 2. Option 2: (Content Summary) 3. Option 3: (Content Summary)""",
    )

    write_or_append_with_version(
        filename=user_input.replace(" ", "-"),
        filetype=".txt",
        content=response.text(),
    )


generate_llm_metadata("How to make a cake")
