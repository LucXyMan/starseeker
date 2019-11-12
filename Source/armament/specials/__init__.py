#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""specials.__init__.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

特殊効果パッケージ。
"""
import special as __special
get = __special.get


def init():
    u"""パッケージ初期化。
    """
    import config as __config
    __config.init()
