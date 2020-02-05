#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""notice.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

情報表示モジュール。
"""
import armament.levels as _levels
import inventories as _inventories
import sprites.string as _string
import utils.const as _const
import utils.layouter as _layouter


class _String(_string.String):
    u"""基本情報パラメータ文字列。
    """
    def __init__(self, pos, groups):
        u"""コンストラクタ。
        """
        super(_String, self).__init__(
            pos, "", _const.SYSTEM_CHAR_SIZE, groups=groups)


class _Speed(_String):
    u"""ピース・カーソル速度文字列。
    """
    def __init__(self, groups=None):
        u"""コンストラクタ。
        """
        super(_Speed, self).__init__((0, 0), groups)

    def update(self):
        u"""文字列更新。
        """
        self.string = u"Speed:{}".format(
            _const.SPEED_TEXTS[_inventories.General.get_speed()])
        _layouter.Menu.set_speed(self)


class _Player(_String):
    u"""現在プレイヤー文字列。
    """
    def __init__(self, groups=None):
        u"""コンストラクタ。
        """
        super(_Player, self).__init__((0, 0), groups=groups)

    def update(self):
        u"""文字列更新。
        """
        import armament.units as __units
        self.string = u"Player:{name}".format(
            name=__units.get_player(_inventories.General.get_player()).name)
        _layouter.Menu.set_speed(self)


class _Next(_String):
    u"""ネクストレベル文字列。
    """
    def __init__(self, groups=None):
        u"""コンストラクタ。
        """
        super(_Next, self).__init__((0, 0), groups)

    def update(self):
        u"""文字列更新。
        """
        level = _inventories.Endless.get_progress()+1
        self.string = u"NextLevel:{level}".format(
            level=(level if level < _const.ENDLESS_LIMIT else u"??"))
        _layouter.Menu.set_speed(self)


class _Level(_String):
    u"""対戦相手レベル文字列。
    """
    def __init__(self, groups=None):
        u"""コンストラクタ。
        """
        super(_Level, self).__init__((0, 0), groups=groups)

    def update(self):
        u"""文字列更新。
        """
        self.string = u"Level:{level}".format(
            level=_levels.get_duel_level()+1)
        _layouter.Menu.set_level(self)


class _Size(_String):
    u"""フィールドサイズ文字列。
    """
    def __init__(self, groups=None):
        u"""コンストラクタ。
        """
        super(_Size, self).__init__((0, 0), groups=groups)

    def update(self):
        u"""文字列更新。
        """
        self.string = u"Size:{size}".format(
            size=_const.FIELD_SIZE_TEXTS[_levels.get_versus_level()])
        _layouter.Menu.set_level(self)


class _Time(_String):
    u"""時間文字列。
    """
    def __init__(self, groups=None):
        u"""コンストラクタ。
        """
        super(_Time, self).__init__((0, 0), groups)

    def update(self):
        u"""文字列更新。
        """
        one_hour = 3600
        one_minute = 60
        hour, minute = divmod(_inventories.get_time(), one_hour)
        minute, second = divmod(minute, one_minute)
        self.string = u"Time:{hour:0>2}:{minute:0>2}:{second:0>2}".format(
            hour=hour, minute=minute, second=second)
        _layouter.Menu.set_time(self)


class _Score(_String):
    u"""得点文字列。
    SPとデュエルモード勝利数。
    """
    def __init__(self, groups=None):
        u"""コンストラクタ。
        """
        super(_Score, self).__init__((0, 0), groups)

    def update(self):
        u"""文字列更新。
        """
        self.string = u"SP:{sp} ★:{wins}".format(
            sp=_inventories.get_sp(), wins=_inventories.Level.get_wins())
        _layouter.Menu.set_level(self)


class Notice(object):
    u"""情報表示管理。
    """
    __slots__ = "__strings",
    __NOTICE_SLOT = 0
    __BOTTOM_LEFT_SLOT = 1
    __TIME_SLOT = 2
    __MID_BOTTOM_SLOT = 3

    def __init__(self):
        u"""コンストラクタ。
        """
        self.__strings = [None, None, None, None]

    def __set_string(self, slot, Cls):
        u"""文字列設定。
        """
        if Cls and not self.__strings[slot]:
            self.__strings[slot] = Cls()
        elif not Cls and self.__strings[slot]:
            self.__strings[slot].kill()
            self.__strings[slot] = None

    def eliminate(self):
        u"""全ての文字列を削除。
        """
        for i, string in enumerate(self.__strings):
            if string:
                string.kill()
                self.__strings[i] = None

    # ---- Property ----
    @property
    def has_notice(self):
        u"""情報表示取得。
        """
        return bool(self.__strings[self.__NOTICE_SLOT])

    @has_notice.setter
    def has_notice(self, value):
        u"""情報表示設定。
        """
        self.__set_string(
            self.__NOTICE_SLOT, _string.Notice if bool(value) else None)

    @property
    def has_speed(self):
        u"""速度表示取得。
        """
        return isinstance(
            self.__strings[self.__BOTTOM_LEFT_SLOT], _Speed)

    @has_speed.setter
    def has_speed(self, value):
        u"""速度表示設定。
        """
        self.__set_string(
            self.__BOTTOM_LEFT_SLOT, _Speed if bool(value) else None)

    @property
    def has_player(self):
        u"""プレイヤー名表示取得。
        """
        return isinstance(
            self.__strings[self.__BOTTOM_LEFT_SLOT], _Player)

    @has_player.setter
    def has_player(self, value):
        u"""プレイヤー名表示設定。
        """
        self.__set_string(
            self.__BOTTOM_LEFT_SLOT, _Player if bool(value) else None)

    @property
    def has_next_level(self):
        u"""ネクストレベル表示取得。
        """
        return isinstance(
            self.__strings[self.__BOTTOM_LEFT_SLOT], _Next)

    @has_next_level.setter
    def has_next_level(self, value):
        u"""ネクストレベル表示設定。
        """
        self.__set_string(
            self.__BOTTOM_LEFT_SLOT, _Next if bool(value) else None)

    @property
    def has_level(self):
        u"""対戦相手レベル表示取得。
        """
        return isinstance(
            self.__strings[self.__MID_BOTTOM_SLOT], _Level)

    @has_level.setter
    def has_level(self, value):
        u"""対戦相手レベル表示設定。
        """
        self.__set_string(
            self.__MID_BOTTOM_SLOT, _Level if bool(value) else None)

    @property
    def has_size(self):
        u"""フィールドサイズ表示取得。
        """
        return isinstance(
            self.__strings[self.__MID_BOTTOM_SLOT], _Size)

    @has_size.setter
    def has_size(self, value):
        u"""フィールドサイズ表示設定。
        """
        self.__set_string(
            self.__MID_BOTTOM_SLOT, _Size if bool(value) else None)

    @property
    def has_time(self):
        u"""時間表示取得。
        """
        return bool(self.__strings[self.__TIME_SLOT])

    @has_time.setter
    def has_time(self, value):
        u"""時間表示設定。
        """
        self.__set_string(self.__TIME_SLOT, _Time if bool(value) else None)

    @property
    def has_sp(self):
        u"""SP表示取得。
        """
        return bool(self.__strings[self.__MID_BOTTOM_SLOT])

    @has_sp.setter
    def has_sp(self, value):
        u"""SP表示設定。
        """
        self.__set_string(
            self.__MID_BOTTOM_SLOT, _Score if bool(value) else None)
