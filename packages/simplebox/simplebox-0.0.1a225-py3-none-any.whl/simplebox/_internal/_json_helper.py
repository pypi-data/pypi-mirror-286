#!/usr/bin/env python
# -*- coding:utf-8 -*-
from collections.abc import Callable
from typing import Optional, Any, Union

import orjson

from ..config.json import JsonConfig


def _build_option(option, orjson_option):
    if option is None:
        return orjson_option
    return option | orjson_option


def _inner_dumps(obj, *, default: Optional[Callable[[Any], Any]] = None, newline: bool = None, indent2: bool = None,
                 naive_utc: bool = None, non_str_keys: bool = None, omit_microseconds: bool = None,
                 passthrough_dataclass: bool = None, passthrough_datetime: bool = None,
                 passthrough_subclass: bool = None, serialize_dataclass: bool = None,
                 serialize_numpy: bool = None, serialize_uuid: bool = None, sort_keys: bool = None,
                 strict_integer: bool = None, utc_z: bool = None) -> bytes:
    """
    Serialize ``obj`` to a JSON formatted ``str``.
    :params ensure_ascii: If ``ensure_ascii`` is false, then the strings written to ``fp`` can
    contain non-ASCII characters if they appear in strings contained in
    ``obj``. Otherwise, all such characters are escaped in JSON strings.
    """
    option = None
    if newline is True or JsonConfig.newline:
        option = _build_option(option, orjson.OPT_APPEND_NEWLINE)
    if indent2 is True or JsonConfig.indent2:
        option = _build_option(option, orjson.OPT_INDENT_2)
    if naive_utc is True or JsonConfig.naive_utc:
        option = _build_option(option, orjson.OPT_NAIVE_UTC)
    if non_str_keys is True or JsonConfig.non_str_keys:
        option = _build_option(option, orjson.OPT_NON_STR_KEYS)
    if omit_microseconds is True or JsonConfig.omit_microseconds:
        option = _build_option(option, orjson.OPT_OMIT_MICROSECONDS)
    if passthrough_dataclass is True or JsonConfig.passthrough_dataclass:
        option = _build_option(option, orjson.OPT_PASSTHROUGH_DATACLASS)
    if passthrough_datetime is True or JsonConfig.passthrough_datetime:
        option = _build_option(option, orjson.OPT_PASSTHROUGH_DATETIME)
    if passthrough_subclass is True or JsonConfig.passthrough_subclass:
        option = _build_option(option, orjson.OPT_PASSTHROUGH_SUBCLASS)
    if serialize_dataclass is True or JsonConfig.serialize_dataclass:
        option = _build_option(option, orjson.OPT_SERIALIZE_DATACLASS)
    if serialize_numpy is True or JsonConfig.serialize_numpy:
        option = _build_option(option, orjson.OPT_SERIALIZE_NUMPY)
    if serialize_uuid is True or JsonConfig.serialize_uuid:
        option = _build_option(option, orjson.OPT_SERIALIZE_UUID)
    if sort_keys is True or JsonConfig.sort_keys:
        option = _build_option(option, orjson.OPT_SORT_KEYS)
    if strict_integer is True or JsonConfig.strict_integer:
        option = _build_option(option, orjson.OPT_STRICT_INTEGER)
    if utc_z is True or JsonConfig.utc_z:
        option = _build_option(option, orjson.OPT_UTC_Z)
    if isinstance(obj, _JsonSerializable):
        return orjson.dumps(obj.serializer(), default=default or JsonConfig.default, option=option)
    return orjson.dumps(obj, default=default or JsonConfig.default, option=option)


def _inner_loads(s: Union[bytes, bytearray, memoryview, str]) -> Any:
    """
    Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing a JSON document) to a Python object.
    """
    return orjson.loads(s)


class _JsonField:

    def __init__(self, value, *, name=None, autoname: bool = False):
        """
        Define a meta property for a JSON field.
        :param value: JSON field's value.
        :param name: The name of the JSON field at the time of serialization
        :param autoname: If the name of the json field is not specified and the autoname is True,
                        the python attribute name will be tried as the json field name, and the private attribute
                        will try to be replaced with a public attribute (only if serialized).
        """
        self.__value = value
        self.__name = name
        self.__autoname = autoname

    @property
    def value(self):
        return self.__value

    @property
    def name(self):
        return self.__name

    @property
    def autoname(self):
        return self.__autoname


def __parser_iter(values):
    for value in values:
        yield __parser(value)


def __parser_dict(values):
    d = {}
    for key, value in values.items():
        d[key] = __parser(value)
    return d


def __parser(value):
    if issubclass(type(value), (list, tuple)):
        return list(__parser_iter(value))
    elif issubclass(type(value), dict):
        return __parser_dict(value)
    elif isinstance(value, _JsonSerializable):
        return value.serializer()
    return value


def parser(value):
    return __parser(value)


class _JsonSerializable:
    """
    simplebox.json the JSON serialization interface provided by the module,
    it will first try to convert the interface into a dictionary when dumping.

    class Class(JsonSerializable):

        def __init__(self, *students):
            self.__students = JsonField(students, name="students")

        @property
        def students(self):
            return self.__students


    class Grades(JsonSerializable):
        def __init__(self, name, score):
            self.__name = JsonField(name, name="name")
            self.__score = JsonField(score, name="score")


    class Student(JsonSerializable):

        def __init__(self, age, name, scores):
            self.__name = JsonField(name, name="name")
            self.__age = JsonField(age, autoname=True)
            self.__scores = JsonField(scores, name="scores")


    student1 = Student(18, "Tony", {"exams": [Grades("chemistry", 80), Grades("biology", 90)]})
    student2 = Student(20, "Pony", {"exams": [Grades("chemistry", 81), Grades("biology", 91)]})

    clz = Class(student1, student2)

    print(clz.serializer())  # {'students': [{'name': 'Tony', 'age': 18, 'scores': {'exams': [{'name': 'chemistry', 'score': 80}, {'name': 'biology', 'score': 90}]}}, {'name': 'Pony', 'age': 20, 'scores': {'exams': [{'name': 'chemistry', 'score': 81}, {'name': 'biology', 'score': 91}]}}]}
    """
    @property
    def autoname(self) -> bool:
        """This property is used when the autoname property of JsonField is false"""
        return False

    def serializer(self):
        """
        simplebox.sjson dumps pre-serialization operation, make sure that the value can be returned when dumps.
        :return:
        """
        d = {}
        prefix = f"_{self.__class__.__name__}__"
        for key, value in self.__dict__.items():
            if isinstance(value, _JsonField):
                if value.autoname or self.autoname:
                    name = key.replace(prefix, "")
                else:
                    name = value.name
                if name:
                    d[name] = parser(value.value)
        return d
