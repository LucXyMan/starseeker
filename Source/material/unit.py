#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""unit.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ユニット画像モジュール。
"""


def init(container):
    u"""モジュール初期化。
    """
    import utils.image as __image
    global __units

    def __player_processing():
        u"""プレイヤー画像加工。
        """
        source = __image.load(container.get("players.png"))
        for i, name in enumerate((
            "b#altair", "a#corvus", "b#nova", "a#sirius",
            "b#castor", "b#pluto", "b#regulus", "b#lucifer"
        )):
            images = __image.segment(
                __image.get_other_color(source, i), (9, 2), (48, 64))
            type_, name = name.split("#")
            __units[name] = (
                (images[i], images[i+9]) if type_ == "a" else
                (images[i], images[i]))
        basic, = __image.segment(
            __image.get_other_color(source, i+1), (1, 1), (72, 96), (0, 128))
        __units["nebula"] = basic, basic

    def __creature_processing():
        u"""クリーチャー画像加工。
        """
        source = __image.load(container.get("creatures.png"))
        for i in range(16):
            other = __image.get_other_color(source, i)
            for image, name in zip(__image.segment(other, (8, 1), (32, 32)), (
                "b#slime", "f#bat", "b#cat", "f#crow", "b#rat", "f#fly",
                "b#snake", "f#fish"
            )):
                type_, name = name.split("#")
                __units[name+"_"+str(i)] = __image.get_flying(image) if \
                    type_ == "f" else image
            for image, name in zip(__image.segment(
                other, (1, 1), (48, 48), (0, 32)), ("wolf",)
            ):
                __units[name+"_"+str(i)] = image
            seed, herb, flower = __image.segment(
                other, (3, 1), (32, 64), (0, 80))
            __units["seed"+"_"+str(i)] = seed
            herb.blit(seed, (0, 0))
            __units["herb"+"_"+str(i)] = herb
            flower.blit(herb, (0, 0))
            __units["flower"+"_"+str(i)] = flower
            doragon, = __image.segment(other, (1, 1), (96, 96), (0, 144))
            __units["doragon"+"_"+str(i)] = doragon
    __units = {}
    for func in (__player_processing, __creature_processing):
        func()


def get(key):
    u"""ユニット画像取得。
    """
    return __units[key]
