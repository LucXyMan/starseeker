#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""misc.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

その他素材モジュール。
"""


def init(container):
    u"""モジュール初期化。
    """
    global __miscs

    def __bg_processing():
        u"""背景画像加工。
        """
        import utils.image as __image
        for name in (
            "bb", "starry_sky", "crypt", "boneyard", "night_city", "ruins",
            "catacombe", "title"
        ):
            __miscs[name] = __image.load(container.get(name+".png"))
    __miscs = {}
    __bg_processing()


def get(key):
    u"""その他画像取得。
    """
    return __miscs[key]
