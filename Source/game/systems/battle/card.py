#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""card.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

カードスプライトモジュール。
"""
import material.icon as _icon
import material.string as _string
import utils.const as _const
import sprites as __sprites


# ---- Simple Card ----
class Card(__sprites.huds.HUD):
    u"""アルカナカード。
    """
    __STEP = 4
    __FLASH_PERIOD = 16
    __FIRE_IMAGES = tuple(
        ("blue_fire",)*(__FLASH_PERIOD >> 1) +
        ("red_fire",)*(__FLASH_PERIOD >> 2) +
        ("white_fire",)*(__FLASH_PERIOD >> 3) +
        ("black_fire",)*(__FLASH_PERIOD >> 3))
    __FRAME = _const.FRAME_DELAY << 2
    __vectors = ()
    _images = ()

    @classmethod
    def _init_images(cls):
        u"""アルカナ画像初期化。
        """
        if not cls._images:
            color, sub_color = cls._COLORS
            sub_image = () if sub_color == -1 else reduce(lambda x, y: x+y, ((
                _icon.get(2+i << 8 | sub_color),)*_const.FRAME_DELAY for
                i in range(4)))
            cls._images = reduce(lambda x, y: x+y, ((
                _icon.get(2+i << 8 | color),)*_const.FRAME_DELAY for
                i in range(4)))+sub_image

    def __init__(self, hand, arcanum, groups=None):
        u"""コンストラクタ。
        """
        def __init_generator(image):
            u"""出現時画像ジェネレータ。
            """
            for i in range(self.__FLASH_PERIOD << 1):
                yield image if i & 0b11 == 0 else _icon.get(0x000)
        super(Card, self).__init__(groups)
        self._init_images()
        self.image = self._images[0]
        self.__animation = __init_generator(self.image)
        self.__frame = 0
        self.__hand = hand
        self._arcanum = arcanum
        self._available_state = 0x001
        self._is_available = isinstance(self, (Support, Shield))
        self._is_colored = False
        self.__is_burning = False
        self.rect = self.image.get_rect()
        self.__dest = self.rect.copy()
        self.update()

    def __repr__(self):
        u"""文字列表現取得。
        """
        return (
            u"<name: {name}, is_front: {is_front}, is_colored: {is_colored}>"
        ).format(
            name=self.__class__.__name__, is_front=self.__is_front,
            is_colored=self._is_colored)

    # ---- Update ----
    def _update_subscript(self):
        u"""添字更新。
        """
        self.image = _string.get_subscript(self.image, "")

    def update(self):
        u"""画像更新。
        召喚使用可能の場合は表、代替召喚使用可能の場合色違い、
        使用不能の場合は裏の画像で表示される。
        """
        def __move():
            u"""移動処理。
            """
            if not self.__hand.is_remaining:
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
            if self.__is_front and self.__frame < self.__FRAME-1:
                self.__frame += 1
            elif 0 < self.__frame:
                self.__frame -= 1
            self.image = self._images[
                self.__frame+(self.__FRAME if self._is_colored else 0)]
        self._update_subscript()
        self.__dest.size = self.rect.size = self.image.get_size()
        __move()

    def burn(self):
        u"""カードを燃やす。
        """
        self.flash()
        self.__is_burning = True

    def flash(self):
        u"""カードを光らせる。
        """
        def __generator():
            u"""フラッシュ画像ジェネレータ。
            """
            import math as __math
            import random as __random
            import sprites.effects as __effects
            import material.sound as __sound
            color = self._COLORS[1] if self._is_colored else self._COLORS[0]
            if self.__is_burning:
                if not Card.__vectors:
                    angle = __math.pi*2/self.__FLASH_PERIOD
                    Card.__vectors = tuple((
                        round(__math.cos(i*angle)), round(__math.sin(i*angle))
                    ) for i in range(self.__FLASH_PERIOD))
                for i, vector in enumerate(Card.__vectors, color):
                    __sound.SE.play("fire")
                    __effects.Image((
                        self.rect.centerx, self.rect.centery),
                        self.__FIRE_IMAGES[i % self.__FLASH_PERIOD],
                        vector=vector)
                    yield _icon.get(2+(self.__frame >> 2) << 8 | i & 0b1111)
            else:
                for i in range(color, color+self.__FLASH_PERIOD):
                    pos = i >> 2
                    __effects.Image((
                        self.rect.centerx+__random.randint(-pos, pos),
                        self.rect.centery+__random.randint(-pos, pos)),
                        "yellow_light#blue_light#green_light#purple_light")
                    yield _icon.get(2+(self.__frame >> 2) << 8 | i & 0b1111)
        self.__animation = __generator()

    # ---- Setter ----
    def set_state(self, system):
        u"""状態設定。
        """
    # ---- Property ----
    @property
    def arcanum(self):
        u"""カード内容取得。
        """
        return self._arcanum

    @property
    def dest(self):
        u"""移動先の位置取得。
        """
        return self.__dest

    # ---- Detection ----
    @property
    def __is_front(self):
        u"""表表示判定。
        """
        order = self._available_state & 0x00F
        return 0 < order and self._is_available

    @property
    def is_moving(self):
        u"""移動状態判定。
        """
        return self.rect != self.__dest


class Support(Card):
    u"""サポートカード。
    """
    _COLORS = 7, -1

    def _update_subscript(self):
        u"""添字の更新処理。
        """
        self.image = _string.get_subscript(
            self.image, self._arcanum.subscript)


class Shield(Card):
    u"""シールドカード。
    """
    _COLORS = 3, -1


class Joker(Card):
    u"""ジョーカーカード。
    """
    _COLORS = 8, -1

    def set_state(self, system):
        u"""状態設定。
        """
        self._is_available = system.battle.is_arcana_available


# ---- Changeable Card ----
class __Changeable(Card):
    u"""色変化カード。
    """
    def _update_subscript(self):
        u"""添字更新。
        """
        order = self._available_state & 0x00F
        star = (self._available_state & 0x0F0) >> 4
        division = (self._available_state & 0xF00) >> 8
        is_sub = 1 < order
        rank = self._arcanum.rank
        rank = rank >> division
        self.image = _string.get_subscript(
            self.image, str(rank+1 if is_sub else rank),
            _string.ElmCharColor.get(star, is_sub))


class Summon(__Changeable):
    u"""サモンカード。
    """
    _COLORS = 1, 6

    def set_state(self, system):
        u"""状態設定。
        """
        group = system.battle.group
        self._available_state = (
            system.resource.get_available_state(self._arcanum))
        self._is_colored = bool(group.adapt(self._arcanum))
        is_fulfill = not group.is_full or self._is_colored
        self._is_available = system.battle.is_arcana_available and is_fulfill


class Sorcery(__Changeable):
    u"""ソーサリーカード。
    """
    _COLORS = 5, 9

    def set_state(self, system):
        u"""状態設定。
        """
        self._available_state = (
            system.resource.get_available_state(self._arcanum))
        self._is_available = system.battle.is_arcana_available
        self._is_colored = (
            system.battle.catalyst and
            self._arcanum.adapt(system.battle.catalyst))
