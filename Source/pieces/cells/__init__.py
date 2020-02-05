#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""cells.__init__.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

セルパッケージ。
"""
__collections = {}


def get(key):
    u"""コレクション取得。
    """
    import block as __block
    import chest as __chest
    import basic as __basic
    import irregular as __irregular
    import item as __item
    import monster as __monster
    global __collections
    if not __collections:
        __collections = {cell.__name__: cell for cell in (
            __block.Block, __block.Blank, __block.Target,
            __basic.Normal, __basic.Solid, __basic.Adamant,
            __irregular.Water, __irregular.Acid, __irregular.Poison,
            __irregular.Chocolate, __irregular.Stone, __irregular.Ice,
            __irregular.Magma, __irregular.Ruined,
            __item.Jupiter, __item.Mars, __item.Saturn, __item.Venus,
            __item.Mercury, __item.Moon, __item.Sun,
            __item.Life, __item.Power, __item.Protect, __item.Speed,
            __item.Summon, __item.Sorcery, __item.Support, __item.Shield,
            __item.Joker,
            __item.HardnessUp, __item.HardnessDown,
            __item.LuckUp, __item.LuckDown,
            __monster.Slime, __monster.Tired,
            __monster.Matango, __monster.LargeMatango,
            __monster.BlockEater, __monster.BlockDemon,
            __monster.ArchDemon, __monster.Maxwell,
            __monster.KingDemon, __monster.Gargoyle,
            __monster.FireGhost, __monster.IceGhost,
            __monster.PoisonGhost, __monster.RIP,
            __chest.BronzeKey, __chest.SilverKey, __chest.GoldKey,
            __chest.IronChest, __chest.BronzeChest, __chest.SilverChest,
            __chest.GoldChest, __chest.Pandora,
            __chest.BronzeMimic, __chest.SilverMimic, __chest.GoldMimic,
            __chest.PandoraMimic)}
    return __collections[key]
