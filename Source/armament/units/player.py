#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""player.py

Copyright(c)2019 Yukio Kuro
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
            u"<type: {type}, name: {name}, power_ups: {power_up}, "
            u"direction: {direction}, another: {another}>").format(
                type=self.__class__.__name__, name=self._data.name,
                power_up=self.power_up_level,
                direction="Right" if self._is_right else "Left",
                another="Another" if self.__is_another else "Basic")

    def set_equip(self, wp, hlm, armr, acs):
        u"""装備設定。
        """
        import armament.equip as __equip

        class __BrokenEquip(object):
            u"""装備データアダプタ。
            装備の破損を表現する。
            """
            __slots__ = "__data", "__broken"
            __TIME_TO_RECOVERY = 6

            def __init__(self, data):
                u"""コンストラクタ。
                data: 装備データ。
                """
                self.__data = data
                self.__broken = 0

            def __repr__(self):
                u"""文字列表現取得。
                """
                return self.__data.__repr__()

            def get_special(self, lv):
                u"""武器効果取得。
                """
                effect = self.__data.get_special(lv)
                return effect if effect and not self.__is_broken else ()

            def get_sustain(self, turn):
                u"""頭防具効果取得。
                """
                effect = self.__data.get_sustain(turn)
                return effect if effect and not self.__is_broken else ()

            def is_prevents(self, target):
                u"""ブロック変化防止判定。
                """
                if self.__data.is_prevents(target) and not self.__is_broken:
                    return True
                else:
                    return False

            def break_(self):
                u"""破損させる。
                """
                self.__broken = self.__TIME_TO_RECOVERY

            def repair(self):
                u"""修復する。
                修復した場合、Trueを返す。
                """
                if 0 < self.__broken:
                    self.__broken = 0
                    return True
                return False

            @property
            def name(self):
                u"""名前取得。
                """
                return self.__data.name

            @property
            def number(self):
                u"""番号取得。
                """
                return self.__data.number

            @property
            def additional(self):
                u"""アクセサリによるパターン変更リクエストを取得。
                """
                return (
                    self.__data.additional if self.__data.additional and
                    not self.__is_broken else ())

            @property
            def value(self):
                u"""能力値取得。
                """
                return 0 if self.__is_broken else self.__data.value

            @property
            def icon(self):
                u"""画像番号からアイコン取得。
                """
                return self.__data.icon

            @property
            def is_useable(self):
                u"""使用可能状態取得。
                """
                return (
                    False if self.__data.number == 0 else
                    self.__broken <= 0)

            @property
            def __is_broken(self):
                u"""破損状態取得。
                徐々に修復される。
                """
                if 0 < self.__broken:
                    self.__broken -= 1
                    return True
                else:
                    return False
        self.__equip = (
            __BrokenEquip(__equip.get(wp)),
            __BrokenEquip(__equip.get(hlm)),
            __BrokenEquip(__equip.get(armr)),
            __BrokenEquip(__equip.get(acs)))

    def add_effect(self, effect):
        u"""エフェクト追加。
        すでに文字表示エフェクトが存在する場合は、eliminateする。
        """
        if self._effect and not self._effect.is_dead:
            self._effect.eliminate()
            self._effect = None
        self._effect = effect

    def attack(self):
        u"""攻撃処理。
        """
        lv = self._power/self._packet
        power = self.release()
        if 0 < power:
            self.flash()
            stroke = self._get_attack(
                self._data.str+self.weapon.value, self.attack_level, power)
            return stroke, lv
        return 0, 0

    @property
    def _vit(self):
        u"""ユニットの守り＋装備の防御力取得。
        """
        return (
            self._data.vit+self.helm.value +
            self.armor.value+self.accessory.value)

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
        u"""装飾品取得。
        """
        _, _, _, accessory = self.__equip
        return accessory
