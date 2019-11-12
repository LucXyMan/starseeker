#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""general.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

汎用スプライトモジュール。
"""
import pygame as __pygame


class General(__pygame.sprite.DirtySprite):
    u"""汎用スプライト。
    """
    def __init__(self, groups):
        u"""コンストラクタ。
        """
        super(General, self).__init__(
            (self.group, self.draw_group) if groups is None else tuple(groups))
