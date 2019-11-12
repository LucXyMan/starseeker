#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""cell.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

セルモジュール。
"""
import pygame as _pygame
import utils.const as _const


class Cell(_pygame.sprite.Sprite):
    u"""セル。
    全てのブロック・空白の基本形。
    """
    _CROSS = 1, 0, 1, 0, 1, 0, 1, 0
    _ALL = 1, 1, 1, 1, 1, 1, 1, 1
    _BELOW = 0, 0, 1, 0, 1, 0, 1, 0
    _HORIZONTAL = 0, 0, 1, 0, 0, 0, 1, 0
    _SCORE = 0
    _collections = {}

    @classmethod
    def get_collection(cls, key):
        u"""コレクション取得。
        """
        return cls._collections[key]

    @classmethod
    def add_collection(cls, value):
        u"""コレクション追加。
        """
        cls._collections.setdefault(value.__name__, value)

    @classmethod
    def get_score(cls):
        u"""スコア取得。
        """
        return cls._SCORE

    def __init__(self, point, state, is_virtual):
        u"""コンストラクタ。
        """
        super(Cell, self).__init__()
        self._point = _pygame.Rect(*point)
        self._piece = None
        self._state = state
        self._is_destroyed = False
        self.__is_virtual = bool(is_virtual)
        self._fall = -1
        self._to_block = ""
        self._to_state = -1
        self._edges = []

    def __repr__(self):
        u"""文字列表現取得。
        """
        return u"<type: {name}, size: {point}, state: {state}>".format(
            name=self.__class__.__name__, point=self._point.size,
            state=self._state)

    def _get_cell(self, point):
        u"""セルを取得。
        """
        x, y = point
        if (
            (x < 0 or self._piece.width <= x) or
            (y < 0 or self._piece.height <= y)
        ):
            return None
        return self._piece[y][x]

    def _destroy(self, _table, _flag):
        u"""破壊処理。
        """
        self._is_destroyed = True

    def _is_target(self, targets):
        u"""対象セル判定。
        """
        return isinstance(self, tuple(
            self._collections[name] for name in targets.split("#")))

    def _is_force_flag(self, flag):
        u"""強制クラックフラグ判定。
        """
        return _const.FORCE_CRACK & flag

    def _is_unlock_flag(self, flag):
        u"""アンロックフラグ判定。
        """
        return _const.UNLOCK_CRACK & flag

    def _is_treasure_flag(self, flag):
        u"""宝箱フラグ判定。
        """
        return _const.TREASURE_CRACK & flag

    def _is_fire_eater_flag(self, flag):
        u"""ファイアイーターフラグ判定。
        """
        return _const.FIRE_EATER_CRACK & flag

    def _is_ice_picker_flag(self, flag):
        u"""アイスピッカーフラグ判定。
        """
        return _const.ICE_PICKER_CRACK & flag

    def _is_acid_eraser_flag(self, flag):
        u"""アシッドイレーザーフラグ判定。
        """
        return _const.ACID_ERASER_CRACK & flag

    def _is_stone_breaker_flag(self, flag):
        u"""ストーンブレーカークラックの場合に真。
        """
        return _const.STONE_BREAKER_CRACK & flag

    def _is_power_flag(self, flag):
        u"""パワークラックフラグ判定。
        """
        return _const.POWER_CRACK & flag

    def _is_exorcist_flag(self, flag):
        u"""エクソシストフラグ判定。
        """
        return _const.EXORCIST_CRACK & flag

    def effect(self):
        u"""セル効果。
        """

    def change(self, name="", state=-1):
        u"""セル変更。
        変化後セルを設定。
        """
        if self.is_changeable:
            self._to_block = name
            if state != -1:
                self._to_state = state
            return True
        return False

    def generation(self):
        u"""セル世代交代。
        セル変化、セル削除など。
        """
        if self._to_block != "":
            if self._to_block == "Blank":
                self._piece.remove(self)
            else:
                block = self._collections[self._to_block](
                    self._point, self._to_state if self._to_state != -1 else 0,
                    self.__is_virtual)
                block._edges = self._edges
                block.update()
                self._piece.remove(self)
                self._piece.add(block)

    def is_collide(self, field):
        u"""セルとフィールドセルの衝突判定。
        """
        left, top = self._point.topleft
        for y in range(top, top+self._point.h):
            for x in range(left, left+self._point.w):
                if field[y][x].is_block:
                    return True
        return False

    def is_leftside(self):
        u"""自身が左側に存在するか判定。
        """
        return self.point.x < self._piece.width >> 1

    def crack(self, flag=0):
        u"""クラック。
        """
        self._destroy(self._piece, flag)

    def move_calc(self, fall=-1):
        u"""落下計算。
        """
        def __get_aboves():
            u"""自身の上にあるセル取得。
            """
            def __get_above():
                u"""(x, 自身のtop)から上のセル取得。
                """
                for y in range(self._point.top-1, -1, -1):
                    result = self._get_cell((x, y))
                    if result:
                        return result
                return None
            result = []
            for x in range(
                self._point.left, self._point.left+self._point.width
            ):
                block = __get_above()
                if block:
                    result.append(block)
            return result
        self._fall = 0 if fall == -1 else fall
        next_ = (
            self._fall+self._point.height if self._is_destroyed else
            self._fall)
        for above in __get_aboves():
            fall = above._fall
            if next_ < fall or fall == -1:
                above.move_calc(next_)

    def remove(self):
        u"""セル除去。
        """
        if self._is_destroyed:
            self._piece.remove(self)

    def drop_down(self):
        u"""セル落下。
        """
        table = self._piece.table
        if 0 < self._fall:
            table.remove(self)
            self._point.move_ip(0, self._fall)
            table.write(self)
        self._fall = -1

    def shift(self, vector):
        u"""セル押上。
        """
        table = self._piece.table
        table.remove(self)
        self._point.move_ip(vector)
        if 0 <= self._point.top:
            table.write(self)

    @property
    def is_changeable(self):
        u"""自身の変更可能判定。
        """
        if (
            self._to_block == "" and self._to_state == -1 and
            not self.is_large and not self.is_destroyed
        ):
            return True
        return False

    @property
    def is_block(self):
        u"""ブロック判定。
        """
        return False

    @property
    def is_blank(self):
        u"""空白判定。
        """
        return False

    @property
    def is_space(self):
        u"""空白のスペース判定
        """
        return self.is_blank and self._state == 1

    @property
    def is_hole(self):
        u"""空白のホール判定。
        """
        return self.is_blank and self._state == 2

    @property
    def is_adjacent(self):
        u"""空白の隣接スペース判定。
        """
        return self.is_blank and self._state == 3

    @property
    def is_destroyed(self):
        u"""破壊判定取得。
        """
        return self._is_destroyed

    @is_destroyed.setter
    def is_destroyed(self, value):
        u"""破壊判定設定。
        """
        self._is_destroyed = bool(value)

    @property
    def is_large(self):
        u"""巨大判定。
        """
        return self._point.size != (1, 1)

    @property
    def is_invincible(self):
        u"""無敵判定。
        """
        return False

    @property
    def is_fragile(self):
        u"""壊れ物判定。
        """
        return False

    @property
    def is_opened(self):
        u"""空箱判定。
        """
        return False

    @property
    def is_key(self):
        u"""鍵判定。
        """
        return False

    @property
    def is_arcanum(self):
        u"""アルカナ判定。
        """
        return False

    @property
    def is_locked(self):
        u"""鍵付き宝箱・ミミック判定。
        """
        return False

    @property
    def is_mimic(self):
        u"""ミミック判定。
        """
        return False

    @property
    def point(self):
        u"""ポイント取得。
        位置と大きさを表す。
        """
        return self._point

    @property
    def height(self):
        u"""セルの高さ取得。
        """
        _, y, _, _ = self._point
        return y

    @property
    def piece(self):
        u"""所属先ピース取得。
        """
        return self._piece

    @piece.setter
    def piece(self, value):
        u"""所属先ピース設定。
        """
        self._piece = value

    @property
    def state(self):
        u"""状態取得。
        """
        return self._state

    @state.setter
    def state(self, value):
        u"""状態設定。
        """
        self._state = int(value)

    @property
    def name(self):
        u"""名前取得。
        """
        return self.__class__.__name__

    @property
    def star_type(self):
        u"""スター種類取得。
        """
        return 0

    @property
    def shard_type(self):
        u"""シャード種類取得。
        """
        return 0

    @property
    def treasure_rank(self):
        u"""宝ランク取得。
        """
        return 0


get = Cell.get_collection
