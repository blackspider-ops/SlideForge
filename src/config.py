"""Configuration management for SlideForge."""

import json
from pathlib import Path
from typing import Dict, Any


DEFAULT_CONFIG = {
    "method": "playwright",
    "slides_dir": "../slides",
    "output_dir": "../output",
    "format": "pdf",
    "quiet": False,
    "verbose": False
}


def get_config_path() -> Path:
    """Get the path to the config file."""
    return Path.home() / '.slideforge' / 'config.json'


def load_config() -> Dict[str, Any]:
    """Load configuration from file or return defaults."""
    config_path = get_config_path()
    
    if not config_path.exists():
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_path, 'r') as f:
            user_config = json.load(f)
        
        # Merge with defaults
        config = DEFAULT_CONFIG.copy()
        config.update(user_config)
        return config
    except Exception as e:
        print(f"Warning: Failed to load config: {e}")
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> bool:
    """Save configuration to file."""
    config_path = get_config_path()
    
    try:
        # Create directory if it doesn't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error: Failed to save config: {e}")
        return False


def show_config():
    """Display current configuration."""
    config = load_config()
    config_path = get_config_path()
    
    print(f"\n{'='*60}")
    print("Current Configuration")
    print(f"{'='*60}\n")
    print(f"Config file: {config_path}")
    print(f"Exists: {'Yes' if config_path.exists() else 'No (using defaults)'}\n")
    
    for key, value in config.items():
        print(f"  {key:<15} : {value}")
    
    print(f"\n{'='*60}")
    print("To change settings, edit the config file or use --set-config")
    print(f"{'='*60}\n")


def set_config_value(key: str, value: str) -> bool:
    """Set a configuration value."""
    config = load_config()
    
    if key not in DEFAULT_CONFIG:
        print(f"Error: Unknown config key '{key}'")
        print(f"Valid keys: {', '.join(DEFAULT_CONFIG.keys())}")
        return False
    
    # Convert value to appropriate type
    if key in ['quiet', 'verbose']:
        value = value.lower() in ['true', '1', 'yes', 'on']
    
    config[key] = value
    
    if save_config(config):
        print(f"✓ Set {key} = {value}")
        return True
    
    return False
