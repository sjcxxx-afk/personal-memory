import logging
import sys
import os
from pathlib import Path
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.settings import LOG_LEVEL


def setup_logging(level: Optional[str] = None) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger
    """
    log_level = level or LOG_LEVEL
    
    # Create logger
    logger = logging.getLogger("personal-memory")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Prevent duplicate handlers
    if not logger.handlers:
        # Create console handler - use stderr for MCP compatibility
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
    
    return logger


def format_timestamp(timestamp_str: str) -> str:
    """
    Format ISO timestamp string to human-readable format.
    
    Args:
        timestamp_str: ISO format timestamp string
    
    Returns:
        Formatted timestamp string
    """
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp_str


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def validate_scene(scene: str) -> bool:
    """
    Validate scene tag.
    
    Args:
        scene: Scene tag to validate
    
    Returns:
        True if valid, False otherwise
    """
    valid_scenes = [
        "general", "work", "life", "health", "finance",
        "education", "entertainment", "social", "travel", "food"
    ]
    return scene.lower() in valid_scenes


def get_scene_emoji(scene: str) -> str:
    """
    Get emoji for scene tag.
    
    Args:
        scene: Scene tag
    
    Returns:
        Emoji string
    """
    scene_emojis = {
        "general": "📝",
        "work": "💼",
        "life": "🏠",
        "health": "🏥",
        "finance": "💰",
        "education": "📚",
        "entertainment": "🎬",
        "social": "👥",
        "travel": "✈️",
        "food": "🍔"
    }
    return scene_emojis.get(scene.lower(), "📝")