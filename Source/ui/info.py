#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""info.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

情報表示モジュール。
"""
import armament.level as _level
import inventory as _inventory
import sprites.string as _string
import utils.const as _const
import utils.layouter as _layouter


class Info(object):
    u"""情報表示管理。
    """
    __slots__ = "__contents",
    __INFO_SLOT = 0
    __BOTTOM_LEFT_SLOT = 1
    __TIME_SLOT = 2
    __MID_BOTTOM_SLOT = 3

    class _String(_string.String):
        u"""基本情報パラメータ文字列。
        """
        def __init__(self, pos, groups):
            u"""コンストラクタ。
            """
            super(Info._String, self).__init__(
                pos, "", _const.SYSTEM_CHAR_SIZE, groups=groups)

    class _Speed(_String):
        u"""ピース・カーソル速度文字列。
        """
        def __init__(self, groups=None):
            u"""コンストラクタ。
            """
            super(Info._Speed, self).__init__((0, 0), groups)

        def update(self):
            u"""文字列更新。
            """
            self.text = u"Speed:{}".format(
                _const.SPEED_TEXTS[_inventory.Utils.get_speed()])
            _layouter.Menu.set_bottomleft(self)

    class _Player(_String):
        u"""現在プレイヤー文字列。
        """
        def __init__(self, groups=None):
            u"""コンストラクタ。
            """
            super(Info._Player, self).__init__((0, 0), groups=groups)

        def update(self):
            u"""文字列更新。
            """
            import armament.units as __units
            self.text = u"Player:{name}".format(
                name=__units.get_player(_inventory.Utils.get_player()).name)
            _layouter.Menu.set_bottomleft(self)

    class _Next(_String):
        u"""ネクストレベル文字列。
        """
        def __init__(self, groups=None):
            u"""コンストラクタ。
            """
            super(Info._Next, self).__init__((0, 0), groups)

        def update(self):
            u"""文字列更新。
            """
            level = _inventory.Utils.get_endless()+1
            self.text = u"NextLevel:{level}".format(
                level=(level if level < _const.ENDLESS_LIMIT else u"??"))
            _layouter.Menu.set_bottomleft(self)

    class _Level(_String):
        u"""対戦相手レベル文字列。
        """
        def __init__(self, groups=None):
            u"""コンストラクタ。
            """
            super(Info._Level, self).__init__((0, 0), groups=groups)

        def update(self):
            u"""文字列更新。
            """
            self.text = u"Level:{level}".format(
                level=_level.get_duel_level()+1)
            _layouter.Menu.set_midbottom(self)

    class _Size(_String):
        u"""フィールドサイズ文字列。
        """
        def __init__(self, groups=None):
            u"""コンストラクタ。
            """
            super(Info._Size, self).__init__((0, 0), groups=groups)

        def update(self):
            u"""文字列更新。
            """
            self.text = u"Size:{size}".format(
                size=_const.FIELD_SIZE_TEXTS[_level.get_versus_level()])
            _layouter.Menu.set_midbottom(self)

    class _Time(_String):
        u"""時間文字列。
        """
        def __init__(self, groups=None):
            u"""コンストラクタ。
            """
            super(Info._Time, self).__init__((0, 0), groups)

        def update(self):
            u"""文字列更新。
            """
            one_hour = 3600
            one_minute = 60
            hour, minute = divmod(_inventory.Time.get(), one_hour)
            minute, second = divmod(minute, one_minute)
            self.text = u"Time:{hour:0>2}:{minute:0>2}:{second:0>2}".format(
                hour=hour, minute=minute, second=second)
            _layouter.Menu.set_time(self)

    class _Score(_String):
        u"""得点文字列。
        SPとデュエルモード勝利数。
        """
        def __init__(self, groups=None):
            u"""コンストラクタ。
            """
            super(Info._Score, self).__init__((0, 0), groups)

        def update(self):
            u"""文字列更新。
            """
            self.text = u"SP:{sp} ★:{wins}".format(
                sp=_inventory.SP.get(), wins=_inventory.Level.get_wins())
            _layouter.Menu.set_midbottom(self)

    def __init__(self):
        u"""コンストラクタ。
        """
        self.__contents = [None, None, None, None]

    def eliminate(self):
        u"""全ての内容物をkill。
        """
        for i, content in enumerate(self.__contents):
            if content:
                content.kill()
                self.__contents[i] = None

    def __set_content(self, slot, Cls):
        u"""コンテンツ設定。
        """
        if Cls and not self.__contents[slot]:
            self.__contents[slot] = Cls()
        elif not Cls and self.__contents[slot]:
            self.__contents[slot].kill()
            self.__contents[slot] = None

    @property
    def has_info(self):
        u"""情報表示取得。
        """
        return bool(self.__contents[self.__INFO_SLOT])

    @has_info.setter
    def has_info(self, value):
        u"""情報表示設定。
        """
        self.__set_content(
            self.__INFO_SLOT, _string.Info if bool(value) else None)

    @property
    def has_speed(self):
        u"""速度表示取得。
        """
        return isinstance(
            self.__contents[self.__BOTTOM_LEFT_SLOT], Info._Speed)

    @has_speed.setter
    def has_speed(self, value):
        u"""速度表示設定。
        """
        self.__set_content(
            self.__BOTTOM_LEFT_SLOT, Info._Speed if bool(value) else None)

    @property
    def has_player(self):
        u"""プレイヤー名表示取得。
        """
        return isinstance(
            self.__contents[self.__BOTTOM_LEFT_SLOT], Info._Player)

    @has_player.setter
    def has_player(self, value):
        u"""プレイヤー名表示設定。
        """
        self.__set_content(
            self.__BOTTOM_LEFT_SLOT, Info._Player if bool(value) else None)

    @property
    def has_next_level(self):
        u"""ネクストレベル表示取得。
        """
        return isinstance(
            self.__contents[self.__BOTTOM_LEFT_SLOT], Info._Next)

    @has_next_level.setter
    def has_next_level(self, value):
        u"""ネクストレベル表示設定。
        """
        self.__set_content(
            self.__BOTTOM_LEFT_SLOT, Info._Next if bool(value) else None)

    @property
    def has_level(self):
        u"""対戦相手レベル表示取得。
        """
        return isinstance(
            self.__contents[self.__MID_BOTTOM_SLOT], Info._Level)

    @has_level.setter
    def has_level(self, value):
        u"""対戦相手レベル表示設定。
        """
        self.__set_content(
            self.__MID_BOTTOM_SLOT, Info._Level if bool(value) else None)

    @property
    def has_size(self):
        u"""フィールドサイズ表示取得。
        """
        return isinstance(
            self.__contents[self.__MID_BOTTOM_SLOT], Info._Size)

    @has_size.setter
    def has_size(self, value):
        u"""フィールドサイズ表示設定。
        """
        self.__set_content(
            self.__MID_BOTTOM_SLOT, Info._Size if bool(value) else None)

    @property
    def has_time(self):
        u"""時間表示取得。
        """
        return bool(self.__contents[self.__TIME_SLOT])

    @has_time.setter
    def has_time(self, value):
        u"""時間表示設定。
        """
        self.__set_content(
            self.__TIME_SLOT, Info._Time if bool(value) else None)

    @property
    def has_sp(self):
        u"""SP表示取得。
        """
        return bool(self.__contents[self.__MID_BOTTOM_SLOT])

    @has_sp.setter
    def has_sp(self, value):
        u"""SP表示設定。
        """
        self.__set_content(
            self.__MID_BOTTOM_SLOT, Info._Score if bool(value) else None)
