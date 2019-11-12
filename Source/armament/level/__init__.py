#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""level.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

レベルパッケージ。
"""
import duel as __duel
import general as __general
get_duel = __duel.get_duel
get_duel_all = __duel.get_duel_all
get_rival = __duel.get_rival
set_rival = __duel.set_rival
get_duel_level = __duel.get_duel_level
set_duel_level = __duel.set_duel_level
get_endless = __general.get_endless
get_reward = __general.get_reward
get_deck = __general.get_deck
get_1p = __general.get_1p
get_versus_level = __general.get_versus_level
set_versus_level = __general.set_versus_level
get_selected_2p = __general.get_selected_2p
set_selected_2p = __general.set_selected_2p
get_2p = __general.get_2p


def init():
    u"""パッケージ初期化。
    """
    __duel.init()
