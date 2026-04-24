"""Configuration module for the Quality Gate service."""

import os
from functools import cached_property

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration settings for Quality Gate service."""

    GCP_PROJECT_ID: str  # Required — no default; fails fast
    LOCATION: str = "us-central1"
    MODEL_ID: str = "gemini-2.5-flash"
    RULES_FILE: str = "rules.md"
    SERVICE_NAME: str = "quality-gate"

    @cached_property
    def rules(self) -> str:
        """Returns the compliance rules to be enforced by AI, cached after first read."""
        # Resolve rules.md relative to the config.py directory
        dir_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(dir_path, self.RULES_FILE)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return f"ERROR: {self.RULES_FILE} not found at {path}."


settings = Settings()
