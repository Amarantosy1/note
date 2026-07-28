from copy import deepcopy
from io import StringIO
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

from .generator import expand_nav


def load_config(path: Path) -> Any:
    yaml = _yaml()
    with path.open(encoding="utf-8") as stream:
        return yaml.load(stream)


def expanded_config(path: Path) -> Any:
    config = load_config(path)
    if not isinstance(config, dict):
        raise ValueError("configuration root must be a mapping")
    result = deepcopy(config)
    result["nav"] = expand_nav(result, path.parent)
    result.pop("zensical_nav", None)
    return result


def dump_config(config: Any, destination: Path | None = None) -> str:
    yaml = _yaml()
    if destination is not None:
        with destination.open("w", encoding="utf-8") as stream:
            yaml.dump(config, stream)
        return ""
    stream = StringIO()
    yaml.dump(config, stream)
    return stream.getvalue()


def expand_config_file(source: Path, destination: Path) -> None:
    dump_config(expanded_config(source), destination)


def _yaml() -> YAML:
    yaml = YAML(typ="rt")
    yaml.preserve_quotes = True
    yaml.width = 4096
    return yaml
