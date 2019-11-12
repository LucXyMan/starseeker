#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""piece.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

基本ピースモジュール。
"""


class State(object):
    u"""ピースの位置と角度を表す。
    """
    def __init__(self, topleft=(0, 0), angle=0):
        u"""コンストラクタ。
        """
        self.__left, self.__top = topleft
        self.__angle = angle

    def __repr__(self):
        u"""正式な文字列表現を取得。
        """
        return u"<{name}: topleft:{topleft}, angle:{angle}>".format(
            name=self.__class__.__name__, topleft=self.topleft,
            angle={0: u"0", 1: u"90", 2: u"180", 3: u"270"}[self.__angle])

    def __eq__(self, other):
        u"""イコール。
        """
        return self.topleft == other.topleft and self.__angle == other.angle

    def __ne__(self, other):
        u"""ノットイコール。
        """
        return self.topleft != other.topleft or self.__angle != other.angle

    @property
    def left(self):
        u"""左座標取得。
        """
        return self.__left

    @property
    def top(self):
        u"""上座標取得。
        """
        return self.__top

    @property
    def topleft(self):
        u"""左上座標取得。
        """
        return self.left, self.top

    @property
    def angle(self):
        u"""角度取得。
        """
        return self.__angle


class Piece(object):
    u"""基本ピース。
    """
    __slots__ = "_pattern", "_blocks", "_window"

    def __init__(self, pattern):
        u"""コンストラクタ。
        """
        self._pattern = pattern
        self._blocks = []

    def vanish(self):
        u"""ピース消去処理。
        """
        for block in self._blocks:
            block.is_destroyed = True
            block.disappear(delay=block.point.y)

    @property
    def pattern(self):
        u"""パターン取得。
        """
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        u"""パターン設定。
        """
        self._pattern = value

    @property
    def width(self):
        u"""横幅取得。
        """
        return self._pattern.width

    @property
    def height(self):
        u"""高さ取得。
        """
        return self._pattern.height

    @property
    def bottom(self):
        u"""下座標取得。
        """
        return self.top+self.height

    @property
    def size(self):
        u"""サイズ取得。
        """
        return self.width, self.height

    @property
    def blocks(self):
        u"""ピースのブロック。
        """
        return self._blocks[:]

    @property
    def squares(self):
        u"""マス目の数を取得。
        """
        return self.width*self.height

    @property
    def number(self):
        u"""ブロックの数を取得。
        """
        return len(self._blocks)
