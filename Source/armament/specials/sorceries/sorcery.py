#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""sorcery.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ソーサリーモジュール。
"""
import utils.const as _const
import armament.specials.special as __special


class Sorcery(__special.Special):
    u"""ソーサリー。
    """
    __slots__ = "__catalyst", "_is_agrsv"

    def __init__(self, string, cost, is_agrsv, catalyst=None):
        u"""コンストラクタ。
        """
        type_, name, description = string.split("###")
        type_ = type_ if type_ else _const.SORCERY_ARCANUM
        super(Sorcery, self).__init__(type_+"##"+name+"##"+description, cost)
        self._is_agrsv = bool(is_agrsv)
        if catalyst:
            self.__catalyst = catalyst.recepter,  catalyst.Sorcery(
                catalyst.string, cost, *catalyst.args, **catalyst.kw)
        else:
            self.__catalyst = ()

    def _get_target(self, systems, is_reverse):
        u"""効果対象選択。
        return: target, other.
        """
        myself, rival = systems
        is_agrsv = not self._is_agrsv if is_reverse else self._is_agrsv
        return (rival, myself) if is_agrsv else (myself, rival)

    def is_available(self, params):
        u"""使用可能判定。
        """
        is_arcana_available = (
            super(Sorcery, self).is_available(params) and
            self._type in (_const.SORCERY_ARCANUM, _const.ALTERED_ARCANUM))
        is_joker_available = (
            not params[0].has_purify and self._type == _const.JOKER_ARCANUM)
        return is_arcana_available or is_joker_available

    def adapt(self, catalyst):
        u"""魔法反応可能な場合に反応後ソーサリーを返す。
        そうでない場合Noneを返す。
        """
        if catalyst and self.__catalyst:
            recepter, sorcery = self.__catalyst
            if recepter == catalyst.name:
                return sorcery
        return None

    # ---- Property ----
    @property
    def recepter(self):
        u"""魔法反応対象名取得。
        """
        if self.__catalyst:
            recepter, _ = self.__catalyst
            return recepter
        return ""

    @property
    def altered(self):
        u"""魔法反応後の名前取得。
        """
        if self.__catalyst:
            _, altered = self.__catalyst
            return altered.name
        return ""
