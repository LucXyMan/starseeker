#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""label.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

アイテムラベルモジュール。
"""
import inventories as _inventories
import sprites.huds as __huds
import utils.image as _image


class __Label(__huds.HUD):
    u"""ラベルスプライト。
    アイコンと名前を持つラベル。
    """
    def _get_item(self, number):
        u"""ラベル画像に使用するアイテム取得。
        """
        import armament.equips as __equips
        return __equips.get(number)

    def _get_image(self, icon, name):
        u"""画像取得。
        """
        import pygame as __pygame
        import material.string as __string
        import utils.const as __const
        import utils.image as __image
        icon_x, icon_y = icon.get_size()
        name = __string.get_string(
            name, __const.SYSTEM_CHAR_SIZE, shorten=False)
        name_x, name_y = name.get_size()
        h = max(icon_y, name_y)
        image = __pygame.Surface((icon_x+name_x, h))
        __image.set_colorkey(image, "0x000000")
        if hasattr(self, "rect"):
            self.rect.size = image.get_size()
        else:
            self.rect = image.get_rect()
        image.blit(icon, (0, 0))
        image.blit(name, (
            icon_x, h-min(icon_y, __const.SYSTEM_CHAR_SIZE) >> 1))
        return image


class General(__Label):
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


class _Customize(__Label):
    u"""カスタムラベル。
    """
    def __init__(self, pos, slot, groups=None):
        u"""コンストラクタ。
        __slot: インベントリの装備位置を表す整数。
        _old: 監視する装備番号。
        """
        super(_Customize, self).__init__(groups)
        self._slot = int(slot)
        self._old = -1
        self.update()
        _image.set_colorkey(self.image, "0x000000")
        self.rect.topleft = pos


class Equip(_Customize):
    u"""現在装備ラベル。
    """
    def update(self):
        u"""アイコンと名前の更新。
        """
        item = _inventories.Equip.get(self._slot)
        if self._old != item:
            equip = self._get_item(item)
            self.image = self._get_image(equip.icon, equip.name)
            self._old = item


class Skill(_Customize):
    u"""現在スキルラベル。
    """
    def update(self):
        u"""アイコンと名前の更新。
        """
        import armament.units as __units
        import armament.skill as __skill
        player = _inventories.Utils.get_player()
        item = _inventories.Skill.has(self._slot)
        if self._old != (player, item):
            try:
                learn = __units.get_player(player).learnable[self._slot]
                skill = __skill.get(learn)
                if skill.is_equippable:
                    if item:
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
