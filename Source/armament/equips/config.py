#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""config.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

装備設定モジュール。
"""


def init():
    u"""アイテムコレクション作成。
    """
    import accessory as __accessory
    import body as __body
    import equip as __equip
    import head as __head
    import utils.const as __const
    import weapon as __weapon
    __equip.Equip.set_collections(
        (__equip.Equip(0x000, u"空#装備なし#何もない#", 0, 0),) +
        __weapon.get()+__head.get()+__body.get()+__accessory.get())
    if __const.IS_OUTPUT:
        for i, equip in enumerate(__equip.Equip.get_collections()):
            print i, u":",  unicode(equip)
        names = []
        image_numbers = []
        for equip in __equip.Equip.get_collections():
            if equip.name not in names:
                names.append(equip.name)
            else:
                raise ValueError("Duplicate Item name.")
            if equip.image_number not in image_numbers:
                image_numbers.append(equip.image_number)
            else:
                raise ValueError("Duplicate Item Icon.")
            if equip.number in equip.keys:
                print unicode(equip)
                raise ValueError("Invalid Key.")
