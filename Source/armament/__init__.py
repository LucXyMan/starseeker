#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""armament.__init__.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ユニット・装備・アルカナデータパッケージ。
"""


def init():
    u"""パッケージの初期化。
    """
    import collectible as __collectible
    import equip as __equip
    import level as __level
    import skill as __skill
    import sorcery as __sorcery
    import units as __units
    __equip.init()
    __skill.init()
    __units.init()
    __sorcery.init()
    __collectible.init()
    __level.init()
