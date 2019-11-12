#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""label.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

アイテムラベルモジュール。
"""
import inventory as _inventory
import sprites.label as __label
import utils.image as _image


class General(__label.Label):
    u"""汎用アイテムラベル。
    """
    def __init__(self, pos, number, groups=None):
        u"""コンストラクタ。
        """
        super(General, self).__init__(groups)
        item = self._get_item(number)
        self.image = self._get_image(item.icon, item.name)
        _image.set_colorkey(self.image, "0x000000")
        self.rect.topleft = pos


class _Item(__label.Label):
    u"""装備アイテムラベル。
    """
    def __init__(self, pos, slot, groups=None):
        u"""コンストラクタ。
        __slot: インベントリの装備位置を表す整数。
        _old: 監視する装備番号。
        """
        super(_Item, self).__init__(groups)
        self._slot = int(slot)
        self._old = -1
        self.update()
        _image.set_colorkey(self.image, "0x000000")
        self.rect.topleft = pos


class Equip(_Item):
    u"""現在装備ラベル。
    """
    def update(self):
        u"""アイコンと名前の更新。
        """
        item = _inventory.Equip.get(self._slot)
        if self._old != item:
            equip = self._get_item(item)
            self.image = self._get_image(equip.icon, equip.name)
            self._old = item


class Skill(_Item):
    u"""現在スキルラベル。
    """
    def update(self):
        u"""アイコンと名前の更新。
        """
        import armament.units as __units
        import armament.skill as __skill
        player = _inventory.Utils.get_player()
        item = _inventory.Skill.has(self._slot)
        if self._old != (player, item):
            try:
                has = _inventory.Skill.has(self._slot)
                learn = __units.get_player(player).learnable[self._slot]
                skill = __skill.get(learn)
                if skill.is_equippable:
                    if has:
                        skill = __skill.get(learn)
                        self.image = self._get_image(skill.icon, skill.name)
                    else:
                        self.image = self._get_image(
                            __skill.get(-2).icon, __skill.get(learn).name)
                else:
                    self.image = self._get_image(
                        __skill.get(-1).icon, __skill.get(learn).name)
            except IndexError:
                skill = __skill.get(-3)
                self.image = self._get_image(skill.icon, skill.name)
            self._old = player, item
