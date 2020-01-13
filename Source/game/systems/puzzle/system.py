#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""system.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

パズルシステムモジュール。
"""
import pieces as _pieces
import utils.const as _const


class System(object):
    u"""パズルシステム。
    ペアレント、ネクスト、ホールド、オペレート、フィールドを管理する。
    """
    __slots__ = (
        "__core", "__drop_point", "__fall_progress", "__field", "__hold",
        "__is_completed", "__minimap", "__next", "__one_pieces", "__parent",
        "__piece", "__pressure", "__window")
    __WINDOW_MIN_ALPHA = 0xB0

    def __init__(self, core, parent, level):
        u"""コンストラクタ。
        """
        import hold as __hold
        import next as __next
        import sprites.huds as __huds
        import utils.layouter as __layouter
        import window as __window

        class _FieldPattern(_pieces.Pattern):
            u"""フィールドパターン。
            """
            __MARGIN = 0

            def __init__(self, level):
                u"""コンストラクタ。
                """
                x1 = "Normal", -1, (1, 1)
                solid = "Solid", -1, (1, 1)
                adamant = "Adamant", -1, (1, 1)
                king_demon = "KingDemon", -1, (2, 2)
                acid = "Acid", -1, (1, 1)
                key = "GoldKey", -1, (1, 1)
                chest = "GoldChest", -1, (1, 1)
                opened = "GoldChest", 15, (1, 1)
                mimic = "GoldChest", 16, (1, 1)
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
                demon_test = (
                    ((0, 9), king_demon), ((2, 9), x1),
                    ((3, 8), king_demon))
                acid_test = (
                    ((0, 8), acid), ((0, 9), solid),
                    ((4, 8), acid), ((4, 9), chest),
                    ((8, 8), acid), ((8, 9), adamant),)
                height_test = (
                    ((0, 0), x1), ((0, 1), x1), ((0, 2), x1), ((0, 3), x1),
                    ((0, 4), x1), ((0, 5), x1), ((0, 6), x1), ((0, 7), x1),
                    ((0, 8), x1), ((0, 9), x1), ((0, 10), x1),)
                key_test = (
                    ((0, 10), chest), ((1, 10), key),
                    ((0, 9), mimic), ((0, 8), key),
                    ((8, 10), chest), ((7, 10), key),
                    ((0, 7), opened))
                super(_FieldPattern, self).__init__(
                    (9, 11+self.__MARGIN) if level == 0 else
                    (12, 11+self.__MARGIN) if level == 1 else
                    (9, 16+self.__MARGIN) if level == 2 else
                    (12, 16+self.__MARGIN),
                    t_spin_test if _const.PIECE_TEST == "T_SPIN_TEST" else
                    demon_test if _const.PIECE_TEST == "DEMON_TEST" else
                    acid_test if _const.PIECE_TEST == "ACID_TEST" else
                    height_test if _const.PIECE_TEST == "HEIGHT_TEST" else
                    key_test if _const.PIECE_TEST == "KEY_TEST" else
                    ())

            @property
            def drop_point(self):
                u"""ピース出現地点を取得。
                """
                return (self.width-3) >> 1, self.__MARGIN
        self.__is_completed = False
        self.__fall_progress = 0
        self.__pressure = 0
        self.__one_pieces = []
        self.__core = core
        self.__parent = parent
        self.__next = __next.Next(level.deck, self.__core.id)
        self.__hold = __hold.Hold(self.__core)
        _, rank = level.player
        pattern = _FieldPattern(rank)
        self.__drop_point = pattern.drop_point
        w, h = pattern.width, pattern.height
        self.__window = __window.Field(
            (0, 0, 9*_const.GRID, 11*_const.GRID),
            (w*_const.GRID, h*_const.GRID))
        __layouter.Game.set_field(self.__window, self.__core.id)
        self.__window.field = self.__field = _pieces.Field(pattern)
        self.__minimap = (
            __huds.Space((0, 0, w, h)) if _const.IS_SPACE_MINIMAP else
            __huds.Block((0, 0, w, h)))
        __layouter.Game.set_minimap(
            self.__minimap, self.__hold, self.__core.id)

    def vanish(self):
        u"""ゲーム終了時のフィールド消去。
        """
        self.__field.vanish()
        self.__piece.vanish()
        self.__window.ghost = None

    # ---- Piece ----
    def forward(self, time=1, level_up=True):
        u"""ピース進行。
        time回ピースを進める。
        """
        for _ in range(time):
            pattern = self.__next.forward(self.__parent.get_pattern(level_up))
        self.__piece = _pieces.Falling(pattern, self.__drop_point)
        self.__window.piece = self.__piece
        self.update_window()

    def skip(self):
        u"""ピーススキップ。
        """
        self.__piece.skip()
        self.__window.ghost = None
        if self.__core.thinker:
            self.__core.thinker.is_changed = True

    # ---- Falling ----
    def fall(self):
        u"""ピース落下処理。
        """
        if not _const.IS_FALL_STOP:
            if self.__fall_progress < _const.FRAME_RATE:
                self.__fall_progress += 1
            else:
                self.__core.input_command(_const.DOWN_COMMAND)
                self.__fall_progress = 0

    def clear_fall(self):
        u"""ファール進行を0に。
        """
        self.__fall_progress = 0

    # ---- Delete Line ----
    def extend_line(self, line):
        u"""消去したライン追加。
        """
        self.__one_pieces.extend(line)

    def clear_line(self):
        u"""消去ライン初期化。
        """
        self.__one_pieces = []

    # ---- Update ----
    def update_parameter(self):
        u"""ゲームパラメータの変動処理。
        """
        if not self.__is_completed:
            self.__parent.hardness_down()
            self.__parent.luck_up()
        else:
            self.__parent.hardness_up()
            self.__parent.luck_down()

    def update_window(self):
        u"""ウィンドウ、ミニマップを更新。
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
            self.__window.ghost = self.__piece.get_target(self.__field)
            self.__window.update_area()
            if _const.IS_WINDOW_TRANSPARENT:
                diff = self.__field.highest+self.__window.difference
                height = (
                    self.__field.height if
                    self.__field.height < diff else diff)
                alpha = int(height/float(self.__field.height)*0xFF)
                self.__window.image.set_alpha(
                    alpha if self.__WINDOW_MIN_ALPHA <
                    alpha else self.__WINDOW_MIN_ALPHA)
            else:
                self.__window.image.set_alpha(None)
        __update_minimap()
        __update_window()

    # ---- Property ----
    @property
    def window(self):
        u"""ブロックウィンドウ取得。
        """
        return self.__window

    @property
    def drop_point(self):
        u"""ピースの落下地点を取得。
        """
        return self.__drop_point

    @property
    def one_pieces(self):
        u"""消去したラインを取得。
        """
        return self.__one_pieces

    # ------ Piece ------
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

    # ------ State ------
    @property
    def has_item(self):
        u"""アイテム保有状態取得。
        """
        return self.__parent.has_item

    @property
    def has_joker(self):
        u"""ジョーカー保有状態取得。
        """
        return self.__parent.has_joker

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
