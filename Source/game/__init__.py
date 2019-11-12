#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""game.__init__.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ゲームパッケージ。
"""
import main as __main
Game = __main.Game


def init():
    u"""パッケージ初期化。
    """
    import mode as __mode
    __mode.init()
