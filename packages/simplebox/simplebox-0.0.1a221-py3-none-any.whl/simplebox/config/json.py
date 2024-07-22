#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import Type

from ..singleton import SingletonMeta


class __JsonConfig(metaclass=SingletonMeta):
    """
    simplebox.json global config.
    use in simplebox.json module.
    """
    def __init__(self):
        self.__ensure_ascii: bool = False
        self.__escape_forward_slashes: bool = True
        self.__encode_html_chars: bool = False
        self.__indent: int = 0
        self.__sort_keys: bool = False

    @staticmethod
    def __check_type(value, t: Type):
        if issubclass(v_type := type(value), t):
            raise TypeError(f"expected type bool, got a {v_type}")

    @property
    def ensure_ascii(self) -> bool:
        return self.__ensure_ascii

    @ensure_ascii.setter
    def ensure_ascii(self, value: bool):
        self.__check_type(value, bool)
        self.__ensure_ascii = value

    @property
    def escape_forward_slashes(self) -> bool:
        return self.__escape_forward_slashes

    @escape_forward_slashes.setter
    def escape_forward_slashes(self, value: bool):
        self.__check_type(value, bool)
        self.__escape_forward_slashes = value

    @property
    def encode_html_chars(self) -> bool:
        return self.__encode_html_chars

    @encode_html_chars.setter
    def encode_html_chars(self, value: bool):
        self.__check_type(value, bool)
        self.__encode_html_chars = value

    @property
    def indent(self) -> int:
        return self.__indent

    @indent.setter
    def indent(self, value: int):
        self.__check_type(value, int)
        self.__indent = value

    @property
    def sort_keys(self) -> bool:
        return self.__sort_keys

    @sort_keys.setter
    def sort_keys(self, value: bool):
        self.__check_type(value, bool)
        self.__sort_keys = value


JsonConfig = __JsonConfig()

__all__ = [JsonConfig]
