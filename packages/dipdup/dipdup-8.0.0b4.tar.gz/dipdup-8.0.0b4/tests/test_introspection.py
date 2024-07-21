from typing import Any

import pytest
from pydantic import BaseModel
from pydantic import RootModel

from dipdup.indexes.tezos_operations.parser import IntrospectionError
from dipdup.indexes.tezos_operations.parser import extract_root_outer_type
from dipdup.indexes.tezos_operations.parser import get_dict_value_type
from dipdup.indexes.tezos_operations.parser import get_list_elt_type
from dipdup.indexes.tezos_operations.parser import is_array_type
from dipdup.indexes.tezos_operations.parser import unwrap_union_type

NoneType = type(None)


def test_list_simple_args() -> None:
    assert get_list_elt_type(list[str]) == str  # noqa: E721
    assert get_list_elt_type(list[int]) == int  # noqa: E721
    assert get_list_elt_type(list[bool]) == bool  # noqa: E721
    assert get_list_elt_type(list[str | None]) == str | None
    assert get_list_elt_type(list[str | int]) == str | int
    assert get_list_elt_type(list[tuple[str]]) == tuple[str]
    assert get_list_elt_type(list[list[str]]) == list[str]
    assert get_list_elt_type(list[dict[str, str]]) == dict[str, str]


def test_list_complex_arg() -> None:
    class Class: ...

    assert get_list_elt_type(list[Class]) == Class
    assert get_list_elt_type(list[Class | None]) == Class | None
    assert get_list_elt_type(list[Class | int]) == Class | int
    assert get_list_elt_type(list[tuple[Class]]) == tuple[Class]
    assert get_list_elt_type(list[list[Class]]) == list[Class]
    assert get_list_elt_type(list[dict[str, Class]]) == dict[str, Class]


def test_pydantic_list_arg() -> None:
    class ListOfMapsStorage(BaseModel):
        root: list[int | dict[str, str]]

    class SomethingElse(BaseModel):
        root: dict[str, str]

    class OptionalList(BaseModel):
        root: list[str] | None

    assert get_list_elt_type(ListOfMapsStorage) == int | dict[str, str]

    with pytest.raises(IntrospectionError):
        get_list_elt_type(OptionalList)

    with pytest.raises(IntrospectionError):
        get_list_elt_type(SomethingElse)


def test_dict_simple_args() -> None:
    assert get_dict_value_type(dict[str, str]) == str  # noqa: E721
    assert get_dict_value_type(dict[str, int]) == int  # noqa: E721
    assert get_dict_value_type(dict[str, bool]) == bool  # noqa: E721
    assert get_dict_value_type(dict[str, str | None]) == str | None
    assert get_dict_value_type(dict[str, str | int]) == str | int
    assert get_dict_value_type(dict[str, tuple[str]]) == tuple[str]
    assert get_dict_value_type(dict[str, list[str]]) == list[str]
    assert get_dict_value_type(dict[str, dict[str, str]]) == dict[str, str]


def test_dict_complex_arg() -> None:
    class Class: ...

    assert get_dict_value_type(dict[str, Class]) == Class
    assert get_dict_value_type(dict[str, Class | None]) == Class | None
    assert get_dict_value_type(dict[str, Class | int]) == Class | int
    assert get_dict_value_type(dict[str, tuple[Class]]) == tuple[Class]
    assert get_dict_value_type(dict[str, list[Class]]) == list[Class]
    assert get_dict_value_type(dict[str, dict[str, Class]]) == dict[str, Class]


def test_pydantic_dict_arg() -> None:
    class DictOfMapsStorage(RootModel[Any]):
        root: dict[str, int | dict[str, str]]

    class SomethingElse(RootModel[Any]):
        root: list[str]

    class OptionalDict(RootModel[Any]):
        root: dict[str, str] | None

    assert get_dict_value_type(DictOfMapsStorage) == int | dict[str, str]
    with pytest.raises(IntrospectionError):
        get_dict_value_type(OptionalDict)

    with pytest.raises(IntrospectionError):
        get_dict_value_type(SomethingElse)


def test_pydantic_object_key() -> None:
    class Storage(BaseModel):
        plain_str: str
        list_str: list[str]
        dict_of_lists: dict[str, list[str]]
        optional_str: str | None
        union_arg: str | int

    assert get_dict_value_type(Storage, 'plain_str') == str  # noqa: E721
    assert get_dict_value_type(Storage, 'list_str') == list[str]
    assert get_dict_value_type(Storage, 'dict_of_lists') == dict[str, list[str]]
    assert get_dict_value_type(Storage, 'optional_str') == str | None
    assert get_dict_value_type(Storage, 'union_arg') == str | int


def test_is_array() -> None:
    class ListOfMapsStorage(RootModel[Any]):
        root: list[int | dict[str, str]]

    class OptionalList(RootModel[Any]):
        root: list[str] | None

    assert is_array_type(list[str]) is True
    assert is_array_type(ListOfMapsStorage) is True
    assert is_array_type(OptionalList) is False


def test_simple_union_unwrap() -> None:
    assert unwrap_union_type(str | None) == (True, (str, NoneType))  # type: ignore[arg-type]
    assert unwrap_union_type(int | str) == (True, (int, str))  # type: ignore[arg-type]


def test_pydantic_optional_unwrap() -> None:
    class UnionIntStr(RootModel[Any]):
        root: int | str

    class OptionalStr(RootModel[Any]):
        root: str | None

    assert unwrap_union_type(OptionalStr) == (True, (str, NoneType))
    assert unwrap_union_type(UnionIntStr) == (True, (int, str))


def test_root_type_extraction() -> None:
    class OptionalStr(RootModel[Any]):
        root: str | None

    class ListOfMapsStorage(RootModel[Any]):
        root: list[int | dict[str, str]]

    assert extract_root_outer_type(OptionalStr) == str | None
    # FIXME: left operand type: "Type[BaseModel]", right operand type: "Type[list[Any]]"
    assert extract_root_outer_type(ListOfMapsStorage) == list[int | dict[str, str]]  # type: ignore[comparison-overlap]
