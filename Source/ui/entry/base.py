#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""base.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

対戦相手選択画面モジュール。
"""
import sprites.general as _general
import sprites as _sprites
import ui.content as _content
import ui.window as _window
import utils.const as _const


class RivalImage(_general.General):
    u"""対戦相手イメージ。
    """
    def __init__(self, content, groups=None):
        u"""コンストラクタ。
        """
        super(RivalImage, self).__init__(groups)
        self._content = content
        self._old = -1
        self.update()


class RivalEquip(_window.Label):
    u"""対戦相手装備ウィンドウ。
    """
    def __init__(self, content, groups=None):
        u"""コンストラクタ。
        """
        self._content = content
        self._old = -1
        w, h = 9, 4
        super(RivalEquip, self).__init__(
            (0, 0, w*_const.GRID, h*_const.GRID), (w, h), groups)


class Entry(_content.Content):
    u"""対戦相手選択画面。
    """
    __slots__ = ()
    _LEVEL_SELECT_TEXT = (
        u"左右キーで対戦相手選択/上下キーで{level}選択#"+_content.Content._PLAYER_SELECT_TEXT)

    class _RivalStatus(_sprites.window.Window):
        u"""対戦相手ステータスウィンドウ。
        """
        __MATRIX = 6, 2

        def __init__(self, content, groups=None):
            u"""コンストラクタ。
            """
            import pygame as __pygame
            import armament.equip as _equip
            import armament.units as _units

            class _StatusString(_sprites.string.String):
                u"""ステータス文字列。
                """
                def __init__(self, pos, window, groups):
                    u"""コンストラクタ。
                    """
                    self._window = window
                    super(_StatusString, self).__init__(
                        pos, "", _const.SYSTEM_CHAR_SIZE,
                        shorten=False, groups=groups)

            class __AttackString(_StatusString):
                u"""攻撃数値文字列。
                """
                def update(self):
                    u"""スプライト更新。
                    """
                    weapon, _, _, _ = self._window.level.equip
                    number, _ = self._window.level.player
                    self.text = (
                        "" if not self._window.level.is_playable else
                        "ATK: {0: >2}".format(
                            _units.get_player(number).str +
                            _equip.get(weapon).value))

            class __DefenceString(_StatusString):
                u"""攻撃数値文字列。
                """
                def update(self):
                    u"""スプライト更新。
                    """
                    _, helm, armor, accessory = self._window.level.equip
                    number, _ = self._window.level.player
                    self.text = (
                        "" if not self._window.level.is_playable else
                        "DEF: {0: >2}".format(
                            _units.get_player(number).vit+sum(
                                _equip.get(equip).value for
                                equip in (helm, armor, accessory))))
            col, row = self.__MATRIX
            super(Entry._RivalStatus, self).__init__(
                (0, 0), __pygame.Surface((col*_const.GRID, row*_const.GRID)),
                groups)
            self.__content = content
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
            return self.__content.level

    def __init__(self):
        u"""コンストラクタ。
        """
        import ui.custom.custom as __custom
        super(Entry, self).__init__()
        __custom.PlayerImage()
        __custom.EquipWindow((0, 0))
        __custom.StatusWindow((0, 0), self)
        self._RivalImage(self)
        self._RivalEquip(self)
        self._RivalStatus(self)

    def _change_bg(self, select, is_gradually=False):
        u"""背景画像変更。
        """
        import material.misc as __misc
        import utils.image as __image
        __image.BackGround.set_image(__misc.get(
            _const.BG_DICT[select]), is_gradually)

    def cancel(self):
        u"""取り消しキー処理。
        """
        return _const.MODE_SELECT_STATUS

    def __change_player(self, value):
        u"""プレイヤー変更。
        """
        import inventory as __inventory
        import material.sound as __sound
        player = __inventory.Utils.get_player()
        __inventory.Utils.set_player((player+value) % _const.PLAYER_NUMBER)
        if __inventory.Utils.get_player() != player:
            __sound.SE.play("Cursor")
        return _const.IGNORE_STATUS

    def delete(self):
        u"""左のプレイヤー選択。
        """
        return self.__change_player(-1)

    def use(self):
        u"""右のプレイヤーを選択。
        """
        return self.__change_player(1)
