#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""creature.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

クリーチャーブロックモジュール。
"""
import utils.const as _const
import block as __block
import irregular as __irregular


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
        def __is_wall(cell):
            u"""cellが壁かどうか判定。
            """
            return cell is None or cell.is_block

        def __tire(cells):
            u"""周囲４マスが壁の場合、スライムを疲れさせる。
            """
            if all(__is_wall(cell) for cell in cells):
                return self.change("Tired", 0)
            return False
        top = self._get_top_cell()
        right = self._get_right_cell()
        bottom = self._get_bottom_cell()
        left = self._get_left_cell()
        if not __tire((top, right, bottom, left)):
            if (
                __is_wall(right) and __is_wall(bottom) and
                __is_wall(left) and not __is_wall(top)
            ):
                top.change(self.__class__.__name__)
            elif (
                __is_wall(top) and __is_wall(bottom) and
                __is_wall(left) and not __is_wall(right)
            ):
                right.change(self.__class__.__name__)
            elif (
                __is_wall(top) and __is_wall(right) and
                __is_wall(left) and not __is_wall(bottom)
            ):
                bottom.change(self.__class__.__name__)
            elif (
                __is_wall(top) and __is_wall(bottom) and
                __is_wall(right) and not __is_wall(left)
            ):
                left.change(self.__class__.__name__)


class _Reviver(object):
    u"""復活ブロック。
    """
    def _is_release(self):
        u"""上下左右どこかに空白が存在する場合に真。
        """
        for cell in self._get_surround(self._CROSS):
            if cell and cell.is_blank:
                return True
        return False


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
        self._surround_effect(
            self.__class__.__name__, "Water#"+_const.BASIC_NAMES, self._BELOW)


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


class Mover(object):
    u"""移動ブロック。
    """
    def _get_dest_cells(self):
        u"""移動ブロック用。
        """
        right, left = self._get_right_cell(), self._get_left_cell()
        return tuple(
            (self._get_bottom_cell(),) +
            ((right, left) if self.is_leftside() else (left, right)) +
            (self._get_top_cell(),))

    def _migration(self, cell, targets, footprint="Blank", replace=""):
        u"""ブロック転移を表現。
        """
        if cell and cell._is_target(targets) and cell.change(
            replace if replace else self.__class__.__name__, self._state
        ):
            return self.change(footprint)
        return False


class _Demon(__irregular.Invincible, Mover):
    u"""周囲のブロックを捕食する悪魔。
    """
    _EFFECT = "blue_fire"
    _FRAME_NUM = 4
    _MALIGNANCY = _const.HIGH_MALIGNANCY

    def _destroy(self, _table, flag):
        u"""強制クラックの場合に破壊される。
        """
        super(_Demon, self)._destroy(_table, flag)
        if self._is_exorcist_flag(flag) and not isinstance(self, Maxwell):
            self._is_destroyed = True

    def _get_rank(self):
        u"""悪魔ランク取得。
        """
        return (
            3 if isinstance(self, Maxwell) else
            2 if isinstance(self, ArchDemon) else
            1 if isinstance(self, BlockDemon) else 0)

    def effect(self):
        u"""シャードやブロックを捕食する。
        シャードを捕食した場合、上位デーモンに進化。
        """
        cells = self._get_dest_cells()
        if hasattr(self, "_SUPERIOR"):
            for cell in cells:
                if self._migration(
                    cell, _const.SHARD_NAMES, replace=self._SUPERIOR
                ):
                    return None
        for cell in cells:
            if self._migration(cell, self._FAVO):
                return None
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
    u"""最上級悪魔。
    全ての基本ブロックを食べる。
    """
    _FAVO = _const.BASIC_NAMES+"#"+_const.SLIME_NAMES
    _IMAGES = "arch_demon"


class Maxwell(_Demon):
    u"""マクスウェルの悪魔。
    スターを生成する。
    """
    _FAVO = _const.BASIC_NAMES
    _IMAGES = "maxwell"
    _MALIGNANCY = 0
    _TARGET_COLOR = "white"

    def effect(self):
        u"""ブロックをスターに変えながら移動する。
        """
        self._state = (self._state+1) % 7
        for cell in self._get_dest_cells():
            if self._migration(
                cell, _const.BASIC_NAMES+"#"+_const.SLIME_NAMES,
                footprint=(
                    "Sun", "Jupiter", "Mars", "Saturn", "Venus", "Mercury",
                    "Moon")[self._state]
            ):
                break
        else:
            self.change("Gargoyle", self._get_rank())


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
        EAT_NAMES = _const.SLIME_NAMES+"#"+_const.SHARD_NAMES
        targets = (
            "Normal#"+EAT_NAMES,
            "Normal#Solid#"+EAT_NAMES,
            _const.BASIC_NAMES+"#"+EAT_NAMES,
            _const.BASIC_NAMES+"#"+_const.SLIME_NAMES)[self._state]
        for cell in self._get_surround(self._CROSS):
            if cell and not cell.is_large and cell._is_target(targets):
                return True
        return False

    def effect(self):
        u"""復活処理。
        """
        if self._is_release():
            self.change((
                "BlockEater", "BlockDemon", "ArchDemon", "Maxwell"
            )[self._state])


class _Ghost(__irregular.Invincible, Mover):
    u"""空白を移動するゴーストブロック。
    """
    __INTERVAL = 4
    _FRAME_NUM = 4
    _MALIGNANCY = _const.HIGH_MALIGNANCY

    def _destroy(self, _table, flag):
        u"""強制クラックの場合に破壊される。
        """
        super(_Ghost, self)._destroy(_table, flag)
        if self._is_exorcist_flag(flag):
            self._is_destroyed = True

    def effect(self):
        u"""フィールドを移動する。
        """
        for cell in self._get_dest_cells():
            if self._migration(
                cell, "Blank", footprint=self._FOOTPRINT if
                hasattr(self, "_FOOTPRINT") else "Blank"
            ):
                break
        else:
            self.change("RIP", self.__rank)

    @property
    def __rank(self):
        u"""幽霊ランク取得。
        """
        return (
            2 if isinstance(self, PoisonGhost) else
            1 if isinstance(self, FireGhost) else 0)


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


class RIP(__block.Block, _Reviver):
    u"""ゴーストの墓。
    """
    _IMAGES = "rip"
    _SCORE = _const.SINGLE_SCORE
    _MALIGNANCY = _const.MID_MALIGNANCY

    def effect(self):
        u"""復活処理。
        """
        if self._is_release():
            self.change(("IceGhost", "FireGhost", "PoisonGhost")[self._state])
