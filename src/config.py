import tomllib
from pathlib import Path
from typing import Any, Dict

def load_config() -> Dict[str, Any]:
    """Load the configuration from the .default_config.toml file."""
    config_path = Path(__file__).parent.parent / ".default_config.toml"
    with open(config_path, "rb") as f:
        return tomllib.load(f)

CONFIG = load_config()

def get_config(section: str, key: str) -> Any:
    """Get a configuration value from the specified section and key."""
    return CONFIG[section][key]