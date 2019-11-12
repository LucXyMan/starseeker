#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""string.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

文字列画像モジュール。
"""
import pygame as _pygame
import utils.const as _const
import utils.image as _image
__source = ""


class CharColor(object):
    u"""文字画像に使用する色。
    """
    __slots__ = "__string"
    __DEFAULT = _const.WHITE+"#"+_const.GRAY+"#"+_const.BLACK

    def __init__(self, color="##"):
        u"""コンストラクタ。
        """
        start, end, back = color.split("#")
        dstart, dend, dback = self.__DEFAULT.split("#")
        self.__string = (
            (start if start else dstart)+"#"+(end if end else dend)+"#" +
            (back if back else dback))

    def __repr__(self):
        u"""文字列表現取得。
        """
        return (
            u"<CharColor: start: {start}, end: {end}, back: {back}>".format(
                start=self.start, end=self.end, back=self.back))

    @property
    def string(self):
        u"""文字列形式の色取得。
        """
        return self.__string

    @property
    def start_string(self):
        u"""文字列形式スタートカラー取得。
        """
        start, _, _ = self.__string.split("#")
        return start

    @property
    def end_string(self):
        u"""文字列形式エンドカラー取得。
        """
        _, end, _ = self.__string.split("#")
        return end

    @property
    def back_string(self):
        u"""文字列形式バックカラー取得。
        """
        _, _, back = self.__string.split("#")
        return back

    @property
    def start(self):
        u"""スタートカラー取得。
        """
        return _pygame.Color(self.start_string)

    @property
    def end(self):
        u"""エンドカラー取得。
        """
        return _pygame.Color(self.end_string)

    @property
    def back(self):
        u"""バックカラー取得。
        """
        return _pygame.Color(self.back_string)


class ElmCharColor(object):
    u"""エレメンタル文字色。
    """
    def __init__(self):
        u"""色を作成する。
        """
        def __set_char_colors():
            u"""文字色設定。
            木、火、土、金、水、月、日。
            """
            ElmCharColor.__CHAR_COLORS = tuple(CharColor(color) for color in (
                _const.GREEN+"#"+_const.YELLOW+"#"+_const.DARK_GREEN,
                _const.RED+"#"+_const.YELLOW+"#"+_const.DARK_RED,
                _const.MAGENTA+"#"+_const.BLUE+"#"+_const.DARK_MAGENTA,
                _const.ORANGE+"#"+_const.YELLOW+"#"+_const.DARK_ORANGE,
                _const.BLUE+"#"+_const.CYAN+"#"+_const.DARK_BLUE,
                _const.BLACK+"#"+_const.GRAY+"#"+_const.BLACK,
                _const.GRAY+"#"+_const.WHITE+"#"+_const.GRAY))

        def __set_dark_char_colors():
            u"""暗い文字色設定。
            木、火、土、金、水、月、日。
            """
            ElmCharColor.__DARK_CHAR_COLORS = tuple(
                CharColor(color) for color in (
                    _const.DARK_GREEN+"#"+_const.DARK_YELLOW+"#" +
                    _const.DARK_GREEN,
                    _const.DARK_RED+"#"+_const.DARK_YELLOW+"#"+_const.DARK_RED,
                    _const.DARK_MAGENTA+"#"+_const.DARK_BLUE+"#" +
                    _const.DARK_MAGENTA,
                    _const.DARK_ORANGE+"#"+_const.DARK_YELLOW+"#" +
                    _const.DARK_ORANGE,
                    _const.DARK_BLUE+"#"+_const.DARK_CYAN+"#"+_const.DARK_BLUE,
                    _const.BLACK+"#"+_const.BLACK+"#"+_const.BLACK,
                    _const.GRAY+"#"+_const.GRAY+"#"+_const.GRAY))
        __set_char_colors()
        __set_dark_char_colors()

    @classmethod
    def get(cls, number, dark=False):
        u"""文字色取得。
        """
        return (
            cls.__DARK_CHAR_COLORS[number] if dark else
            cls.__CHAR_COLORS[number])


def init():
    u"""モジュール初期化。
    """
    import os as __os
    global __source
    __source = __os.path.join(__os.path.dirname(__file__), "ipaexg.ttf")
    ElmCharColor()


def get_string(text, size, color=None, shorten=True):
    u"""文字列画像取得。
    """
    import utils.memoize as __memoize

    @__memoize.memoize()
    def __get_gradient_char(text, size, color):
        u"""グラデーション文字列画像取得。
        """
        @__memoize.memoize()
        def __get_shadow_char(text, size, color):
            u"""影付き文字列画像取得。
            """
            @__memoize.memoize()
            def __get_char(text, size, color):
                u"""文字列画像取得。
                """
                return _pygame.font.Font(
                    __source, size).render(text, False, color.start)

            def __color_to_string(color):
                u"""色情報を文字列に変換する。
                """
                return "0x"+reduce(lambda x, y: x+y, (
                    "{0:0>2}".format(hex(c).lstrip("0x")) for c in color[:3]))
            h, s, v, a = color.back.hsva
            back_mid = _pygame.Color("0xFFFFFF")
            back_mid.hsva = tuple(int(c) for c in (h, s, v*0.5, a))
            h, s, v, a = back_mid.hsva
            back_bottom = _pygame.Color("0xFFFFFF")
            back_bottom.hsva = tuple(int(c) for c in (h, s, v*0.75, a))
            font = __get_char(
                text, size, CharColor(__color_to_string(color.back)+"##"))
            font_size = font.get_size()
            image = _pygame.Surface((font_size[0]+2, font_size[1]+2))
            image.set_colorkey(_pygame.Color("0x000000"))
            for pos in ((0, 0), (1, 0), (2, 0)):
                image.blit(font, pos)
            font = __get_char(
                text, size, CharColor(__color_to_string(back_bottom)+"##"))
            for pos in ((0, 2), (1, 2), (2, 2)):
                image.blit(font, pos)
            font = __get_char(text, size, CharColor(
                __color_to_string(back_mid)+"##"))
            for pos in ((0, 1), (2, 1)):
                image.blit(font, pos)
            image.blit(
                __get_char(text, size, CharColor(
                    color.start_string+"##")), (1, 1))
            return image
        color_key = "0xFFFFFF"
        sc = __get_shadow_char(
            text, size, CharColor(color_key+"##"+color.back_string))
        surf = _pygame.Surface(sc.get_size())
        surf.blit(sc, (0, 0))
        surf.set_colorkey(_pygame.Color(color_key))
        size = surf.get_size()
        gradient = _pygame.transform.scale(
            _image.get_gradient(size, (color.start, color.end), True), size)
        gradient.blit(surf, (0, 0))
        surf.blit(gradient, (0, 0))
        surf.set_colorkey(_pygame.Color("0x000000"))
        return surf
    if text:
        values = []
        color = color if color else CharColor()
        for c in text:
            img = __get_gradient_char(c, size, color)
            values.append((img, img.get_size()))
        m = max(h for _, (_, h) in values)
        surf = _pygame.Surface((
            sum(w for _, (w, _) in values) if shorten else
            (size+2)*len(text), m))
        surf.set_colorkey(_pygame.Color("0x000000"))
        x = 0
        for i, (img, (w, h)) in enumerate(values):
            surf.blit(img, (x if shorten else (size+2)*i, (m-h) >> 1))
            x += w
        return surf
    else:
        return _pygame.Surface((0, 0))


def get_subscript(surf, char, char_color=None):
    u"""画像の右下に添字を設定した画像を返す。
    """
    surf = _image.copy(surf)
    if char:
        char = (get_string(
            char, _const.GRID >> 1, CharColor() if
            char_color is None else char_color, True))
        w, h = surf.get_size()
        cw, ch = char.get_size()
        surf.blit(char, (w-cw, h-ch))
    return surf
