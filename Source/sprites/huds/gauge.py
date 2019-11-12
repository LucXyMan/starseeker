#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""gauge.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ゲージモジュール。
"""
import pygame as _pygame
import hud as __hud
import material.string as _string
import utils.const as _const
import utils.image as _image
import utils.layouter as _layouter


class Gauge(__hud.HUD):
    u"""ゲージスプライト。
    """
    __ALPHA = None
    __GAUGE_SIZE = 42, 4
    _BACK_COLORS = _const.GRAY, _const.BLACK
    _LAYER = 0

    def __init__(self, caster, groups=None):
        u"""コンストラクタ。
        """
        super(Gauge, self).__init__(groups)
        self._caster = caster
        self._layer = -1
        self._old = -1
        self._scale = self._dest = 0
        self._text = ""
        self._color = _string.CharColor()
        self._images = self._get_images()
        self.update()

    def _get_gauge_images(self, front, back, scale):
        u"""ゲージ画像作成。
        """
        import utils.memoize as __memoize

        @__memoize.memoize()
        def __get_gauge_image(length, front, back, scale):
            u"""ゲージフレーム画像作成。
            """
            def __draw_partition(surf, scale):
                u"""ゲージの区切り線を描く。
                """
                w, h, = self.__GAUGE_SIZE
                if scale != 1:
                    for i in range(1, scale):
                        _pygame.draw.rect(
                            surf, (0, 0, 0), _pygame.Rect(w/scale*i, 0, 1, h))
            w, h, = self.__GAUGE_SIZE
            surf = _pygame.Surface((w, h)).convert()
            surf.fill((0, 0, 0))
            if back:
                _image.draw_gradient_h(
                    surf, back, _pygame.Rect(1, 1, w-2, h-2))
            else:
                _pygame.draw.rect(
                    surf, _pygame.Color(_const.BLACK),
                    _pygame.Rect(1, 1, w-2, h-2))
            if length != 0:
                _image.draw_gradient_h(
                    surf, front, _pygame.Rect(1, 1, length, h-2))
            __draw_partition(surf, scale)
            return surf
        w, _, = self.__GAUGE_SIZE
        return tuple(
            __get_gauge_image(x, front, back, scale) for x in range(0, w-1))

    def _rise_and_fall(self):
        u"""目盛り増減。
        """
        if self._scale < self._dest:
            self._scale += 1
        elif self._scale > self._dest:
            self._scale -= 1

    def _get_images(self):
        u"""ゲージ画像取得。
        """
        def __get_multi_gauge_images(colors, scale):
            u"""複数色の組み合わせゲージ作成。
            """
            return reduce(lambda x, y: x+y, (
                self._get_gauge_images(color[0], color[1], scale) for
                color in colors))
        front = tuple(_pygame.Color(c) for c in self._FRONT_COLORS)
        return __get_multi_gauge_images(((
            front[0:2], tuple(_pygame.Color(c) for c in self._BACK_COLORS)),) +
            tuple((
                front[(i << 1):(i << 1)+2], front[(i-1) << 1:i << 1]) for
                i in range(1, 4)), self._SCALE)

    def _set_string(self):
        u"""文字列設定。
        """
        gauge = _pygame.Surface(self.image.get_size())
        gauge.blit(self.image, (0, 0))
        gw, gh = gauge.get_size()
        char_size = 8
        surf = _pygame.Surface((gw, gh+char_size))
        surf.fill((255, 255, 255))
        surf.set_colorkey((255, 255, 255))
        sw, _ = surf.get_size()
        surf.blit(gauge, ((sw-gw) >> 1, char_size))
        char = _string.get_string(self._text, char_size, self._color)
        cw, _ = char.get_size()
        surf.blit(char, ((sw-cw) >> 1, 0))
        surf.set_alpha(self.__ALPHA)
        self.image = surf

    def update(self):
        u"""スプライト更新。
        _casterがキルされた場合に自身をキルする。
        """
        def __set_layer():
            u"""レイヤー設定。
            """
            current_layer = self._caster.layer_of_sprite
            if self._layer != current_layer:
                self._layer = current_layer
                self.draw_group.change_layer(self, self._layer+self._LAYER)
        if self._caster.alive():
            __set_layer()
        else:
            self.kill()


class Life(Gauge):
    u"""ライフゲージ。
    """
    __FULL_GAUGE = 500
    __LIFE_DISPLAY_LIMIT = 9999
    _FRONT_COLORS = (
        _const.YELLOW, _const.RED, _const.YELLOW, _const.YELLOW,
        _const.YELLOW, _const.GREEN, _const.CYAN, _const.BLUE)
    _SCALE = 1
    _LAYER = 1

    def update(self):
        u"""ゲージ更新。
        """
        def __set_parameter():
            u"""目的の値を設定する。
            """
            life = self._caster.life
            if life != self._old:
                scale = int(
                    (self._caster.life/float(self.__FULL_GAUGE)) *
                    (len(self._images)-1))
                self._dest = (
                    scale if scale < len(self._images) else
                    len(self._images)-1)
                self._text = str(
                    life if life < self.__LIFE_DISPLAY_LIMIT else
                    self.__LIFE_DISPLAY_LIMIT)
                self._color = (
                    _string.CharColor(_const.RED+"##") if
                    self._caster.is_quarter else
                    _string.CharColor(_const.YELLOW+"##") if
                    self._caster.is_half else
                    _string.CharColor())
            self._old = self._caster.life
        super(Life, self).update()
        __set_parameter()
        self._rise_and_fall()
        if self._caster.is_dead:
            self.image = _image.get_clear(self.image)
        else:
            self.image = self._images[self._scale]
            self._set_string()
            self.rect = self.image.get_rect()
            _layouter.Game.set_gauge(self, self._caster)


class Charge(Gauge):
    u"""チャージゲージ。
    """
    _LAYER = 2

    def _get_images(self):
        u"""ゲージ画像取得。
        """
        return self._get_gauge_images(
            (_pygame.Color(_const.CYAN), _pygame.Color(_const.MAGENTA)),
            (_pygame.Color(_const.GRAY), _pygame.Color(_const.BLACK)), 1)

    def update(self):
        u"""ゲージ更新。
        """
        def __set_parameter():
            u"""目的の値を設定する。
            """
            if self._caster.power != self._old:
                limit = len(self._images)-1
                ratio = self._caster.power/float(self._caster.packet)
                scale = int(ratio*limit)
                self._dest = scale if scale < limit else limit
                self._text = str(int(ratio*100))+"%"
            self._old = self._caster.power
        super(Charge, self).update()
        __set_parameter()
        self._rise_and_fall()
        if self._caster.is_dead or self._caster.is_frozen:
            self.image = _image.get_clear(self.image)
        else:
            self.image = self._images[self._scale]
            self._set_string()
            self.rect = self.image.get_rect()
            _layouter.Game.set_charge_gauge(self, self._caster)


class Freeze(Gauge):
    u"""凍結ゲージ。
    """
    _LAYER = 2

    def __init__(self, caster, groups=None):
        u"""コンストラクタ。
        """
        super(Freeze, self).__init__(caster, groups)
        self._text = "Freeze"

    def _get_images(self):
        u"""ゲージ画像取得。
        """
        return self._get_gauge_images(
            (_pygame.Color(_const.YELLOW), _pygame.Color(_const.CYAN)),
            (_pygame.Color(_const.GRAY), _pygame.Color(_const.BLACK)), 1)

    def update(self):
        u"""ゲージ更新。
        """
        def __set_parameter():
            u"""目的の値を設定する。
            """
            if self._caster.frozen_time != self._old:
                scale = (
                    self._caster.frozen_time /
                    float(self._caster.packet << 2)*(len(self._images)-1))
                self._dest = int(
                    scale if scale < len(self._images) else
                    len(self._images)-1)
            self._old = self._caster.frozen_time
        super(Freeze, self).update()
        __set_parameter()
        self._rise_and_fall()
        self.image = self._images[self._scale]
        self._set_string()
        if self._caster.is_dead or not self._caster.is_frozen:
            self.image = _image.get_clear(self.image)
        self.rect = self.image.get_rect()
        _layouter.Game.set_charge_gauge(self, self._caster)


class Pressure(Gauge):
    u"""圧力ゲージ。
    """
    _FRONT_COLORS = (
        _const.YELLOW, _const.YELLOW, _const.YELLOW, _const.CYAN,
        _const.CYAN, _const.BLUE, _const.YELLOW, _const.MAGENTA)
    _SCALE = 4

    def __init__(self, caster, system, groups=None):
        u"""コンストラクタ。
        """
        self.__accumulate = system.accumulate
        super(Pressure, self).__init__(caster, groups)

    def update(self):
        u"""ゲージ更新。
        """
        def __set_parameter():
            u"""目的の値を設定する。
            """
            def __get_string_color():
                u"""ゲージ文字色取得。
                """
                adamant_lv = (_const.ADAMANT_PRESS_LEVEL+1)*_const.PRESS_POINT
                solid_lv = (_const.SOLID_PRESS_LEVEL+1)*_const.PRESS_POINT
                pressure = self.__accumulate.pressure
                return (
                    _string.CharColor(_const.RED+"##") if
                    adamant_lv < pressure else
                    _string.CharColor(_const.YELLOW+"##") if
                    solid_lv < pressure else _string.CharColor())
            if self.__accumulate.pressure != self._old:
                limit = len(self._images)-1
                value = int(
                    self.__accumulate.pressure/float(_const.PRESS_LIMIT)*limit)
                self._dest = value if value < limit else limit
                self._text = "{level}/{effects}".format(
                    level=self.__accumulate.level,
                    effects=self.__accumulate.effects)
                self._color = __get_string_color()
            self._old = self.__accumulate.pressure
        super(Pressure, self).update()
        __set_parameter()
        self._rise_and_fall()
        self.image = self._images[self._scale]
        self._set_string()
        self.rect = self.image.get_rect()
        _layouter.Game.set_gauge(self, self._caster)
