#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""mode.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ゲームモードモジュール。
"""
import pygame as _pygame
import sprites.general as _general
import utils.const as _const
import utils.screen as _screen


def init():
    u"""モジュール初期化。
    スプライトグループの設定など。
    """
    import armament.units as __units
    import sprites.decorator as __decorator
    import sprites.effects as __effects
    import sprites.indicator as __indicator
    import sprites.shadow as __shadow
    import sprites.string as __string
    import sprites.window as __window
    import system.battle as __battle
    global _clock, _classes, _group, _arcanum_group, _effect_group
    _clock = _pygame.time.Clock()
    _classes = (
        __shadow.Shadow,
        __units.Unit,
        __indicator.Gauge,
        __window.Window,
        __decorator.Decorator,
        _general.General,
        __indicator.Star,
        __indicator.Indicator,
        __battle.Arcanum,
        __string.String,
        __effects.Effect)
    _group = _pygame.sprite.Group()
    for Sprite in _classes:
        Sprite.group = _group
        Sprite.draw_group = _pygame.sprite.RenderUpdates()
    __units.Unit.draw_group = __indicator.Gauge.draw_group = (
        _pygame.sprite.LayeredUpdates())
    _arcanum_group = __battle.Arcanum.group = _pygame.sprite.Group()
    __battle.Arcanum.draw_group = _pygame.sprite.LayeredUpdates()
    _effect_group = __effects.Effect.group = _pygame.sprite.Group()


class Mode(object):
    u"""ゲームモード。
    """
    __slots__ = "_background", "_fade", "__frame", "_result"

    def __init__(self):
        u"""コンストラクタ。
        """
        class __Fade(_pygame.sprite.DirtySprite):
            u"""フェード用画像。
            """
            __FADE_SPEED = 4/_const.FRAME_DELAY << 4

            def __init__(self):
                u"""コンストラクタ。
                """
                self.__is_fade = False
                self.image = _pygame.Surface(
                    _screen.Screen.get_base().get_size())
                self.image.set_alpha(0xFF)
                self.rect = self.image.get_rect()
                self.is_white = False
                self.update()

            def update(self):
                u"""画像更新。
                """
                self.image.set_alpha(self.image.get_alpha()+(
                    self.__FADE_SPEED if self.__is_fade else
                    -self.__FADE_SPEED))

            def start(self):
                u"""フェード開始。
                """
                self.__is_fade = True

            @property
            def is_white(self):
                u"""フェード色取得。
                """
                return self.__is_white

            @is_white.setter
            def is_white(self, value):
                u"""フェード色設定。
                """
                self.__is_white = bool(value)
                if self.__is_white:
                    self.image.fill(_pygame.Color(_const.WHITE))
                else:
                    self.image.fill(_pygame.Color("0x000000"))

            @property
            def is_fading(self):
                u"""フェードしている場合に真。
                """
                return 0x00 < self.image.get_alpha() < 0xFF
        self.__frame = 0
        self._result = 0
        self._fade = __Fade()

    def _expansion(self):
        u"""メインサーフェスにベースサーフェスを拡大して描画。
        """
        main = _screen.Screen.get_main()
        main.blit(_pygame.transform.scale(
            _screen.Screen.get_base(), main.get_size()), (0, 0))

    def _update(self):
        u"""画面更新。
        """
        import utils.counter as __counter
        import utils.image as __image
        __counter.forward()
        _group.update()
        _arcanum_group.update()
        _effect_group.update()
        __image.BackGround.update()
        __image.BackGround.transcribe(_screen.Screen.get_base())
        for sprite in _classes:
            if hasattr(sprite, "draw_group"):
                sprite.draw_group.draw(_screen.Screen.get_base())
        self._fade.update()
        _screen.Screen.get_base().blit(
            self._fade.image, self._fade.rect.topleft)
        self._expansion()
        _pygame.display.flip()

    def _switch(self, status):
        u"""モード切り替え。
        """
        self._result = status
        if self._result:
            self._fade.start()

    def loop(self):
        u"""ゲームループ。
        '約'一秒で時間を更新。
        """
        import inventory as __inventory
        import material.sound as __sound
        _clock.tick(_const.FRAME_RATE)
        self.__frame = self.__frame+1 & 0b111111
        if self.__frame == 0:
            __inventory.Time.forward()
        events = _pygame.event.get()
        __sound.BGM.loop(events)
        return events

    def terminate(self):
        u"""終了処理。
        """
        import utils.memoize as __memoize
        for Sprite in _classes:
            for sprite in Sprite.group.sprites():
                sprite.kill()
        __memoize.clear()

    @property
    def _is_loopable(self):
        u"""ループ可能時に真。
        """
        return not self._result or self._fade.is_fading
