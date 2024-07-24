from dataclasses import dataclass
from typing import List

from pytest import raises
from tecton import Entity, RequestSource
from tecton.types import Bool, Field, Float32, Float64, Int32, Int64, String, Timestamp

from tecton_utils.ai._utils import (
    _parse_arguments,
    build_dummy_function,
    entity_to_tool_schema,
    fields_to_tool_schema,
)


def test_entity_to_tool_schema():
    def _assert(keys, schema):
        assert entity_to_tool_schema(Entity(name="a", join_keys=keys)) == schema

    _assert([Field("a", Int32)], {"a": "int"})
    _assert(
        [
            Field("a", String),
            Field("b", Int64),
            Field("c", Int32),
            Field("d", Float32),
            Field("e", Float64),
            Field("f", Bool),
        ],
        {
            "a": "str",
            "b": "int",
            "c": "int",
            "d": "float",
            "e": "float",
            "f": "bool",
        },
    )

    with raises(ValueError):
        _assert([Field("a", Timestamp)], {})
    with raises(ValueError):
        _assert([Field("a b", String)], {})
    with raises(ValueError):
        _assert([], {})


def test_fields_to_tool_schema():
    def _assert(fields, schema):
        assert fields_to_tool_schema(fields) == schema

    _assert([], {})
    _assert([Field("a", Int32)], {"a": "int"})
    _assert(
        [
            Field("a", String),
            Field("b", Int64),
            Field("c", Int32),
            Field("d", Float32),
            Field("e", Float64),
            Field("f", Bool),
        ],
        {
            "a": "str",
            "b": "int",
            "c": "int",
            "d": "float",
            "e": "float",
            "f": "bool",
        },
    )

    with raises(ValueError):
        _assert([Field("a", Timestamp)], {})
    with raises(ValueError):
        _assert([Field("a b", String)], {})


def test_build_dummy_function():
    def ab(
        x,
        y: int,
        z: str,
    ) -> str:
        """Docstring"""
        return x + y

    assert (
        build_dummy_function(ab, "xyz")
        == "def xyz(x, y: int, z: str) -> str:\n    pass"
    )
    assert (
        build_dummy_function(ab, "xyz", exclude_args=["y"])
        == "def xyz(x, z: str) -> str:\n    pass"
    )
    with raises(ValueError):
        build_dummy_function(ab, "x y z")
    with raises(ValueError):
        build_dummy_function(ab, "")
    with raises(AttributeError):
        build_dummy_function(ab, None)


def test_parse_arguments():
    fvs = [
        _mock_fv("fv1", ["c", "d"]),
        _mock_fv("fv2", ["c", "d"]),
    ]

    def ff1(c, d, a, fv1, b, fv2):
        pass

    def ff2(a, fv1, b, fv2):
        pass

    def ff3(d, a, fv1, b, fv2):
        pass

    assert _parse_arguments(ff1, fvs, assert_entity_defined=True) == (
        ["c", "d", "a", "b"],
        ["fv1", "fv2"],
        ["c", "d"],
        False,
    )

    assert _parse_arguments(ff2, fvs, assert_entity_defined=False) == (
        ["a", "b"],
        ["fv1", "fv2"],
        ["c", "d"],
        False,
    )

    assert _parse_arguments(ff1, [], assert_entity_defined=False) == (
        ["c", "d", "a", "fv1", "b", "fv2"],
        [],
        [],
        False,
    )

    with raises(ValueError):
        _parse_arguments(ff2, fvs, assert_entity_defined=True)

    with raises(ValueError):
        _parse_arguments(ff3, fvs, assert_entity_defined=True)

    with raises(ValueError):
        _parse_arguments(ff3, fvs, assert_entity_defined=False)

    rfvs = [
        RequestSource(schema=[Field("a", String), Field("b", Int32)]),
        _mock_fv("fv1", ["c", "d"]),
        _mock_fv("fv2", ["c", "d"]),
    ]

    def ff4(req, fv1, fv2):  # with request_source
        pass

    assert _parse_arguments(ff4, rfvs, assert_entity_defined=False) == (
        ["a", "b"],
        ["fv1", "fv2"],
        ["c", "d"],
        True,
    )

    with raises(ValueError):
        _parse_arguments(ff1, rfvs, assert_entity_defined=False)


def _mock_fv(name, keys):
    @dataclass
    class MockFV:
        name: str
        join_keys: List[str]

    return MockFV(name, keys)
