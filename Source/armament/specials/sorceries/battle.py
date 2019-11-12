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

    def is_usable(self, params):
        u"""使用可能判定。
        """
        is_agrsv = (
            not self._is_agrsv if params[0].has_reverse_sorcery else
            self._is_agrsv)
        param = params[1] if is_agrsv else params[0]
        is_fulfill = bool(
            (param.equip_broken_state ^ self.__target) & self.__target)
        return (
            super(Break, self).is_usable((params[0], params[1])) and
            is_fulfill)

    def use(self, systems, is_exist):
        u"""効果発動。
        """
        for i, item in enumerate(systems[0].battle.player.equip):
            if 1 << i & self.__target:
                item.break_()


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

    def use(self, systems, is_exist):
        u"""効果発動。
        """
        for _ in range(systems[0].battle.destroy()*self.__power):
            if not systems[0].resorce.disappear():
                break

    def is_usable(self, params):
        u"""使用可能判定。
        """
        is_agrsv = (
            not self._is_agrsv if params[0].has_reverse_sorcery else
            self._is_agrsv)
        param = params[1] if is_agrsv else params[0]
        return (
            super(Delete, self).is_usable((params[0], params[1])) and
            self._rank <= len(param.hand) and not param.jokers)


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

    def use(self, systems, is_exist):
        u"""効果発動。
        """
        group = systems[0].battle.group
        if group:
            if self.__is_all:
                for unit in group:
                    unit.life_with_effect += int(unit.max_life*self.__rate)
            else:
                unit = group.get_injured(group.get_livings(group))
                if unit:
                    unit.life_with_effect += int(unit.max_life*self.__rate)

    def is_usable(self, params):
        u"""使用可能判定。
        """
        is_agrsv = (
            not self._is_agrsv if params[0].has_reverse_sorcery else
            self._is_agrsv)
        param = params[1] if is_agrsv else params[0]
        return (
            super(Recovery, self).is_usable((params[0], params[1])) and
            param.has_damaged)


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

    def use(self, systems, is_exist):
        u"""効果発動。
        """
        group = systems[0].battle.group
        if group:
            if self.__is_all:
                for unit in group:
                    if (
                        self.__hit_rate <= _random.random() or
                        not unit.death(self.__is_force)
                    ):
                        unit.flash("damage")
            else:
                unit = group.get_healthy(group.get_livings(group))
                if unit and (
                    self.__hit_rate <= _random.random() or
                    not unit.death(self.__is_force)
                ):
                    unit.flash("damage")
            group.destroy()
            systems[0].battle.update()

    def is_usable(self, params):
        u"""使用可能判定。
        """
        is_agrsv = (
            not self._is_agrsv if params[0].has_reverse_sorcery else
            self._is_agrsv)
        param = params[1] if is_agrsv else params[0]
        return (
            super(Critical, self).is_usable((params[0], params[1])) and
            param.has_normal)


# ---- Unit ----
class _Clone(_sorcery.Sorcery):
    u"""複製ソーサリー。
    """
    __slots__ = ()

    def is_usable(self, params):
        u"""使用可能判定。
        """
        def __is_fulfill(params):
            u"""条件判定。
            """
            return params[1].is_group_exsit and not params[0].is_full_group
        is_agrsv = (
            not self._is_agrsv if params[0].has_reverse_sorcery else
            self._is_agrsv)
        return (
            super(_Clone, self).is_usable((params[0], params[1])) and
            __is_fulfill(params if is_agrsv else params[::-1]))


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

    def use(self, systems, is_exist):
        u"""効果発動。
        """
        target = systems[0].battle.group
        receive = systems[1].battle.group
        if target:
            unit = _random.choice(target)
            if receive.summon(unit.data):
                receive[-1].copy_parameter(unit)


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

    def use(self, systems, is_exist):
        u"""効果発動。
        """
        target = systems[0].battle.group
        receive = systems[1].battle.group
        if target:
            unit = _random.choice(target)
            if (
                _random.random() < self.__hit_rate and
                receive.summon(unit.data)
            ):
                receive[-1].copy_parameter(unit)
                unit.death(True)
                target.destroy()
            else:
                unit.flash("damage")


class Spawn(_sorcery.Sorcery):
    u"""生成ソーサリー。
    """
    __slots__ = "__name", "__is_all"

    def __init__(
        self, string, cost, is_agrsv,
        is_all=False, catalyst=None
    ):
        u"""コンストラクタ。
        """
        type_, name, description, self.__name = string.split("###")
        self.__is_all = bool(is_all)
        super(Spawn, self).__init__(
            type_+"###"+name+"###"+description, cost, is_agrsv, catalyst)

    def use(self, systems, is_exist):
        u"""効果発動。
        """
        import armament.collectible as __collectible
        import armament.units.data as __data
        import utils.const as __const

        def __get_name(skill):
            u"""スキル名取得。
            """
            name, _ = skill.split("#")
            return name
        name = _random.choice((
            u"ジョーカードラゴン", u"ジョーカーフライ"
        )) if not self.__name else self.__name
        total = systems[1].resorce.total
        if name == u"ジョーカードラゴン":
            summon = __data.Summon(
                u"##dragon_11##"+__const.DRAGON_TRIBE +
                u"##ジョーカードラゴン##死神竜#"
                u"相手の合計スターによって強さが変わる",
                (10+(total >> 4), 10+(total >> 3)),
                (1+(total >> 6), 5), 300+total, ability=__data.Ability(
                    __const.ADDITION_ABILITY+"###" +
                    __get_name(__const.COMPLETE_ASSIST_SKILL)))
            systems[0].battle.group.summon(summon)
        elif name == u"ジョーカーフライ":
            summon = __data.Summon(
                u"##fly_15##"+__const.SKY_TRIBE +
                u"##ジョーカーフライ##死神バエ#"
                u"相手の合計スターによって強さが変わる",
                (10+(total >> 5), 10+(total >> 4)),
                (1+(total >> 6), 5), 300+(total >> 1))
            for _ in range(__const.FIELD_UNITS):
                systems[0].battle.group.summon(summon)
        else:
            number, = __collectible.Collectible.get_by_name(self.__name)
            for _ in range(__const.FIELD_UNITS if self.__is_all else 1):
                systems[0].battle.group.summon(__collectible.get(number))

    def is_usable(self, params):
        u"""使用可能判定。
        """
        is_agrsv = (
            not self._is_agrsv if params[0].has_reverse_sorcery else
            self._is_agrsv)
        param = params[1] if is_agrsv else params[0]
        return (
            super(Spawn, self).is_usable((params[0], params[1])) and
            not param.is_full_group)
