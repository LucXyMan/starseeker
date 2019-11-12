#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""utils.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

汎用関数パッケージ。
"""


def init():
    u"""パッケージ初期化。
    """
    import counter as __counter
    import layouter as __layouter
    import screen as __screen
    __screen.init()
    __layouter.init()
    __counter.init()
