#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""lottery.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

くじ引きモジュール。
"""
import random as _random


class Lottery(object):
    u"""くじ引き。
    """
    __slots__ = "_box",

    def __init__(self):
        u"""リロードして初期化。
        """
        self._reload()

    def draw(self):
        u"""くじを引く。空になればリロードする。
        """
        if not self._box:
            self._reload()
        return self._box.pop()


class Item(Lottery):
    u"""アイテムブロックくじ引き。
    """
    __slots__ = ()
    __CAPACITY = 128
    BLANK_TICKET = 0
    ELEMENTAL_TICKET = 1
    SHARDS_TICKET = 2
    KEY_TICKET = 3
    CHEST_TICKET = 4
    JOEKER_TICKET = 5

    def _reload(self):
        u"""くじの中身の生成。
        """
        self._box = []
        remaining = self.__CAPACITY
        for ticket, number in (
            (self.ELEMENTAL_TICKET, 8), (self.SHARDS_TICKET, 16),
            (self.KEY_TICKET, 32), (self.CHEST_TICKET, 64),
            (self.JOEKER_TICKET, 128)
        ):
            self._box.extend([ticket]*(self.__CAPACITY/number))
            remaining -= self.__CAPACITY/number
        self._box.extend([self.BLANK_TICKET]*remaining)
        _random.shuffle(self._box)


class Piece(Lottery):
    u"""ピースくじ引き。
    基本ピースとレベルピースの切り替えに使用。
    """
    __slots__ = ()

    def _reload(self):
        u"""くじの中身の生成。
        """
        self._box = [False]*7+[True]
        _random.shuffle(self._box)


class Star(Lottery):
    u"""スターくじ引き。
    """
    __slots__ = ()

    def _reload(self):
        u"""くじの中身の生成。
        """
        self._box = [
            "Jupiter", "Mars", "Saturn", "Venus", "Mercury", "Moon", "Sun"]
        _random.shuffle(self._box)


class Shard(Lottery):
    u"""シャードくじ引き。
    """
    __slots__ = ()

    def _reload(self):
        u"""くじの中身の生成。
        """
        self._box = ["Life", "Power", "Protect", "Speed"]
        _random.shuffle(self._box)


class Joker(Lottery):
    u"""ジョーカー効果くじ引き。
    """
    __slots__ = ()

    def _reload(self):
        u"""くじの中身の生成。
        """
        import armament.collectible as __collectible
        jokers = -1, -2, -3, -4, -5, -6
        self._box = [__collectible.get(joker).number for joker in jokers]
        _random.shuffle(self._box)


class Card(Lottery):
    u"""カードのくじ引き。
    """
    __CAPACITY = 32
    BLANK_TICKET = -1

    def __init__(self, deck):
        u"""リロードして初期化。
        """
        self.__deck = list(deck)
        super(Card, self).__init__()

    def _reload(self):
        u"""くじの中身の生成。
        """
        self._box = self.__deck[:]
        self._box.extend([self.BLANK_TICKET]*(self.__CAPACITY-len(self._box)))
        _random.shuffle(self._box)
