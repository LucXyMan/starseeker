#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""irregular.py

Copyright (c) 2019 Yukio Kuro
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
    _SCORE = _const.QUARTER_SCORE

    @property
    def is_fragile(self):
        u"""壊れ物判定。
        """
        return True


class Water(__block.Block):
    u"""ウォーターブロック。
    """
    _EFFECT = "blue_bubble"
    _FRAME = 4
    _IMAGES = "water"
    _MALIGNANCY = 0
    _SCORE = _const.QUARTER_SCORE
    _SMALL_IMAGE = "!_8"
    _TARGET_COLOR = "white"

    def effect(self):
        u"""水浸しに。
        火スターと力の欠片をウォーターに変える。
        """
        target = self.name+"##Blank#Mars#Power"
        if all(
            not cell.is_target(self.name) for cell in self._get_bottom()
        ) and not self._affect(target, 0b0100):
            self._affect(target, 0b1010)


class Poison(__block.Block):
    u"""ポイズンブロック。
    消去するとスター減少。
    """
    __LIMIT = 4
    _EFFECT = "purple_bubble"
    _FRAME = 4
    _IMAGES = "poison"
    _MALIGNANCY = _const.MID_MALIGNANCY
    _SCORE = _const.SINGLE_SCORE

    def effect(self):
        u"""周囲のブロックへの効果。
        """
        self._state += 1
        if self.__LIMIT <= self.state:
            self.change("Ruined")
        else:
            self._affect(
                self.name+"##Normal#Jupiter#Mars#Venus#Mercury#Moon#Sun",
                self._BELOW)

    @property
    def star_type(self):
        u"""スター種類。
        """
        return _const.NUMBER_OF_STAR


# ---- Invincible ----
class Invincible(__block.Block):
    u"""無敵ブロック。
    """
    _SCORE = 0

    def crack(self, flag=0):
        u"""強制クラックの場合に破壊される。
        """
        if self._is_force_flag(flag):
            self._is_destroyed = True

    @property
    def is_invincible(self):
        u"""無敵判定。
        """
        return True


class Magma(Invincible):
    u"""マグマブロック。
    """
    _EFFECT = "red_fire"
    _FRAME = 4
    _IMAGES = "magma"
    _MALIGNANCY = _const.MID_MALIGNANCY
    _SCORE = _const.DOUBLE_SCORE

    def crack(self, flag=0):
        u"""クラック処理。
        """
        super(Magma, self).crack(flag)
        if self._is_fire_eater_flag(flag):
            self._is_destroyed = True

    def effect(self):
        u"""周囲のブロックを溶岩に変える。
        """
        def __is_cooldown():
            u"""冷却される場合に真。
            """
            return any(
                cell.is_blank or isinstance(cell, Water) for
                cell in self._get_around(self._CROSS))
        if __is_cooldown():
            self.change("Solid")
        self._affect("Magma##Normal#Matango#"+_const.CARD_NAMES, self._BELOW)


class Ice(Invincible):
    u"""アイスブロック。
    周囲のブロックを凍結する。
    """
    _EFFECT = "blue_light"
    _FRAME = 16
    __STOP_TIME = (_FRAME >> 1)+(_FRAME >> 2)
    _IMAGES = "ice"
    _MALIGNANCY = _const.MID_MALIGNANCY
    _SCORE = _const.DOUBLE_SCORE

    # ---- Completion ----
    def crack(self, flag=0):
        u"""クラック処理。
        """
        super(Ice, self).crack(flag)
        if self._is_ice_picker_flag(flag):
            self._is_destroyed = True

    # ---- Effect ----
    def effect(self):
        u"""ブロック効果。
        状況によって周囲のブロックを凍結。
        """
        def __is_lower():
            u"""このブロックより上にブロックがあれば真。
            """
            for y in range(self._point.top-1, -1, -1):
                if self._get((self._point.x, y)).is_block:
                    return True
            return False

        def __is_heated():
            u"""周囲にマグマがあれば真。
            """
            return any(
                isinstance(cell, Magma) for
                cell in self._get_around(self._CROSS))
        if not __is_lower() or __is_heated():
            self.change("Water")
        else:
            self._affect(
                self.name+"##Normal#Solid#Jupiter#Mars#Saturn#Venus#Moon#Sun",
                self._BELOW)

    # ---- Property ----
    @property
    def _current_image(self):
        u"""現在画像取得。
        """
        import utils.counter as __counter
        frame = __counter.get_frame(self._FRAME)
        return self._scaled_images[
            0 if frame <= self.__STOP_TIME else frame-self.__STOP_TIME]


