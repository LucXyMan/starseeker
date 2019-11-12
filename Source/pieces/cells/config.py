#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""config.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ブロック設定モジュール。
"""


def init():
    u"""モジュール初期化。
    """
    import block as __block
    import cell as __cell
    import chest as __chest
    import creature as __creature
    import basic as __basic
    import irregular as __irregular
    import item as __item
    for cell in (
        __block.Block, __block.Blank, __block.Target,
        __basic.Normal, __basic.Solid, __basic.Adamant,
        __irregular.Water, __irregular.Acid, __irregular.Poison,
        __irregular.Chocolate, __irregular.Stone, __irregular.Ice,
        __irregular.Magma, __irregular.Ruined,
        __item.Jupiter, __item.Mars, __item.Saturn, __item.Venus,
        __item.Mercury, __item.Moon, __item.Sun,
        __item.Life, __item.Power, __item.Protect, __item.Speed,
        __item.Summon, __item.Sorcery, __item.Shield, __item.Joeker,
        __creature.Slime, __creature.Tired,
        __creature.Matango, __creature.LargeMatango,
        __creature.BlockEater, __creature.BlockDemon, __creature.ArchDemon,
        __creature.Maxwell, __creature.Gargoyle,
        __creature.FireGhost, __creature.IceGhost, __creature.PoisonGhost,
        __creature.RIP,
        __chest.BronzeKey, __chest.SilverKey, __chest.GoldKey,
        __chest.IronChest, __chest.BronzeChest, __chest.SilverChest,
        __chest.GoldChest, __chest.Pandora,
        __chest.BronzeMimic, __chest.SilverMimic, __chest.GoldMimic,
        __chest.PandoraMimic
    ):
        __cell.Cell.add_collection(cell)
