#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""collections.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

アイテム・カードコレクションモジュール。
"""
import inventory as __inventory
import utils.const as _const


class Item(__inventory.Inventory):
    u"""アイテム管理。
    """
    __slots__ = ()

    # ---- Detection ----
    @classmethod
    def is_completion(cls):
        u"""クラウン以外のアイテムコンプ判定。
        """
        return all(
            item.category == _const.CROWN_CATEGORY or cls.has(i) for
            i, item in enumerate(cls._equips[1:]))

    @classmethod
    def is_crown_completion(cls):
        u"""クラウンコンプ判定。
        """
        items = cls._equips[1:]
        crowns = sum(
            1 for item in items if
            item.category == _const.CROWN_CATEGORY)
        return crowns-1 <= sum(
            1 for i, item in enumerate(items) if
            item.category == _const.CROWN_CATEGORY and cls.has(i))

    # ---- Getter ----
    @classmethod
    def has(cls, slot):
        u"""位置slotのアイテム状態を取得。
        """
        return cls._item.has(slot)

    @classmethod
    def get_value(cls):
        u"""数値を取得。
        """
        return sum(cls._item.raw)

    # ---- Setter ----
    @classmethod
    def on(cls, slot):
        u"""slotのアイテム状態を設定。
        """
        cls._item.on(slot)


class Card(__inventory.Inventory):
    u"""カード管理。
    """
    __slots__ = ()

    # ---- Detection ----
    @classmethod
    def is_completion(cls):
        u"""コンプリート判定。
        """
        card = cls._card
        return all(cls.get(i) for i in range(len(card)))

    # ---- Getter ----
    @classmethod
    def get(cls, slot):
        u"""位置slotのカード状態取得。
        """
        return cls._card.get(slot)

    @classmethod
    def get_consume(cls, got):
        u"""カード取得に必要なSPを取得。
        """
        return cls._get_require(got)

    @classmethod
    def get_value(cls):
        u"""数値を取得。
        """
        return sum(cls._card.raw)

    # ---- Setter ----
    @classmethod
    def set(cls, slot, value):
        u"""位置slotのカード状態設定。
        """
        cls._card.set(slot, value)
