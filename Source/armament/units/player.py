#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""player.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

プレイヤーモジュール。
"""
import unit as __unit
import utils.memoize as _memoize


class Player(__unit.Unit):
    u"""プレイヤー。
    """
    _PLANET = 0
    _ABILITY = []

    def __init__(self, pos, data, packet, group=None):
        u"""コンストラクタ。
        """
        self.__is_another = False
        super(Player, self).__init__(pos, data, packet, group)

    def __repr__(self):
        u"""文字列表現取得。
        """
        return (
            u"<type: {type}, name: {name}, level: {level}, "
            u"direction: {direction}, another: {another}>").format(
                type=self.__class__.__name__, name=self._data.name,
                level=self.level,
                direction="Right" if self._is_right else "Left",
                another="Another" if self.__is_another else "Basic")

    # ---- Equip ----
    def set_equip(self, equip):
        u"""装備設定。
        """
        import armament.equips as __equips

        class __BreakableEquip(object):
            u"""装備アダプタ。
            装備の破損を表現する。
            """
            __slots__ = "__broken", "__equip"
            __TIME_TO_RECOVERY = 24

            def __init__(self, equip):
                u"""コンストラクタ。
                """
                self.__equip = equip
                self.__broken = 0

            def __repr__(self):
                u"""文字列表現取得。
                """
                return self.__equip.__repr__()

            # ---- Ability ----
            def get_enchant(self, lv):
                u"""武器効果取得。
                """
                effect = self.__equip.get_enchant(lv)
                return () if self.__broken else effect

            def get_persistence(self, turn):
                u"""頭防具効果取得。
                """
                effect = self.__equip.get_persistence(turn)
                return () if self.__broken else effect

            def is_prevention(self, target):
                u"""ブロック変化防止判定。
                """
                return (
                    not self.__broken and
                    self.__equip.is_prevention(target))

            # ---- Break and Repair ----
            def break_(self, time=__TIME_TO_RECOVERY):
                u"""破損処理。
                """
                is_broken = False
                if self.__broken <= 0:
                    is_broken = True
                self.__broken = time
                return is_broken

            def repair(self):
                u"""修復処理。
                修復した場合Trueを返す。
                """
                if 0 < self.__broken:
                    self.__broken = 0
                    return True
                return False

            def turn(self):
                u"""毎ターン少しずつ装備修復。
                """
                if 0 < self.__broken:
                    self.__broken -= 1

            # ---- Property ----
            @property
            def name(self):
                u"""名前取得。
                """
                return self.__equip.name

            @property
            def number(self):
                u"""番号取得。
                """
                return self.__equip.number

            @property
            def value(self):
                u"""能力値取得。
                """
                return 0 if self.__broken else self.__equip.value

            @property
            def image_number(self):
                u"""画像番号取得。
                """
                return self.__equip.image_number

            @property
            def icon(self):
                u"""画像番号からアイコン取得。
                """
                return self.__equip.icon

            @property
            def is_available(self):
                u"""使用可能状態取得。
                """
                return (
                    False if self.__equip.number == 0 else
                    self.__broken <= 0)

            # ------ Ability ------
            @property
            def spell(self):
                u"""装飾効果取得。
                """
                return () if self.__broken else self.__equip.spell

            @property
            def skills(self):
                u"""スキル取得。
                """
                return "" if self.__broken else self.__equip.skills
        weapon, head, body, accessory = equip
        self.__equip = (
            __BreakableEquip(__equips.get(weapon)),
            __BreakableEquip(__equips.get(head)),
            __BreakableEquip(__equips.get(body)),
            __BreakableEquip(__equips.get(accessory)))

    def turn(self):
        u"""ターン毎の処理。
        """
        self.count_down()
        for item in self.__equip:
            item.turn()

    # ---- Attack ----
    def attack(self):
        u"""攻撃処理。
        """
        level = self._power/self._packet
        power = self.release()
        if 0 < power:
            self.flash()
            stroke = self._get_attack(
                self._data.str+self.weapon.value, self.attack_level, power)
            return stroke, level
        return 0, 0

    # ---- Update ----
    def add_effect(self, effect):
        u"""エフェクト追加。
        すでに文字表示エフェクトが存在する場合は、eliminateする。
        """
        if self._effect and not self._effect.is_dead:
            self._effect.eliminate()
            self._effect = None
        self._effect = effect

    # ---- Property ----
    @property
    def _vit(self):
        u"""ユニットの守り+装備の防御力取得。
        """
        return (
            self._data.vit+self.helm.value +
            self.armor.value+self.accessory.value)

    # ------ Image ------
    @property
    def base_image(self):
        u"""基本画像取得。
        """
        return self._data.get_image(False, self.__is_another)

    @property
    @_memoize.memoize()
    def current_image(self):
        u"""現在画像取得。
        """
        return self.data.get_image(self.is_right, self.__is_another)

    @property
    def is_another(self):
        u"""アナザー状態取得。
        """
        return self.__is_another

    @is_another.setter
    def is_another(self, value):
        u"""アナザー状態設定。
        """
        self.__is_another = bool(value)
        self.image = self.current_image

    # ------ Equip ------
    @property
    def equip(self):
        u"""装備取得。
        """
        return self.__equip

    @property
    def weapon(self):
        u"""武器取得。
        """
        weapon, _, _, _ = self.__equip
        return weapon

    @property
    def helm(self):
        u"""頭防具取得。
        """
        _, helm, _, _ = self.__equip
        return helm

    @property
    def armor(self):
        u"""体防具取得。
        """
        _, _, armor, _ = self.__equip
        return armor

    @property
    def accessory(self):
        u"""装飾取得。
        """
        _, _, _, accessory = self.__equip
        return accessory

    @property
    def skills(self):
        u"""スキル取得。
        """
        skills = tuple(item.skills for item in self.__equip if item.skills)
        return reduce(lambda x, y: x+"#"+y, skills) if skills else ""
