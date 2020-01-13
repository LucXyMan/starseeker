#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""window.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ゲームウィンドウモジュール。
"""
import pygame as _pygame


class Window(_pygame.sprite.DirtySprite):
    u"""ゲームウィンドウ。
    """
    def __init__(self, pos, image, groups=None):
        u"""コンストラクタ。
        """
        import decorator as __decorator
        super(Window, self).__init__(
            (self.group, self.draw_group) if groups is None else groups)
        self.image = image
        self.image.set_colorkey(_pygame.Color("0x000000"))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self._decoration = 0b1111
        self._is_light = False
        __decorator.set_decorator(self)

    @property
    def decoration(self):
        u"""デコレータ状態取得。
        """
        return self._decoration

    @property
    def is_light(self):
        u"""発光判定。
        """
        return self._is_light

    @is_light.setter
    def is_light(self, value):
        u"""発光設定。
        """
        self._is_light = bool(value)
