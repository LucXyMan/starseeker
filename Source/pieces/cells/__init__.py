#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""cell.__init__.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

セルパッケージ。
"""
import cell as __cell
get = __cell.Cell.get_collection


def init():
    u"""パッケージの初期化。
    """
    import config as __config
    __config.init()
