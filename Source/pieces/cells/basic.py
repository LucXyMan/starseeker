#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""basic.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

基本ブロックモジュール。
"""
import block as __block
import utils.const as _const


class Basic(__block.Block):
    u"""ベーシックブロック。
    """
    _TARGET_COLOR = "white"
    __box = []

    @classmethod
    def __get_color(cls):
        u"""ペイント用のくじ引き。
        """
        import random as __random
        if not cls.__box:
            cls.__box = range(_const.BASIC_COLORS)
            __random.shuffle(cls.__box)
        return cls.__box.pop()

    # ---- Completion ----
    def crack(self, flag=0):
        u"""クラック処理。
        """
        if self._is_power_flag(flag):
            self._is_destroyed = True
        else:
            self.hp += 1
            if self._MAX_HP < self.hp:
                self._is_destroyed = True

    # ---- Effect ----
    def paint(self, color=-1):
        u"""着色処理。
        piece単位で色をつける時に使用する。
        値はpatternによって決定される。
        """
        if color == -1:
            color = self.__get_color()
        self.color = color if isinstance(self, Normal) else color >> 1

    # ---- Property ----
    @property
    def _current_image(self):
        u"""現在画像取得。
        """
        hp = self.hp if self.hp < self._MAX_HP else self._MAX_HP
        color = (
            self.color << 2 if isinstance(self, Adamant) else
            self.color << 1 if isinstance(self, Solid) else self.color)
        return self._scaled_images[hp+color]

    @property
    def hp(self):
        u"""HP取得。
        """
        return self._state & 0x0F

    @hp.setter
    def hp(self, value):
        u"""HP設定。
        """
        self._state = self.color << 4 | value

    @property
    def color(self):
        u"""カラー取得。
        """
        return (self._state & 0xF0) >> 4

    @color.setter
    def color(self, value):
        u"""カラー設定。
        """
        self._state = value << 4 | self.hp


class Normal(Basic):
    u"""ノーマルブロック。
    一回のクラックで破壊できる。
    """
    _IMAGES = "normal"
    _MAX_HP = 0
    _SCORE = _const.SINGLE_SCORE
    _SMALL_IMAGE = "square_0"


class Solid(Basic):
    u"""ソリッドブロック。
    二回のクラックで破壊できる。
    """
    _IMAGES = "solid"
    _MAX_HP = 1
    _SCORE = _const.HALF_SCORE
    _SMALL_IMAGE = "square_9"


class Adamant(Basic):
    u"""アダマントブロック。
    四回のクラックで破壊できる。
    """
    _IMAGES = "adamant"
    _MAX_HP = 3
    _SCORE = _const.QUARTER_SCORE
    _SMALL_IMAGE = "square_8"
