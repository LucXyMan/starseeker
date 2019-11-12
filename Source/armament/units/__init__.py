#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""units.__init__.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ユニットパッケージ。
"""
import data as __data
import unit as __unit
import player as __player
import creature as __creature
import group as __group
get_player = __data.Player.get_collection
get_player_all = __data.Player.get_collections
get_creature = __data.Summon.get_collection
get_creature_all = __data.Summon.get_collections
Unit = __unit.Unit
Player = __player.Player
Creature = __creature.Creature
Group = __group.Group


def init():
    u"""パッケージ初期化。
    """
    import config as __config
    __config.init()
