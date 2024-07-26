#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import Any, Union

from ._internal._collections_serialization import _SerializeField, _Serializable, _serializer
from .config.serialize import SerializeConfig
from .generic import T

"""
Serialization (pre-processing) tools that convert objects into serializable objects such as dict and list.
eg:
class Class(Serializable):

    def __init__(self, *students):
        self.__students = SerializeField(students, name="students")


class Grades(Serializable):
    def __init__(self, name, score):
        self.__name = SerializeField(name, name="name")
        self.__score = SerializeField(score, name="score")

    def serializer(self):
        '''
        overwrite
        '''
        return f"{self.__name.value}: {self.__score.value}"


class Student(Serializable):

    def __init__(self, age, name, scores):
        self.__name = SerializeField(name, name="name")
        self.__age = SerializeField(age, autoname=True)
        self.__scores = SerializeField(scores, name="scores")

    @property
    def name(self):
        return self.__name

    @property
    def scores(self):
        return self.__scores.value  # 'value' attribute is the true value of self.__scores


student1 = Student(18, "Tony", {"exams": [Grades("chemistry", 80), Grades("biology", 90)]})
student2 = Student(20, "Pony", {"exams": [Grades("chemistry", 81), Grades("biology", 91)]})

print(student1.name.value)   =>   Tony
print(sjson.dumps(student1.scores))   =>   {"exams":["chemistry: 80","biology: 90"]}

clz = Class(student1, student2)

print(serializer(1))   #    1
print(serializer("2"))   #   2
print(serializer(clz))   #   {'students': [{'name': 'Tony', 'age': 18, 'scores': {'exams': ['chemistry: 80', 'biology: 90']}}, {'name': 'Pony', 'age': 20, 'scores': {'exams': ['chemistry: 81', 'biology: 91']}}]}
print(serializer([student1, student2]))   #   [{'name': 'Tony', 'age': 18, 'scores': {'exams': ['chemistry: 80', 'biology: 90']}}, {'name': 'Pony', 'age': 20, 'scores': {'exams': ['chemistry: 81', 'biology: 91']}}]
print(sjson.dumps(clz))   #   {"students":[{"name":"Tony","age":18,"scores":{"exams":["chemistry: 80","biology: 90"]}},{"name":"Pony","age":20,"scores":{"exams":["chemistry: 81","biology: 91"]}}]}
print(serializer([1, 2]))   #   [1, 2]
print(serializer({"a": 1, "b": 2}))   #   {'a': 1, 'b': 2}
"""


def serializer(value) -> dict[str, Any]:
    """
    Try converting an object to a dict or list.
    """
    return _serializer(value, SerializeConfig.camel)


class SerializeField(_SerializeField):
    def __init__(self, value: T, *, name=None, autoname: bool = False, camel: bool = False):
        """
        Connect the property to the key-value of the dictionary.
        :param value: JSON field's value.
        :param name: The name of the JSON field at the time of serialization.
                    After a name is specified, autoname and camel do not take effect.
        :param autoname: If the name of the json field is not specified and autoname is True,
                        an attempt will be made to name the json field name with the attribute name.
        :param camel: The recommended attribute format for python is snake, and this option will use camel.
                      autoname is True will camel take effect.
        """
        super().__init__(value, name=name, autoname=autoname, camel=camel)

    @property
    def value(self) -> T:
        return super().value

    @property
    def name(self) -> str:
        return super().name

    @property
    def autoname(self) -> bool:
        return super().autoname

    @property
    def camel(self) -> bool:
        return super().camel


class Serializable(_Serializable):
    """
    Converts an object's properties into a dictionary to support serialization.
    """

    @property
    def autoname(self) -> bool:
        """This property is used when the autoname property of JsonField is false"""
        return super().autoname

    def serializer(self) -> dict[str, Any]:
        """
        Convert attributes to dict.
        """
        return super().serializer()


__all__ = [Serializable, SerializeField, serializer]
