#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""label.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ラベルモジュール。
"""
import sprites.general as __general


class Label(__general.General):
    u"""ラベルスプライト。
    アイコンと名前を持つラベル。
    """
    def _get_item(self, number):
        u"""ラベル画像に使用するアイテム取得。
        """
        import armament.equip as __equip
        return __equip.get(number)

    def _get_image(self, icon, name):
        u"""画像取得。
        """
        import pygame as __pygame
        import material.string as __string
        import utils.const as __const
        import utils.image as __image
        icon_x, icon_y = icon.get_size()
        name = __string.get_string(
            name, __const.SYSTEM_CHAR_SIZE, shorten=False)
        name_x, name_y = name.get_size()
        h = max(icon_y, name_y)
        image = __pygame.Surface((icon_x+name_x, h))
        __image.set_colorkey(image, "0x000000")
        if hasattr(self, "rect"):
            self.rect.size = image.get_size()
        else:
            self.rect = image.get_rect()
        image.blit(icon, (0, 0))
        image.blit(
            name, (icon_x, ((h-min(icon_y, __const.SYSTEM_CHAR_SIZE))/2)))
        return image
