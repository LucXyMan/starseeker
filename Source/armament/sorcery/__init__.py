#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""sorcery.__init__.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

魔術パッケージ。
"""
import data as __data
get = __data.get
get_all = __data.get_all


def init():
    u"""パッケージ初期化。
    """
    import config as __config
    __config.init()
