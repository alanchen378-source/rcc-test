import pathlib
from typing import Any, Dict

import yaml

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent


def load_yaml(path: pathlib.Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_env_config() -> Dict[str, Any]:
    return load_yaml(BASE_DIR / "config_env.yml")


def load_app_config() -> Dict[str, Any]:
    return load_yaml(BASE_DIR / "config_app.yml")


def load_rtsp_config() -> Dict[str, Any]:
    return load_yaml(BASE_DIR / "config_rtsp.yml")
