#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""collectible.py

Copyright(c)2019 Yukio Kuro
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

    def get_costs(self, cut):
        u"""エレメンタルコストを取得。
        """
        import utils.const as __const
        cost = [0, 0, 0, 0, 0, 0, 0]
        if self._rank == 0 or self._star == -1:
            return cost,
        else:
            cost[self._star] = self._rank*(__const.STAR_ENERGY >> cut)
            costs = cost,
        if self._star == 6:
            for i in range(5):
                c = [0, 0, 0, 0, 0, 0, 0]
                c[i] = (self._rank+1)*(__const.STAR_ENERGY >> cut)
                costs += c,
        elif self._star == 5:
            c = [0, 0, 0, 0, 0, 0, 0]
            c[6] = (self._rank+1)*(__const.STAR_ENERGY >> cut)
            costs += c,
        else:
            c = [0, 0, 0, 0, 0, 0, 0]
            c[(self._star-1) % 5] = (self._rank+1)*(__const.STAR_ENERGY >> cut)
            costs += c,
            c = [0, 0, 0, 0, 0, 0, 0]
            c[5] = (self._rank+1)*(__const.STAR_ENERGY >> cut)
            costs += c,
        return costs

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

    def is_usable(self, system, _other):
        u"""使用可能判定。
        """
        cost, _ = system.resorce.get_available(self)
        return bool(cost)

    @property
    def rank(self):
        u"""ランク取得。
        """
        return self._rank

    @property
    def star(self):
        u"""スター数値取得。
        木:0, 火:1, 土:2, 金:3, 水:4, 月:5, 日:6.
        """
        return self._star

    @property
    def description(self):
        u"""概要取得。
        """
        return self._description

    @property
    def is_no_cost(self):
        u"""ノーコスト判定。
        """
        return self._rank == 0 or self._star == -1


def init():
    u"""コレクション初期化。
    """
    import units as __units
    import sorcery as __sorcery
    import utils.const as __const
    Collectible.set_collections(__units.get_creature_all()+__sorcery.get_all())
    if __const.IS_OUTPUT:
        print u"Collections"
        for i, collection in enumerate(Collectible.get_collections()):
            print i, u":",  unicode(collection)


get = Collectible.get_collection
get_all = Collectible.get_collections
get_by_name = Collectible.get_by_name
