#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""irregular.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

変則ブロックモジュール。
"""
import utils.const as _const
import block as __block


class Ruined(__block.Block):
    u"""破壊されたブロック。
    """
    _EFFECT = "white_smoke"
    _IMAGES = "ruin"

    @property
    def is_fragile(self):
        u"""壊れ物判定。
        """
        return True


class Water(__block.Block):
    u"""ウォーターブロック。
    """
    _EFFECT = "blue_bubble"
    _FRAME_NUM = 4
    _IMAGES = "water"
    _MALIGNANCY = 0
    _SCORE = _const.QUARTER_SCORE
    _SMALL_IMAGE = "!_8"
    _TARGET_COLOR = "white"

    def effect(self):
        u"""水浸しに。
        火スターと力の欠片をウォーターに変える。
        """
        right = self._get_right_cell()
        bottom = self._get_bottom_cell()
        left = self._get_left_cell()
        new = self.__class__.__name__
        if bottom and bottom.is_blank:
            bottom.change(new)
        elif not isinstance(bottom, self.__class__):
            if right and right.is_blank:
                right.change(new)
            if left and left.is_blank:
                left.change(new)
        self._surround_effect(
            self.__class__.__name__, "Mars#Power", self._BELOW)


class Poison(__block.Block):
    u"""ポイズンブロック。
    消去するとスターを減少させる。
    """
    __LIMIT = 2
    _EFFECT = "purple_bubble"
    _FRAME_NUM = 4
    _IMAGES = "poison"
    _MALIGNANCY = _const.MID_MALIGNANCY
    _SCORE = _const.SINGLE_SCORE

    def effect(self):
        u"""周囲のブロックへの効果。
        """
        self._state += 1
        if self.__LIMIT <= self.state:
            self.change("Ruined")
        self._surround_effect(
            self.__class__.__name__,
            "Normal#Jupiter#Mars#Venus#Mercury#Moon#Sun", self._BELOW)

    @property
    def star_type(self):
        u"""スター種類。
        """
        return -1


class Invincible(__block.Block):
    u"""無敵ブロック。
    """
    _SCORE = 0

    def _destroy(self, _table, flag):
        u"""強制クラックの場合に破壊される。
        """
        if self._is_force_flag(flag):
            self._is_destroyed = True

    @property
    def is_invincible(self):
        u"""無敵判定。
        """
        return True


class _Link(__block.Block):
    u"""リンクブロック。
    他のリンクブロックとリンクする。
    """
    def _get_cells(self):
        u"""周囲のブロック取得。
        """
        return tuple(cell for is_linked, cell in zip(
            self._linked, self._get_surround(self._CROSS)) if is_linked and
            isinstance(cell, self.__class__))

    def move_calc(self, fall=-1):
        u"""ブロック落下計算。
        """
        super(_Link, self).move_calc(fall)
        next_ = (
            self._fall+self._point.height if self._is_destroyed else
            self._fall)
        for block in self._get_cells():
            fall = block._fall
            if next_ < fall or fall == -1:
                block.move_calc(next_)

    def set_link(self):
        u"""リンク設定。
        """
        link = 0
        left, top = self._point.topleft
        for i, cell in enumerate((
            self._get_cell((left, top-1)), self._get_cell((left+1, top)),
            self._get_cell((left, top+1)), self._get_cell((left-1, top))
        )):
            if cell and isinstance(cell, self.__class__):
                link += 1 << i
        self._link = link

    @property
    def _current_image(self):
        u"""現在画像取得。
        """
        return self._scaled_images[self._link]

    @property
    def _linked(self):
        u"""周囲のリンク状態取得。
        """
        return tuple(bool(self._link & (1 << i)) for i in range(4))

    @property
    def _progress(self):
        u"""進行状態取得。
        """
        return self._state & 0b0000000011111111

    @_progress.setter
    def _progress(self, value):
        u"""進行状態設定。
        """
        self._state = self._link << 8 | value

    @property
    def _link(self):
        u"""リンク状態取得。
        """
        return (self._state & 0b1111111100000000) >> 8

    @_link.setter
    def _link(self, value):
        u"""リンク状態設定。
        """
        self._state = value << 8 | self._progress


class Chocolate(_Link):
    u"""チョコレートブロック。
    他のチョコレートブロックとリンクする。
    通常ブロックより高得点。
    """
    _IMAGES = "chocolate"
    _SCORE = _const.DOUBLE_SCORE
    _SMALL_IMAGE = "!_8"
    _TARGET_COLOR = "white"

    def crack(self, flag=0):
        u"""ブロック破壊前処理。
        """
        super(Chocolate, self).crack(flag)
        for block in self._get_cells():
            if not block._is_destroyed:
                block.crack(flag)


class Stone(Invincible, _Link):
    u"""石化ブロック。
    他の石化ブロックとリンクする。
    """
    __LIMIT = 32
    _IMAGES = "stone"
    _MALIGNANCY = _const.MID_MALIGNANCY

    def _destroy(self, _field, flag):
        u"""ブロック破壊の処理。
        """
        super(Stone, self)._destroy(_field, flag)
        if self._is_stone_breaker_flag(flag):
            self._is_destroyed = True

    def effect(self):
        u"""リンク状況に合わせて値を進行させる。
        """
        self._progress += {0: 8, 1: 4, 2: 2, 3: 1, 4: 0}[sum(self._linked)]
        if self.__LIMIT <= self._progress:
            self.change("Ruined")


class Magma(Invincible):
    u"""マグマブロック。
    """
    _COOLDOWN = "Solid"
    _EFFECT = "red_fire"
    _FRAME_NUM = 4
    _IMAGES = "magma"
    _MALIGNANCY = _const.MID_MALIGNANCY

    def _destroy(self, _field, flag):
        u"""ブロック破壊処理。
        """
        super(Magma, self)._destroy(_field, flag)
        if self._is_fire_eater_flag(flag):
            self._is_destroyed = True

    def effect(self):
        u"""周囲のブロックを溶岩に変える。
        """
        def __is_cooldown():
            u"""冷却される場合に真。
            """
            return any(
                cell and cell.is_blank or isinstance(cell, Water) for
                cell in self._get_surround(self._CROSS))
        if __is_cooldown():
            self.change(self._COOLDOWN)
        self._surround_effect(
            "Magma", "Normal#Matango#"+_const.CARD_NAMES, self._BELOW)


class Ice(Invincible):
    u"""アイスブロック。
    周囲のブロックを凍結する。
    """
    _EFFECT = "blue_light"
    _FRAME_NUM = 16
    _IMAGES = "ice"
    _MALIGNANCY = _const.MID_MALIGNANCY

    def _destroy(self, _field, flag):
        u"""ブロック破壊の処理。
        """
        super(Ice, self)._destroy(_field, flag)
        if self._is_ice_picker_flag(flag):
            self._is_destroyed = True

    def effect(self):
        u"""ブロック効果。
        状況によって周囲のブロックを凍結。
        """
        def __is_lower():
            u"""このブロックより上にブロックがあれば真。
            """
            for y in range(self._point.top-1, -1, -1):
                if self._get_cell((self._point.x, y)).is_block:
                    return True
            return False

        def __is_heated():
            u"""周囲にマグマがあれば真。
            """
            return any(
                cell and isinstance(cell, Magma) for
                cell in self._get_surround(self._CROSS))
        if not __is_lower() or __is_heated():
            self.change("Water")
        else:
            self._surround_effect(
                self.__class__.__name__,
                "Normal#Solid#Jupiter#Mars#Saturn#Venus#Moon#Sun", self._BELOW)

    @property
    def _current_image(self):
        u"""現在画像取得。
        """
        import utils.counter as __counter
        static = 12
        frame = __counter.get_frame(self._FRAME_NUM)
        return self._scaled_images[
            0 if frame in range(static+1) else frame-static]


class Acid(Invincible):
    u"""アシッドブロック。
    下方向のブロックを溶かす。
    """
    _EFFECT = "yellow_bubble"
    _FRAME_NUM = 4
    _IMAGES = "acid"
    _MALIGNANCY = _const.MID_MALIGNANCY

    def _destroy(self, _field, flag):
        u"""ブロック破壊処理。
        """
        super(Acid, self)._destroy(_field, flag)
        if self._is_acid_eraser_flag(flag):
            self._is_destroyed = True

    def effect(self):
        u"""アイテムを浸食。
        """
        if self._piece.height-1 <= self._point.y:
            self.change("Ruined")
        else:
            bottom = self._get_bottom_cell()
            new = self.__class__.__name__
            if bottom and bottom.is_blank:
                bottom.change(new)
            else:
                self._surround_effect(new, (
                    _const.BASIC_NAMES+"#"+_const.STAR_NAMES+"#" +
                    _const.SHARD_NAMES+"#"+_const.KEY_NAMES+"#" +
                    _const.CARD_NAMES), (0, 0, 0, 0, 1, 0, 0, 0))
