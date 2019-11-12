#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""decorator.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

デコレータモジュール。
ウィンドウなどの枠を設定する。
"""
import pygame as _pygame


class Decorator(_pygame.sprite.DirtySprite):
    u"""デコレータ。
    """
    _ALPHA = 0x80
    _DECORATOR_LINE_SIZE = 2
    _BASE_COLORS = "0xD0D0D0", "0x606060", "0x202020"
    _LIGHT_COLORS = "0xD0F0D0", "0xB0D0B0", "0x406040"

    def __init__(self, caster, groups=None):
        u"""コンストラクタ。
        """
        super(Decorator, self).__init__(
            (Decorator.group, Decorator.draw_group) if groups is None else
            tuple(groups))
        self._caster = caster
        self._base_image = self._get_image(False)
        self._light_image = self._get_image(True)
        self.image = self._base_image
        self.rect = self.image.get_rect()
        self.update()

    def _get_horizon(self, is_light):
        u"""水平ライン画像取得。
        """
        width = self._caster.rect.width
        height = self._DECORATOR_LINE_SIZE
        line_width = height >> 1
        surf = _pygame.Surface((width, height))
        light, _, dark = (
            self._BASE_COLORS if is_light == 0 else self._LIGHT_COLORS)
        _pygame.draw.line(
            surf, _pygame.Color(light), (0, 0), (width, 0), line_width)
        _pygame.draw.line(
            surf, _pygame.Color(dark), (0, line_width), (width, line_width),
            line_width)
        return surf

    def _get_vertical(self, is_light):
        u"""垂直ライン画像取得。
        """
        width = self._DECORATOR_LINE_SIZE
        height = self._caster.rect.height
        line_width = width >> 1
        surf = _pygame.Surface((width, height))
        light, _, dark = (
            self._BASE_COLORS if is_light == 0 else self._LIGHT_COLORS)
        _pygame.draw.line(
            surf, _pygame.Color(light), (0, 0), (0, height), line_width)
        _pygame.draw.line(
            surf, _pygame.Color(dark), (line_width, 0), (line_width, height),
            line_width)
        return surf


def set_decorator(caster, groups=None):
    u"""デコレータ設定。
    """
    class __Top(Decorator):
        u"""上部デコレータ。
        """
        def _get_image(self, is_light):
            u"""画像取得。
            """
            return self._get_horizon(is_light)

        def update(self):
            u"""画像更新。
            通常画像と発光画像の切り替え。
            """
            if self._caster.alive():
                self.image = (
                    self._light_image if self._caster.is_light else
                    self._base_image)
                top, _, _, _ = self._caster.decorate
                self.image.set_alpha(self._ALPHA if not top else None)
                self.rect.midbottom = self._caster.rect.midtop
            else:
                self.kill()

    class __Left(Decorator):
        u"""左部デコレータ。
        """
        def _get_image(self, is_light):
            u"""画像取得。
            """
            return self._get_vertical(is_light)

        def update(self):
            u"""画像更新。
            通常画像と発光画像の切り替え。
            """
            if self._caster.alive():
                self.image = (
                    self._light_image if self._caster.is_light else
                    self._base_image)
                _, _, _, left = self._caster.decorate
                self.image.set_alpha(self._ALPHA if not left else None)
                self.rect.midright = self._caster.rect.midleft
            else:
                self.kill()

    class __Right(Decorator):
        u"""右部デコレータ。
        """
        def _get_image(self, is_light):
            u"""右部ライン画像取得。
            """
            return self._get_vertical(is_light)

        def update(self):
            u"""画像更新。
            通常画像と発光画像の切り替え。
            """
            if self._caster.alive():
                self.image = (
                    self._light_image if self._caster.is_light else
                    self._base_image)
                _, right, _, _ = self._caster.decorate
                self.image.set_alpha(self._ALPHA if not right else None)
                self.rect.midleft = self._caster.rect.midright
            else:
                self.kill()

    class __Bottom(Decorator):
        u"""下部デコレータ。
        """
        def _get_image(self, is_light):
            u"""下部ライン画像の取得。
            """
            return self._get_horizon(is_light)

        def update(self):
            u"""画像の更新。
            通常画像と発光画像の切り替え。
            """
            if self._caster.alive():
                self.image = (
                    self._light_image if self._caster.is_light else
                    self._base_image)
                _, _, bottom, _ = self._caster.decorate
                self.image.set_alpha(self._ALPHA if not bottom else None)
                self.rect.midtop = self._caster.rect.midbottom
            else:
                self.kill()

    class __Corner(Decorator):
        u"""角デコレータ。
        """
        def _get_image(self, is_light):
            u"""角部画像を取得。
            """
            surf = _pygame.Surface(
                (self._DECORATOR_LINE_SIZE, self._DECORATOR_LINE_SIZE))
            light, mid, dark = (
                self._BASE_COLORS if is_light == 0 else self._LIGHT_COLORS)
            surf.fill(_pygame.Color(mid))
            _pygame.draw.rect(
                surf, _pygame.Color(light), _pygame.Rect(0, 0, 0, 0))
            _pygame.draw.rect(
                surf, _pygame.Color(dark), _pygame.Rect(2, 2, 0, 0))
            return surf

    class __TopLeft(__Corner):
        u"""左上部デコレータ。
        """
        def update(self):
            u"""画像の更新。
            通常画像と発光画像の切り替え。
            """
            if self._caster.alive():
                self.image = (
                    self._light_image if self._caster.is_light else
                    self._base_image)
                top, _, _, left = self._caster.decorate
                self.image.set_alpha(
                    self._ALPHA if not top and not left else None)
                self.rect.bottomright = self._caster.rect.topleft
            else:
                self.kill()

    class __TopRight(__Corner):
        u"""右上部デコレータ。
        """
        def update(self):
            u"""画像の更新。
            通常画像と発光画像の切り替え。
            """
            if self._caster.alive():
                self.image = (
                    self._light_image if self._caster.is_light else
                    self._base_image)
                top, right, _, _ = self._caster.decorate
                self.image.set_alpha(
                    self._ALPHA if not top and not right else None)
                self.rect.bottomleft = self._caster.rect.topright
            else:
                self.kill()

    class __BottomLeft(__Corner):
        u"""左下部デコレータ。
        """
        def update(self):
            u"""画像の更新。
            通常画像と発光画像の切り替え。
            """
            if self._caster.alive():
                self.image = (
                    self._light_image if self._caster.is_light else
                    self._base_image)
                _, _, bottom, left = self._caster.decorate
                self.image.set_alpha(
                    self._ALPHA if not bottom and not left else None)
                self.rect.topright = self._caster.rect.bottomleft
            else:
                self.kill()

    class __BottomRight(__Corner):
        u"""右下部デコレータ。
        """
        def update(self):
            u"""画像の更新。
            通常画像と発光画像の切り替え。
            """
            if self._caster.alive():
                self.image = (
                    self._light_image if self._caster.is_light else
                    self._base_image)
                _, right, bottom, _ = self._caster.decorate
                self.image.set_alpha(
                    self._ALPHA if not right and not bottom else None)
                self.rect.topleft = self._caster.rect.bottomright
            else:
                self.kill()
    for Cls in (
        __Top, __TopRight, __Right, __BottomRight,
        __Bottom, __BottomLeft, __Left, __TopLeft
    ):
        Cls(caster, groups)
