#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""puzzle.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

パズルモードモジュール。
"""
import pygame as _pygame
import mode as __mode
import utils.const as _const
import system as _system


class _Puzzle(__mode.Mode):
    u"""パズルモード。
    """
    __slots__ = "__bgm_loop", "_is_error", "_manager"

    def __init__(self):
        u"""コンストラクタ。
        """
        super(_Puzzle, self).__init__()
        _pygame.display.flip()
        self._is_error = self._manager.is_error

    def loop(self):
        u"""ループ処理。
        """
        import utils.screen as __screen
        import sprites.string as __string

        class _Paused(__string.String):
            u"""一時停止文字列。
            """
            __COLOR = _const.MAGENTA+"#"+_const.YELLOW+"#"+_const.DARK_MAGENTA

            def __init__(self):
                u"""コンストラクタ。
                """
                import utils.layouter as __layouter
                super(_Paused, self).__init__(
                    (0, 0), "Paused", _const.MODE_CHAR_SIZE, self.__COLOR,
                    True, ())
                __layouter.Game.set_paused(self)
        if self._is_error:
            return _const.MODE_SELECT_STATUS
        paused = _Paused()
        is_paused = False
        while self._is_loopable:
            super(_Puzzle, self).loop()
            if not self._fade.is_fading:
                self._manager.manage()
                if self._manager.is_done:
                    self._switch(self._manager.is_win)
            if self._manager.is_paused:
                if not is_paused:
                    __screen.Screen.get_base().blit(paused.image, paused.rect)
                    is_paused = True
                self._fade.update()
                __screen.Screen.get_base().blit(
                    self._fade.image, self._fade.rect.topleft)
                self._expansion()
                _pygame.display.flip()
            else:
                self._update()
                is_paused = False
        return self._result


class Duel(_Puzzle):
    u"""デュエルモード。
    """
    __slots__ = ()

    def __init__(self):
        u"""コンストラクタ。
        """
        self._manager = _system.Duel()
        super(Duel, self).__init__()

    def _switch(self, is_win):
        u"""モード切り替え処理。
        報奨SP・アイテム取得、レベルフラグオン。
        """
        import armament.level as __level
        import inventory as __inventory
        if is_win:
            level = __level.get_duel()
            if not __inventory.Level.has(level.number):
                for reward in level.rewards:
                    __inventory.Cards.set(
                        reward, __inventory.Cards.get(reward)+1)
                number, player_level = level.player
                __inventory.SP.add((player_level+1)*(
                    200 if number == _const.PLAYER_NUMBER else 100))
                __inventory.Level.on(level.number)
        super(Duel, self)._switch(_const.MODE_SELECT_STATUS)


class Versus(_Puzzle):
    u"""ヴァーサスモード。
    """
    __slots__ = ()

    def __init__(self):
        u"""コンストラクタ。
        """
        self._manager = _system.Versus()
        super(Versus, self).__init__()

    def _switch(self, _):
        u"""モード切り替え処理。
        """
        super(Versus, self)._switch(_const.MODE_SELECT_STATUS)


class Endless(_Puzzle):
    u"""エンドレスモード。
    """
    __slots__ = ()

    def __init__(self):
        u"""コンストラクタ。
        """
        self._manager = _system.Endless()
        super(Endless, self).__init__()

    def _switch(self, is_win):
        u"""モード切り替え処理。
        """
        super(Endless, self)._switch(
            _const.RESULT_STATUS if is_win else
            _const.MODE_SELECT_STATUS)
