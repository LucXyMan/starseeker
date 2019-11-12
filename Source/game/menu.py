#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-
u"""menu.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

メニューモードモジュール。
"""
import mode as __mode
import ui.entries as _entries
import ui.menu as _menu


class _Menu(__mode.Mode):
    u"""メニューモード。
    """
    __slots__ = "_controler", "_info", "_operate"

    def __init__(self):
        u"""コンストラクタ。
        """
        import input as __input
        import ui.info as __info
        super(_Menu, self).__init__()
        self._controler = __input.Menu(0)
        self._info = __info.Info()
        self._info.has_info = True

    def __command_io(self):
        u"""コマンド入出力。
        """
        if not self._fade.is_fading:
            self._controler.input()
            self._operate.command_input(self._controler.output())
            self._switch(self._operate.command_run())

    def loop(self):
        u"""ループ処理。
        """
        while self._is_loopable:
            super(_Menu, self).loop()
            self.__command_io()
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
        import ui as __ui
        super(ModeSelect, self).__init__()
        self._info.has_time = True
        self._info.has_sp = True
        self._info.has_speed = True
        self._operate = __ui.ModeSelect()


class DuelEntry(_Menu):
    u"""デュエル選択モード。
    """
    __slots__ = ()

    def __init__(self):
        u"""コンストラクタ。
        """
        super(DuelEntry, self).__init__()
        self._operate = _entries.Duel()
        self._info.has_time = True
        self._info.has_level = True
        self._info.has_player = True


class VersusEntry(_Menu):
    u"""VS選択モード。
    """
    __slots__ = ()

    def __init__(self):
        u"""コンストラクタ。
        """
        super(VersusEntry, self).__init__()
        self._operate = _entries.Versus()
        self._info.has_time = True
        self._info.has_size = True
        self._info.has_player = True


class Customize(_Menu):
    u"""カスタムモード。
    """
    __slots__ = ()

    def __init__(self):
        u"""コンストラクタ。
        """
        super(Customize, self).__init__()
        self._operate = _menu.Customize()
        self._info.has_time = True
        self._info.has_sp = True
        self._info.has_player = True

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
        self._operate = _menu.Result()
        self._info.has_time = True
        self._info.has_sp = True
        self._info.has_next_level = True
