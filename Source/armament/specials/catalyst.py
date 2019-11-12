#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""catalyst.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

触媒モジュール。
"""


class Catalyst(object):
    u"""触媒。
    """
    __slots__ = "_Sorcery", "__args", "__kw", "__recepter", "__string"

    def __init__(self, Sorcery, string, *args, **kw):
        u"""コンストラクタ。
        """
        self._Sorcery = Sorcery
        self.__string = string
        self.__args = args
        self.__kw = kw

    @property
    def recepter(self):
        u"""変化対象の名前取得。
        """
        recepter, _ = self.__string.split("####")
        return recepter

    @property
    def Sorcery(self):
        u"""ソーサリーデータクラス取得。
        """
        return self._Sorcery

    @property
    def string(self):
        u"""テキスト取得。
        """
        import utils.const as __const
        _, string = self.__string.split("####")
        return __const.ALTERED_ARCANUM+"###"+string

    @property
    def args(self):
        u"""引数取得。
        """
        return self.__args

    @property
    def kw(self):
        u"""キーワード引数取得。
        """
        return self.__kw
