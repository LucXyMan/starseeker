#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""effects.__init__.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

エフェクトスプライトパッケージ。
"""
import effect as __effect
import image as __image
import string as __string
Effect = __effect.Effect
Image = __image.Image
Damage = __string.Damage
Recovery = __string.Recovery
Special = __string.Special
Spell = __string.Spell
Delete = __string.Delete
Rival = __string.Rival
Level = __string.Level
Win = __string.Win
Lose = __string.Lose
Draw = __string.Draw
Bonus = __string.Bonus


def init():
    u"""パッケージ初期化。
    """
