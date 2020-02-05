#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""unit.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ユニット画像モジュール。
"""


def init(container):
    u"""モジュール初期化。
    """
    import utils.image as __image
    global __units

    def __process_player():
        u"""プレイヤー画像加工。
        """
        source = __image.load(container.get("players.png"))
        colors = [
            __image.get_segment(
                __image.get_another_color(source, color), (8, 2), (48, 64)
            ) for color in range(9)]
        __units["altair"] = colors[0][0], colors[1][0]
        __units["corvus"] = colors[1][1], colors[0][9]
        __units["nova"] = colors[2][2], colors[1][2]
        __units["sirius"] = colors[3][3], colors[7][11]
        __units["castor"] = colors[4][4], colors[0][4]
        __units["pluto"] = colors[5][5], colors[2][5]
        __units["regulus"] = colors[6][6], colors[1][6]
        __units["lucifer"] = colors[3][7], colors[7][7]
        image, = __image.get_segment(
            __image.get_another_color(source, 8), (1, 1), (72, 96), (0, 128))
        __units["nebula"] = (image,)*2

    def __process_creature():
        u"""クリーチャー画像加工。
        """
        source = __image.load(container.get("creatures.png"))
        for i in range(16):
            other = __image.get_another_color(source, i)
            for image, name in zip(
                __image.get_segment(other, (8, 2), (32, 32)), (
                    "basic#slime", "flying#bat", "basic#cat", "flying#crow",
                    "basic#rat", "flying#fly", "basic#snake", "flying#fish",
                    "flying#elemental", "basic#mole", "basic#spider")
            ):
                type_, name = name.split("#")
                __units[name+"_"+str(i)] = (
                    __image.get_flying(image) if type_ == "flying" else image)
            __units["wolf_"+str(i)], = __image.get_segment(
                other, (1, 1), (48, 48), (0, 64))
            __units["baku_"+str(i)], = __image.get_segment(
                other, (1, 1), (48, 32), (48, 80))
            seed, herb = __image.get_segment(other, (2, 1), (32, 32), (0, 144))
            flower, = __image.get_segment(other, (1, 1), (32, 64), (64, 112))
            __units["seed"+"_"+str(i)] = seed
            herb.blit(seed, (0, 0))
            __units["herb"+"_"+str(i)] = herb
            flower.blit(herb, (0, 32))
            __units["flower"+"_"+str(i)] = flower
            dragon, = __image.get_segment(other, (1, 1), (64, 64), (0, 176))
            __units["dragon"+"_"+str(i)] = dragon
    __units = {}
    for func in (__process_player, __process_creature):
        func()


def get(key):
    u"""ユニット画像取得。
    """
    return __units[key]
