#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import Generic

from ..config.serialize import SerializeConfig
from ..generic import T
from ..utils.strings import StringUtils
from ..utils.objects import ObjectsUtils


class _SerializeField(Generic[T]):

    def __init__(self, value: T, *, name=None, autoname: bool = False, camel: bool = False):
        ObjectsUtils.check_type(name, str)
        ObjectsUtils.check_type(autoname, bool)
        ObjectsUtils.check_type(camel, bool)
        self.__value: T = value
        self.__name: str = name
        self.__autoname: bool = autoname
        self.__camel: bool = camel

    @property
    def value(self) -> T:
        return self.__value

    @property
    def name(self) -> str:
        return self.__name

    @property
    def autoname(self) -> bool:
        return self.__autoname

    @property
    def camel(self) -> bool:
        return self.__camel


def __parser_iter(values, camel):
    l = []
    l_append = l.append
    for value in values:
        l_append(__parser(value, camel))
    return l


def __parser_dict(values, camel):
    d = {}
    for key, value in values.items():
        if camel:
            k = StringUtils.convert_to_camel(key).origin()
        else:
            k = key
        d[k] = __parser(value, camel)
    return d


def __parser(value, camel):
    if issubclass(type(value), (list, tuple, set)):
        return __parser_iter(value, camel)
    elif issubclass(type(value), dict):
        return __parser_dict(value, camel)
    elif isinstance(value, _Serializable):
        return value.serializer()
    return value


def _serializer(value, camel):
    return __parser(value, camel)


class _Serializable(Generic[T]):

    @property
    def autoname(self) -> bool:
        return False

    @property
    def camel(self) -> bool:
        return False

    def serializer(self) -> dict[str, T]:
        d = {}
        prefix = f"_{self.__class__.__name__}__"
        for key, value in self.__dict__.items():
            if isinstance(value, _SerializeField):
                camel = value.value, value.camel or self.camel or SerializeConfig.camel
                name = value.name or ""
                if not name:
                    if value.autoname or self.autoname or SerializeConfig.autoname:
                        if key.startswith(prefix):
                            name = key.replace(prefix, "")
                        elif key[0] == "_" and key[1] != "_":
                            name = key[1:]
                        else:
                            name = key
                    if camel:
                        name = StringUtils.convert_to_camel(name).origin()
                if (len(name) == 1 and len("_")) or StringUtils.is_black(name):
                    continue
                if name:
                    d[name] = _serializer(value.value, camel)
        return d


__all__ = [_Serializable, _SerializeField, _serializer]
