#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""main.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ゲームモジュール。
"""


class Game(object):
    u"""ゲーム開始。
    """
    __slots__ = ()

    def loop(self):
        u"""ループ処理。
        """
        import utils.const as __const
        import inventories as __inventories
        import puzzle as __puzzle
        import menu as __menu
        if __inventories.load():
            status = __const.MODE_SELECT_STATUS
            while True:
                if status == __const.MODE_SELECT_STATUS:
                    mode = __menu.ModeSelect()
                elif status == __const.DUEL_SELECT_STATUS:
                    mode = __menu.DuelEntry()
                elif status == __const.DUEL_STATUS:
                    mode = __puzzle.Duel()
                elif status == __const.ENDLESS_STATUS:
                    mode = __puzzle.Endless()
                elif status == __const.VERSUS_SELECT_STATUS:
                    mode = __menu.VersusEntry()
                elif status == __const.VERSUS_STATUS:
                    mode = __puzzle.Versus()
                elif status == __const.CUSTOM_STATUS:
                    mode = __menu.Customize()
                elif status == __const.RESULT_STATUS:
                    mode = __menu.Result()
                else:
                    return None
                status = mode.loop()
                mode.terminate()
