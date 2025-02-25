#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""hud.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

HUDモジュール。
"""
import pygame as _pygame
import utils.const as _const


class HUD(_pygame.sprite.DirtySprite):
    u"""ヘッドアップディスプレイ。
    """
    def __init__(self, gropus=None):
        u"""コンストラクタ。
        """
        super(HUD, self).__init__(
            (self.group, self.draw_group) if gropus is None else gropus)


class Equip(HUD):
    u"""装備表示。
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
                    __icon.get(0xB00 | self.__SEAL_IMAGE_COLOR),
                    __icon.get(0xC00 | self.__SEAL_IMAGE_COLOR),
                    __icon.get(0xD00 | self.__SEAL_IMAGE_COLOR),
                    _pygame.transform.flip(__icon.get(
                        0xC00 | self.__SEAL_IMAGE_COLOR), True, False))
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
        """
        def __generator():
            u"""フラッシュジェネレータ。
            """
            import random as __random
            import sprites.effects as __effects
            import material.icon as __icon
            x = (self.__item.image_number & 0xF00) >> 8
            y = (self.__item.image_number & 0x0F0) >> 4
            color = self.__item.image_number & 0x00F
            for i in range(color, color+self.__FLASH_PERIOD):
                pos = i >> 2
                __effects.Image((
                    self.rect.centerx+__random.randint(-pos, pos),
                    self.rect.centery+__random.randint(-pos, pos)),
                    "yellow_light#blue_light#green_light#purple_light")
                yield __icon.get(x << 8 | y << 4 | i % self.__FLASH_PERIOD)
        self.__animation = __generator()

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
            if not self.__item.is_available and self.__item.number != 0:
                image = __image.copy(self.__base_image)
                image.blit(self.__seal_images[__counter.get_frame(4)], (0, 0))
                self.image = image
            else:
                self.image = self.__base_image


class Star(HUD):
    u"""スター表示。
    取得したスターの量を表示する。
    """
    __FRAME = 4
    __IMAGES = (
        "jupiter", "mars", "saturn", "venus", "mercury", "moon", "sun")
    __EFFECTS = (
        _const.JUPITER_EFFECT, _const.MARS_EFFECT, _const.SATURN_EFFECT,
        _const.VENUS_EFFECT, _const.MERCURY_EFFECT, _const.MOON_EFFECT,
        _const.SUN_EFFECT)
    __LV2_THRESHOLD = 8
    __LV3_THRESHOLD = 16

    def __init__(self, resource, type_, groups=None):
        u"""__typeによりスター画像種類を決定。
        """
        super(Star, self).__init__(groups)
        self.__resource = resource
        self.__type = type_
        self.__amount = 0
        self.update()
        self.rect = self.image.get_rect()

    def update(self):
        u"""画像と添字の更新。
        """
        import material.block as __block
        import material.string as __string
        import utils.counter as __counter

        def __fluctuate():
            u"""目盛りの増減。
            """
            def __effect():
                u"""エフェクト発動。
                """
                import random as __random
                import sprites.effects as __effects
                pos = self.__amount >> 1
                __effects.Image((
                    self.rect.centerx+__random.randint(-pos, pos),
                    self.rect.centery+__random.randint(-pos, pos)),
                    self.__EFFECTS[self.__type], vector=(0, -1))
            stars = self.__resource.stars
            if self.__amount < stars[self.__type]:
                self.__amount += 1
            elif self.__amount > stars[self.__type]:
                self.__amount -= 1
                __effect()
        super(Star, self).update()
        __fluctuate()
        dummy, = __block.get("dummy")
        images = __block.get(self.__IMAGES[self.__type])
        level = (
            0 if self.__amount < self.__LV2_THRESHOLD else
            1 if self.__amount < self.__LV3_THRESHOLD else 2)
        image = __string.get_subscript(
            images[self.__FRAME*level+__counter.get_frame(4)],
            str(self.__amount >> _const.STAR_ENERGY_SHIFT),
            __string.ElmCharColor.get(self.__type))
        self.image = image if self.__amount else dummy
