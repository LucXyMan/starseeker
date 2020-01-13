#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""versus.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ヴァーサス選択画面モジュール。
"""
import armament.levels as _levels
import armament.units as _units
import entry as _entry
import material.sound as _sound
import utils.const as _const
import utils.layouter as _layouter


class Entry(_entry.Entry):
    u"""ヴァーサス選択。
    """
    __slots__ = ()

    def __init__(self):
        u"""コンストラクタ。
        """
        class __RivalImage(_entry.RivalImage):
            u"""対戦相手イメージ。
            """
            def update(self):
                u"""スプライト更新。
                """
                import utils.image as __image
                number, _ = self._ui.level.player
                if self._old != number:
                    self.image = (
                        _units.get_player(number).get_image(False, False))
                    __image.set_colorkey(self.image, "0x000000")
                    if hasattr(self, "rect"):
                        self.rect.size = self.image.get_size()
                    else:
                        self.rect = self.image.get_rect()
                    _layouter.Menu.set_player(self, True)
                    self._old = number

        class _RivalEquip(_entry.RivalEquip):
            u"""装備ウィンドウ。
            """
            def update(self):
                u"""ウィンドウの更新処理。
                """
                import uis.label as __label
                level = self._ui.level
                number, _ = self._ui.level.player
                if self._old != number:
                    self._items = tuple(
                        __label.General((0, i*_const.GRID), item, ()) for
                        i, item in enumerate(level.equip))
                    self._old = number
                    _layouter.Menu.set_equip(self, True)
                super(_RivalEquip, self).update()
        super(Entry, self).__init__()
        __RivalImage(self)
        _RivalEquip(self)
        self._change_bg(_levels.get_selected_2p())
        self.__update_notice()

    def __update_notice(self):
        u"""情報更新。
        """
        import sprites as __sprites
        __sprites.Notice.notify(_units.get_player(
            _levels.get_selected_2p()).notice+u"#" +
            self._LEVEL_SELECT_TEXT.format(level=u"サイズ"))

    # ---- Up and Down ----
    def __change_field(self, value):
        u"""フィールドサイズ変更。
        """
        limit = len(_const.FIELD_SIZE_TEXTS)-1
        size = _levels.get_versus_level()
        _size = size+value
        _levels.set_versus_level(
            0 if _size < 0 else _size if _size < limit else limit)
        if _levels.get_versus_level() != size:
            _sound.SE.play("cursor_1")
        return _const.IGNORE_STATUS

    def up(self):
        u"""サイズを大きく。
        """
        return self.__change_field(1)

    def down(self):
        u"""サイズを小さく。
        """
        return self.__change_field(-1)

    # ---- Left and Right ----
    def __change_rival(self, value):
        u"""対戦相手変更。
        """
        rival = _levels.get_selected_2p()
        _rival = rival+value
        _rival = (
            _const.PLEYERS-1 if _rival < 0 else
            _rival if _rival < _const.PLEYERS else 0)
        self._change_bg(_rival, True)
        _levels.set_selected_2p(_rival)
        if _levels.get_selected_2p() != rival:
            _sound.SE.play("cursor_1")
        self.__update_notice()
        return _const.IGNORE_STATUS

    def left(self):
        u"""カーソルを左に。
        """
        return self.__change_rival(-1)

    def right(self):
        u"""カーソルを右に。
        """
        return self.__change_rival(1)

    # ---- Decision ----
    def decision(self):
        u"""決定キー入力。
        """
        _sound.SE.play("decision")
        return _const.VERSUS_STATUS

    # ---- Property ----
    @property
    def level(self):
        u"""選択レベル取得。
        """
        return _levels.get_2p()
