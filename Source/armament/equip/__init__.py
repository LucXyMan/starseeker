#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""equip.__init__.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

装備パッケージ。
"""
import data as __data
get = __data.Equip.get_collection
get_all = __data.Equip.get_collections
get_by_name = __data.Equip.get_by_name
get_chest = __data.get_chest


def init():
    u"""パッケージ初期化。
    """
    import config as __config
    __config.init()
