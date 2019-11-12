#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""operate.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

操作ピースモジュール。
"""
import piece as _piece
import utils.const as _const


class _Operate(_piece.Piece):
    u"""操作ピース。
    """
    __slots__ = "_left", "_top"

    def __init__(self, pattern, topleft):
        u"""コンストラクタ。
        """
        super(_Operate, self).__init__(pattern)
        self._left, self._top = topleft

    @property
    def left(self):
        u"""左位置取得。
        """
        return self._left

    @left.setter
    def left(self, value):
        u"""左位置設定。
        """
        self.clear()
        self._left = value
        self._create()

    @property
    def top(self):
        u"""上位置取得。
        """
        return self._top

    @top.setter
    def top(self, value):
        u"""上位置設定。
        """
        self.clear()
        self._top = value
        self._create()


class Dropping(_Operate):
    u"""ドロップピース。
    """
    __slots__ = (
        "__ghost", "__is_commanded", "__is_rested", "__is_t_spin",
        "__is_virtual", "__rotated")
    __ROTATE_LIMIT = 16
    __BASE_ROTATION = ({
        _const.A0: (_const.RIGHT, _const.UP_RIGHT, (0, 2), (1, 2)),
        _const.A90: (_const.RIGHT, _const.DOWN_RIGHT, (0, -2), (1, -2)),
        _const.A180: (_const.LEFT, _const.UP_LEFT, (0, 2), (-1, 2)),
        _const.A270: (_const.LEFT, _const.DOWN_LEFT, (0, -2), (-1, -2))}, {
        _const.A0: (_const.LEFT, _const.UP_LEFT, (0, 2), (-1, 2)),
        _const.A90: (_const.RIGHT, _const.DOWN_RIGHT, (0, -2), (1, -2)),
        _const.A180: (_const.RIGHT, (_const.UP_RIGHT), (0, 2), (1, 2)),
        _const.A270: (_const.LEFT, _const.DOWN_LEFT, (0, -2), (-1, -2))})
    __I_ROTATION = ({
        _const.A0: (_const.LEFT, (2, 0), (-1, -2), (2, 1)),
        _const.A90: ((2, 0), _const.LEFT, (2, -1), (-1, 2)),
        _const.A180: (_const.RIGHT, (-2, 0), (1, -2), (-2, 1)),
        _const.A270: (_const.RIGHT, (-2, 0), (-2, 1), (1, -2))}, {
        _const.A0: ((-2, 0), _const.RIGHT, (-2, 1), (1, -2)),
        _const.A90: (_const.LEFT, (2, 0), (-1, -2), (2, 1)),
        _const.A180: ((2, 0), _const.LEFT, (2, -1), (-1, -2)),
        _const.A270: ((-2, 0), _const.RIGHT, (1, 2), (-2, -1))})

    def __init__(self, pattern, pos=(0, 0), is_virtual=False):
        u"""コンストラクタ。
        """
        super(Dropping, self).__init__(pattern, pos)
        self.__is_rested = False
        self.__rotated = 0
        self.__is_commanded = False
        self.__is_t_spin = False
        self.__is_virtual = is_virtual
        self._create()

    # ---- Create and Remove ----
    def _create(self):
        u"""ブロック作成。
        """
        for block in self._pattern.get_blocks(
            (self.left, self.top), self.__is_virtual
        ):
            block.piece = self
            self._blocks.append(block)

    def remove(self, block):
        u"""ブロック削除。
        """
        if block in self._blocks[:]:
            self._blocks.remove(block)

    # ---- Operation ----
    def clear(self):
        u"""ブロック消去。
        """
        self._blocks = []

    def stamp(self, field):
        u"""ピースをフィールドに転写。
        """
        if not self.__is_rested:
            field.add(*self._pattern.get_blocks(
                (self.left, self.top), self.__is_virtual))
            self.clear()

    def rest(self, field):
        u"""ピースの固着。
        """
        if not self.__is_rested:
            self.stamp(field)
            self.__is_rested = True

    def skip(self):
        u"""ピースを消去してレスト。
        フィールド変化魔術発動の際に使用。
        """
        self.clear()
        self.__is_rested = True

    # ---- Move ----
    def move(self, field, vector):
        u"""ピースの移動。
        """
        if not self.__is_rested:
            old_topleft = self.left, self.top
            self.clear()
            self._left += vector[0]
            self._top += vector[1]
            self._create()
            if self.is_collide(field):
                self.topleft = old_topleft
                return False
            else:
                self.__is_t_spin = False
                return True
        return False

    def slide(self, field, is_right):
        u"""左右移動。
        """
        self.__is_commanded = True
        return (
            self.move(field, _const.RIGHT) if is_right else
            self.move(field, _const.LEFT))

    def down(self, field):
        u"""下への移動。場合によって固着する。
        """
        self.__is_commanded = True
        moved = self.move(field, _const.DOWN)
        if not moved:
            self.rest(field)
        return moved

    def to_bottom(self, field):
        u"""ピースを最下に。
        """
        if not self.__is_rested:
            while True:
                if not self.move(field, _const.DOWN):
                    return

    def drop(self, field):
        u"""フィールド一番下に落下。
        コマンドを一度入力しなければ反応しない。
        """
        if self.__is_commanded:
            self.to_bottom(field)
            self.rest(field)
        else:
            self.__is_commanded = True

    # ---- Rotate ----
    def _rotate(self, field, clock_wise, time):
        u"""回数付き回転処理。
        """
        def __rotate(field, clock_wise):
            u"""回転処理。
            時計回転は+反時計回転は-。
            """
            def __get_rotate_rule(form, angle, clock_wise):
                u"""スーパーローテーションルール取得。
                """
                return (_const.CENTER,) + (
                    self.__I_ROTATION if form == "I" else
                    self.__BASE_ROTATION)[clock_wise][angle]
            if not self.__is_rested:
                self.__is_commanded = True
                old_angle = self.angle
                self._pattern.angle = self._pattern.angle + (
                    1 if clock_wise else -1)
                for topleft in __get_rotate_rule(
                        self._pattern.form, old_angle, clock_wise):
                    if self.move(field, topleft):
                        return True
                self.clear()
                self._pattern.rotate(old_angle)
                self._create()
            return False
        for _rotate in range(time % self.angles):
            if not __rotate(field, clock_wise):
                return False
        return True

    def rotate(self, field, clock_wise=True, time=1):
        u"""通常使用する回転処理。
        """
        import material.sound as __sound
        old_state = self.state
        if self.__is_rotatable:
            is_rotated = self._rotate(field, clock_wise, time)
            if is_rotated:
                self.__is_t_spin = True if (
                    self.is_t and self.is_three_corner(field) and
                    old_state != self.state) else False
            self.__rotated += 1
            return is_rotated
        else:
            __sound.SE.play("error")
            return False

    def test_rotate(self, field, clock_wise=True, time=1):
        u"""回転種類を判定するAI用回転処理。
        """
        old_state = self.state
        if (
            not self.__is_rotatable or
            not self._rotate(field, clock_wise, time)
        ):
            return _const.UNROTATABLE
        rotated = self.state
        if not self._rotate(field, not clock_wise, time):
            self.__rotated += 1
            return _const.ROTATABLE
        elif old_state.top < rotated.top:
            self.state = rotated
            self.__rotated += 1
            return _const.SHIFTED
        elif self.state == old_state:
            self.state = rotated
            self.__rotated += 1
            return _const.FLEXIBLE
        else:
            self.state = rotated
            self.__rotated += 1
            return _const.ROTATABLE

    # ---- Target ----
    def get_target(self, field):
        u"""ターゲットピース取得。
        """
        class _Target(_Operate):
            u"""ターゲットピース。
            """
            __slots__ = ()

            def __init__(self, pattern, pos):
                u"""コンストラクタ。
                """
                super(_Target, self).__init__(pattern.get_target(), pos)
                self._create()

            def _create(self):
                u"""ブロック作成。
                """
                for block in self._pattern.get_blocks((self.left, self.top)):
                    block.piece = self
                    self._blocks.append(block)
                for block in self._blocks:
                    block.set_piece_edge()
        if not self.__is_rested:
            old_topleft = self.topleft
            self.to_bottom(field)
            bottom = self.topleft
            self.topleft = old_topleft
            return _Target(self._pattern, bottom)

    # ---- Detect ----
    def is_collide(self, field):
        u"""接触テスト。
        """
        return field.is_outer(self) or field.is_collide(self)

    def is_three_corner(self, field):
        u"""角判定。
        角に3つ以上の壁が存在する場合に真。
        """
        def __is_wall(point):
            u"""壁判定。
            """
            cell = field.table.get_cell(point)
            return not cell or cell.is_block
        return 3 <= sum(1 for point in (
            (self._left, self._top),
            (self._left+self.width-1, self._top),
            (self._left, self._top+self.height-1),
            (self._left+self.width-1, self._top+self.height-1)
        ) if __is_wall(point))

    def is_flexible(self, field):
        u"""逆回転可能判定。
        """
        old_state = self.state
        for is_clock_wise in (True, False):
            if _const.FLEXIBLE == self.test_rotate(field, is_clock_wise):
                self.state = old_state
                return True
            self.state = old_state
        return False

    # ---- Property ----
    @property
    def virtual(self):
        u"""AI計算用ピース取得。
        """
        return self.__class__(self._pattern, self.topleft, True)

    @property
    def parameter(self):
        u"""ピース生成パラメータ取得。
        """
        piece = self.virtual
        piece.topleft = 0, 0
        return (
            piece.size, piece._pattern.pruning,
            tuple(block.parameter for block in piece._blocks))

    @property
    def right(self):
        return self._left + self.width

    @property
    def topleft(self):
        u"""ピースの左上座標を取得。
        """
        return self._left, self._top

    @topleft.setter
    def topleft(self, value):
        u"""ピースの左上座標を設定。
        """
        self.clear()
        self._left, self._top = tuple(value)
        self._create()

    @property
    def bottomleft(self):
        u"""左上位置取得。
        """
        return tuple((self._left, self._top+self.height))

    @bottomleft.setter
    def bottomleft(self, value):
        u"""左上位置設定。
        """
        left, bottom = value
        self.clear()
        self._left, self._top = left, bottom-self.height
        self._create()

    @property
    def centerx(self):
        u"""中心x取得。
        """
        return self.left+(self.width >> 1)

    @property
    def centery(self):
        u"""中心y取得。
        """
        return self.top+(self.height >> 1)

    @property
    def angle(self):
        u"""角度取得。
        """
        return self._pattern.angle

    @angle.setter
    def angle(self, value):
        u"""角度設定。
        """
        self.clear()
        self._pattern.angle = value
        self._create()

    @property
    def state(self):
        u"""状態を取得。
        """
        return _piece.State(self.topleft, self.angle)

    @state.setter
    def state(self, value):
        u"""状態を設定。
        """
        self.topleft = value.topleft
        self.angle = value.angle

    @property
    def form(self):
        u"""ブロックの形を取得。
        """
        return self._pattern.form

    @property
    def pruning(self):
        u"""枝きり種類取得。
        """
        return self._pattern.pruning

    @property
    def angles(self):
        u"""回転パターンの数を取得。
        """
        return self._pattern.angles

    # ------ Detect ------
    @property
    def __is_rotatable(self):
        u"""回転可能の場合に真。
        """
        return self.__rotated < self.__ROTATE_LIMIT

    @property
    def is_rested(self):
        u"""下に落ちた場合に真。
        """
        return self.__is_rested

    @property
    def is_t(self):
        u"""形がTの場合に真。
        """
        return self._pattern.form == "T"

    @property
    def is_t_spin(self):
        u"""T-Spin状態取得。
        """
        return self.__is_t_spin
