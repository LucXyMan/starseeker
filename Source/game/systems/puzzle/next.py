#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""next.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ネクストピースモジュール。
"""
import utils.const as _const
import utils.layouter as _layouter
import pieces as _pieces


class Next(object):
    u"""ネクストピース。
    """
    __slots__ = "__array", "__card_lot", "__id", "__pieces", "__windows"

    def __init__(self, deck, id_=-1):
        u"""パターンとウィンドウを設定。
        self.__id: オブジェクトの位置決定に使用。
        self.__array: ネクストピースパターンを保持。
        self.__windows: ウィンドウスプライト。
        self.__display: ネクストピースの表示。
        """
        import lottery as __lottery
        import window as __window
        self.__id = id_
        length = 2
        self.__array = _pieces.Array(length=length)
        self.__array.append(
            *[_pieces.Rotatable((1, 1), _const.SINGLE_PRUNING, ())]*length)
        w, h = _const.NEXT_WINDOW_SIZE
        rect = 0, 0, w, h
        self.__card_lot = __lottery.Card(deck)
        self.__windows = __window.Next(rect), __window.Next(rect)
        _layouter.Game.set_next(self.__windows, self.__id)
        self.__display()

    def __display(self):
        u"""ピースを表示する。
        """
        self.__pieces = []
        for i, window in enumerate(self.__windows):
            piece = _pieces.Dropping(self.__array[i], (0, 0))
            window.piece = piece
            self.__pieces.append(piece)

    def forward(self, pattern):
        u"""ピース進行。
        """
        def __feature():
            u"""パターンの変更全般。
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
                    _const.BASIC_NAMES, ticket)
        for piece in self.__pieces:
            piece.clear()
        __feature()
        result, = self.__array.append(pattern)
        self.__display()
        return result
