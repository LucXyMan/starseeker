#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""screen.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

スクリーン管理モジュール。
"""


def init():
    u"""初期化処理。
    """
    Screen()


class Screen(object):
    u"""スクリーン管理。
    """
    def __init__(self):
        u"""スクリーン生成。
        """
        import pygame as __pygame
        import const as __const
        import material as __material
        __pygame.display.set_caption(__const.CAPTION)
        icon, _, _, _ = __material.block.get("demon")
        __pygame.display.set_icon(icon)
        __pygame.mouse.set_visible(False)
        Screen.__base = __pygame.Surface(__const.BASE_SCREEN_SIZE)
        Screen.__main = __pygame.display.set_mode(__const.MAIN_SCREEN_SIZE)
        __pygame.display.update()

    @classmethod
    def get_base(cls):
        u"""ベーススクリーン取得。
        これを拡大してメインスクリーンに描画。
        """
        return cls.__base

    @classmethod
    def get_main(cls):
        u"""メインスクリーン取得。
        """
        return cls.__main
