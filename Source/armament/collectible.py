#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""collectible.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

カードコレクションモジュール。
"""


class Collectible(object):
    u"""カードコレクション。
    スター属性の並びは木、火、土、金、水、月、日。
    """
    __slots__ = "_name", "_description", "_rank", "_star", "_type"

    @classmethod
    def get_collections(cls):
        u"""コレクション取得。
        """
        return Collectible.__collections[:]

    @classmethod
    def set_collections(cls, value):
        u"""コレクション設定。
        """
        Collectible.__collections = tuple(value)

    @classmethod
    def get_collection(cls, key):
        u"""コレクション要素取得。
        """
        return Collectible.__collections[key]

    @classmethod
    def get_by_name(cls, *names):
        u"""カード名による番号取得。
        """
        result = []
        for name in names:
            for collection in Collectible.__collections:
                if name == collection.name:
                    break
            else:
                raise ValueError("Name not found.")
            result.append(collection.number)
        return tuple(result)

    # ---- Getter ----
    def get_costs(self, division):
        u"""コスト取得。
        """
        import utils.const as __const
        energy = __const.STAR_ENERGY >> division
        if self._star == -1 or self._rank == 0:
            return (-1, 0),
        costs = (self._star, self._rank*energy),
        if self._star == 6:
            costs += tuple((i, (self._rank+1)*energy) for i in range(5))
        elif self._star == 5:
            costs += (6, (self._rank+1)*energy),
        else:
            costs += ((self._star-1) % 5, (self._rank+1)*energy),
            costs += (5, (self._rank+1)*energy),
        return costs

    def get_enchant(self, level):
        u"""追加効果取得。
        """
        return ()

    def get_persistence(self, turn):
        u"""持続効果取得。
        """
        return ()

    def get_special(self, turn):
        u"""特殊効果取得。
        """
        return ""

    # ---- Property ----
    @property
    def number(self):
        u"""番号取得
        """
        return Collectible.__collections.index(self)

    @property
    def name(self):
        u"""名前取得。
        """
        return self._name

    @property
    def type(self):
        u"""種類取得。
        """
        return self._type

    @property
    def rank(self):
        u"""ランク取得。
        """
        return self._rank

    @property
    def star(self):
        u"""スター数値取得。
        木:0, 火:1, 土:2, 金:3, 水:4, 月:5, 日:6
        """
        return self._star

    @property
    def description(self):
        u"""概要取得。
        """
        return self._description

    @property
    def skills(self):
        u"""カードスキル取得。
        """
        return ""

    @property
    def subscript(self):
        u"""カード添字取得。
        """
        return ""

    # ------ Detection ------
    def is_available(self, params):
        u"""使用可能判定。
        """
        myself, _ = params
        return bool(myself.resource.get_available_state(self) & 0x00F)


def init():
    u"""コレクション初期化。
    """
    import units as __units
    import specials as __specials
    import utils.const as __const
    Collectible.set_collections(__units.get_summons()+__specials.get())
    if __const.IS_OUTPUT:
        print u"Collections"
        for i, collection in enumerate(Collectible.get_collections()):
            print i, u":",  unicode(collection)


get = Collectible.get_collection
get_all = Collectible.get_collections
get_by_name = Collectible.get_by_name
