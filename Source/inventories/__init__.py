#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""inventories.__init__.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

インベントリパッケージ。
"""
import collections as __collections
import equips as __equips
import inventory as __inventory
import various as __various
# ---- Utils ----
get_config_dir = __inventory.get_config_dir
load = __inventory.Inventory.load
save = __inventory.Inventory.save
# ---- SP ----
get_sp = __inventory.Inventory.get_sp
add_sp = __inventory.Inventory.add_sp
is_buyable = __inventory.Inventory.is_buyable
buy_item = __inventory.Inventory.buy_item
buy_card = __inventory.Inventory.buy_card
# ---- Time ----
get_time = __inventory.Inventory.get_time
forward_time = __inventory.Inventory.forward_time
# ---- Interface ----
General = __various.General
Level = __various.Level
Item = __collections.Item
Card = __collections.Card
Equip = __equips.Equip
Skill = __equips.Skill
Deck = __equips.Deck


def init():
    u"""パッケージ初期化。
    """
    __inventory.init()
