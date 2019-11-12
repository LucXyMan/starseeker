#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""monster.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

モンスターブロックモジュール。
"""
import random as _random
import utils.const as _const
import block as __block
import irregular as __irregular


# ---- Interface ----
class Mover(object):
    u"""移動ブロック。
    """
    def _move(self, targets, footprint="Blank", replace=""):
        u"""移動処理。
        """
        def __get_dest_cells():
            u"""移動先セル取得。
            """
            right, left = self._get_right(), self._get_left()
            return self._get_bottom()+(
                right+left if self._is_leftside() else
                left+right)+self._get_top()
        for cell in __get_dest_cells():
            if cell.is_target(targets) and cell.change(
                replace if replace else self.name, self._state
            ):
                return self.change(footprint)
        return False


class _Reviver(object):
    u"""復活ブロック。
    """
    def _is_release(self):
        u"""上下左右どこかに空白が存在する場合に真。
        """
        for cell in self._get_around(self._CROSS):
            if cell and cell.is_blank:
                return True
        return False


# ---- Slime ----
class Slime(__block.Block):
    u"""スライムブロック。
    周囲の空白に増殖する。
    """
    _SCORE = _const.QUARTER_SCORE
    _IMAGES = "slime"
    _SMALL_IMAGE = "!_8"
    _FRAME_NUM = 4
    _TARGET_COLOR = "white"
    _MALIGNANCY = 0

    def effect(self):
        u"""周囲の状況によって増殖。
        """
        def __is_wall(cells):
            u"""cellsが壁かどうか判定。
            """
            return all(cell.is_block for cell in cells)

        def __multiply(cells):
            u"""増殖処理。
            空白を変化させる。
            """
            for cell in cells:
                if cell.is_blank:
                    cell.change(self.name)
        top = self._get_top()
        right = self._get_right()
        bottom = self._get_bottom()
        left = self._get_left()
        around = (
            __is_wall(top) |
            __is_wall(right) << 1 |
            __is_wall(bottom) << 2 |
            __is_wall(left) << 3)
        if around & 0b1111 == 0b1111:
            self.change("Tired")
        elif around & 0b1110 == 0b1110:
            __multiply(top)
        elif around & 0b1101 == 0b1101:
            __multiply(right)
        elif around & 0b1011 == 0b1011:
            __multiply(bottom)
        elif around & 0b0111 == 0b0111:
            __multiply(left)


class Tired(__block.Block, _Reviver):
    u"""疲れスライムブロック。
    """
    _SCORE = _const.QUARTER_SCORE
    _IMAGES = "tired"
    _TARGET_COLOR = "white"

    def effect(self):
        u"""復活処理。
        """
        if self._is_release():
            self.change("Slime")


# ---- Matango ----
class Matango(__block.Block):
    u"""きのこブロック。
    相手のチャージを妨害する無得点ブロック。
    """
    _IMAGES = "matango"
    _FRAME_NUM = 4
    _MALIGNANCY = _const.MID_MALIGNANCY

    def effect(self):
        u"""基本ブロック・ウォーターを媒介して増殖。
        """
        self._affect(self.name+"##Water#"+_const.BASIC_NAMES, self._BELOW)


class LargeMatango(__block.Block):
    u"""巨大きのこブロック。
    スターを減少させる。
    """
    _IMAGES = "large_matango"
    _FRAME_NUM = 4
    _MALIGNANCY = _const.MID_MALIGNANCY

    @property
    def star_type(self):
        u"""スター種類。
        """
        return -1


# ---- Demon ----
class _Demon(__irregular.Invincible, Mover):
    u"""周囲のブロックを捕食する悪魔。
    """
    _EFFECT = "blue_fire"
    _FRAME_NUM = 4
    _MALIGNANCY = _const.HIGH_MALIGNANCY

    def clack(self, flag):
        u"""強制クラックの場合に破壊される。
        """
        super(_Demon, self).clack(flag)
        if self._is_exorcist_flag(flag) and not isinstance(self, Maxwell):
            self._is_destroyed = True

    def _get_rank(self):
        u"""悪魔ランク取得。
        """
        return (
            3 if isinstance(self, Maxwell) else
            2 if isinstance(self, ArchDemon) else
            1 if isinstance(self, BlockDemon) else
            0)

    def effect(self):
        u"""シャードやブロックを捕食する。
        シャードを捕食した場合、上位デーモンに進化。
        """
        if (not hasattr(self, "_SUPERIOR") or not self._move(
            _const.SHARD_NAMES, replace=self._SUPERIOR
        )) and not self._move(self._FAVO):
            self.change("Gargoyle", self._get_rank())


class BlockEater(_Demon):
    u"""ブロックを食べる生物。
    Normalを食べる。
    """
    _FAVO = "Normal"+"#"+_const.SLIME_NAMES
    _IMAGES = "eater"
    _SUPERIOR = "BlockDemon"


class BlockDemon(_Demon):
    u"""ブロックを食べる悪魔。
    NormalとSolidを食べる。
    """
    _FAVO = "Normal#Solid"+"#"+_const.SLIME_NAMES
    _IMAGES = "demon"
    _SUPERIOR = "ArchDemon"


class ArchDemon(_Demon):
    u"""最上級悪魔ブロック。
    全ての基本ブロックを食べる。
    """
    _FAVO = _const.BASIC_NAMES+"#"+_const.SLIME_NAMES+"#"+_const.SHARD_NAMES
    _IMAGES = "arch_demon"


class Maxwell(_Demon):
    u"""マクスウェルの悪魔ブロック。
    スターを生成する。
    """
    _FAVO = _const.BASIC_NAMES
    _IMAGES = "maxwell"
    _MALIGNANCY = 0
    _TARGET_COLOR = "white"
    __box = []

    @classmethod
    def __get_star(cls):
        u"""スター用のくじ引き。
        """
        if not cls.__box:
            cls.__box = range(7)
            _random.shuffle(cls.__box)
        return cls.__box.pop()

    def __init__(self, point, state, is_virtual):
        u"""コンストラクタ。
        """
        state = (
            0 if is_virtual else self.__get_star() if
            state == -1 else state)
        super(Maxwell, self).__init__(point, state, is_virtual)

    def effect(self):
        u"""ブロックをスターに変えながら移動する。
        """
        self._state = (self._state+1) % 7
        stars = _const.STAR_NAMES.split("#")
        if not self._move(
            _const.BASIC_NAMES+"#"+_const.SLIME_NAMES,
            footprint=stars[self._state]
        ):
            self.change("Gargoyle", self._get_rank())


class KingDemon(__irregular.Invincible):
    u"""悪魔王ブロック。
    ブロックとアイテムを食べる。
    """
    __ENDURANCE = 8
    _FRAME_NUM = 4
    _IMAGES = "king_demon"
    _MALIGNANCY = _const.HIGH_MALIGNANCY

    def effect(self):
        u"""ブロックを食べながら移動する。
        """
        def __move(direction):
            u"""移動処理。
            """
            cells, point = (
                (self._get_top(), (0, -1)) if direction == 0 else
                (self._get_right(), (1, 0)) if direction == 1 else
                (self._get_bottom(), (0, 1)) if direction == 2 else
                (self._get_left(), (-1, 0)))
            if cells:
                is_changeable = all(cell.is_changeable for cell in cells)
                names = (
                    _const.BASIC_NAMES+"#"+_const.ITEM_NAMES+"#" +
                    _const.SLIME_NAMES)
                is_target = is_impurities = False
                for cell in cells:
                    if cell.is_target(names):
                        is_target = True
                    elif cell.is_block:
                        is_impurities = True
                if is_changeable and is_target and not is_impurities:
                    for cell in cells:
                        self._piece.remove(cell)
                    self._piece.remove(self)
                    x, y = point
                    self._piece.add(self.__class__((
                        self._point.x+x, self._point.y+y, 2, 2
                    ), self._state, self._is_virtual))
                    return True
            return False
        for direction in (2, 1, 3, 0) if self._is_leftside() else (2, 3, 1, 0):
            if __move(direction):
                return None
        else:
            self._state += 1
            if self.__ENDURANCE <= self._state:
                self._piece.remove(self)
                for x in range(self._point.left, self._point.right):
                    for y in range(self._point.top, self._point.bottom):
                        self._get((x, y)).change("BlockEater")


class Gargoyle(__block.Block, _Reviver):
    u"""悪魔像ブロック。
    周囲のブロックに反応する。
    """
    _IMAGES = "gargoyle"
    _SCORE = _const.SINGLE_SCORE
    _MALIGNANCY = _const.MID_MALIGNANCY

    def _is_release(self):
        u"""上下左右どこかに食べられるブロックが存在する場合に真。
        """
        EAT = _const.SLIME_NAMES+"#"+_const.SHARD_NAMES
        targets = (
            "Normal#"+EAT,
            "Normal#Solid#"+EAT,
            _const.BASIC_NAMES+"#"+EAT,
            _const.BASIC_NAMES+"#"+_const.SLIME_NAMES)
        target = targets[self._state]
        return any(
            not cell.is_large and cell.is_target(target) for
            cell in self._get_around(self._CROSS))

    def effect(self):
        u"""復活処理。
        """
        if self._is_release():
            demons = "BlockEater", "BlockDemon", "ArchDemon", "Maxwell"
            self.change(demons[self._state])


# ---- Ghost ----
class _Ghost(__irregular.Invincible, Mover):
    u"""ゴーストブロック。
    """
    _FRAME_NUM = 4
    _MALIGNANCY = _const.HIGH_MALIGNANCY

    def clack(self, flag):
        u"""強制クラックの場合に破壊される。
        """
        super(_Ghost, self).clack(flag)
        if self._is_exorcist_flag(flag):
            self._is_destroyed = True

    def effect(self):
        u"""フィールドを移動する。
        """
        def __get_rank():
            u"""幽霊ランク取得。
            """
            return (
                2 if isinstance(self, PoisonGhost) else
                1 if isinstance(self, FireGhost) else 0)
        if not self._move(
            "Blank", footprint=self._FOOTPRINT if
            hasattr(self, "_FOOTPRINT") else "Blank"
        ):
            self.change("RIP", __get_rank())


class FireGhost(_Ghost):
    u"""ファイアゴーストブロック。
    移動時にマグマを生成する。
    """
    _FOOTPRINT = "Magma"
    _IMAGES = "fire_ghost"


class IceGhost(_Ghost):
    u"""アイスゴーストブロック。
    移動時にアイスを生成する。
    """
    _FOOTPRINT = "Ice"
    _IMAGES = "ice_ghost"


class PoisonGhost(_Ghost):
    u"""ポイズンゴーストブロック。
    移動時にポイズンを生成する。
    """
    _FOOTPRINT = "Poison"
    _IMAGES = "poison_ghost"


class RIP(__irregular.Invincible, _Reviver):
    u"""墓ブロック。
    """
    _IMAGES = "rip"
    _SCORE = _const.SINGLE_SCORE
    _MALIGNANCY = _const.MID_MALIGNANCY

    def clack(self, flag):
        u"""強制クラックの場合に破壊される。
        """
        super(RIP, self).clack(flag)
        if self._is_exorcist_flag(flag):
            self._is_destroyed = True

    def effect(self):
        u"""復活処理。
        フィールド底辺に到達すると消滅する。
        """
        if self._piece.height <= self._point.bottom:
            self.change("Ruined")
        elif self._is_release():
            names = "IceGhost", "FireGhost", "PoisonGhost"
            self.change(names[self._state])
