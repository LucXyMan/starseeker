#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""arcnaum.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

アルカナスプライトモジュール。
"""
import pygame as __pygame
import material.string as _string
import utils.const as _const


class Arcanum(__pygame.sprite.DirtySprite):
    u"""アルカナスプライト。
    """
    __STEP = 4
    __FLASH_PERIOD = 16
    _PART = _const.FRAME_DELAY*4

    @classmethod
    def _init_images(cls):
        u"""アルカナ画像初期化。
        """
        import material.icon as __icon
        if not hasattr(cls, "_IMAGES"):
            color, sub_color = cls._COLORS
            sub_image = (() if sub_color == -1 else reduce(lambda x, y: x+y, (
                (__icon.get(2+i, 0, sub_color),)*_const.FRAME_DELAY for
                i in range(4))))
            cls._IMAGES = reduce(lambda x, y: x+y, (
                (__icon.get(2+i, 0, color),)*_const.FRAME_DELAY for
                i in range(4)))+sub_image

    def __init__(self, system, contents, groups=None):
        u"""コンストラクタ。
        """
        def __init_generator(image):
            u"""出現時アニメーションジェネレータ。
            """
            import material.block as __block
            for i in range(self.__FLASH_PERIOD << 1):
                yield image if i & 0b11 == 0 else __block.get("dummy")[0]
        super(Arcanum, self).__init__(
            (self.group, self.draw_group) if groups is None else ())
        self._init_images()
        self.image = self._IMAGES[0]
        self._system = system
        self._contents = contents
        self._cost = -1
        self._star = -1
        self.__frame = 0
        self._is_front = isinstance(self, Shield)
        self._is_colored = False
        self.__is_burning = False
        self.__animation = __init_generator(self.image)
        self.rect = self.image.get_rect()
        self.__dest = self.rect.copy()
        self.__fires = (key for key in (
            ("blue_fire",)*(self.__FLASH_PERIOD >> 1) +
            ("red_fire",)*(self.__FLASH_PERIOD >> 2) +
            ("white_fire",)*(self.__FLASH_PERIOD >> 3) +
            ("black_fire",)*(self.__FLASH_PERIOD >> 3)))
        self.update()

    def __repr__(self):
        u"""文字列表現取得。
        """
        return (
            u"<name: {name}, is_useable: {is_useable}, "
            u"is_colored: {is_colored}>").format(
                name=self.__class__.__name__, is_useable=self.__is_useable,
                is_colored=self._is_colored)

    def set_available(self):
        u"""コスト番号とエレメンタル種類を設定。
        """
    def burn(self):
        u"""カードの消失処理を設定。
        """
        def __burn_generator():
            u"""カード消失時画像ジェネレータ。
            """
            import math as __math
            import sprites.effects as __effects
            import utils.memoize as __memoize
            import material.sound as __sound

            @__memoize.memoize()
            def __get_burn_images(self):
                u"""カード消失時画像取得。
                """
                import utils.image as __image
                image = self._IMAGES[
                    (self._PART-1 if self.__is_useable else 0) +
                    (self._PART if self._is_colored else 0)]
                return tuple(
                    image if i & 0b11 == 0 else __image.get_colored_add(
                        image, _const.BURNING[i & 0b111]) for i in range(
                            self.__FLASH_PERIOD))
            __sound.SE.play("Fire")
            for i, image in enumerate(__get_burn_images(self)):
                angle = 6.28/self.__FLASH_PERIOD
                vector = round(__math.cos(i*angle)), round(__math.sin(i*angle))
                __effects.Image(
                    (self.rect.centerx, self.rect.centery),
                    self.__fires.next(), vector=vector)
                yield image
        self.__animation = __burn_generator()
        self.__is_burning = True

    def _update_subscript(self):
        u"""添字の更新処理。
        """
        self.image = _string.get_subscript(
            self.image, str(self._contents.rank), _string.CharColor() if
            self._contents.rank == 0 else _string.ElmCharColor.get(
                self._star, False if self._cost < 2 else True))

    def update(self):
        u"""画像の更新。
        召喚使用可能の場合は表、代替召喚使用可能の場合色違い、
        使用不能の場合は裏の画像で表示される。
        """
        def __move():
            u"""移動処理。
            """
            if (
                hasattr(self, "rect") and not any(
                    self._system.id == sprite._system.id and
                    sprite.__is_burning for sprite in self.group)
            ):
                dest_x, dest_y = self.__dest.topleft
                if self.rect.x != dest_x:
                    self.rect.move_ip(
                        self.__STEP if self.rect.x < dest_x else
                        -self.__STEP, 0)
                if self.rect.y != dest_y:
                    self.rect.move_ip(
                        0, self.__STEP if self.rect.y < dest_y else
                        -self.__STEP)
        if self.__animation:
            try:
                self.image = self.__animation.next()
            except StopIteration:
                if self.__is_burning:
                    self.kill()
                else:
                    self.__animation = None
        else:
            if self.__is_useable:
                if self.__frame < self._PART-1:
                    self.__frame += 1
            else:
                if 0 < self.__frame:
                    self.__frame -= 1
            self.image = self._IMAGES[self.__frame+(
                self._PART if self._is_colored else 0)]
        self._update_subscript()
        self.__dest.size = self.rect.size = self.image.get_size()
        __move()

    @property
    def contents(self):
        u"""コンテンツ取得。
        """
        return self._contents

    @property
    def dest(self):
        u"""移動先の位置取得。
        """
        return self.__dest

    @property
    def __is_useable(self):
        u"""使用可能状態で真。
        """
        return self._cost and self._is_front

    @property
    def is_moving(self):
        u"""移動状態で真。
        """
        return self.rect != self.__dest


class Summon(Arcanum):
    u"""召喚アルカナ。
    """
    _COLORS = 1, 6

    def set_available(self):
        u"""コスト番号とエレメンタル種類を設定。
        """
        battle = self._system.battle
        self._cost, self._star = (
            self._system.resorce.get_available(self._contents))
        is_fusionable = bool(battle.group.adapt(self._contents))
        self._is_front = battle.is_sorcery_usable and (
            is_fusionable if battle.group.is_full else True)
        self._is_colored = is_fusionable


class Sorcery(Arcanum):
    u"""魔術アルカナ。
    """
    _COLORS = 5, 4

    def set_available(self):
        u"""コスト番号とエレメンタル種類を設定。
        """
        def __is_pileable():
            u"""魔術合成可能な場合に真。
            """
            if battle.pile:
                return bool(self._contents.adapt(battle.pile))
            return False
        battle = self._system.battle
        self._cost, self._star = self._system.resorce.get_available(
            self._contents)
        self._is_front = battle.is_sorcery_usable
        self._is_colored = __is_pileable()


class __Simple(Arcanum):
    u"""色変化しないアルカナ。
    """
    def _update_subscript(self):
        u"""添字の更新処理。
        """
        self.image = _string.get_subscript(self.image, "")


class Shield(__Simple):
    u"""シールドアルカナ。
    """
    _COLORS = 3, -1


class Joeker(__Simple):
    u"""ジョーカーアルカナ。
    """
    _COLORS = 8, -1

    def set_available(self):
        u"""コスト番号とエレメンタル種類を設定。
        """
        self._is_front = self._system.battle.is_sorcery_usable
