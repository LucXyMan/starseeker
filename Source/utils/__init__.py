#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""utils.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

汎用関数パッケージ。
"""
import counter as __counter
forward = __counter.forward
get_frame = __counter.get_frame


def init():
    u"""パッケージ初期化。
    """
    import inventory as __inventory
    import layouter as __layouter
    import screen as __screen
    import image as __image
    __screen.init()
    __layouter.init()
    __counter.init()
