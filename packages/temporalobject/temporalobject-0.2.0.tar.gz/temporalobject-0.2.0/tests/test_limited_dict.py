import pytest

from temporal.util import LimitedDict


def test_limited_dict_insertion():
    limited_dict = LimitedDict(2)
    limited_dict["a"] = 1
    limited_dict["b"] = 2
    assert len(limited_dict) == 2
    assert "a" in limited_dict
    assert "b" in limited_dict


def test_limited_dict_update():
    limited_dict = LimitedDict(2)
    limited_dict["a"] = 1
    limited_dict["b"] = 2
    limited_dict["a"] = 3
    assert len(limited_dict) == 2
    assert limited_dict["a"] == 3
    assert "b" in limited_dict
