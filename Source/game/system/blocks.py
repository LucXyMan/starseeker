#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""blocks.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ブロックシステムモジュール。
"""
import pieces as _pieces
import utils.const as _const


class System(object):
    u"""ブロックシステム。
    ペアレント、ネクスト、ホールド、オペレート、フィールドを管理する。
    """
    __slots__ = (
        "__del_lines", "__drop_pos", "__fall_progress", "__field", "__hold",
        "__is_completed", "__main", "__minimap", "__next", "__parent",
        "__piece", "__pressure", "__window")
    __WINDOW_MIN_ALPHA = 176

    def __init__(self, main, parent, level):
        u"""コンストラクタ。
        __main: メインシステム。
        """
        import hold as __hold
        import next as __next
        import sprites.indicator as __indicator
        import utils.layouter as __layouter
        import window as __window

        class _FieldPattern(_pieces.Pattern):
            u"""フィールドパターン。
            """
            __MARGIN = 0

            def __init__(self, level):
                u"""コンストラクタ。
                """
                x1 = "Normal", 0, (1, 1)
                t_spin_test = (
                    ((0, 6), x1),  ((1, 6), x1), ((2, 6), x1),
                    ((3, 6), x1),
                    ((4, 6), x1), ((5, 6), x1), ((6, 6), x1),
                    ((0, 7), x1), ((1, 7), x1), ((2, 7), x1), ((3, 7), x1),
                    ((4, 7), x1), ((5, 7), x1),
                    ((0, 8), x1), ((1, 8), x1), ((2, 8), x1), ((3, 8), x1),
                    ((4, 8), x1), ((5, 8), x1), ((7, 8), x1), ((8, 8), x1),
                    ((0, 9), x1), ((1, 9), x1), ((2, 9), x1), ((3, 9), x1),
                    ((4, 9), x1), ((5, 9), x1), ((8, 9), x1),
                    ((0, 10), x1), ((1, 10), x1), ((2, 10), x1), ((3, 10), x1),
                    ((4, 10), x1), ((5, 10), x1), ((7, 10), x1), ((8, 10), x1))
                super(_FieldPattern, self).__init__(
                    (9, 11 + self.__MARGIN) if level == 0 else
                    (12, 11 + self.__MARGIN) if level == 1 else
                    (9, 16 + self.__MARGIN) if level == 2 else
                    (12, 16 + self.__MARGIN),
                    t_spin_test if _const.PIECE_TEST == "T_SPIN_TEST" else ())

            @property
            def drop_pos(self):
                u"""ピース出現地点を取得。
                """
                return (self.width - 3) >> 1, self.__MARGIN
        self.__main = main
        self.__parent = parent
        self.__next = __next.Next(level.deck, self.__main.id)
        self.__hold = __hold.Hold(self.__main)
        _, rank = level.player
        self.__fall_progress = 0
        self.__pressure = 0
        self.__del_lines = ()
        self.__is_completed = False
        pattern = _FieldPattern(rank)
        self.__drop_pos = pattern.drop_pos
        w, h = pattern.width, pattern.height
        self.__window = __window.Field(
            (0, 0, 9*_const.GRID, 11*_const.GRID),
            (w*_const.GRID, h*_const.GRID))
        __layouter.Game.set_field(self.__window, self.__main.id)
        self.__window.field = self.__field = _pieces.Field(
            pattern, self.__main.skills)
        self.__minimap = (
            __indicator.Space((0, 0, w, h)) if _const.IS_SPACE_MINIMAP else
            __indicator.Block((0, 0, w, h)))
        __layouter.Game.set_minimap(
            self.__minimap, self.__hold, self.__main.id)

    def fall(self):
        u"""ブロックの落下処理。
        """
        if not _const.IS_FALL_STOP:
            if self.__fall_progress < _const.FRAME_RATE:
                self.__fall_progress += 1
            else:
                self.__main.command_input(_const.DOWN_COMMAND)
                self.__fall_progress = 0

    def fall_clear(self):
        u"""ファール進行を0に。
        """
        self.__fall_progress = 0

    def advance(self, time=1, level_up=True):
        u"""ピース進行。
        time回ピースを進める。
        """
        if hasattr(self, "__piece"):
            self.__piece.clear()
        for _ in range(time):
            pattern = self.__next.advance(self.__parent.get_pattern(level_up))
        self.__piece = _pieces.Dropping(pattern, self.__drop_pos)
        self.__window.piece = self.__piece
        self.update_display()

    def skip(self):
        u"""ピーススキップ。
        """
        self.__piece.skip()
        self.__window.ghost = None
        if self.__main.thinker:
            self.__main.thinker.is_changed = True

    def del_line_plus(self, line):
        u"""消去ライン追加。
        """
        self.__del_lines += line

    def del_line_clear(self):
        u"""消去ライン初期化。
        """
        self.__del_lines = ()

    def vanish(self):
        u"""ゲーム終了時のフィールド消去。
        """
        self.__field.vanish()
        self.__piece.vanish()
        self.__window.ghost = None

    def update_parameter(self):
        u"""ゲームパラメータの変動処理。
        """
        if not self.__is_completed:
            self.__parent.hardness_down()
            self.__parent.luck_up()
        else:
            self.__parent.hardness_up()
            self.__parent.luck_down()

    def update_display(self):
        u"""ウィンドウ、ガイドを更新。
        """
        def __update_minimap():
            u"""ミニマップの更新。
            """
            if _const.IS_SPACE_MINIMAP:
                self.__minimap.write_blocks(False, self.__field.table)
            else:
                self.__minimap.write_blocks(True, *self.__field.blocks)
                self.__minimap.write_blocks(False, *self.__piece.blocks)

        def __update_window():
            u"""ウィンドウの値を更新。
            """
            self.__window.update_area()
            if _const.IS_WINDOW_TRANSPARENT:
                diff = self.__field.highest+self.__window.difference
                height = (
                    self.__field.height if self.__field.height < diff else
                    diff)
                alpha = int(height/float(self.__field.height)*255)
                self.__window.image.set_alpha(
                    alpha if self.__WINDOW_MIN_ALPHA < alpha else
                    self.__WINDOW_MIN_ALPHA)
            else:
                self.__window.image.set_alpha(None)
        self.__window.ghost = self.__piece.get_target(self.__field)
        __update_minimap()
        __update_window()

    @property
    def hold(self):
        u"""ホールド取得。
        """
        return self.__hold

    @property
    def field(self):
        u"""フィールド取得。
        """
        return self.__field

    @property
    def piece(self):
        u"""ピース取得。
        """
        return self.__piece

    @property
    def window(self):
        u"""ブロックウィンドウ取得。
        """
        return self.__window

    @property
    def drop_pos(self):
        u"""ピースの落下地点を取得。
        """
        return self.__drop_pos

    @property
    def del_lines(self):
        u"""消去したラインを取得。
        """
        return self.__del_lines

    @property
    def has_item(self):
        u"""アイテム保有状態取得。
        """
        return self.__parent.has_item

    @property
    def is_completed(self):
        u"""コンプリート状態取得。
        """
        return self.__is_completed

    @is_completed.setter
    def is_completed(self, value):
        u"""コンプリート状態設定。
        """
        self.__is_completed = bool(value)
