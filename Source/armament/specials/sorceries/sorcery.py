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

    def is_usable(self, params):
        u"""使用可能判定。
        params[0]: 自身のパラメータ。
        params[1]: 相手のパラメータ。
        """
        is_sorcery_useable = (
            super(Sorcery, self).is_usable((params[0], params[1])) and
            self._type in (_const.SORCERY_ARCANUM, _const.ALTERED_ARCANUM))
        is_joker_useable = (
            not params[0].has_purify and
            self._type == _const.JOKER_ARCANUM)
        return is_sorcery_useable or is_joker_useable

    def adapt(self, catalyst):
        u"""魔法反応可能な場合に反応後魔術を返す。
        そうでない場合Noneを返す。
        """
        if catalyst and self.__catalyst:
            recepter, sorcery = self.__catalyst
            if recepter == catalyst.name:
                return sorcery
        return None

    @property
    def is_agrsv(self):
        u"""攻勢属性取得。
        """
        return self._is_agrsv

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
