#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""string.py

Copyright(c)2019 Yukio Kuro
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
    def __init__(self, pos, text, size, color="##", shorten=True, groups=None):
        u"""コンストラクタ。
        """
        super(String, self).__init__(
            (self.group, self.draw_group) if groups is None else tuple(groups))
        self.__text = str(text)
        self.__size = int(size)
        self.__color = str(color)
        self.__shorten = bool(shorten)
        self.__old = ()
        self.__set_image()
        self.rect.topleft = tuple(pos)
        self.update()

    def __repr__(self):
        u"""文字列表現取得。
        """
        return u"<'text:{text}, size:{size}, color:{color}'>".format(
            text=self.__text, size=self.__size, color=self.__color)

    def __set_image(self):
        u"""画像の設定。
        """
        import material.string as __string
        if self.__old != (
            self.__text, self.__size, self.__color, self.__shorten
        ):
            has_rect = hasattr(self, "rect")
            if has_rect:
                midleft = self.rect.midleft
            self.image = __string.get_string(
                self.__text, self.__size, __string.CharColor(self.__color),
                self.__shorten)
            if has_rect:
                self.rect.size = self.image.get_size()
                self.rect.midleft = midleft
            else:
                self.rect = self.image.get_rect()
            self.__old = self.__text, self.__size, self.__color, self.__shorten

    @property
    def text(self):
        u"""テキスト取得。
        """
        return self.__text

    @text.setter
    def text(self, value):
        u"""テキスト設定。
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
    def shorten(self):
        u"""文字間隔取得。
        """
        return self.__shorten

    @shorten.setter
    def shorten(self, value):
        u"""文字間隔設定。
        """
        self.__shorten = bool(value)


class Info(String):
    u"""ゲーム情報表示。
    """
    __INTERVAL = _const.FRAME_RATE*2
    __texts = _collections.deque()
    __color = _const.WHITE+"#"+_const.GRAY+"#"+_const.BLACK
    __waiting = 0
    __is_ignore = False

    @classmethod
    def send(cls, text, is_warning=False):
        u"""情報文字列設定。
        """
        if Info.__is_ignore and not is_warning:
            Info.__is_ignore = False
        else:
            if is_warning:
                Info.__color = _const.YELLOW+"#"+_const.GRAY+"#"+_const.BLACK
                Info.__is_ignore = True
            else:
                Info.__color = _const.WHITE+"#"+_const.GRAY+"#"+_const.BLACK
            Info.__texts = _collections.deque(text.split("#"))
            Info.__waiting = 0

    def __init__(self, groups=None):
        u"""コンストラクタ。
        """
        super(Info, self).__init__(
            (0, 0), "", _const.SYSTEM_CHAR_SIZE+2, groups=groups)
        _layouter.Menu.set_info(self)

    def update(self):
        u"""文字列の更新。
        """
        if Info.__waiting == 0:
            if Info.__texts:
                self.text = Info.__texts.popleft()
                self.color = Info.__color
                _layouter.Menu.set_info(self)
                Info.__waiting = self.__INTERVAL
        if 0 <= Info.__waiting:
            Info.__waiting -= 1
