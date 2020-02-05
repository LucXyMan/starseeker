#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""parent.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ペアレントモジュール。
"""
import random as _random
import pygame as _pygame
import pieces as _pieces
import utils.const as _const


class Parent(object):
    u"""ペアレントフィールド。
    親パターンの生成と変化を管理する。
    """
    __slots__ = (
        "__consumed", "__basics", "__elm_lot", "__item_lot", "__item_state",
        "__levels", "__lv_lot", "__piece", "__piece_level_string",
        "__piece_lot", "__srd_lot", "__release", "__joker_lot", "__window")
    __ITEM_NAMES = (
        _const.STAR_NAMES+"#"+_const.SHARD_NAMES+"#" +
        _const.KEY_NAMES+"#"+_const.CHEST_NAMES)

    def __init__(self):
        u"""ウィンドウ・点数文字列と最初のブロックを生成する。
        """
        import lottery as __lottery
        import sprites.string as __string
        import utils.layouter as __layouter
        import window as __window

        # ---- Array ----
        class __PieceArray(_pieces.Array):
            u"""ピース配列。
            """
            __slots__ = ()

            def get(self):
                u"""パターンの取得。
                """
                if self.is_empty:
                    self._reload()
                return self._patterns.pop()

        class __BasicArray(__PieceArray):
            u"""基本ピース配列。
            """
            __slots__ = ()

            def _reload(self):
                u"""パターン生成。
                """
                self._patterns = _pieces.get_basics()
                _random.shuffle(self._patterns)

        class _LevelArray(__PieceArray):
            u"""レベルピース配列。
            """
            __slots__ = "__level",

            def __init__(self):
                u"""コンストラクタ。
                """
                self.__level = 0
                super(_LevelArray, self).__init__()

            def _reload(self):
                u"""パターン生成。
                """
                self._patterns = _pieces.get_levels(self.__level+1)
                _random.shuffle(self._patterns)

            @property
            def level(self):
                u"""現在レベル取得。
                """
                return self.__level

            @level.setter
            def level(self, value):
                u"""現在レベル設定。
                """
                limit = _pieces.get_total()-1
                self.__level = int(value if value < limit else limit)

        # ---- String ----
        class __PieceLevel(__string .Block):
            u"""ピースレベル文字列。
            """
            _COLOR = _const.YELLOW+"#"+_const.ORANGE+"#"+_const.DARK_YELLOW

            def _get_string(self):
                u"""文字列取得。
                """
                return "P{0:0>2}".format(self._param)

            def _set_dest(self):
                u"""目的の値を設定。
                """
                if self._old != self._piece.level:
                    self._old = self._dest = self._piece.level

        rect = _pygame.Rect((0, 0), _const.NEXT_WINDOW_SIZE)
        self.__basics = __BasicArray()
        self.__levels = _LevelArray()
        self.__window = __window.Next(rect)
        self.__window.rect.topleft = rect.topleft
        __layouter.Game.set_parent(self.__window)
        self.__consumed = 0
        self.__piece_level_string = __PieceLevel((0, 0), self)
        __layouter.Game.set_piece_level(self.__piece_level_string)
        self.__release = _pieces.Array(length=1)
        self.__release.append(_pieces.Rotatable(
            (1, 1), _const.SINGLE_PRUNING, ()))
        self.__piece_lot = __lottery.Piece()
        self.__item_lot = __lottery.Item()
        self.__elm_lot = __lottery.Star()
        self.__srd_lot = __lottery.Shard()
        self.__lv_lot = __lottery.LevelUp()
        self.__joker_lot = __lottery.Joker()
        self.__item_state = 0
        self.__display()

    def __display(self):
        u"""ピースの表示。
        """
        release, = self.__release
        self.__piece = _pieces.Falling(release, (0, 0))
        self.__window.piece = self.__piece

    # ---- Create Piece ----
    def get_pattern(self, level_up=True):
        u"""生成したパターンを返す。
        """
        def __level_up():
            u"""ピースLVの上昇。
            """
            if level_up:
                level = self.__levels.level
                if level:
                    if self.__consumed % level == 0:
                        self.__levels.level += 1
                        self.__consumed = 0
                else:
                    self.__levels.level += 1
                self.__consumed += 1

        def __form():
            u"""パターンの変更全般。
            """
            if level_up:
                ticket = self.__item_lot.draw()
                if ticket == self.__item_lot.STAR_TICKET:
                    new.append(self.__elm_lot.draw(), "Normal")
                elif ticket == self.__item_lot.SHARDS_TICKET:
                    new.append(self.__srd_lot.draw(), "Normal")
                elif ticket == self.__item_lot.LEVEL_UP_TICKET:
                    new.append(self.__lv_lot.draw(), "Normal")
                elif ticket == self.__item_lot.KEY_TICKET:
                    new.append("BronzeKey", "Normal")
                elif ticket == self.__item_lot.CHEST_TICKET:
                    return new.append("IronChest", "Normal")
                elif ticket == self.__item_lot.JOEKER_TICKET:
                    new.append("Joker", "Normal", self.__joker_lot.draw())

        def __has_item(names):
            u"""保有アイテム判定。
            """
            return any(any(
                shape and shape.type in names.split("#") for
                shape in line) for line in new)
        __level_up()
        self.__piece.clear()
        new = (
            self.__levels.get() if self.__piece_lot.draw() else
            self.__basics.get())
        __form()
        has_item = __has_item(self.__ITEM_NAMES)
        has_joker = __has_item("Joker") << 1
        has_level_up = __has_item(_const.LEVEL_UP_NAMES) << 2
        has_bad_level_up = __has_item(_const.BAD_LEVEL_UP_NAMES) << 3
        self.__item_state = (
            has_item | has_joker | has_level_up | has_bad_level_up)
        result, = self.__release.append(new)
        self.__display()
        return result

    # ---- Property ----
    @property
    def level(self):
        u"""現在レベル取得。
        """
        return self.__levels.level

    @property
    def has_item(self):
        u"""アイテム保有状態取得。
        """
        return bool(self.__item_state & 0b0001)

    @property
    def has_joker(self):
        u"""ジョーカー保有状態取得。
        """
        return bool(self.__item_state & 0b0010)

    @property
    def has_level_up(self):
        u"""良性レベルアップ保有状態取得。
        """
        return bool(self.__item_state & 0b0100)

    @property
    def has_bad_level_up(self):
        u"""悪性レベルアップ保有状態取得。
        """
        return bool(self.__item_state & 0b1000)

    @property
    def piece_level_string(self):
        u"""ピースレベル文字列取得。
        """
        return self.__piece_level_string
