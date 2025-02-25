#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""accumulate.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ダメージ管理モジュール。
"""
import utils.const as _const


class Accumulate(object):
    u"""ダメージ管理。
    溜まったダメージとエフェクトを処理する。
    """
    __slots__ = "__effects", "__pressure"
    __NUMBER_OF_EFFECT = 4

    def __init__(self):
        u"""プレッシャーと特殊効果リスト作成。
        """
        import collections as __collections
        self.__pressure = 0
        self.__effects = __collections.deque()

    # ---- Pressure ----
    def add_pressure(self, pressure):
        u"""プレッシャー追加。
        """
        value = self.__pressure+pressure
        self.__pressure = (
            value if value < _const.PRESS_LIMIT else _const.PRESS_LIMIT)

    def release_pressure(self):
        u"""プレッシャー開放。
        """
        result, self.__pressure = divmod(self.__pressure, _const.PRESS_POINT)
        return result

    # ---- Effect ----
    def add_effect(self, effect):
        u"""エフェクト追加。
        """
        if effect:
            if self.__NUMBER_OF_EFFECT <= self.effects:
                self.__effects.popleft()
            self.__effects.append(effect)

    def release_effects(self):
        u"""エフェクト開放。
        """
        result = tuple(self.__effects)
        self.__effects.clear()
        return result

    # ---- Property ----
    @property
    def pressure(self):
        u"""負荷取得。
        """
        return self.__pressure

    @property
    def level(self):
        u"""負荷レベル取得。
        """
        return self.__pressure/_const.PRESS_POINT

    @property
    def effects(self):
        u"""エフェクト数取得。
        """
        return len(self.__effects)
