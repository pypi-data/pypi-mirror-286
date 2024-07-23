#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: meta.py
@DateTime: 2024/7/19 11:57
@SoftWare: 
"""

from typing import Any, Dict


class OptionMeta(type):
    def __new__(cls, name: str, bases: tuple, dct: Dict[str, Any]) -> Any:
        """
        Creates a new class and dynamically adds methods based on the 'options' attribute.
        :param name: str
        :param bases: tuple
        :param dct: dict
        """
        options = dct.get('options', {})
        for option in options:
            method_name = option.lstrip('-') if option.startswith('-') else option
            dct[method_name] = cls.create_method(option)
        return super().__new__(cls, name, bases, dct)

    @staticmethod
    def create_method(option: str) -> Any:
        """
        Creates a method that appends a command with the given option and value to the commands list.
        :param option: str: default is '', The option string to be used in the method.
        :return:
        """
        def method(self, value: str = '') -> object:
            if not value:
                self.commands.append(f"{option}")
            else:
                self.commands.append(f"{option} {value}")
            return self

        return method

