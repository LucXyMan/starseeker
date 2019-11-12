#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""main.py

Copyright(c)2019 Yukio Kuro
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
        import inventory as __inventory
        import puzzle as __puzzle
        import menu as __menu
        if __inventory.load():
            status = __const.MODE_SELECT_STATUS
            while True:
                if status == __const.MODE_SELECT_STATUS:
                    mode = __menu.ModeSelect()
                    status = mode.loop()
                elif status == __const.DUEL_SELECT_STATUS:
                    mode = __menu.DuelEntry()
                    status = mode.loop()
                elif status == __const.DUEL_STATUS:
                    mode = __puzzle.Duel()
                    status = mode.loop()
                elif status == __const.ENDLESS_STATUS:
                    mode = __puzzle.Endless()
                    status = mode.loop()
                elif status == __const.VERSUS_SELECT_STATUS:
                    mode = __menu.VersusEntry()
                    status = mode.loop()
                elif status == __const.VERSUS_STATUS:
                    mode = __puzzle.Versus()
                    status = mode.loop()
                elif status == __const.CUSTOM_STATUS:
                    mode = __menu.Custom()
                    status = mode.loop()
                elif status == __const.RESULT_STATUS:
                    mode = __menu.Result()
                    status = mode.loop()
                else:
                    return None
                mode.terminate()
        else:
            print "Savedata is incorrect."
