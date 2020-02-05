#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""next.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ネクストピースモジュール。
"""
import random as _random
import utils.const as _const
import pieces as _pieces
_HARDNESS_LIMIT = 10
_LUCK_LIMIT = 10


class Next(object):
    u"""ネクストピース。
    """
    __slots__ = (
        "__array", "__card_lot", "__hardness", "__id", "__luck", "__pieces",
        "__windows")

    def __init__(self, deck, parent, id_):
        u"""パターンとウィンドウを設定。
        """
        import lottery as __lottery
        import sprites.string as __string
        import utils.layouter as __layouter
        import window as __window

        class __HardnessString(__string.Block):
            u"""硬度数値文字列。
            """
            _COLOR = _const.MAGENTA+"#"+_const.YELLOW+"#"+_const.DARK_MAGENTA

            def _get_string(self):
                u"""文字列取得。
                """
                param = "?" if _LUCK_LIMIT <= self._param else self._param
                return "H{0:0>1}".format(param)

            def _set_dest(self):
                u"""目的の値を設定。
                """
                if self._old != self._piece.hardness:
                    self._dest = self._piece.hardness
                    self._old = self._piece.hardness

        class __LuckString(__string.Block):
            u"""幸運数値文字列。
            """
            _COLOR = _const.CYAN+"#"+_const.YELLOW+"#"+_const.DARK_CYAN

            def _get_string(self):
                u"""文字列取得。
                """
                param = "?" if _LUCK_LIMIT <= self._param else self._param
                return "L{0:0>1}".format(param)

            def _set_dest(self):
                u"""目的の値を設定。
                """
                if self._old != self._piece.luck:
                    self._dest = self._piece.luck
                    self._old = self._piece.luck
        self.__id = id_
        self.__luck = 0
        self.__hardness = 0
        __layouter.Game.set_parameter(
            (__HardnessString((0, 0), self), __LuckString((0, 0), self)),
            parent.piece_level_string, self.__id)
        length = 2
        self.__array = _pieces.Array(length=length)
        self.__array.append(
            *[_pieces.Rotatable((1, 1), _const.SINGLE_PRUNING, ())]*length)
        w, h = _const.NEXT_WINDOW_SIZE
        rect = 0, 0, w, h
        self.__card_lot = __lottery.Card(deck)
        self.__windows = __window.Next(rect), __window.Next(rect)
        __layouter.Game.set_next(self.__windows, self.__id)
        self.__display()

    def __display(self):
        u"""ピースを表示する。
        """
        self.__pieces = []
        for i, window in enumerate(self.__windows):
            piece = _pieces.Falling(self.__array[i], (0, 0))
            window.piece = piece
            self.__pieces.append(piece)

    def forward(self, pattern):
        u"""ピース進行。
        """
        def __form():
            u"""パターンの変更全般。
            """
            def __draw():
                u"""カード追加。
                """
                import armament.collectible as __collectible
                ticket = self.__card_lot.draw()
                if ticket != self.__card_lot.BLANK_TICKET:
                    arcana = {
                        _const.SUMMON_ARCANUM: "Summon",
                        _const.SORCERY_ARCANUM: "Sorcery",
                        _const.SHIELD_ARCANUM: "Shield",
                        _const.SUPPORT_ARCANUM: "Support"}
                    pattern.append(
                        arcana[__collectible.get(ticket).type],
                        "Normal", ticket)

            def __harden():
                u"""ブロック硬化。
                """
                rate = self.__hardness*0.1
                if _random.random() < rate:
                    pattern.change("Solid", "Normal", is_lchange=True)
                if (
                    _HARDNESS_LIMIT >> 1 < self.__hardness and
                    _random.random() < rate
                ):
                    pattern.change("Adamant", "Solid", is_lchange=True)

            def __enhance_key():
                u"""鍵強化。
                """
                rate = _random.random()
                for name, value in zip(
                    ("GoldKey", "SilverKey"),
                    ((self.__luck*0.1)**i for i in range(2, 0, -1))
                ):
                    if rate <= value:
                        return pattern.append(name, "BronzeKey")

            def __enhance_chest():
                u"""チェスト強化。
                """
                rate = _random.random()
                for name, value in zip(
                    ("GoldChest", "SilverChest", "BronzeChest"),
                    ((self.__luck*0.1)**i for i in range(3, 0, -1))
                ):
                    if rate <= value:
                        return pattern.append(name, "IronChest")
            __draw()
            __harden()
            __enhance_chest()
            __enhance_key()
        for piece in self.__pieces:
            piece.clear()
        __form()
        result, = self.__array.append(pattern)
        self.__display()
        return result

    # ---- Level Up ----
    def level_up(self, level_ups):
        u"""レベルアップ処理。
        """
        hu, hd, lu, ld = level_ups
        hardness = self.__hardness+hu-hd
        self.__hardness = (
            0 if hardness < 0 else hardness if hardness <
            _HARDNESS_LIMIT else _HARDNESS_LIMIT)
        luck = self.__luck+lu-ld
        self.__luck = (
            0 if luck < 0 else luck if luck <
            _LUCK_LIMIT else _LUCK_LIMIT)

    # ---- Property ----
    @property
    def hardness(self):
        u"""硬度レベル取得。
        """
        return self.__hardness

    @property
    def luck(self):
        u"""ラックレベル取得。
        """
        return self.__luck
