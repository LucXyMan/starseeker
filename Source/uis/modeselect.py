#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""modeselect.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

モードセレクトモジュール。
"""
import input as _input
import inventories as _inventories
import material.sound as _sound
import sprites as _sprites
import ui as __ui
import utils.const as _const
import utils.layouter as _layouter


class ModeSelect(__ui.UI):
    u"""モードセレクト。
    """
    __slots__ = "_selector",
    __MODES = "Duel#Endless#Versus#Customize#Exit"
    __cursor = 0

    def __init__(self):
        u"""コンストラクタ。
        """
        import material.misc as _misc
        import sprites.huds as __huds
        import utils.image as __image
        import utils.screen as __screen

        class _Title(__huds.HUD):
            u"""タイトルスプライト。
            """
            def __init__(self, groups=None):
                u"""コンストラクタ。
                """
                super(_Title, self).__init__(groups)
                self.image = _misc.get("title")
                self.rect = self.image.get_rect()
                _layouter.Menu.set_title(self)

        class _Selector(object):
            u"""セレクタ。
            文字列選択。
            """
            __slots__ = "__cursor", "__strings"

            def __init__(self, string, cursor=0):
                u"""コンストラクタ。
                """
                class _Flashable(_sprites.String):
                    u"""点滅文字列。
                    """
                    __COLORS = (
                        "0x202040#0x202040#0x202040",
                        "0x404040#0x404040#0x202040",
                        "0x404040#0x808040#0x404040",
                        "0x808040#0xFFFF40#0x808040")

                    def __set_char_color(self):
                        u"""文字色を取得。
                        """
                        self.__COLORS = reduce(lambda x, y: x+y, (
                            (color,)*_const.FRAME_DELAY for
                            color in self.__COLORS+self.__COLORS[::-1]))

                    def __init__(self, pos, string, size, groups=None):
                        u"""コンストラクタ。
                        """
                        self.__frame = 0
                        self.__set_char_color()
                        self.__is_flash = False
                        super(_Flashable, self).__init__(
                            pos, string, size, self.__COLORS[self.__frame],
                            groups=groups)

                    def update(self):
                        u"""スプライト更新。
                        """
                        if self.__is_flash:
                            frame = self.__frame+1
                            self.__frame = frame if frame < (
                                len(self.__COLORS)) else 0
                        else:
                            self.__frame = 0
                        self.color = self.__COLORS[self.__frame]

                    @property
                    def is_flash(self):
                        u"""点滅状態を取得。
                        """
                        return self.__is_flash

                    @is_flash.setter
                    def is_flash(self, value):
                        u"""点滅状態を設定。
                        """
                        self.__is_flash = bool(value)
                super(_Selector, self).__init__()
                self.__strings = [
                    _Flashable((0, 0), mode, 12) for mode in string.split("#")]
                _layouter.Menu.set_selector(self.__strings)
                self.cursor = cursor

            def eliminate(self):
                u"""全ての表示物を除去。
                """
                for string in self.__strings:
                    string.kill()

            @property
            def cursor(self):
                u"""カーソル位置の取得。
                """
                return self.__cursor

            @cursor.setter
            def cursor(self, value):
                u"""カーソル位置の設定。
                """
                limit = len(self.__strings)-1
                pos = int(value)
                strings = self.__strings
                self.__cursor = 0 if limit < pos else limit if pos < 0 else pos
                for string in strings:
                    string.is_flash = False
                strings[self.__cursor].is_flash = True
        super(ModeSelect, self).__init__()
        _sound.BGM.play("menu")
        _Title()
        self._selector = _Selector(self.__MODES, self.__cursor)
        __image.BackGround.set_image(_misc.get("starry_sky"))
        __image.BackGround.transcribe(__screen.Screen.get_base())
        self.__update_notice()

    def __update_notice(self):
        u"""情報更新。
        """
        def __get_endless():
            u"""エンドレス説明文取得。
            """
            base = u"{1}:ランダムに連戦"
            endless = _inventories.Endless.get_progress()
            reached = _inventories.Endless.get_reached()
            max_level = reached if reached < _const.ENDLESS_LIMIT else u"??"
            max_ = u"/最大★:{}".format(max_level) if reached else u""
            if endless:
                level = endless if endless < _const.ENDLESS_LIMIT else u"??"
                streaks = u"/現在★:{}".format(level) if endless else u""
                return base+streaks+u"#"+base+max_+u"##"
            elif reached:
                return base+max_+u"##"
            return base+u"##"
        joystick = (
            u"##" if _input.is_second_playable() else
            u"/ジョイパッドが2つ必要です##")
        description = (
            u"{0}:相手を選んで対戦##"+__get_endless() +
            u"{2}:対人戦"+joystick+u"{3}:装備設定##" +
            u"{4}:セーブして終了").format(*self.__MODES.split("#")).split("##")
        _sprites.Notice.notify((
            u"{}#使用・削除キーでスピード変更#" +
            _const.COPYRIGHT+u"#Version "+_const.VERSION
        ).format(description[self._selector.cursor]))

    def eliminate(self):
        u"""全ての表示物を除去。
        """
        self._selector.eliminate()

    def delete(self):
        u"""削除キー入力。
        上下左右キーの速度調整。
        """
        value = _inventories.General.get_speed()-1
        _inventories.General.set_speed(0 if value < 0 else value)
        return _const.IGNORE_STATUS

    def use(self):
        u"""使用キー入力。
        上下左右キーの速度調整。
        """
        value = _inventories.General.get_speed()+1
        limit = len(_const.SPEED_TEXTS)-1
        _inventories.General.set_speed(value if value < limit else limit)
        return _const.IGNORE_STATUS

    def up(self):
        u"""上方向キー入力。
        """
        old_cursor = self._selector.cursor
        self._selector.cursor -= 1
        if self._selector.cursor != old_cursor:
            _sound.SE.play("cursor_1")
        self.__update_notice()
        return 0

    def down(self):
        u"""下方向キー入力。
        """
        old_cursor = self._selector.cursor
        self._selector.cursor += 1
        if self._selector.cursor != old_cursor:
            _sound.SE.play("cursor_1")
        self.__update_notice()
        return 0

    def decision(self):
        u"""決定キー入力。
        """
        cursor = self.__class__.__cursor = self._selector.cursor
        if cursor == 0:
            _sound.SE.play("decision")
            return _const.DUEL_SELECT_STATUS
        elif cursor == 1:
            _sound.SE.play("decision")
            return _const.ENDLESS_STATUS
        elif cursor == 2:
            if _input.is_second_playable():
                _sound.SE.play("decision")
                return _const.VERSUS_SELECT_STATUS
            else:
                _sound.SE.play("error")
                return _const.IGNORE_STATUS
        elif cursor == 3:
            _sound.SE.play("decision")
            return _const.CUSTOM_STATUS
        elif cursor == 4:
            _inventories.save()
            return _const.EXIT_STATUS
        return _const.IGNORE_STATUS
