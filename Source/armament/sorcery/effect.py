#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""effect.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

魔術エフェクトモジュール。
"""
import random as _random


class _Effect(object):
    u"""魔術エフェクト。
    魔術で使用するエフェクト。
    """
    __slots__ = "_is_all",

    def __init__(self, is_all):
        u"""対象を決定する。
        """
        self._is_all = is_all

    @property
    def is_all(self):
        u"""全体効果判定取得。
        """
        return self._is_all

    @is_all.setter
    def is_all(self, value):
        u"""全体効果判定設定。
        """
        self._is_all = bool(value)


class Recovery(_Effect):
    u"""回復エフェクト。
    """
    __slots__ = "__rate",

    def __init__(self, rate, is_all):
        u"""対象と回復量を設定する。
        __rateが1の場合、全回復。0.5の場合半分だけ回復する。
        """
        super(Recovery, self).__init__(is_all)
        self.__rate = float(rate if rate <= 1 else 1)

    def use(self, system, _other):
        u"""効果発動。
        """
        group = system.battle.group
        if group:
            if self._is_all:
                for unit in group:
                    unit.life += int(unit.max_life*self.__rate)
            else:
                unit = group.get_injured(group.get_livings(group))
                if unit:
                    unit.life += int(unit.max_life*self.__rate)


class Forming(_Effect):
    u"""ブロックエフェクト。
    """
    __slots__ = "__new", "__old", "__param"

    def __init__(self, target, param):
        u"""対象を決定する。
        """
        new, old = target.split("##")
        self.__new = new
        self.__old = tuple(name for name in old.split("#"))
        self.__param = param

    def use(self, system, _other):
        u"""効果発動。
        """
        if system.battle.player.armor.is_prevents(self.__new):
            _, _, armor_info, _ = system.battle.equip_info
            armor_info.flash()
        elif (
            not system.battle.group.is_prevents(self.__new) and
            system.blocks.field.replace(self.__param, (self.__new, self.__old))
        ):
            system.blocks.skip()


class Poison(_Effect):
    u"""毒エフェクト。
    """
    __slots__ = ()

    def use(self, system, _other):
        u"""効果発動。
        """
        healths = system.battle.group.healths
        if healths:
            if self._is_all:
                for unit in healths:
                    unit.poisoning()
                    unit.flash("Damage")
            else:
                unit = _random.choice(healths)
                unit.poisoning()
                unit.flash("Damage")


class Frozen(_Effect):
    u"""凍結エフェクト。
    """
    __slots__ = ()

    def use(self, system, _other):
        u"""効果発動。
        """
        healths = system.battle.group.healths
        if healths:
            if self._is_all:
                for unit in healths:
                    unit.freezing()
                    unit.flash("Damage")
            else:
                unit = _random.choice(healths)
                unit.freezing()
                unit.flash("Damage")


class Critical(_Effect):
    u"""即死エフェクト。
    """
    __slots__ = "__is_force",

    def __init__(self, is_all, is_force=False):
        u"""対象を決定する。
        __is_force: 強制キルするかを決定する。
        """
        super(Critical, self).__init__(is_all)
        self.__is_force = is_force

    def use(self, system, _other):
        u"""効果発動。
        """
        group = system.battle.group
        if group:
            if self._is_all:
                for unit in group:
                    if not unit.death(self.__is_force):
                        unit.flash("Damage")
            else:
                unit = group.get_healthy(group.get_livings(group))
                if not unit.death(self.__is_force):
                    unit.flash("Damage")
            for card in system.battle.hand:
                card.set_available()
            group.destroy()


class Delete(_Effect):
    u"""カード削除エフェクト。
    """
    __slots__ = "__is_force",

    def __init__(self, is_all):
        u"""対象を決定する。
        __is_force: 強制削除するかを決定する。
        """
        super(Delete, self).__init__(is_all)

    def use(self, system, _other):
        u"""効果発動。
        """
        system.battle.discard(self._is_all)


class Star(_Effect):
    u"""スターエフェクト。
    """
    __slots__ = "__target", "__add"

    def __init__(self, target, add):
        u"""対象を決定する。
        """
        self.__target = target
        self.__add = add

    def use(self, system, _other):
        u"""効果発動。
        """
        if self.__target == -1 and self.__add == -99:
            system.resorce.init_stars()
        else:
            system.resorce.add_star(self.__target, self.__add)


class Hold(_Effect):
    u"""ホールドエフェクト。
    """
    __slots__ = "__is_single", "__target"

    def __init__(self, is_single, target):
        u"""対象を決定する。
        """
        self.__target = target
        self.__is_single = is_single

    def use(self, system, _other):
        u"""効果発動。
        """
        system.blocks.hold.change(self.__is_single, self.__target)


class Exchange(_Effect):
    u"""ピース交換エフェクト。
    """
    __slots__ = ()

    def use(self, system, other):
        u"""効果発動。
        """
        system.blocks.hold.exchange(other.blocks.hold)


class Equip(_Effect):
    u"""装備破壊エフェクト。
    """
    __slots__ = "__target"

    def __init__(self, target):
        u"""対象を決定する。
        """
        self.__target = target

    def use(self, system, _other):
        u"""効果発動。
        """
        for i, item in enumerate(system.battle.player.equip):
            if 1 << i & self.__target:
                item.break_()
