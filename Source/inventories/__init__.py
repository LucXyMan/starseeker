#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""inventories.__init__.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

インベントリパッケージ。
"""
import inventory as __inventory
import interface as __interface
get_config_dir = __inventory.get_config_dir
load = __inventory.Inventory.load
save = __inventory.Inventory.save
Time = __interface.Time
SP = __interface.SP
Utils = __interface.Utils
Level = __interface.Level
Items = __interface.Items
Card = __interface.Card
Equip = __interface.Equip
Skill = __interface.Skill
Deck = __interface.Deck


def init():
    u"""パッケージ初期化。
    """
    __inventory.init()
    __interface.init()
