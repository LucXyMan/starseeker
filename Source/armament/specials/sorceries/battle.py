#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""battle.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

戦闘関連ソーサリーモジュール。
"""
import random as _random
import sorcery as _sorcery


# ---- Break ----
class Break(_sorcery.Sorcery):
    u"""装備破壊ソーサリー。
    """
    __slots__ = "__target",

    def __init__(self, string, cost, target, catalyst=None):
        u"""コンストラクタ。
        """
        is_agrsv, _target = target
        super(Break, self).__init__(string, cost, is_agrsv, catalyst)
        self.__target = int(_target)

    def activate(self, systems, is_reverse):
        u"""効果発動。
        """
        target, _ = self._get_target(systems, is_reverse)
        is_broken = False
        for i, item in enumerate(target.battle.player.equip):
            if 1 << i & self.__target and item.break_():
                is_broken = True
        if is_broken:
            target.update()

    def is_available(self, params):
        u"""使用可能判定。
        """
        target, _ = self._get_target(params, params[0].has_reverse_sorcery)
        is_fulfill = bool(
            (target.equip_broken_state ^ self.__target) & self.__target)
        return super(Break, self).is_available(params) and is_fulfill


class Delete(_sorcery.Sorcery):
    u"""カード削除ソーサリー。
    """
    __slots__ = "__power",

    def __init__(
        self, string, cost, is_agrsv,
        power=0, catalyst=None
    ):
        u"""コンストラクタ。
        """
        super(Delete, self).__init__(string, cost, is_agrsv, catalyst)
        self.__power = power

    def activate(self, systems, is_reverse):
        u"""効果発動。
        """
        target, _ = self._get_target(systems, is_reverse)
        hand = target.battle.hand
        power = len(hand)*self.__power
        for card in hand[:]:
            hand.remove(card)
        target.resource.disappear(power)

    def is_available(self, params):
        u"""使用可能判定。
        """
        target, _ = self._get_target(params, params[0].has_reverse_sorcery)
        return (
            super(Delete, self).is_available(params) and
            self._rank <= len(target.hand) and not target.jokers)


# ---- Life ----
class Recovery(_sorcery.Sorcery):
    u"""回復ソーサリー。
    """
    __slots__ = "__is_all", "__rate",

    def __init__(self, string, cost, target, rate=1.0, catalyst=None):
        u"""コンストラクタ。
        """
        is_agrsv, is_all = target
        self.__is_all = bool(is_all)
        super(Recovery, self).__init__(string, cost, is_agrsv, catalyst)
        self.__rate = float(rate if rate < 1 else 1)

    def activate(self, systems, is_reverse):
        u"""効果発動。
        """
        target, _ = self._get_target(systems, is_reverse)
        group = target.battle.group
        if group:
            if self.__is_all:
                for unit in group:
                    unit.life_with_effect += int(unit.max_life*self.__rate)
            else:
                unit = group.get_injured(group.get_livings(group))
                if unit:
                    unit.life_with_effect += int(unit.max_life*self.__rate)

    def is_available(self, params):
        u"""使用可能判定。
        """
        target, _ = self._get_target(params, params[0].has_reverse_sorcery)
        return (
            super(Recovery, self).is_available(params) and target.has_damaged)


class Critical(_sorcery.Sorcery):
    u"""即死ソーサリー。
    """
    __slots__ = "__hit_rate", "__is_all", "__is_force"

    def __init__(
        self, string, cost, target,
        hit_rate=1.0, is_force=False, catalyst=None
     ):
        u"""コンストラクタ。
        """
        is_agrsv, is_all = target
        self.__is_all = bool(is_all)
        super(Critical, self).__init__(string, cost, is_agrsv, catalyst)
        self.__hit_rate = float(hit_rate if hit_rate < 1 else 1)
        self.__is_force = bool(is_force)

    def activate(self, systems, is_reverse):
        u"""効果発動。
        """
        target, _ = self._get_target(systems, is_reverse)
        group = target.battle.group
        if group:
            if self.__is_all:
                for unit in group:
                    if (
                        self.__hit_rate <= _random.random() or
                        not unit.die(self.__is_force)
                    ):
                        unit.flash("damage")
            else:
                unit = group.get_healthy(group.get_livings(group))
                if unit and (
                    self.__hit_rate <= _random.random() or
                    not unit.die(self.__is_force)
                ):
                    unit.flash("damage")
            group.destroy()
            target.update()

    def is_available(self, params):
        u"""使用可能判定。
        """
        target, _ = self._get_target(params, params[0].has_reverse_sorcery)
        return super(Critical, self).is_available(params) and target.has_normal


# ---- Unit ----
class _Clone(_sorcery.Sorcery):
    u"""複製ソーサリー。
    """
    __slots__ = ()

    def is_available(self, params):
        u"""使用可能判定。
        """
        target, other = self._get_target(
            params, params[0].has_reverse_sorcery)
        return (
            super(_Clone, self).is_available(params) and
            target.is_group_exsit and not other.is_full_group)


class Double(_Clone):
    u"""分身ソーサリー。
    """
    __slots__ = ()

    def __init__(self, string, cost, is_agrsv, catalyst=None):
        u"""コンストラクタ。
        """
        type_, name, description = string.split("###")
        super(Double, self).__init__(
            type_+"###"+name+"###"+description, cost, is_agrsv, catalyst)

    def activate(self, systems, is_reverse):
        u"""効果発動。
        """
        target, other = self._get_target(systems, is_reverse)
        target_group = target.battle.group
        other_group = other.battle.group
        if target_group and not other_group.is_full:
            unit = _random.choice(target_group)
            if other_group.summon(unit.data):
                other_group[-1].copy_parameter(unit)
                other.update()


class Attract(_Clone):
    u"""引き抜きソーサリー。
    """
    __slots__ = "__hit_rate",

    def __init__(
        self, string, cost, is_agrsv,
        hit_rate=1.0, catalyst=None
    ):
        u"""コンストラクタ。
        """
        type_, name, description = string.split("###")
        super(Attract, self).__init__(
            type_+"###"+name+"###"+description, cost, is_agrsv, catalyst)
        self.__hit_rate = float(hit_rate if hit_rate < 1 else 1)

    def activate(self, systems, is_reverse):
        u"""効果発動。
        """
        target, other = self._get_target(systems, is_reverse)
        target_group = target.battle.group
        other_group = other.battle.group
        if target_group and not other_group.is_full:
            unit = _random.choice(target_group)
            if (
                _random.random() < self.__hit_rate and
                other_group.summon(unit.data)
            ):
                other_group[-1].copy_parameter(unit)
                other.update()
                unit.die(True)
                target_group.destroy()
                target.update()
            else:
                unit.flash("damage")


class Spawn(_sorcery.Sorcery):
    u"""生成ソーサリー。
    """
    __slots__ = "__name", "__is_whole"

    def __init__(
        self, string, cost, is_agrsv,
        is_whole=False, catalyst=None
    ):
        u"""コンストラクタ。
        """
        type_, name, description, self.__name = string.split("###")
        self.__is_whole = bool(is_whole)
        super(Spawn, self).__init__(
            type_+"###"+name+"###"+description, cost, is_agrsv, catalyst)

    def activate(self, systems, is_reverse):
        u"""効果発動。
        """
        import armament.collectible as __collectible
        import armament.units.data as __data
        import utils.const as __const
        import utils.general as __general
        POWER = 300
        target, other = self._get_target(systems, is_reverse)
        group = target.battle.group
        if not group.is_full:
            if not self.__name:
                total = other.resource.total
                summon = __data.Summon(
                    u"##dragon_11##"+__const.DRAGON_TRIBE +
                    u"##ジョーカードラゴン##死神竜#"
                    u"自身の合計スターによって強さが変化",
                    (10+(total << 1), total), (4, -1), POWER+(total << 2),
                    ability=__data.Ability(
                        __const.ADDITION_ABILITY+"###" +
                        __general.get_skill_names(
                            __const.COMPLETE_ASSIST_SKILL)))
                if group.summon(summon):
                    target.update()
            else:
                number, = __collectible.Collectible.get_by_name(self.__name)
                for _ in range(group.empty if self.__is_whole else 1):
                    if group.summon(__collectible.get(number)):
                        target.update()

    def is_available(self, params):
        u"""使用可能判定。
        """
        target, _ = self._get_target(params, params[0].has_reverse_sorcery)
        return (
            super(Spawn, self).is_available(params) and
            not target.is_full_group)
