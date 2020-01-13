#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""entry.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

対戦相手選択画面モジュール。
"""
import sprites.huds as __huds
import uis.ui as _ui
import uis.window as __window
import utils.const as _const


class RivalImage(__huds.HUD):
    u"""対戦相手イメージ。
    """
    def __init__(self, ui, groups=None):
        u"""コンストラクタ。
        """
        super(RivalImage, self).__init__(groups)
        self._ui = ui
        self._old = -1
        self.update()


class RivalEquip(__window.Label):
    u"""対戦相手装備ウィンドウ。
    """
    def __init__(self, ui, groups=None):
        u"""コンストラクタ。
        """
        self._ui = ui
        self._old = -1
        w, h = 9, 4
        super(RivalEquip, self).__init__(
            (0, 0, w*_const.GRID, h*_const.GRID), (w, h), groups)


class Entry(_ui.UI):
    u"""対戦相手選択画面。
    """
    __slots__ = ()
    _LEVEL_SELECT_TEXT = (
        u"左右キーで対戦相手選択/上下キーで{level}選択#" +
        _ui.UI._PLAYER_SELECT_TEXT)

    def __init__(self):
        u"""コンストラクタ。
        """
        import uis.menu.customize as __customize
        import sprites as _sprites

        class _RivalStatus(_sprites.Window):
            u"""対戦相手ステータスウィンドウ。
            """
            __MATRIX = 6, 2

            def __init__(self, ui, groups=None):
                u"""コンストラクタ。
                """
                import pygame as __pygame
                import armament.equips as _equips
                import armament.units as _units

                class _StatusString(_sprites.String):
                    u"""ステータス文字列。
                    """
                    def __init__(self, pos, window, groups):
                        u"""コンストラクタ。
                        """
                        self._window = window
                        super(_StatusString, self).__init__(
                            pos, "", _const.SYSTEM_CHAR_SIZE,
                            is_short=False, groups=groups)

                class __AttackString(_StatusString):
                    u"""攻撃数値文字列。
                    """
                    def update(self):
                        u"""スプライト更新。
                        """
                        weapon, _, _, _ = self._window.level.equip
                        number, _ = self._window.level.player
                        self.string = (
                            "" if not self._window.level.is_playable else
                            "ATK: {0: >2}".format(
                                _units.get_player(number).str +
                                _equips.get(weapon).value))

                class __DefenceString(_StatusString):
                    u"""防御数値文字列。
                    """
                    def update(self):
                        u"""スプライト更新。
                        """
                        _, helm, armor, accessory = self._window.level.equip
                        number, _ = self._window.level.player
                        self.string = (
                            "" if not self._window.level.is_playable else
                            "DEF: {0: >2}".format(
                                _units.get_player(number).vit+sum(
                                    _equips.get(equip).value for
                                    equip in (helm, armor, accessory))))
                col, row = self.__MATRIX
                super(_RivalStatus, self).__init__((0, 0), __pygame.Surface((
                    col*_const.GRID, row*_const.GRID)), groups)
                self.__ui = ui
                self.__strings = []
                for i, String in enumerate((__AttackString, __DefenceString)):
                    string = String((0, 0), self, ())
                    string.rect.midleft = 0, (_const.GRID >> 1)+_const.GRID*i
                    self.__strings.append(string)
                self.update()

            def __string_blit(self):
                u"""文字列書き込み。
                """
                for string in self.__strings:
                    string.update()
                    self.image.blit(string.image, string.rect.topleft)

            def update(self):
                u"""更新処理。
                """
                import utils.image as __image
                import utils.layouter as __layouter
                col, row = self.__MATRIX
                self.image.blit(__image.get_checkered(col, row, 1), (0, 0))
                self.__string_blit()
                __layouter.Menu.set_status(self, True)

            @property
            def level(self):
                u"""レベル取得。
                """
                return self.__ui.level
        super(Entry, self).__init__()
        __customize.PlayerImage()
        __customize.EquipWindow((0, 0))
        __customize.StatusWindow((0, 0), self)
        _RivalStatus(self)

    def __change_player(self, value):
        u"""プレイヤー変更。
        """
        import inventories as __inventories
        import material.sound as __sound
        player = __inventories.General.get_player()
        __inventories.General.set_player((player+value) % _const.PLEYERS)
        if __inventories.General.get_player() != player:
            __sound.SE.play("cursor_1")
        return _const.IGNORE_STATUS

    def _change_bg(self, select, is_gradually=False):
        u"""背景画像変更。
        """
        import material.misc as __misc
        import utils.image as __image
        __image.BackGround.set_image(
            __misc.get(_const.BG_DICT[select]), is_gradually)

    def cancel(self):
        u"""取り消しキー処理。
        """
        return _const.MODE_SELECT_STATUS

    def delete(self):
        u"""左のプレイヤー選択。
        """
        return self.__change_player(-1)

    def use(self):
        u"""右のプレイヤーを選択。
        """
        return self.__change_player(1)
