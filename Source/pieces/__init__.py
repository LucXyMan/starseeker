#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""pieces.__init__.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ピースパッケージ。
"""
import config as __config
import pattern as __pattern
import piece as __piece
import field as __field
import falling as __falling
get_basics = __config.get_basics
get_levels = __config.get_levels
get_total = __config.get_total
Array = __pattern.Array
Pattern = __pattern.Pattern
Rotatable = __pattern.Rotatable
State = __piece.State
Field = __field.Field
Falling = __falling.Falling


def init():
    u"""パッケージ初期化。
    """
    __config.init()
