import os
import pickle
from typing import Any

import pandas as pd
import yaml


def _write_pickle(data: Any, path: str) -> None:
    with open(path, "wb") as f:
        pickle.dump(data, f)


def _write_yaml(data: Any, path: str) -> None:
    with open(path, "w") as f:
        yaml.safe_dump(data, f)


def _read_pickle(path: str) -> Any:
    with open(path, "rb") as f:
        return pickle.load(f)


def _read_yaml(path: str) -> Any:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def _read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


_WRITERS = {"p": _write_pickle, "pkl": _write_pickle, "yml": _write_yaml, "yaml": _write_yaml}
_READERS = {"p": _read_pickle, "pkl": _read_pickle, "yml": _read_yaml, "yaml": _read_yaml, "csv": _read_csv}


def writer(data: Any, output_path: str) -> None:
    ext = os.path.basename(output_path).rsplit(".", 1)[-1].lower()
    if ext not in _WRITERS:
        raise ValueError(f"No writer registered for extension '.{ext}'")
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    _WRITERS[ext](data, output_path)


def reader(input_path: str) -> Any:
    ext = os.path.basename(input_path).rsplit(".", 1)[-1].lower()
    if ext not in _READERS:
        raise ValueError(f"No reader registered for extension '.{ext}'")
    return _READERS[ext](os.path.normpath(input_path))
