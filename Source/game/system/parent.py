#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""parent.py

Copyright(c)2019 Yukio Kuro
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
        "__consumed", "__basics", "__elm_lot", "__hardness", "__has_item",
        "__levels", "__luck", "__piece", "__piece_lot", "__srd_lot",
        "__release", "__item_lot", "__joeker_lot", "__window")
    __HARDNESS_LIMIT = 200
    __LEVEL_UP_STEP = 1
    __LUCK_LIMIT = 100
    __LUCK_MINUS = 8
    __TREASURE_HIT = 0.01
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

        class __PieceArray(_pieces.Array):
            u"""ピース配列。
            """
            __slots__ = ()

            def get(self):
                u"""パターンの取得。
                """
                if self.is_empty:
                    self._reload()
                return self._patterns.pop(0)

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
                self._patterns = _pieces.get_levels(0, self.__level+1)
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

        class _BlockString(__string.String):
            u"""ブロック情報文字列。
            """
            def __init__(self, pos, parent, groups=None):
                u"""コンストラクタ。
                """
                self._parent = parent
                self._old = -1
                self._param = self._dest = 0
                super(_BlockString, self).__init__(
                    pos, "", _const.SYSTEM_CHAR_SIZE, self._COLOR, True,
                    groups)

            def update(self):
                u"""文字列の更新。
                """
                def __rise_and_fall():
                    u"""値の変動。
                    """
                    if self._param < self._dest:
                        self._param += 1
                    elif self._param > self._dest:
                        self._param -= 1
                self._set_dest()
                __rise_and_fall()
                self.text = self._get_string()

        class __LevelString(_BlockString):
            u"""レベル数値文字列。
            """
            _COLOR = _const.MAGENTA+"#"+_const.YELLOW+"#"+_const.DARK_MAGENTA

            def _get_string(self):
                u"""文字列取得。
                """
                return "PL{0:0>2}".format(self._param)

            def _set_dest(self):
                u"""目的の値を設定。
                """
                if self._old != self._parent.level:
                    self._old = self._dest = self._parent.level

        class __HardnessString(_BlockString):
            u"""硬度数値文字列。
            """
            _COLOR = _const.YELLOW+"#"+_const.ORANGE+"#"+_const.DARK_YELLOW

            def _get_string(self):
                u"""文字列取得。
                """
                return "H{0:0>3}".format(self._param >> 1)

            def _set_dest(self):
                u"""目的の値を設定。
                """
                if self._old != self._parent.hardness:
                    self._dest = self._parent.hardness
                    self._old = self._parent.hardness

        class __LuckString(_BlockString):
            u"""幸運数値文字列。
            """
            _COLOR = _const.CYAN+"#"+_const.YELLOW+"#"+_const.DARK_CYAN

            def _get_string(self):
                u"""文字列取得。
                """
                return "L{0:0>3}".format(self._param)

            def _set_dest(self):
                u"""目的の値を設定。
                """
                if self._old != self._parent.luck:
                    self._dest = self._parent.luck
                    self._old = self._parent.luck
        rect = _pygame.Rect((0, 0), _const.NEXT_WINDOW_SIZE)
        self.__basics = __BasicArray()
        self.__levels = _LevelArray()
        self.__window = __window.Next(rect)
        self.__window.rect.topleft = rect.topleft
        __layouter.Game.set_parent(self)
        self.__consumed = 0
        self.__luck = 0
        self.__hardness = 0
        __layouter.Game.set_block_level(tuple(
            String((0, 0), self) for
            String in (__LevelString, __HardnessString, __LuckString)))
        self.__release = _pieces.Array(length=1)
        self.__release.append(_pieces.Rotatable(
            (1, 1), _const.SINGLE_PRUNING, ()))
        self.__piece_lot = __lottery.Piece()
        self.__item_lot = __lottery.Item()
        self.__elm_lot = __lottery.Star()
        self.__srd_lot = __lottery.Shard()
        self.__joeker_lot = __lottery.Joeker()
        self.__has_item = False
        self.__display()

    def __display(self):
        u"""ピースの表示。
        """
        release, = self.__release
        self.__piece = _pieces.Dropping(release, (0, 0))
        self.__window.piece = self.__piece

    def eliminate(self):
        u"""スプライトの削除等。
        """
        self.__piece.eliminate()
        self.__window.kill()
        _pygame.mixer.music.stop()

    def hardness_up(self):
        u"""硬度を上げる。
        """
        self.__hardness = (
            self.__HARDNESS_LIMIT if
            self.__HARDNESS_LIMIT < self.__hardness+(self.level >> 2) else
            self.__hardness+(self.level >> 2) if
            self.__HARDNESS_LIMIT >> 1 < self.__hardness else
            self.__hardness+(self.level >> 1))

    def hardness_down(self):
        u"""硬度を下げる。
        """
        self.__hardness = self.__hardness-1 if 0 < self.__hardness-1 else 0

    def luck_up(self):
        u"""幸運を上げる。
        """
        self.__luck = (
            self.__LUCK_LIMIT if
            self.__LUCK_LIMIT < self.__luck+(self.level >> 1) else
            self.__luck+(self.level >> 1))

    def luck_down(self):
        u"""幸運を下げる。
        """
        self.__luck = (
            self.__luck-self.__LUCK_MINUS if
            0 < self.__luck-self.__LUCK_MINUS else 0)

    def get_pattern(self, level_up=True):
        u"""生成したパターンを返す。
        """
        def __level_up():
            u"""ピースLVの上昇。
            """
            if level_up:
                level = self.__levels.level
                if level:
                    if self.__consumed % int(level*self.__LEVEL_UP_STEP) == 0:
                        self.__levels.level += 1
                        self.__consumed = 0
                else:
                    self.__levels.level += 1
                self.__consumed += 1

        def __feature():
            u"""パターンの変更全般。
            """
            def __hardness_change():
                u"""ブロックの硬度を強化。
                """
                rate = self.__hardness*0.005
                if _random.random() <= rate:
                    new.change("Solid", "Normal", is_lchange=True)
                if (self.__HARDNESS_LIMIT >> 1 < self.__hardness and
                        _random.random() <= rate):
                    new.change("Adamant", "Solid", is_lchange=True)

            def __add_key():
                u"""パターンに鍵追加。
                """
                rate = _random.random()
                for name, value in zip(
                    ("GoldKey", "SilverKey"),
                    ((self.__luck*0.01)**i for i in range(2, 0, -1))
                ):
                    if rate <= value:
                        return new.append(name, "Normal")
                else:
                    return new.append("BronzeKey", "Normal")

            def __add_chest():
                u"""パターンにチェスト追加。
                """
                rate = _random.random()
                for name, value in zip(
                    ("GoldChest", "SilverChest", "BronzeChest"),
                    ((self.__luck*0.01)**i for i in range(3, 0, -1))
                ):
                    if rate <= value:
                        return new.append(name, "Normal")
                else:
                    return new.append("IronChest", "Normal")
            ticket = self.__item_lot.draw()
            if ticket == self.__item_lot.ELEMENTAL_TICKET:
                new.append(self.__elm_lot.draw(), "Normal")
            elif ticket == self.__item_lot.SHARDS_TICKET:
                new.append(self.__srd_lot.draw(), "Normal")
            elif ticket == self.__item_lot.KEY_TICKET:
                __add_key()
            elif ticket == self.__item_lot.CHEST_TICKET:
                __add_chest()
            elif ticket == self.__item_lot.JOEKER_TICKET:
                new.append("Joeker", "Normal", self.__joeker_lot.draw())
            __hardness_change()
        __level_up()
        self.__piece.clear()
        new = (
            self.__levels.get() if self.__piece_lot.draw() else
            self.__basics.get())
        __feature()
        self.__has_item = any(any(
            shape and shape.type in self.__ITEM_NAMES.split("#") for
            shape in line) for line in new)
        result, = self.__release.append(new)
        self.__display()
        return result

    @property
    def has_item(self):
        u"""アイテム保有状態取得。
        """
        return self.__has_item

    @property
    def window(self):
        u"""ウィンドウ取得。
        """
        return self.__window

    @window.setter
    def window(self, value):
        u"""ウィンドウ設定。
        """
        self.__window = value

    @property
    def level(self):
        u"""現在レベル取得。
        """
        return self.__levels.level

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
