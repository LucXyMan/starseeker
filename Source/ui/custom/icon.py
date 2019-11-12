#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""icon.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

アイコンスプライトモジュール。
"""
import inventory as _inventory
import armament.collectible as _collectible
import material.string as _string
import sprites.general as __general
import utils.image as _image


class _Icon(__general.General):
    u"""アイコンスプライト。
    """
    def __init__(self, pos, item, groups=None):
        u"""コンストラクタ。
        __num: アイテム番号。
        _old: 監視するパラメータ。
        """
        super(_Icon, self).__init__(groups)
        self._number = item.number
        self._old = ()
        self.update()
        self.rect.topleft = pos


class Item(_Icon):
    u"""アイテムアイコン。
    """
    def update(self):
        u"""アイコン更新。
        """
        import armament.equip as __equip
        ep_value = _inventory.SP.get()
        utils_value = _inventory.Utils.get_value()
        level_value = _inventory.Level.get_value()
        items_value = _inventory.Items.get_value()
        skill_value = _inventory.Skill.get_value()
        equip_value = _inventory.Equip.get_value()
        if self._old != (
            ep_value, utils_value, level_value, items_value, skill_value,
            equip_value
        ):
            item = __equip.get(self._number)
            has = _inventory.Items.has(self._number-1)
            chest = __equip.get_chest(item.is_locked, item.rank).icon
            image = ((
                chest if not item.is_sealed else
                _image.get_dull(chest)) if not has else
                item.icon if _inventory.Skill.is_item_equippable(
                    __equip.get(self._number)) else _image.get_dull(item.icon))
            _image.set_colorkey(image, "0x000000")
            subscript = (
                "E" if self._number == _inventory.Equip.get(item.type) else
                "G" if not has and not item.is_locked and
                not item.is_sealed and _inventory.SP.is_buyable(item) else "")
            self.image = _string.get_subscript(image, subscript)
            self._old = (
                ep_value, utils_value, level_value, items_value, skill_value,
                equip_value)
            if hasattr(self, "rect"):
                self.rect.size = self.image.get_size()
            else:
                self.rect = self.image.get_rect()


class Reward(_Icon):
    u"""褒賞カードアイコン。
    取得していないカードはほんのり光る。
    """
    def __init__(self, pos, item, groups=None):
        u"""コンストラクタ。
        """
        self.__is_front = False
        super(Reward, self).__init__(pos, item, groups)

    def update(self):
        u"""アイコン更新。
        """
        is_front = self.__is_front
        cards_value = _inventory.Cards.get_value()
        if self._old != (cards_value, is_front,):
            back, front, _ = _collectible.get(self._number).icons
            self.image = _string.get_subscript(
                front if is_front else back, "")
            got = _inventory.Cards.get(self._number)
            if got < 3:
                self.image = _image.get_colored_add(
                    self.image, hex(0x30 << (2-got) << 16))
            self._old = cards_value, is_front,
            if hasattr(self, "rect"):
                self.rect.size = self.image.get_size()
            else:
                self.rect = self.image.get_rect()

    @property
    def number(self):
        u"""番号取得。
        """
        return self._number

    @property
    def is_front(self):
        u"""表裏取得。
        """
        return self.__is_front

    @is_front.setter
    def is_front(self, value):
        u"""表裏設定。
        """
        self.__is_front = bool(value)


class Card(_Icon):
    u"""カードアイコン。
    """
    def update(self):
        u"""アイコン更新。
        """
        utils_value = _inventory.Utils.get_value()
        skill_value = _inventory.Skill.get_value()
        cards_value = _inventory.Cards.get_value()
        deck_value = _inventory.Deck.get_value()
        if self._old != (cards_value, utils_value, skill_value, deck_value):
            card_number = _inventory.Cards.get(self._number)
            deck_number = _inventory.Deck.get(self._number)
            collection = _collectible.get(self._number)
            back, front, empty = collection.icons
            image = front if deck_number else back if card_number else empty
            _image.set_colorkey(image, "0x000000")
            subscript = (
                str(deck_number) if deck_number else
                str(card_number) if card_number else "")
            self.image = _string.get_subscript(
                image, subscript, _string.ElmCharColor.get(
                    collection.star, not deck_number))
            self._old = cards_value, utils_value, skill_value, deck_value
            if hasattr(self, "rect"):
                self.rect.size = self.image.get_size()
            else:
                self.rect = self.image.get_rect()
