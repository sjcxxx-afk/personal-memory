import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database paths
SQLITE_DB_PATH = BASE_DIR / "data" / "memory.db"
CHROMA_DB_PATH = BASE_DIR / "data" / "chroma"
FACTS_DIR = BASE_DIR / "data" / "facts"

# Ensure directories exist
SQLITE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
CHROMA_DB_PATH.mkdir(parents=True, exist_ok=True)
FACTS_DIR.mkdir(parents=True, exist_ok=True)

# MCP Server settings
MCP_SERVER_NAME = "personal-memory"
MCP_SERVER_VERSION = "0.1.0"

# Memory settings
DEFAULT_HOT_THRESHOLD = 30  # days
DEFAULT_WARM_THRESHOLD = 7  # days
DEFAULT_HOT_LAYER_MAX = 500  # max facts in hot layer

# Embedding model settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # or "text-embedding-ada-002" for OpenAI
USE_LOCAL_EMBEDDINGS = True

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")