#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""icon.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

アイコン画像素材モジュール。
"""


def init(container):
    u"""モジュール初期化。
    """
    global __items

    def __icon_proc():
        u"""アイテム画像加工。
        """
        import utils.image as __image
        basic = __image.load(container.get("items.png"))
        height = 6
        for surf in (__image.get_other_color(basic, i) for i in range(16)):
            part = __image.segment(surf, (16, height))
            __items.append([part[j*16:j*16+16] for j in range(height)])
    __items = []
    __icon_proc()


def get(x, y, c):
    u"""アイコン画像取得。
    """
    return __items[c][y][x]
