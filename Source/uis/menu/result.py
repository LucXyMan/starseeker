#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""result.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

リザルト画面モジュール。
"""
import armament.collectible as _collectible
import inventories as _inventories
import utils.const as _const
import uis.ui as _ui


class Result(_ui.Controllable):
    u"""リザルト画面。
    """
    __slots__ = "__deck", "__got", "__reward"

    def __init__(self):
        u"""操作ウィンドウの初期設定。
        """
        import random as __random
        import armament.levels as __levels
        import icon as __icon
        import uis.window as __window
        import utils.layouter as __layouter

        class _RewardWindow(__window.Label):
            u"""褒賞ウィンドウ。
            """
            __MATRIX = 9, 1

            def __init__(self, pos, number, groups=None):
                u"""コンストラクタ。
                """
                import uis.label as __label
                x, y = pos
                col, row = self.__MATRIX
                super(_RewardWindow, self).__init__(
                    (x, y, col*_const.GRID, row*_const.GRID),
                    (col, row), groups)
                if number != 0:
                    self.append(__label.General((0, 0), number, ()))
        super(Result, self).__init__()
        col, row = _ui.Controllable.WINDOW_COL, 2
        self._controls = []
        window = __window.Icon(
            (0, 0, col*_const.GRID, row*_const.GRID), (col, row))
        deck = list(__levels.get_deck())
        __random.shuffle(deck)
        for card in deck:
            window.append(__icon.Reward((0, 0), _collectible.get(card), ()))
        window.is_light = window.is_active = True
        if _inventories.Endless.get_progress() % _const.ENDLESS_INTRVAL == 0:
            reward = __levels.get_reward()
            if reward != 0:
                _inventories.Item.on(reward-1)
                self.__reward = _RewardWindow((0, 0), reward)
            else:
                self.__reward = None
            __layouter.Menu.set_result(window, self.__reward)
        else:
            __layouter.Menu.set_result(window)
        self._controls.append(window)
        self.__got = 0
        self._update_notice()

    def _update_notice(self):
        u"""情報を表示。
        """
        import sprites as __sprites
        window = self.active_window
        if window.items:
            icon = window.items[window.cursor]
            item = _collectible.get(icon.number)
            consume = _inventories.Card.get_consume(self.__got)
            __sprites.Notice.notify(
                item.notice if icon.is_front else
                u"決定キーで{type}カード取得/{consume}SP消費".
                format(type=item.type, consume=consume))

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
                _inventories.buy_card(icon.number, self.__got)
            ):
                sound.SE.play("get")
                icon.is_front = True
                self.__got += 1
                self._update_notice()
            else:
                sound.SE.play("error")
        return _const.IGNORE_STATUS

    def cancel(self):
        u"""取り消しキー処理。
        """
        return _const.MODE_SELECT_STATUS
