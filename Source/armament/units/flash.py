#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""flash.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

フラッシュ画像生成モジュール。
"""


def get(unit, type_):
    u"""フラッシュジェネレータ取得。
    """
    import utils.const as _const
    import utils.image as _image
    __FLASH_TIME = _const.FRAME_DELAY << 2

    def __create_effect(unit, name):
        u"""エフェクト生成。
        """
        import random as __random
        import sprites.effects as __effects
        w = unit.rect.width >> 2
        h = unit.rect.height >> 2
        if name:
            __effects.Image((
                unit.rect.centerx+__random.randint(-w, w),
                unit.rect.centery+__random.randint(-h, h)),
                name, vector=(0, -1))

    def __generator(color="", effect=""):
        u"""フラッシュジェネレータ。
        """
        image = unit.current_image
        flash = _image.get_colored_add(image, color)
        for i in range(__FLASH_TIME):
            __create_effect(unit, effect)
            yield flash if i & 0b11 == 0 else image

    def __normal_generator():
        u"""基本フラッシュジェネレータ。
        """
        image = unit.current_image
        flash = _image.get_colored_sub(image, _const.WHITE)
        for i in range(__FLASH_TIME):
            yield flash if i & 0b11 == 0 else image

    def __summon_generator():
        u"""召喚フラッシュジェネレータ。
        """
        for image in ((_image.get_colored_add(
            unit.current_image, _const.RAINBOW[i & 0b111])
        ) for i in range(__FLASH_TIME)):
            yield image

    def __skill_generator():
        u"""スキルフラッシュジェネレータ。
        """
        for image in ((_image.get_colored_add(
            unit.current_image, _const.BURNING[i & 0b111])
        ) for i in range(__FLASH_TIME)):
            __create_effect(unit, "red_light")
            yield image
    return (
        __generator(
            _const.DARK_RED) if type_ == "damage" else
        __generator(
            _const.DARK_BLUE, "blue_light") if type_ == "recovery" else
        __generator(
            _const.DARK_GREEN, "purple_bubble") if type_ == "poison" else
        __summon_generator() if type_ == "summon" else
        __skill_generator() if type_ == "skill" else
        __normal_generator())
