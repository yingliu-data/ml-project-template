import os

from PACKAGE_NAME.utils.io import reader, writer


def test_yaml_roundtrip(tmp_path):
    payload = {"model": {"lr": 1e-3, "layers": [32, 64]}}
    path = tmp_path / "cfg.yml"
    writer(payload, str(path))
    assert reader(str(path)) == payload


def test_pickle_roundtrip(tmp_path):
    payload = {"arr": [1, 2, 3], "nested": {"k": "v"}}
    path = tmp_path / "obj.pkl"
    writer(payload, str(path))
    assert reader(str(path)) == payload


def test_unknown_extension_raises(tmp_path):
    import pytest
    with pytest.raises(ValueError):
        writer({"a": 1}, str(tmp_path / "bad.xyz"))
