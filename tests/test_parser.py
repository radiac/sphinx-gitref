"""
Test sphinx_gitref.parser
"""
import pytest

from sphinx_gitref.exceptions import ParseError
from sphinx_gitref.parser import python_string_to_lineno


def test_string__var_exists__returns_lineno():
    assert python_string_to_lineno("a = 1", "a") == 1


def test_string__var_does_not_exist__raises_error():
    with pytest.raises(ParseError):
        python_string_to_lineno("a = 1", "b")


def test_string__var_on_different_line__returns_lineno():
    assert (
        python_string_to_lineno(
            """
a = 1
b = 2
            """,
            "b",
        )
        == 3
    )


def test_string__function_exists__returns_lineno():
    assert (
        python_string_to_lineno(
            """
def foo():
    pass
            """,
            "foo",
        )
        == 2
    )


def test_string__py2_class_exists__returns_lineno():
    assert (
        python_string_to_lineno(
            """
class Foo(object):
    pass
            """,
            "Foo",
        )
        == 2
    )


def test_string__class_exists__returns_lineno():
    assert (
        python_string_to_lineno(
            """
class Foo:
    pass
            """,
            "Foo",
        )
        == 2
    )


def test_string__py2_class_attribute_exists__returns_lineno():
    assert (
        python_string_to_lineno(
            """
class Foo(object):
    bar = 1
            """,
            "Foo.bar",
        )
        == 3
    )


def test_string__class_attribute_exists__returns_lineno():
    assert (
        python_string_to_lineno(
            """
class Foo:
    bar = 1
            """,
            "Foo.bar",
        )
        == 3
    )


def test_string__class_method_exists__returns_lineno():
    assert (
        python_string_to_lineno(
            """
class Foo:
    def bar(self):
        pass
            """,
            "Foo.bar",
        )
        == 3
    )


def test_string__class_attribute_exists_but_incorrect_path__raises_error():
    with pytest.raises(ParseError):
        python_string_to_lineno(
            """
class Foo:
    bar = 1
            """,
            "bar",
        )
