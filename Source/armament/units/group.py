#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""group.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

クリーチャーグループモジュール。
"""
import creature as _creature
import material.sound as _sound
import utils.layouter as _layouter


class Group(object):
    u"""クリーチャーグループ。
    """
    __slots__ = "__id", "__packet", "__player", "__units"

    def __init__(self, core, player):
        u"""コンストラクタ。
        playerとidは位置・向き設定用。
        """
        self.__id = core.id
        self.__packet = core.puzzle.field.packet
        self.__player = player
        self.__units = []

    def __getitem__(self, key):
        u"""クリーチャー取得。
        """
        return self.__units[key]

    def __iter__(self):
        u"""イテレータ取得。
        """
        return iter(self.__units)

    def __len__(self):
        u"""len()で使用。
        """
        return len(self.__units)

    def __nonzero__(self):
        u"""グループ判定。
        クリーチャが一体でも存在する場合に真。
        """
        return bool(self.__units)

    # ---- Summon ----
    def summon(self, data):
        u"""召喚処理。
        """
        if not self.is_full:
            _sound.SE.play("summon")
            creature = _creature.Creature((0, 0), data, self.__packet)
            creature.is_right = not self.__id
            self.__units.append(creature)
            _layouter.Game.set_creature_init(self.__units[-1], self.__player)
            _layouter.Game.set_creature(self.__units, self.__player, self.__id)
            creature.flash("summon")
            return True
        return False

    def adapt(self, target):
        u"""融合可能クリーチャ取得。
        融合可能クリーチャーが存在する場合、融合後クリーチャーを返す。
        """
        for unit in self.__units:
            fusioned = unit.adapt(target)
            if fusioned:
                return fusioned
        return None

    def fusion(self, data):
        u"""融合処理。
        """
        for i, unit in enumerate(self.__units):
            fusioned = unit.adapt(data)
            if fusioned:
                _sound.SE.play("fusion")
                unit.kill()
                new = _creature.Creature((0, 0), fusioned, self.__packet)
                new.power = unit.power
                new.power_ups = unit.power_ups
                new.rect.midbottom = new.dest.midbottom = unit.rect.midbottom
                new.is_right = not self.__id
                self.__units[i] = new
                _layouter.Game.set_creature(
                    self.__units, self.__player, self.__id)
                new.flash("summon")
                return True
        return False

    # ---- Battle ----
    def charge(self, onepiece):
        u"""チャージ処理。
        """
        for monster in self.__units:
            monster.charge(onepiece)

    def receive(self, stroke):
        u"""攻撃を受け取る。
        """
        if self.__units:
            return sum(
                unit.receive(unit.defense(stroke/len(self.__units))) for
                unit in self.__units)
        return stroke

    # ---- Power Up ----
    def enhance(self, type_, plus):
        u"""パワーアップ追加。
        """
        for unit in self.__units:
            unit.enhance(type_, plus)

    # ---- Turn ----
    def turn(self, is_game_over=False):
        u"""ターン毎の処理。
        is_game_overの時は全滅。
        """
        if not is_game_over:
            for unit in self.__units:
                unit.count_down()
                if unit.is_poison:
                    unit.poison_effect()
                    unit.flash("poison")
                if unit.is_regeneratable:
                    unit.regenerate()
        self.destroy(is_game_over)

    def destroy(self, is_game_over=False):
        u"""ユニット破壊処理。
        """
        for unit in self.__units[:]:
            if unit.is_dead or is_game_over:
                unit.destroy()
                self.__units.remove(unit)
        _layouter.Game.set_creature(self.__units, self.__player, self.__id)

    # ---- Detect ----
    def is_prevention(self, new):
        u"""状態変化を防止した場合に真。
        真の場合にフラッシュする。
        new: 変化後ブロック。
        """
        for unit in self.__units:
            if new in unit.prevents:
                unit.flash("skill")
                return True
        return False

    # ---- Getter ----
    def get_healthy(self, units):
        u"""回復優先度の低いユニットを取得。
        """
        return min(
            units, key=lambda unit: unit.healing_priority) if units else None

    def get_injured(self, units):
        u"""回復優先度の高いユニットを取得。
        """
        return max(
            units, key=lambda unit: unit.healing_priority) if units else None

    def get_healths(self, units):
        u"""状態異常以外のユニットを取得。
        """
        return tuple(unit for unit in units if unit.is_healths)

    def get_damaged(self, units):
        u"""ライフ半分のユニットを取得。
        """
        return tuple(unit for unit in units if unit.is_half)

    def get_livings(self, units):
        u"""不死属以外のクリーチャ取得。
        """
        return tuple(unit for unit in units if not unit.is_undead)

    # ---- Property ----
    @property
    def healths(self):
        u"""状態異常以外のユニットを取得。
        """
        return self.get_healths(self.__units)

    @property
    def damaged(self):
        u"""ライフ半分のユニットを取得。
        """
        return self.get_damaged(self.__units)

    @property
    def recepters(self):
        u"""融合可能クリーチャー名取得。
        """
        if self.__units:
            return set(reduce(
                lambda x, y: x+y, (unit.recepters for unit in self.__units)))
        return set()

    @property
    def skills(self):
        u"""スキル取得。
        """
        skills = tuple(unit.skills for unit in self.__units if unit.skills)
        return reduce(lambda x, y: x+"#"+y, skills) if skills else ""

    # ------ Detect ------
    @property
    def is_full(self):
        u"""ユニットが満員状態の時に真。
        """
        import utils.const as __const
        return __const.FIELD_UNITS <= len(self.__units)
