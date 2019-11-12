#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""content.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

UIコンテンツモジュール。
"""
import material.sound as _sound
import utils.const as _const


class Content(object):
    u"""UIコンテンツ。
    """
    __slots__ = "_cmds",
    _PLAYER_SELECT_TEXT = u"使用・削除キーでプレイヤー変更"

    def __init__(self):
        u"""コンストラクタ。
        """
        self._cmds = ""

    def left(self):
        u"""左方向キー入力。
        """
        return _const.IGNORE_STATUS

    def right(self):
        u"""右方向キー入力。
        """
        return _const.IGNORE_STATUS

    def up(self):
        u"""上方向キー入力。
        """
        return _const.IGNORE_STATUS

    def down(self):
        u"""下方向キー入力。
        """
        return _const.IGNORE_STATUS

    def decision(self):
        u"""決定キー入力。
        """
        return _const.IGNORE_STATUS

    def cancel(self):
        u"""取り消しキー入力。
        """
        return _const.IGNORE_STATUS

    def hold(self):
        u"""ホールドキー処理。
        """
        return _const.IGNORE_STATUS

    def remove(self):
        u"""リムーブキー処理。
        """
        return _const.IGNORE_STATUS

    def delete(self):
        u"""削除キー処理。
        """
        return _const.IGNORE_STATUS

    def use(self):
        u"""使用キー処理。
        """
        return _const.IGNORE_STATUS

    def command_input(self, cmd):
        u"""コマンド入力。
        """
        self._cmds += cmd

    def command_run(self):
        u"""コマンドの実行。
        """
        if self._cmds:
            cmd = self._cmds[0]
            self._cmds = self._cmds[1:]
            if cmd == _const.LEFT_COMMAND:
                return self.left()
            elif cmd == _const.RIGHT_COMMAND:
                return self.right()
            elif cmd == _const.UP_COMMAND:
                return self.up()
            elif cmd == _const.DOWN_COMMAND:
                return self.down()
            elif cmd == _const.DECISION_COMMAND:
                return self.decision()
            elif cmd == _const.CANCEL_COMMAND:
                return self.cancel()
            elif cmd == _const.HOLD_COMMAND:
                return self.hold()
            elif cmd == _const.REMOVE_COMMAND:
                return self.remove()
            elif cmd == _const.DELETE_COMMAND:
                return self.delete()
            elif cmd == _const.USE_COMMAND:
                return self.use()
            elif cmd == _const.VOLUMEUP_COMMAND:
                _sound.BGM.volume_up()
                return _const.IGNORE_STATUS
            elif cmd == _const.VOLUMEDOWN_COMMAND:
                _sound.BGM.volume_down()
                return _const.IGNORE_STATUS
            elif cmd == _const.MUTE_COMMAND:
                _sound.BGM.mute()
                return _const.IGNORE_STATUS

    @property
    def active_window(self):
        u"""アクティブウィンドウ取得。
        """
        return None


class Control(Content):
    u"""操作画面。
    """
    __slots__ = "_controls", "_cursor"
    WINDOW_ROW = 8

    def __init__(self):
        u"""コンストラクタ。
        """
        super(Control, self).__init__()
        self._cursor = 0

    def _update_info(self):
        u"""情報を更新。
        """
    def eliminate(self):
        u"""削除処理。
        """
        for control in self._controls:
            control.kill()

    def left(self):
        u"""カーソルを左に。
        """
        window = self.active_window
        if window and not window.is_label:
            window.cursor -= 1
            self._update_info()
        return 0

    def right(self):
        u"""カーソルを右に。
        """
        window = self.active_window
        if window and not window.is_label:
            window.cursor += 1
            self._update_info()
        return 0

    def up(self):
        u"""カーソルを上に。
        """
        window = self.active_window
        if window:
            if window.is_label:
                window.cursor -= 1
            else:
                window.cursor -= self.WINDOW_ROW
        else:
            self.cursor -= 1
        self._update_info()
        return 0

    def down(self):
        u"""カーソルを下に。
        """
        window = self.active_window
        if window:
            if window.is_label:
                window.cursor += 1
            else:
                window.cursor += self.WINDOW_ROW
        else:
            self.cursor += 1
        self._update_info()
        return 0

    @property
    def cursor(self):
        u"""カーソル位置取得。
        """
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        u"""カーソル位置設定。
        """
        limit = len(self._controls)-1
        old = self._cursor
        pos = int(value)
        self._cursor = 0 if pos < 0 else limit if limit < pos else pos
        if self._cursor != old:
            _sound.SE.play("cursor_1")
        for control in self._controls:
            control.is_light = False
        self._controls[self._cursor].is_light = True

    @property
    def active_window(self):
        u"""アクティブウィンドウ取得。
        """
        for window in self._controls:
            if window.is_active:
                return window
        return None
