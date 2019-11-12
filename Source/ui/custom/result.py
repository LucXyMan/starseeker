#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""result.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

リザルト画面モジュール。
"""
import armament.collectible as _collectible
import inventory as _inventory
import utils.const as _const
import ui.content as _content


class Result(_content.Control):
    u"""リザルト画面。
    """
    __slots__ = "__deck", "__got", "__reward"

    def _update_info(self):
        u"""情報を表示。
        """
        import sprites.string as __string
        window = self.active_window
        if window.items:
            icon = window.items[window.cursor]
            item = _collectible.get(icon.number)
            __string.Info.send(
                item.info if icon.is_front else
                u"決定キーで{type}カード取得/{got}S.P消費".format(
                    type=item.type, got=_inventory.Cards.get_consume(
                        self.__got)))

    def __init__(self):
        u"""操作ウィンドウの初期設定。
        """
        import random as __random
        import armament.level as __level
        import icon as __icon
        import ui.window as __window
        import utils.layouter as __layouter

        class _RewardWindow(__window.Label):
            u"""褒賞ウィンドウ。
            """
            __MATRIX = 9, 1

            def __init__(self, pos, number, groups=None):
                u"""コンストラクタ。
                """
                import ui.label as __label
                x, y = pos
                col, row = self.__MATRIX
                super(_RewardWindow, self).__init__(
                    (x, y, col*_const.GRID, row*_const.GRID),
                    (col, row), groups)
                if number != 0:
                    self.append(__label.General((0, 0), number, ()))
        super(Result, self).__init__()
        col, row = _content.Control.WINDOW_ROW, 2
        self._controls = []
        window = __window.Icon(
            (0, 0, col*_const.GRID, row*_const.GRID), (col, row))
        deck = list(__level.get_deck())
        __random.shuffle(deck)
        for card in deck:
            window.append(__icon.Reward((0, 0), _collectible.get(card), ()))
        window.is_light = window.is_active = True
        if _inventory.Utils.get_endless() % _const.ENDLESS_INTRVAL == 0:
            reward = __level.get_reward()
            if reward != 0:
                _inventory.Items.on(reward-1)
                self.__reward = _RewardWindow((0, 0), reward)
            else:
                self.__reward = None
            __layouter.Menu.set_result(window, self.__reward)
        else:
            __layouter.Menu.set_result(window)
        self._controls.append(window)
        self.__got = 0
        self._update_info()

    def eliminate(self):
        u"""パースの削除処理。
        """
        if self.__reward:
            self.__reward.kill()
        super(Result, self).eliminate()

    def decision(self):
        u"""決定キー処理。
        """
        import material.sound as sound
        window = self.active_window
        if window.items:
            icon = window.items[window.cursor]
            if (
                not icon.is_front and
                _inventory.SP.buy_card(icon.number, self.__got)
            ):
                sound.SE.play("Get")
                icon.is_front = True
                self.__got += 1
                self._update_info()
            else:
                sound.SE.play("Error")
        return _const.IGNORE_STATUS

    def cancel(self):
        u"""取り消しキー処理。
        """
        return _const.MODE_SELECT_STATUS
