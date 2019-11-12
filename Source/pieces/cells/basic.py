#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""basic.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

基本ブロックモジュール。
"""
import utils.const as _const
import block as __block


class Basic(__block.Block):
    u"""ベーシックブロック。
    """
    _TARGET_COLOR = "white"

    def __init__(self, point, state, is_virtual):
        u"""コンストラクタ。
        """
        import random as __random
        super(Basic, self).__init__(point, state, is_virtual)
        if state == 0:
            self.__color = __random.randint(0, 7)
            if isinstance(self, (Solid, Adamant)):
                self.__color >>= 1

    def _destroy(self, _field, flag):
        u"""破壊処理。
        """
        if self._is_power_flag(flag):
            self._is_destroyed = True
        else:
            self.__hp += 1
            if self._MAX_HP < self.__hp:
                self._is_destroyed = True

    def paint(self, color):
        u"""ブロックの色付け。
        piece単位で色をつける時に使用する。
        値はpatternによって決定される。
        """
        self.__color = color
        if isinstance(self, (Solid, Adamant)):
            self.__color >>= 1

    @property
    def _current_image(self):
        u"""現在画像取得。
        """
        hp = self.__hp if self.__hp < self._MAX_HP else self._MAX_HP
        color = (
            self.__color << 2 if isinstance(self, Adamant) else
            self.__color << 1 if isinstance(self, Solid) else
            self.__color)
        return self._scaled_images[hp+color]

    @property
    def __hp(self):
        u"""HP取得。
        """
        return self._state & 0b00001111

    @__hp.setter
    def __hp(self, value):
        u"""HP設定。
        """
        self._state = self.__color << 4 | value

    @property
    def __color(self):
        u"""カラー取得。
        """
        return (self._state & 0b11110000) >> 4

    @__color.setter
    def __color(self, value):
        u"""カラー設定。
        """
        self._state = value << 4 | self.__hp


class Normal(Basic):
    u"""ノーマルブロック。
    一回のクラックで破壊できる。
    """
    _SCORE = _const.SINGLE_SCORE
    _IMAGES = "normal"
    _SMALL_IMAGE = "square_0"
    _MAX_HP = 0


class Solid(Basic):
    u"""ソリッドブロック。
    二回のクラックで破壊できる。
    """
    _SCORE = _const.HALF_SCORE
    _IMAGES = "solid"
    _SMALL_IMAGE = "square_9"
    _MAX_HP = 1


class Adamant(Basic):
    u"""アダマントブロック。
    四回のクラックで破壊できる。
    """
    _SCORE = _const.QUARTER_SCORE
    _IMAGES = "adamant"
    _SMALL_IMAGE = "square_8"
    _MAX_HP = 3
