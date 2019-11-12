#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""next.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ネクストピースモジュール。
"""
import utils.const as _const
import utils.layouter as _layouter
import pieces as _pieces


class Next(object):
    u"""ネクストピース。
    """
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
        rects = tuple(window.rect for window in self.__windows)
        _layouter.Game.set_next(rects, self.__id)
        self.__pieces = []
        for i in range(len(rects)):
            piece = _pieces.Dropping(self.__array[i], (0, 0))
            self.__windows[i].piece = piece
            self.__pieces.append(piece)

    def __feature(self, pattern):
        u"""パターンの変更全般。
        """
        import armament.collectible as __collectible
        ticket = self.__card_lot.draw()
        if ticket != self.__card_lot.BLANK_TICKET:
            pattern.append({
                _const.SUMMON_TYPE: "Summon",
                _const.SORCERY_TYPE: "Sorcery",
                _const.SHIELD_TYPE: "Shield"
            }[__collectible.get(ticket).type], _const.BASIC_NAMES, ticket)

    def advance(self, apnd):
        u"""ピース進行。
        """
        for piece in self.__pieces:
            piece.clear()
        self.__feature(apnd)
        result, = self.__array.append(apnd)
        self.__display()
        return result
