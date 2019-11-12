#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""flash.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

フラッシュ画像生成モジュール。
"""
import utils.const as _const
import utils.image as _image
import utils.memoize as _memoize
__FLASH_TIME = _const.FRAME_DELAY << 2


def __get_key(*args):
    u"""フラッシュ画像キャッシュキー取得。
    """
    func, unit = args
    return u"{method}##{name}##{is_right}##{state}".format(
        method=u"{module}.{name}".format(
            module=func.__module__, name=func.__name__
        ), name=unit.data.name, is_right=unit.is_right, state=unit.state)


def __create_effect(unit, name):
    u"""エフェクト生成。
    """
    import random as __random
    import sprites.effects as __effects
    w = unit.rect.width >> 2
    h = unit.rect.height >> 2
    __effects.Image((
        unit.rect.centerx+__random.randint(-w, w),
        unit.rect.centery+__random.randint(-h, h)), name, vector=(0, -1))


def normal_generator(unit):
    u"""通常フラッシュジェネレータ。
    """
    @_memoize.memoize(get_key=__get_key)
    def __normal_generator(unit):
        u"""通常フラッシュに使用する画像を取得。
        """
        image = unit.current_image
        flash = _image.get_colored_sub(image, _const.WHITE)
        return tuple(
            flash if i & 0b11 == 0 else image for i in range(__FLASH_TIME))
    for image in __normal_generator(unit):
        yield image


def damage_generator(unit):
    u"""ダメージフラッシュジェネレータ。
    """
    @_memoize.memoize(get_key=__get_key)
    def __damage_generator(unit):
        u"""ダメージフラッシュに使用する画像を取得。
        """
        image = unit.current_image
        flash = _image.get_colored_add(image, _const.DARK_RED)
        return tuple(
            flash if i & 0b11 == 0 else image for i in range(__FLASH_TIME))
    for image in __damage_generator(unit):
        yield image


def recovery_generator(unit):
    u"""回復フラッシュジェネレータ。
    """
    @_memoize.memoize(get_key=__get_key)
    def __recovery_generator(unit):
        u"""回復フラッシュに使用する画像を取得。
        """
        image = unit.current_image
        flash = _image.get_colored_add(image, _const.DARK_BLUE)
        return tuple(
            flash if i & 0b11 == 0 else image for i in range(__FLASH_TIME))
    for image in __recovery_generator(unit):
        __create_effect(unit, "blue_light")
        yield image


def poison_generator(unit):
    u"""毒フラッシュジェネレータ。
    """
    @_memoize.memoize(get_key=__get_key)
    def __poison_generator(unit):
        u"""毒フラッシュに使用する画像を取得。
        """
        image = unit.current_image
        flash = _image.get_colored_add(image, _const.DARK_GREEN)
        return tuple(
            flash if i & 0b11 == 0 else image for i in range(__FLASH_TIME))
    for image in __poison_generator(unit):
            __create_effect(unit, "purple_bubble")
            yield image


def summon_generator(unit):
    u"""召喚フラッシュジェネレータ。
    """
    @_memoize.memoize(get_key=__get_key)
    def __summon_generator(unit):
        u"""召喚フラッシュに使用する画像を取得。
        """
        return tuple((_image.get_colored_add(
            unit.current_image, _const.RAINBOW[i & 0b111])
        ) for i in range(__FLASH_TIME))
    for image in __summon_generator(unit):
            yield image


def ability_generator(unit):
    u"""アビリティフラッシュジェネレータ。
    """
    @_memoize.memoize(get_key=__get_key)
    def __ability_generator(unit):
        u"""アビリティフラッシュに使用する画像を取得。
        """
        return tuple((_image.get_colored_add(
            unit.current_image, _const.BURNING[i & 0b111])
        ) for i in range(__FLASH_TIME))
    for image in __ability_generator(unit):
        __create_effect(unit, "red_light")
        yield image


def get(unit, type_):
    u"""フラッシュジェネレータ取得。
    """
    return (
        damage_generator(unit) if type_ == "Damage" else
        recovery_generator(unit) if type_ == "Recovery" else
        summon_generator(unit) if type_ == "Summon" else
        poison_generator(unit) if type_ == "Poison" else
        ability_generator(unit) if type_ == "Ability" else
        normal_generator(unit))