class Acid(Invincible):
    u"""アシッドブロック。
    下方向のブロックを溶かす。
    """
    _EFFECT = "yellow_bubble"
    _FRAME = 4
    _IMAGES = "acid"
    _MALIGNANCY = _const.MID_MALIGNANCY
    _SCORE = _const.DOUBLE_SCORE

    def crack(self, flag=0):
        u"""クラック処理。
        """
        super(Acid, self).crack(flag)
        if self._is_acid_eraser_flag(flag):
            self._is_destroyed = True

    def effect(self):
        u"""アイテムを浸食。
        """
        old = "Normal#Solid#"+_const.ITEM_NAMES
        ruined = "Ruined"
        if self._piece.height <= self._point.bottom:
            self.change(ruined)
        elif not self._affect(self.name+"##Blank", 0b0100) and all(
            not cell.is_target(self.name+"#"+ruined) for
            cell in self._get_bottom()
        ) and not self._affect(ruined+"##"+old, 0b0100):
            self._affect(self.name+"##Blank#"+old, 0b1010)


# ---- Link ----
class _Link(__block.Block):
    u"""リンクブロック。
    他のリンクブロックとリンクする。
    """
    def link(self):
        u"""リンク設定。
        """
        link = 0
        left, top = self._point.topleft
        for i, cell in enumerate((
            self._get((left, top-1)), self._get((left+1, top)),
            self._get((left, top+1)), self._get((left-1, top))
        )):
            if cell and isinstance(cell, self.__class__):
                link += 1 << i
        self._link = link

    # ---- Completion ----
    def calculate(self, fall=-1):
        u"""ブロック落下計算。
        """
        super(_Link, self).calculate(fall)
        next_ = (
            self._fall+self._point.height if self._is_destroyed else
            self._fall)
        for block in self._linked:
            fall = block._fall
            if next_ < fall or fall == -1:
                block.calculate(next_)

    # ---- Property ----
    @property
    def _linked(self):
        u"""周囲のリンクブロック取得。
        """
        return tuple(cell for is_link_state, cell in zip(
            self._link_state, self._get_around(self._CROSS)
        ) if is_link_state and isinstance(cell, self.__class__))

    @property
    def _link_state(self):
        u"""周囲のリンク状態取得。
        """
        return tuple(bool(self._link & (1 << i)) for i in range(4))

    @property
    def _link(self):
        u"""リンク状態取得。
        """
        return (self._state & 0xFF00) >> 8

    @_link.setter
    def _link(self, value):
        u"""リンク状態設定。
        """
        self._state = value << 8 | self._progress

    @property
    def _progress(self):
        u"""進行状態取得。
        """
        return self._state & 0x00FF

    @_progress.setter
    def _progress(self, value):
        u"""進行状態設定。
        """
        self._state = self._link << 8 | value

    @property
    def _current_image(self):
        u"""現在画像取得。
        """
        return self._scaled_images[self._link]


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
        u"""クラック処理。
        """
        super(Chocolate, self).crack(flag)
        for block in self._linked:
            if not block._is_destroyed:
                block.crack(flag)


class Stone(Invincible, _Link):
    u"""石化ブロック。
    他の石化ブロックとリンクする。
    """
    __LIMIT = 32
    _IMAGES = "stone"
    _MALIGNANCY = _const.MID_MALIGNANCY
    _SCORE = _const.DOUBLE_SCORE

    def crack(self, flag=0):
        u"""クラック処理。
        """
        super(Stone, self).crack(flag)
        if self._is_stone_breaker_flag(flag):
            self._is_destroyed = True

    def effect(self):
        u"""リンク状況に合わせて値を進行させる。
        """
        steps = {0: 8, 1: 4, 2: 2, 3: 1, 4: 0}
        self._progress += steps[sum(self._link_state)]
        if self.__LIMIT <= self._progress:
            self.change("Ruined")
