#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""group.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

クリーチャーグループモジュール。
"""
import creature as _creature
import material.sound as _sound
import utils.layouter as _layouter


class Group(object):
    u"""クリーチャーグループ。
    """
    __LIMIT = 3

    def __init__(self, main, battle):
        u"""コンストラクタ。
        playerとidは位置・向き設定用。
        """
        self.__player = battle.player
        self.__id = main.id
        self.__units = []

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

    def summon(self, info, packet):
        u"""召喚処理。
        """
        if not self.is_full:
            _sound.SE.play("Summon")
            creature = _creature.Creature((0, 0), info, packet)
            creature.is_right = not self.__id
            self.__units.append(creature)
            _layouter.Game.set_creature_init(
                len(self.__units)-1, self.__units, self.__player)
            _layouter.Game.set_creature_dest(
                self.__units, self.__player, self.__id)
            _layouter.Game.set_creature_layer(self.__units)
            creature.flash("Summon")

    def adapt(self, target):
        u"""融合可能クリーチャ取得。
        融合可能クリーチャーが存在する場合、融合後クリーチャーを返す。
        """
        for unit in self.__units:
            fusioned = unit.adapt(target)
            if fusioned:
                return fusioned
        return None

    def fusion(self, info, packet):
        u"""融合処理。
        """
        for i, unit in enumerate(self.__units):
            fusioned = unit.adapt(info)
            if fusioned:
                _sound.SE.play("Fusion")
                unit.kill()
                new = _creature.Creature((0, 0), fusioned, packet)
                new.power = unit.power
                new.power_ups = unit.power_ups
                new.rect.midbottom = new.dest.midbottom = unit.rect.midbottom
                new.is_right = not self.__id
                self.__units[i] = new
                _layouter.Game.set_creature_layer(self.__units)
                new.flash("Summon")
                return None

    def __poison_effect(self):
        u"""毒効果エフェクト。
        """
        for unit in self.__units:
            if unit.is_poison:
                unit.poison_effect()
                unit.flash("Poison")

    def __regenerate(self):
        u"""自己再生効果。
        """
        for unit in self.__units:
            if unit.is_regeneratable:
                unit.regenerate()

    def destroy(self, extinction=False):
        u"""ユニット破壊処理。
        即死魔術使用後にも使用する。
        """
        for unit in self.__units[:]:
            if unit.is_dead or extinction:
                unit.destroy()
                self.__units.remove(unit)
        _layouter.Game.set_creature_dest(
            self.__units, self.__player, self.__id)
        _layouter.Game.set_creature_layer(self.__units)

    def turn(self, extinction=False):
        u"""ターン毎の処理。
        extinctionがTrueの時は全滅。
        """
        for unit in self.__units:
            unit.count_down()
        self.__poison_effect()
        self.__regenerate()
        self.destroy(extinction)

    def receive(self, stroke):
        u"""攻撃を受け取る。
        """
        if self.__units:
            return sum(
                unit.receive(unit.defense(stroke/len(self.__units))) for
                unit in self.__units)
        return stroke

    def charge(self, onepiece):
        u"""チャージ処理。
        """
        for monster in self.__units:
            monster.charge(onepiece)

    def power_plus(self, plus):
        u"""力パワーアップ追加。
        """
        for unit in self.__units:
            unit.power_plus(plus)

    def protect_plus(self, plus):
        u"""守りパワーアップ追加。
        """
        for unit in self.__units:
            unit.protect_plus(plus)

    def speed_plus(self, plus):
        u"""スピードパワーアップ追加。
        """
        for unit in self.__units:
            unit.speed_plus(plus)

    def power_minus(self, minus):
        u"""パワーアップ除去。
        """
        for unit in self.__units:
            unit.power_minus(minus)

    def get_healthy(self, units):
        u"""回復優先度の低いユニットを取得。
        """
        return min(
            units, key=lambda unit: unit.hialing_priority) if units else None

    def get_injured(self, units):
        u"""回復優先度の高いユニットを取得。
        """
        return max(
            units, key=lambda unit: unit.hialing_priority) if units else None

    def get_healths(self, units):
        u"""状態異常以外のユニットを取得。
        """
        return tuple(unit for unit in units if unit.is_healths)

    def is_prevents(self, new):
        u"""状態変化を防止した場合、ユニットをフラッシュして真を返す。
        new: 変化後ブロック。
        """
        for unit in self.__units:
            if new in unit.prevents:
                unit.flash("Ability")
                return True
        return False

    @property
    def healths(self):
        u"""状態異常以外のユニットを取得。
        """
        return self.get_healths(self.__units)

    def get_damaged(self, units):
        u"""ライフ半分のユニットを取得。
        """
        return tuple(unit for unit in units if unit.is_half)

    @property
    def damaged(self):
        u"""ライフ半分のユニットを取得。
        """
        return self.get_damaged(self.__units)

    def get_livings(self, units):
        u"""不死属以外のクリーチャ取得。
        """
        return tuple(unit for unit in units if not unit.is_undead)

    @property
    def is_full(self):
        u"""ユニットが満員状態の時に真。
        """
        return self.__LIMIT <= len(self.__units)

    @property
    def recepters(self):
        u"""融合可能クリーチャー名取得。
        """
        if self.__units:
            return set(reduce(
                lambda x, y: x+y, (unit.recepters for unit in self.__units)))
        return set()
