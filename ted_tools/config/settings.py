import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

# API Endpoints
OLLAMA_API_ENDPOINT = os.getenv("OLLAMA_API_ENDPOINT", "http://127.0.0.1:11434/v1")
YOUTUBE_API_ENDPOINT = os.getenv(
    "YOUTUBE_API_ENDPOINT", "https://www.googleapis.com/youtube/v3"
)

# Default file paths
DEFAULT_METADATA_DIR = os.getenv("DEFAULT_METADATA_DIR", "ted_tools/data")

# Application settings
DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1", "t"]
