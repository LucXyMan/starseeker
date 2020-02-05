#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""string.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

文字列スプライトモジュール。
"""
import collections as _collections
import pygame as __pygame
import utils.layouter as _layouter
import utils.const as _const


class String(__pygame.sprite.DirtySprite):
    u"""文字列スプライト。
    """
    def __init__(
        self, pos, string, size,
        color="##", is_short=True, groups=None
    ):
        u"""コンストラクタ。
        """
        super(String, self).__init__(
            (self.group, self.draw_group) if groups is None else tuple(groups))
        self.__text = str(string)
        self.__size = int(size)
        self.__color = str(color)
        self.__is_short = bool(is_short)
        self.__old = ()
        self.__set_image()
        self.rect.topleft = tuple(pos)
        self.update()

    def __repr__(self):
        u"""文字列表現取得。
        """
        return u"<'string:{string}, size:{size}, color:{color}'>".format(
            string=self.__text, size=self.__size, color=self.__color)

    def __set_image(self):
        u"""画像の設定。
        """
        import material.string as __string
        if self.__old != (
            self.__text, self.__size, self.__color, self.__is_short
        ):
            if hasattr(self, "rect"):
                midleft = self.rect.midleft
            self.image = __string.get_string(
                self.__text, self.__size, __string.CharColor(self.__color),
                self.__is_short)
            if hasattr(self, "rect"):
                self.rect.size = self.image.get_size()
                self.rect.midleft = midleft
            else:
                self.rect = self.image.get_rect()
            self.__old = (
                self.__text, self.__size, self.__color, self.__is_short)

    @property
    def string(self):
        u"""文字列取得。
        """
        return self.__text

    @string.setter
    def string(self, value):
        u"""文字列設定。
        """
        self.__text = value
        self.__set_image()

    @property
    def size(self):
        u"""サイズ取得。
        """
        return self.__size

    @size.setter
    def size(self, value):
        u"""サイズ設定。
        """
        self.__size = value
        self.__set_image()

    @property
    def color(self):
        u"""色取得。
        """
        return self.__color

    @color.setter
    def color(self, value):
        u"""色設定。
        """
        self.__color = value
        self.__set_image()

    @property
    def is_short(self):
        u"""文字間隔取得。
        """
        return self.__is_short

    @is_short.setter
    def is_short(self, value):
        u"""文字間隔設定。
        """
        self.__is_short = bool(value)


class Block(String):
    u"""ブロック情報文字列。
    """
    def __init__(self, pos, piece, groups=None):
        u"""コンストラクタ。
        """
        self._piece = piece
        self._old = -1
        self._param = self._dest = 0
        super(Block, self).__init__(
            pos, "", _const.SYSTEM_CHAR_SIZE, self._COLOR, True,
            groups)

    def update(self):
        u"""文字列の更新。
        """
        def __fluctuate():
            u"""値の変動。
            """
            if self._param < self._dest:
                self._param += 1
            elif self._param > self._dest:
                self._param -= 1
        self._set_dest()
        __fluctuate()
        self.string = self._get_string()


class Notice(String):
    u"""ゲーム情報表示。
    """
    __INTERVAL = _const.FRAME_RATE*3
    __texts = _collections.deque()
    __color = _const.WHITE+"#"+_const.GRAY+"#"+_const.BLACK
    __waiting = 0
    __is_ignore = False

    @classmethod
    def notify(cls, string, is_warning=False):
        u"""情報文字列設定。
        """
        if Notice.__is_ignore and not is_warning:
            Notice.__is_ignore = False
        else:
            if is_warning:
                Notice.__color = _const.YELLOW+"#"+_const.GRAY+"#"+_const.BLACK
                Notice.__is_ignore = True
            else:
                Notice.__color = _const.WHITE+"#"+_const.GRAY+"#"+_const.BLACK
            Notice.__texts = _collections.deque(string.split("#"))
            Notice.__waiting = 0

    def __init__(self, groups=None):
        u"""コンストラクタ。
        """
        super(Notice, self).__init__(
            (0, 0), "", _const.SYSTEM_CHAR_SIZE+2, groups=groups)
        _layouter.Menu.set_notice(self)

    def update(self):
        u"""文字列の更新。
        """
        if Notice.__waiting == 0 and Notice.__texts:
            self.string = Notice.__texts.popleft()
            self.color = Notice.__color
            _layouter.Menu.set_notice(self)
            Notice.__waiting = self.__INTERVAL
        if 0 <= Notice.__waiting:
            Notice.__waiting -= 1
