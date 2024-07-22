#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import Any

import ujson

from .config.json import JsonConfig

"""
This module just wraps the ujson module and set params by JsonConfig(global config). 
For all usages, please refer to the ujson module.
https://pypi.org/project/ujson/
"""


def dump(obj, fp, *, escape_forward_slashes: bool = JsonConfig.escape_forward_slashes,
         ensure_ascii: bool = JsonConfig.ensure_ascii,
         encode_html_chars: bool = JsonConfig.encode_html_chars, indent: int = JsonConfig.indent,
         sort_keys: bool = JsonConfig.sort_keys) -> None:
    """Serialize ``obj`` as a JSON formatted stream to ``fp`` (a
    ``.write()``-supporting file-like object).
    :params fp: open("file", "w"), not bytes.

    :params ensure_ascii: If ``ensure_ascii`` is false, then the strings written to ``fp`` can
    contain non-ASCII characters if they appear in strings contained in
    ``obj``. Otherwise, all such characters are escaped in JSON strings.

    :params indent: If ``indent`` is a non-negative integer, then JSON array elements and
    object members will be pretty-printed with that indent level. An indent
    level of 0 will only insert newlines. ``None`` is the most compact
    representation.

    :params encode_html_chars: Used to enable special encoding of "unsafe" HTML characters into safer Unicode
    sequences, default is :False

    :params escape_forward_slashes: Controls whether forward slashes () are escaped. Default is True.

    :params sort_keys: If *sort_keys* is true (default: ``False``), then the output of
    dictionaries will be sorted by key.
    """
    return ujson.dump(obj, fp, ensure_ascii=ensure_ascii, sort_keys=sort_keys,
                      escape_forward_slashes=escape_forward_slashes, encode_html_chars=encode_html_chars, indent=indent)


def dumps(obj, *, escape_forward_slashes: bool = JsonConfig.escape_forward_slashes,
          ensure_ascii: bool = JsonConfig.ensure_ascii,
          encode_html_chars: bool = JsonConfig.encode_html_chars, indent: int = JsonConfig.indent,
          sort_keys: bool = JsonConfig.sort_keys) -> str:
    """
    Serialize ``obj`` to a JSON formatted ``str``.
    :params ensure_ascii: If ``ensure_ascii`` is false, then the strings written to ``fp`` can
    contain non-ASCII characters if they appear in strings contained in
    ``obj``. Otherwise, all such characters are escaped in JSON strings.

    :params indent: If ``indent`` is a non-negative integer, then JSON array elements and
    object members will be pretty-printed with that indent level. An indent
    level of 0 will only insert newlines. ``None`` is the most compact
    representation.

    :params encode_html_chars: Used to enable special encoding of "unsafe" HTML characters into safer Unicode
    sequences, default is :False

    :params escape_forward_slashes: Controls whether forward slashes () are escaped. Default is True.

    :params sort_keys: If *sort_keys* is true (default: ``False``), then the output of
    dictionaries will be sorted by key.
    """
    return ujson.dumps(obj, ensure_ascii=ensure_ascii, sort_keys=sort_keys, indent=indent,
                       escape_forward_slashes=escape_forward_slashes, encode_html_chars=encode_html_chars)


def load(fp) -> Any or dict or list:
    """
    Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    a JSON document) to a Python object.
    """
    return ujson.load(fp)


def loads(s) -> Any:
    """
    Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing a JSON document) to a Python object.
    """
    return ujson.loads(s)


def decode(s) -> Any or dict or list:
    return ujson.decode(s)


def encode(obj, escape_forward_slashes: bool = JsonConfig.escape_forward_slashes,
           ensure_ascii: bool = JsonConfig.ensure_ascii,
           encode_html_chars: bool = JsonConfig.encode_html_chars, indent: int = JsonConfig.indent,
           sort_keys: bool = JsonConfig.sort_keys) -> str:
    return ujson.encode(obj, escape_forward_slashes=escape_forward_slashes, encode_html_chars=encode_html_chars,
                        ensure_ascii=ensure_ascii, sort_keys=sort_keys, indent=indent)
