#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""shadow.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

影スプライトモジュール。
"""
import pygame as _pygame


class Shadow(_pygame.sprite.DirtySprite):
    u"""ユニットの影。
    """
    __FRAME = 8

    def __init__(self, caster, groups=None):
        u"""ユニットをキャストする。
        """
        super(Shadow, self).__init__(
            (self.group, self.draw_group) if groups is None else groups)
        self.__caster = caster
        self.update()

    def __repr__(self):
        u"""文字列表現取得。
        """
        return u"<caster: {caster}>".format(caster=self.__caster)

    def update(self):
        u"""画像更新。
        ユニットのパワーアップ状態に合わせて色が変化。
        """
        import utils.counter as __counter
        import utils.memoize as __memoize

        def __get_key(*args):
            u"""影画像キャッシュキー取得。
            """
            func, myself = args
            return u"{method}##{name}##{level}##{is_right}".format(
                method=u"{module}.{name}".format(
                    module=func.__module__, name=func.__name__),
                name=myself.__caster.data.name, level=myself.__caster.level,
                is_right=myself.__caster.is_right)

        @__memoize.memoize(get_key=__get_key)
        def __get_images(myself):
            u"""影画像タプル取得。
            """
            import utils.image as __image
            images = []
            for i in range(1, 5):
                image = __image.copy(myself.__caster.base_image)
                array = _pygame.PixelArray(image)
                r, b, g = myself.__caster.level
                color = _pygame.Color(*map(
                    lambda x: 0xFF if 0xFF < x*(i << 4)+0x04 else
                    x*(i << 4)+0x04, (r, g, b)))
                for x in range(len(array)):
                    for y in range(len(array[0])):
                        if array[x][y] != 0x000000:
                            array[x][y] = color
                w, h = image.get_size()
                image = _pygame.transform.scale(image, (w, h >> 2))
                if myself.__caster.is_right:
                    image = _pygame.transform.flip(image, True, False)
                images.append(image)
            images = images+images[::-1]
            return tuple(images)
        if self.__caster.alive():
            images = __get_images(self)
            self.image = images[__counter.get_frame(self.__FRAME)]
            self.rect = self.image.get_rect()
            self.rect.midbottom = self.__caster.rect.midbottom
        else:
            self.kill()
