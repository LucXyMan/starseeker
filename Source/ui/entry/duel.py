#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""duel.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

デュエル選択画面モジュール。
"""
import armament.level as _level
import armament.units as _units
import base as _base
import material.sound as _sound
import inventory as _inventory
import sprites.string as _string
import utils.const as _const
import utils.layouter as _layouter


class Entry(_base.Entry):
    u"""デュエル選択。
    """
    __slots__ = "__old",
    __IS_LEVEL_CORRECT = True

    class _RivalImage(_base.RivalImage):
        u"""対戦相手イメージ。
        """
        def update(self):
            u"""スプライト更新。
            """
            import utils.image as __image
            level = self._content.level
            if self._old != level.number:
                number, _ = level.player
                self.image = _units.get_player(number).get_image(
                    False, False)
                if _inventory.Level.has(level.number):
                    self.image = __image.get_dull(self.image)
                elif not level.is_playable:
                    self.image = __image.get_colored_fill(
                        self.image, _const.BLACK)
                __image.set_colorkey(self.image, "0x000000")
                if hasattr(self, "rect"):
                    self.rect.size = self.image.get_size()
                else:
                    self.rect = self.image.get_rect()
                _layouter.Menu.set_player_image(self, True)
                self._old = level.number

    class _RivalEquip(_base.RivalEquip):
        u"""ライバル装備ウィンドウ。
        """
        def update(self):
            u"""ウィンドウの更新処理。
            """
            import ui.label as __label
            level = self._content.level
            if self._old != level.number:
                self._items = () if not level.is_playable else tuple(
                    __label.General((0, i*_const.GRID), equip, ()) for
                    i, equip in enumerate(level.equip))
                self._old = level.number
                _layouter.Menu.set_equip(self, True)
            super(Entry._RivalEquip, self).update()

    def __init__(self):
        u"""コンストラクタ。
        """
        def __level_correct():
            u"""初期選択レベル補正処理。
            """
            if self.__IS_LEVEL_CORRECT:
                for level in _level.get_duel_all():
                    if level.is_playable and not _inventory.Level.has(
                        level.number
                    ):
                        number, player_level = level.player
                        _level.set_rival(number)
                        _level.set_duel_level(player_level)
                        return None
        super(Entry, self).__init__()
        __level_correct()
        self._change_bg(_level.get_rival())
        self.__old = ()
        self.__update_info()

    def __update_info(self):
        u"""情報更新。
        """
        rival = _level.get_rival()
        playable = _level.get_duel().is_playable
        if self.__old != (rival, playable):
            operation = u"#"+self._LEVEL_SELECT_TEXT.format(level=u"レベル")
            if playable:
                _string.Info.send(_units.get_player(
                    _level.get_rival()).info+operation)
            else:
                _string.Info.send(u"???/まだ戦えません"+operation)
            self.__old = rival, playable

    def __level_change(self, value):
        u"""レベル変更。
        """
        limit = 3
        level = _level.get_duel_level()
        set_ = level+value
        _level.set_duel_level(
            0 if set_ < 0 else set_ if set_ < limit else limit)
        if _level.get_duel_level() != level:
            _sound.SE.play("Cursor")
        self.__update_info()
        return _const.IGNORE_STATUS

    def up(self):
        u"""上方向キー入力。
        """
        return self.__level_change(1)

    def down(self):
        u"""下方向キー入力。
        """
        return self.__level_change(-1)

    def __rival_change(self, value):
        u"""対戦相手変更。
        """
        rival = _level.get_rival()
        set_ = rival+value
        set_ = (
            _const.PLAYER_NUMBER if set_ < 0 else
            set_ if set_ <= _const.PLAYER_NUMBER else 0)
        self._change_bg(set_, True)
        _level.set_rival(set_)
        if _level.get_rival() != rival:
            _sound.SE.play("Cursor")
        self.__update_info()
        return _const.IGNORE_STATUS

    def left(self):
        u"""カーソルを左に。
        """
        return self.__rival_change(-1)

    def right(self):
        u"""カーソルを右に。
        """
        return self.__rival_change(1)

    def decision(self):
        u"""決定キー入力。
        """
        if not _level.get_duel().is_playable:
            _sound.SE.play("Error")
            return _const.IGNORE_STATUS
        _sound.SE.play("Decision")
        return _const.DUEL_STATUS

    @property
    def level(self):
        u"""選択レベル取得。
        """
        return _level.get_duel()
