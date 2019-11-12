#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""levels.__init__.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

レベルパッケージ。
"""
import duel as __duel
import level as __level
get_duel = __duel.get_duel
get_duel_all = __duel.get_duel_all
get_rival = __duel.get_rival
set_rival = __duel.set_rival
get_duel_level = __duel.get_duel_level
set_duel_level = __duel.set_duel_level
get_endless = __level.get_endless
get_reward = __level.get_reward
get_deck = __level.get_deck
get_1p = __level.get_1p
get_versus_level = __level.get_versus_level
set_versus_level = __level.set_versus_level
get_selected_2p = __level.get_selected_2p
set_selected_2p = __level.set_selected_2p
get_2p = __level.get_2p


def init():
    u"""パッケージ初期化。
    """
    __duel.init()
