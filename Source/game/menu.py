#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-
u"""menu.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

メニューモードモジュール。
"""
import mode as __mode
import uis.entries as _entries
import uis.menu as _menu


class _Menu(__mode.Mode):
    u"""メニューモード。
    """
    __slots__ = "_controler", "_notice", "_operation"

    def __init__(self):
        u"""コンストラクタ。
        """
        import input as __input
        import uis.notice as __notice
        super(_Menu, self).__init__()
        self._controler = __input.Menu(0)
        self._notice = __notice.Notice()
        self._notice.has_notice = True

    def loop(self):
        u"""ループ処理。
        """
        def __io_command():
            u"""コマンド入出力。
            """
            if not self._fade.is_fading:
                self._controler.input()
                self._operation.input_command(self._controler.output())
                self._switch(self._operation.run_command())
        while self._is_loopable:
            super(_Menu, self).loop()
            __io_command()
            self._update()
        return self._result


class ModeSelect(_Menu):
    u"""モード選択。
    ゲームの初期画面。
    """
    __slots__ = ()

    def __init__(self):
        u"""コンストラクタ。
        """
        import uis as __uis
        super(ModeSelect, self).__init__()
        self._notice.has_time = True
        self._notice.has_sp = True
        self._notice.has_speed = True
        self._operation = __uis.ModeSelect()


class DuelEntry(_Menu):
    u"""デュエル選択モード。
    """
    __slots__ = ()

    def __init__(self):
        u"""コンストラクタ。
        """
        super(DuelEntry, self).__init__()
        self._operation = _entries.Duel()
        self._notice.has_time = True
        self._notice.has_level = True
        self._notice.has_player = True


class VersusEntry(_Menu):
    u"""VS選択モード。
    """
    __slots__ = ()

    def __init__(self):
        u"""コンストラクタ。
        """
        super(VersusEntry, self).__init__()
        self._operation = _entries.Versus()
        self._notice.has_time = True
        self._notice.has_size = True
        self._notice.has_player = True


class Customize(_Menu):
    u"""カスタムモード。
    """
    __slots__ = ()

    def __init__(self):
        u"""コンストラクタ。
        """
        super(Customize, self).__init__()
        self._operation = _menu.Customize()
        self._notice.has_time = True
        self._notice.has_sp = True
        self._notice.has_player = True

    def _switch(self, status):
        u"""モード切り替え。
        """
        import utils.const as __const
        if status == __const.EXIT_STATUS:
            super(Customize, self)._switch(__const.MODE_SELECT_STATUS)


class Result(_Menu):
    u"""リザルトモード。
    """
    __slots__ = ()

    def __init__(self):
        u"""コンストラクタ。
        """
        super(Result, self).__init__()
        self._operation = _menu.Result()
        self._notice.has_time = True
        self._notice.has_sp = True
        self._notice.has_next_level = True
