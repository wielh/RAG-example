from pathlib import Path
import yaml

def load_config() -> dict:
    path: Path = Path(__file__).resolve().parent.parent.parent / "config.yaml"
    with open(path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

config = load_config()