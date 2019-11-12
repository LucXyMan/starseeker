#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""armament.__init__.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ユニット・装備・特殊効果パッケージ。
"""


def init():
    u"""パッケージの初期化。
    """
    import collectible as __collectible
    import equips as __equips
    import levels as __levels
    import skill as __skill
    import specials as __specials
    import units as __units
    __equips.init()
    __skill.init()
    __units.init()
    __specials.init()
    __collectible.init()
    __levels.init()
