#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""material.__init__.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

素材パッケージ。
"""
import sound as __sound
BGM = __sound.BGM


def init():
    u"""パッケージの初期化。
    """
    import os as __os
    import block as __block
    import effect as __effect
    import icon as __icon
    import misc as __misc
    import string as __string
    import utils.packer as __packer
    import unit as __unit
    container = __packer.Container(
        __os.path.join(__os.path.dirname(__file__), "images.enc"))
    __sound.init()
    __string.init()
    __icon.init(container)
    __block.init(container)
    __effect.init(container)
    __misc.init(container)
    __unit.init(container)
