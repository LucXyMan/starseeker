#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""input.__init__.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

コマンド入力パッケージ。
"""
import controler as __controler
import thinker as __thinker
is_second_playable = __controler.is_second_playable
Main = __controler.Main
Menu = __controler.Menu
Thinker = __thinker.Thinker


def init():
    u"""初期化処理。
    """
    __controler.init()
