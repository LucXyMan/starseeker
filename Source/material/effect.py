#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""effect.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

エフェクト画像加工モジュール。
"""


def init(container):
    u"""モジュール初期化。
    """
    import utils.image as __image
    global __effects

    def __process_light():
        u"""光エフェクト画像加工。
        """
        basic = __image.load(container.get("light_effect.png"))
        for i, name in enumerate(("blue", "green", "purple", "red", "yellow")):
            __effects[name+"_light"] = __image.get_segment(
                __image.get_another_color(basic, i), (5, 1), (9, 9))

    def __process_fire():
        u"""炎エフェクト画像加工。
        """
        basic = __image.load(container.get("fire_effect.png"))
        for i, name in enumerate((
            "red", "blue", "green", "white", "black", "yellow"
        )):
            image = __image.get_another_color(basic, i)
            __effects[name+"_fire"] = __image.get_segment(
                image, (5, 1), (9, 11))
            __effects[name+"_explosion"] = __image.get_segment(
                image, (6, 1), (11, 11), (0, 11))
            __effects[name+"_smoke"] = __image.get_segment(
                image, (5, 1), (11, 11), (0, 22))

    def __process_bubble():
        u"""泡エフェクト画像加工。
        """
        basic = __image.load(container.get("bubble_effect.png"))
        for i, name in enumerate(("blue", "purple", "yellow")):
            image = __image.get_another_color(basic, i)
            __effects[name+"_bubble"] = __image.get_segment(
                image, (5, 1), (10, 10))
            __effects[name+"_ice"] = __image.get_segment(
                image, (4, 1), (9, 9), (0, 10))
            __effects[name+"_line"] = __image.get_segment(
                image, (6, 1), (1, 6), (0, 19))

    def __process_star():
        u"""星形エフェクト画像加工処理。
        """
        def __create_rainbow(start):
            u"""レインボーの星型を生成する。
            """
            return tuple(
                comets[j+5*((i+start) & 0b111)] for
                i, j in enumerate(range(5)+range(5)[-1::-1]))
        basic = __image.load(container.get("star_effect.png"))
        comets = reduce(lambda x, y: x+y, (
            __image.get_segment(star, (5, 1), (19, 20), (0, 20)) for
            star in (__image.get_another_color(basic, i) for i in range(8))))
        for i in range(8):
            __effects["comet_"+str(i)] = __create_rainbow(i)
    __effects = {}
    for func in (
        __process_light, __process_fire,
        __process_bubble, __process_star
    ):
        func()


def get(key):
    u"""エフェクト画像取得。
    """
    return __effects[key]
