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

    def activate(self, systems, is_reverse):
        u"""効果発動。
        """
        target, _ = self._get_target(systems, is_reverse)
        new, old = self.__target.split("##")
        if target.battle.player.armor.is_prevention(new):
            _, _, armor, _ = target.battle.equip_huds
            armor.flash()
        elif (
            not target.battle.group.is_prevention(new) and
            target.puzzle.field.replace(
                (1, 1) if self.__power == 0 else
                (self.__power, self.__power+1),
                (new, tuple(name for name in old.split("#"))))
        ):
            target.puzzle.skip()

    def is_available(self, params):
        u"""使用可能判定。
        """
        target, _ = self._get_target(params, params[0].has_reverse_sorcery)
        _, field = target.field
        _, old = self.__target.split("##")
        if self.__is_strictly:
            is_fulfill = any((block_name in (
                name for name, _, _ in (block for _, block in field))) for
                block_name in old.split("#"))
        else:
            is_fulfill = target.field_one_eighth < sum((tuple(
                name for name, _, _ in (block for _, block in field)
            ).count(block_name)) for block_name in old.split("#"))
        return super(Forming, self).is_available(params) and is_fulfill


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

    def activate(self, systems, is_reverse):
        u"""効果発動。
        """
        target, _ = self._get_target(systems, is_reverse)
        if target.puzzle.field.harden():
            target.puzzle.skip()

    def is_available(self, params):
        u"""使用可能判定。
        """
        target, _ = self._get_target(params, params[0].has_reverse_sorcery)
        _, field = target.field
        is_fulfill = target.field_one_eighth < sum((tuple(
            name for name, _, _ in (block for _, block in field)
        ).count(block_name)) for block_name in ("Normal", "Solid"))
        return (
            super(Hardening, self).is_available((params[0], params[1])) and
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

    def activate(self, systems, is_reverse):
        u"""効果発動。
        """
        target, _ = self._get_target(systems, is_reverse)
        if target.battle.group:
            healths = target.battle.group.healths
            if healths:
                if self.__is_all:
                    for unit in healths:
                        unit.freeze()
                        unit.flash("damage")
                else:
                    unit = _random.choice(healths)
                    unit.freeze()
                    unit.flash("damage")
                target.update()
        else:
            super(Freeze, self).activate(systems, is_reverse)

    def is_available(self, params):
        u"""使用可能判定。
        """
        target, _ = self._get_target(params, params[0].has_reverse_sorcery)
        return (
            _sorcery.Sorcery.is_available(self, params) and
            target.has_health if target.is_group_exsit else
            super(Freeze, self).is_available(params))


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

    def activate(self, systems, is_reverse):
        u"""効果発動。
        """
        target, _ = self._get_target(systems, is_reverse)
        group = target.battle.group
        if group:
            healths = group.healths
            if healths:
                if self.__is_all:
                    for unit in healths:
                        unit.poison()
                        unit.flash("damage")
                else:
                    unit = _random.choice(healths)
                    unit.poison()
                    unit.flash("damage")
        else:
            super(Poison, self).activate(systems, is_reverse)

    def is_available(self, params):
        u"""使用可能判定。
        アンデッド以外の健康なクリーチャーが存在する場合使用する。
        """
        is_reverse = params[0].has_reverse_sorcery
        target, _ = self._get_target(params, is_reverse)
        is_fulfill = target.has_health if is_reverse else target.has_normal
        return (
            _sorcery.Sorcery.is_available(self, params) and
            is_fulfill if target.is_group_exsit else
            super(Poison, self).is_available(params))


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

    def activate(self, systems, is_reverse):
        u"""効果発動。
        """
        target, _ = self._get_target(systems, is_reverse)
        target.puzzle.hold.change(self.__is_single, self.__target)


class Unlock(Hold):
    u"""アンロックソーサリー。
    ホールドソーサリーに判定を追加。
    """
    __slots__ = ()

    def is_available(self, params):
        u"""使用可能判定。
        """
        target, _ = self._get_target(params, params[0].has_reverse_sorcery)
        is_fulfill = (
            not target.has_phantom_thief and
            target.hold_item_state & 0b0011 == 0b0011 and
            target.has_alone_chest)
        return super(Unlock, self).is_available(params) and is_fulfill


class Exchange(_sorcery.Sorcery):
    u"""ホールド交換ソーサリー。
    """
    __slots__ = ()

    def __init__(self, string, cost, catalyst=None):
        u"""コンストラクタ。
        """
        super(Exchange, self).__init__(string, cost, True, catalyst)

    def activate(self, systems, is_reverse):
        u"""効果発動。
        """
        myself, rival = systems
        myself.puzzle.hold.exchange(rival.puzzle.hold)

    def is_available(self, params):
        u"""使用可能判定。
        """
        myself, rival = params
        is_exist = (
            myself.hold_item_state & 0b0001 and
            rival.hold_item_state & 0b0001)
        is_fulfill = 2 < (
            (not bool(myself.hold_item_state & 0b0100)) +
            bool(myself.hold_item_state & 0b1000) +
            bool(rival.hold_item_state & 0b0100) +
            (not bool(rival.hold_item_state & 0b1000))
        ) if is_exist else False
        return super(Exchange, self).is_available(
            (myself, rival)) and is_fulfill


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

    def activate(self, systems, is_reverse):
        u"""効果発動。
        """
        target, _ = self._get_target(systems, is_reverse)
        target.puzzle.field.add_demon()
