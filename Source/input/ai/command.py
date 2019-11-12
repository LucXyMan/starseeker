#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""command.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

AIコマンドモジュール。
"""


class __Command(object):
    u"""コマンド基礎。
    """
    __slots__ = ()

    @property
    def is_basic(self):
        u"""単純コマンドの場合に真。
        """
        return isinstance(self, Simple)


class Simple(__Command):
    u"""単純コマンド。
    """
    __slots__ = "__queue",

    def __init__(self, queue):
        u"""コンストラクタ。
        """
        self.__queue = queue

    def __repr__(self):
        u"""文字列表現取得。
        """
        return u"<{name}: queue:{state}>".format(
            name=self.__class__.__name__, state=self.__queue)

    @property
    def queue(self):
        u"""コマンドキュー種類取得。
        """
        return self.__queue


class Breadcrumb(__Command):
    u"""パンくずコマンド。
    目的位置までのパンくず。
    """
    __slots__ = "__state",

    def __init__(self, state):
        u"""コンストラクタ。
        """
        self.__state = state

    def __repr__(self):
        u"""文字列表現取得。
        """
        return u"<{name}: state:{state}>".format(
            name=self.__class__.__name__, state=self.__state)

    @property
    def state(self):
        u"""ピース状態取得。
        """
        return self.__state
