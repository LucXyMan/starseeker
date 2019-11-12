#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""generalpy

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

汎用表示物モジュール。
"""
import pygame as _pygame


class Indicator(_pygame.sprite.DirtySprite):
    u"""インジケータ。
    """
    def __init__(self, gropus=None):
        u"""コンストラクタ。
        """
        super(Indicator, self).__init__(
            (self.group, self.draw_group) if gropus is None else gropus)


class Equip(Indicator):
    u"""装備情報。
    効果発動時に点滅する。
    """
    __FLASH_PERIOD = 16
    __SEAL_IMAGE_COLOR = 15
    __seal_images = ()

    def __init__(self, pos, item, groups=None):
        u"""コンストラクタ。
        """
        def __init_seal_images():
            u"""封印画像が設定されていない時に画像を作成。
            """
            import material.icon as __icon
            if not Equip.__seal_images:
                Equip.__seal_images = (
                    __icon.get(11, 0, self.__SEAL_IMAGE_COLOR),
                    __icon.get(12, 0, self.__SEAL_IMAGE_COLOR),
                    __icon.get(13, 0, self.__SEAL_IMAGE_COLOR),
                    _pygame.transform.flip(__icon.get(
                        12, 0, self.__SEAL_IMAGE_COLOR), True, False))
        super(Equip, self).__init__(groups)
        self.__item = item
        self.image = self.__base_image = self.__item.icon
        __init_seal_images()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.__animation = None
        self.update()

    def __repr__(self):
        u"""文字列表現取得。
        """
        return u"<name: {name}>".format(name=self.__item.name)

    def flash(self):
        u"""フラッシュ開始。
        フラッシュジェネレータ設定。
        """
        import utils.memoize as __memoize

        def __flash_generator():
            u"""フラッシュジェネレータ。
            """
            import random as __random
            import sprites.effects as __effects
            import utils.const as __const

            @__memoize.memoize()
            def __get_flash_images(item):
                u"""フラッシュに使用する値を取得。
                """
                import utils.image as __image
                return tuple((
                    __image.get_colored_add(
                        item.icon, __const.RAINBOW[i & 0b111]))
                    for i in range(self.__FLASH_PERIOD))
            for i, image in enumerate(__get_flash_images(self.__item)):
                pos = i >> 1
                __effects.Image((
                    self.rect.centerx+__random.randint(-pos, pos),
                    self.rect.centery+__random.randint(-pos, pos)),
                    "yellow_light#blue_light#green_light#purple_light")
                yield image
        self.__animation = __flash_generator()

    def update(self):
        u"""画像の更新。
        """
        import utils.counter as __counter
        import utils.image as __image
        if self.__animation:
            try:
                self.image = self.__animation.next()
            except StopIteration:
                self.image = self.__item.icon
                self.__animation = None
        else:
            if not self.__item.is_useable and self.__item.number != 0:
                image = __image.copy(self.__base_image)
                image.blit(self.__seal_images[__counter.get_frame(4)], (0, 0))
                self.image = image
            else:
                self.image = self.__base_image


class Star(Indicator):
    u"""スターインジケータ。
    取得したスターの量を表示する。
    """
    __IMAGES = (
        "jupiter", "mars", "saturn", "venus", "mercury", "moon", "sun")
    __PART = 4
    __LV2_IMAGE_LINE = 8
    __LV3_IMAGE_LINE = 16

    def __init__(self, system, type_, groups=None):
        u"""__typeによりスター画像種類を決定。
        """
        super(Star, self).__init__(groups)
        self.__resorce = system.resorce
        self.__type = type_
        self.__old = -1
        self.__number = self.__dest = 0
        self.update()
        self.rect = self.image.get_rect()

    def update(self):
        u"""画像と添字の更新。
        """
        def __set_dest():
            u"""目的の値を設定。
            """
            stars = self.__resorce.stars
            if self.__old != stars[self.__type]:
                self.__dest = stars[self.__type]
                self.__old = stars[self.__type]

        def __rise_and_fall():
            u"""目盛りの増減。
            """
            if self.__number < self.__dest:
                self.__number += 1
            elif self.__number > self.__dest:
                self.__number -= 1
        import material.block as __block
        import material.string as __string
        import utils.const as __const
        super(Star, self).update()
        get = __block.get
        stars = self.__resorce.stars
        __set_dest()
        __rise_and_fall()
        dummy, = get("dummy")
        self.image = __string.get_subscript(
            get(self.__IMAGES[self.__type])[self.__PART*(
                0 if stars[self.__type] < self.__LV2_IMAGE_LINE else
                1 if stars[self.__type] < self.__LV3_IMAGE_LINE else
                2)], str(self.__number >> __const.STAR_ENERGY_SHIFT),
            __string.ElmCharColor.get(self.__type)
        ) if self.__number else dummy
