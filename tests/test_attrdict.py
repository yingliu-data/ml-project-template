from PACKAGE_NAME.utils.attrdict import AttrDict


def test_attribute_access():
    d = AttrDict({"a": 1, "b": 2})
    assert d.a == 1
    assert d.b == 2
    assert d["a"] == 1


def test_nested_conversion():
    raw = {"outer": {"inner": {"leaf": 42}}, "sibling": [1, 2, 3]}
    d = AttrDict.from_nested_dicts(raw)
    assert d.outer.inner.leaf == 42
    assert d.sibling == [1, 2, 3]


def test_non_dict_passthrough():
    assert AttrDict.from_nested_dicts(5) == 5
    assert AttrDict.from_nested_dicts("x") == "x"
