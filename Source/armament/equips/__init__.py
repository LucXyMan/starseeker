#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""equips.__init__.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

装備パッケージ。
"""
import equip as __equip
get = __equip.Equip.get_collection
get_all = __equip.Equip.get_collections
get_by_name = __equip.Equip.get_by_name
get_chest = __equip.get_chest


def init():
    u"""パッケージ初期化。
    """
    import config as __config
    __config.init()
