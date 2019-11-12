#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""piece.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ピース関連ソーサリーモジュール。
"""
import random as _random
import sorcery as _sorcery


# ---- Field ----
class Forming(_sorcery.Sorcery):
    u"""フォーミングソーサリー。
    """
    __slots__ = "__is_strictly", "__power", "__target"

    def __init__(
        self, string, cost, is_agrsv, power,
        is_strictly=False, catalyst=None
    ):
        u"""コンストラクタ。
        """
        type_, name, description, self.__target = string.split("###")
        super(Forming, self).__init__(
            type_+"###"+name+"###"+description, cost, is_agrsv, catalyst)
        self.__power = power
        self.__is_strictly = bool(is_strictly)

    def use(self, systems, is_exist):
        u"""効果発動。
        """
        new, old = self.__target.split("##")
        if systems[0].battle.player.armor.is_prevention(new):
            _, _, armor_info, _ = systems[0].battle.equip
            armor_info.flash()
        elif (
            not systems[0].battle.group.is_prevention(new) and
            systems[0].puzzle.field.replace(
                (1, 1) if self.__power == 0 else
                (self.__power, self.__power+1),
                (new, tuple(name for name in old.split("#"))))
        ):
            systems[0].puzzle.skip()

    def is_usable(self, params):
        u"""使用可能判定。
        """
        is_agrsv = (
            not self._is_agrsv if params[0].has_reverse_sorcery else
            self._is_agrsv)
        param = params[1] if is_agrsv else params[0]
        _, field = param.field
        _, old = self.__target.split("##")
        if self.__is_strictly:
            is_fulfill = any((block_name in (
                name for name, _, _ in (block for _, block in field))) for
                block_name in old.split("#"))
        else:
            is_fulfill = param.field_one_eighth < sum((tuple(
                name for name, _, _ in (block for _, block in field)
            ).count(block_name)) for block_name in old.split("#"))
        return (
            super(Forming, self).is_usable((params[0], params[1])) and
            is_fulfill)


class Hardening(_sorcery.Sorcery):
    u"""ハードニングソーサリー。
    """
    __slots__ = "__name",

    def __init__(self, string, cost, is_agrsv, catalyst=None):
        u"""コンストラクタ。
        """
        type_, name, description = string.split("###")
        super(Hardening, self).__init__(
            type_+"###"+name+"###"+description, cost, is_agrsv, catalyst)

    def use(self, systems, is_exist):
        u"""効果発動。
        """
        if systems[0].puzzle.field.hardening(0):
            systems[0].puzzle.skip()

    def is_usable(self, params):
        u"""使用可能判定。
        """
        is_agrsv = (
            not self._is_agrsv if params[0].has_reverse_sorcery else
            self._is_agrsv)
        param = params[1] if is_agrsv else params[0]
        _, field = param.field
        is_fulfill = param.field_one_eighth < sum((tuple(
            name for name, _, _ in (block for _, block in field)
        ).count(block_name)) for block_name in "Normal#Solid".split("#"))
        return (
            super(Hardening, self).is_usable((params[0], params[1])) and
            is_fulfill)


# ------ Status Effect ------
class Freeze(Forming):
    u"""凍結ソーサリー。
    """
    __slots__ = "__is_all",

    def __init__(
        self, string, cost, target, power,
        is_strictly=False, catalyst=None
    ):
        u"""コンストラクタ。
        """
        is_agrsv, is_all = target
        self.__is_all = bool(is_all)
        super(Freeze, self).__init__(
            string, cost, is_agrsv, power, is_strictly, catalyst)

    def use(self, systems, is_exist):
        u"""効果発動。
        """
        if is_exist:
            healths = systems[0].battle.group.healths
            if healths:
                if self.__is_all:
                    for unit in healths:
                        unit.freezing()
                        unit.flash("damage")
                else:
                    unit = _random.choice(healths)
                    unit.freezing()
                    unit.flash("damage")
        else:
            super(Freeze, self).use(systems, is_exist)

    def is_usable(self, params):
        u"""使用可能判定。
        """
        is_agrsv = (
            not self._is_agrsv if params[0].has_reverse_sorcery else
            self._is_agrsv)
        param = params[1] if is_agrsv else params[0]
        return (
            _sorcery.Sorcery.is_usable(self, (params[0], params[1])) and
            param.has_health if param.is_group_exsit else
            super(Freeze, self).is_usable((params[0], params[1])))


class Poison(Forming):
    u"""毒ソーサリー。
    """
    __slots__ = "__is_all",

    def __init__(
        self, string, cost, target, power,
        is_strictly=False, catalyst=None
    ):
        u"""コンストラクタ。
        """
        is_agrsv, is_all = target
        self.__is_all = bool(is_all)
        super(Poison, self).__init__(
            string, cost, is_agrsv, power, is_strictly, catalyst)

    def use(self, systems, is_exist):
        u"""効果発動。
        """
        if is_exist:
            healths = systems[0].battle.group.healths
            if healths:
                if self.__is_all:
                    for unit in healths:
                        unit.poisoning()
                        unit.flash("damage")
                else:
                    unit = _random.choice(healths)
                    unit.poisoning()
                    unit.flash("damage")
        else:
            super(Poison, self).use(systems, is_exist)

    def is_usable(self, params):
        u"""使用可能判定。
        アンデッド以外の健康なクリーチャーが存在する場合使用する。
        """
        is_agrsv = (
            not self._is_agrsv if params[0].has_reverse_sorcery else
            self._is_agrsv)
        param = params[1] if is_agrsv else params[0]
        is_fulfill = (
            param.has_health if params[0].has_reverse_sorcery else
            param.has_normal)
        return (
            _sorcery.Sorcery.is_usable(self, (params[0], params[1])) and
            is_fulfill if param.is_group_exsit else
            super(Poison, self).is_usable((params[0], params[1])))


# ---- Hold ----
class Hold(_sorcery.Sorcery):
    u"""ホールドソーサリー。
    """
    __slots__ = "__is_single", "__target"

    def __init__(self, string, cost, target, catalyst=None):
        u"""コンストラクタ。
        """
        is_agrsv, is_single = target
        self.__is_single = bool(is_single)
        type_, name, description, self.__target = string.split("###")
        super(Hold, self).__init__(
            type_+"###"+name+"###"+description, cost, is_agrsv, catalyst)

    def use(self, systems, is_exist):
        u"""効果発動。
        """
        systems[0].puzzle.hold.change(self.__is_single, self.__target)


class Unlock(Hold):
    u"""アンロックソーサリー。
    ホールドソーサリーに判定を追加。
    """
    __slots__ = ()

    def is_usable(self, params):
        u"""使用可能判定。
        """
        is_agrsv = (
            not self._is_agrsv if params[0].has_reverse_sorcery else
            self._is_agrsv)
        param = params[1] if is_agrsv else params[0]
        is_fulfill = (
            not param.has_phantom_thief and
            param.hold_item_state & 0b0011 == 0b0011 and
            param.has_alone_chest)
        return (
            super(Unlock, self).is_usable((params[0], params[1])) and
            is_fulfill)


class Exchange(_sorcery.Sorcery):
    u"""ホールド交換ソーサリー。
    """
    __slots__ = ()

    def __init__(self, string, cost, catalyst=None):
        u"""コンストラクタ。
        """
        super(Exchange, self).__init__(string, cost, True, catalyst)

    def use(self, systems, is_exist):
        u"""効果発動。
        """
        systems[0].puzzle.hold.exchange(systems[1].puzzle.hold)

    def is_usable(self, params):
        u"""使用可能判定。
        """
        is_exist = (
            params[0].hold_item_state & 0b0001 and
            params[1].hold_item_state & 0b0001)
        is_fulfill = 2 < (
            (not bool(params[0].hold_item_state & 0b0100)) +
            bool(params[0].hold_item_state & 0b1000) +
            bool(params[1].hold_item_state & 0b0100) +
            (not bool(params[1].hold_item_state & 0b1000))
        ) if is_exist else False
        return (
            super(Exchange, self).is_usable((params[0], params[1])) and
            is_fulfill)


# ---- Joker ----
class KingDemon(_sorcery.Sorcery):
    u"""悪魔王ジョーカー。
    """
    __slots__ = "__name",

    def __init__(self, string):
        u"""コンストラクタ。
        """
        type_, name, description, self.__name = string.split("###")
        super(KingDemon, self).__init__(
            type_+"###"+name+"###"+description, (1, -1), False)

    def use(self, systems, is_exist):
        u"""効果発動。
        """
        systems[0].puzzle.field.add_demon()
