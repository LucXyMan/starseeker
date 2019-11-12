#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""support.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

サポートモジュール。
"""
import utils.const as _const
import special as __special


class _Support(__special.Special):
    u"""サポート。
    """
    __slots__ = ()

    def __init__(self, string):
        u"""コンストラクタ。
        """
        super(_Support, self).__init__(
            _const.SUPPORT_ARCANUM+"##"+string, (1, -1))


class Enchant(_Support):
    u"""追加効果サポート。
    """
    __slots__ = "__is_single", "__target"

    def __init__(self, string, is_single=False):
        u"""コンストラクタ。
        """
        name, description, self.__target = string.split("###")
        self.__is_single = is_single
        super(Enchant, self).__init__(name+"##"+description)

    def get_enchant(self, level):
        u"""追加効果を取得。
        """
        if level and self.__target:
            new, old = self.__target.split("##")
            return new, tuple(old.split("#")), (
                (1, 1) if self.__is_single else (level, level+1))
        return ()

    @property
    def subscript(self):
        u"""カード添字取得。
        """
        return u""


class Persistence(_Support):
    u"""持続サポート。
    """
    __slots__ = "__interval", "__target"

    def __init__(self, string, interval):
        u"""コンストラクタ。
        """
        name, description, self.__target = string.split("###")
        self.__interval = interval
        super(Persistence, self).__init__(name+"##"+description)

    def get_persistence(self, turn):
        u"""持続特殊効果を取得。
        """
        if turn & self.__interval == 0:
            new, old = self.__target.split("##")
            return new, old.split("#"), (1, 1)
        return ()

    @property
    def subscript(self):
        u"""カード添字取得。
        """
        return u"∞"


class Skill(_Support):
    u"""スキルサポート。
    """
    __slots__ = "__skills", "__subscript"

    def __init__(self, string):
        u"""コンストラクタ。
        """
        name, description, self.__subscript, self.__skills = string.split("##")
        super(Skill, self).__init__(name+"##"+description)

    @property
    def skills(self):
        u"""カードスキル取得。
        """
        return self.__skills

    @property
    def subscript(self):
        u"""カード添字取得。
        """
        return self.__subscript
