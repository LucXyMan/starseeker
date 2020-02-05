#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""pattern.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

パターンモジュール。
"""
import random as _random
import utils.const as _const


class _Shape(object):
    u"""ブロックの形を決定する。
    """
    __slots__ = "__h", "__state", "__type", "__w"

    def __init__(self, type_, state, size):
        u"""コンストラクタ。
        """
        self.__type = str(type_)
        self.__state = int(state)
        self.__w, self.__h = size

    def get_block(self, point, is_virtual):
        u"""ブロック取得。
        """
        x, y = point
        return self.Block((x, y, self.__w, self.__h), self.__state, is_virtual)

    # ---- Property ----
    @property
    def Block(self):
        u"""ブロッククラス取得。
        """
        import cells as __cells
        return __cells.get(self.__type)

    @property
    def copy(self):
        u"""シェイプをコピー。
        """
        return self.__class__(
            self.__type, self.__state, (self.__w, self.__h))

    @property
    def type(self):
        u"""型名取得。
        """
        return self.__type

    @type.setter
    def type(self, value):
        u"""型名設定。
        """
        self.__type = str(value)

    @property
    def state(self):
        u"""状態取得。
        """
        return self.__state

    @state.setter
    def state(self, value):
        u"""状態設定。
        """
        self.__state = int(value)

    @property
    def w(self):
        u"""幅取得。
        """
        return self.__w

    @w.setter
    def w(self, value):
        u"""幅設定。
        """
        self.__w = int(value)

    @property
    def h(self):
        u"""高さ取得。
        """
        return self.__h

    @h.setter
    def h(self, value):
        u"""高さ設定。
        """
        self.__h = int(value)

    @property
    def size(self):
        u"""サイズ取得。
        """
        return self.__w, self.__h

    @property
    def is_large(self):
        u"""大型シェイプ判定。
        """
        return 1 < self.__w or 1 < self.__h


class Pattern(object):
    u"""ピースの形を決定する。
    """
    __slots__ = "__color", "_shapes"
    __box = []

    @classmethod
    def __get_color(cls):
        u"""ペイント用のくじ引き。
        """
        if not cls.__box:
            cls.__box = range(_const.BASIC_COLORS)
            _random.shuffle(cls.__box)
        return cls.__box.pop()

    def __init__(self, size, params=()):
        u"""コンストラクタ。
        """
        self._shapes = self._get_empty(size)
        for (x, y), param in params:
            self._shapes[y][x] = _Shape(*param)
        self.__color = Pattern.__get_color()

    def __getitem__(self, key):
        u"""シェイプテーブルライン取得。
        """
        return self._shapes[key]

    def _get_empty(self, size, pad=None):
        u"""空のパターン作成。
        """
        w, h = size
        return [[pad for _ in range(w)] for _ in range(h)]

    def get_blocks(self, pos=(0, 0), is_virtual=False):
        u"""ブロックを取得。
        """
        blocks = []
        for x in range(self.width):
            for y in range(self.height):
                if self._shapes[y][x]:
                    shape = self._shapes[y][x]
                    block = shape.get_block((x+pos[0], y+pos[1]), is_virtual)
                    if not is_virtual:
                        block.paint(self.__color)
                    blocks.append(block)
        return blocks

    def get_target(self):
        u"""ターゲットピース取得。
        """
        def __map_number(color):
            u"""ターゲットカラー番号取得。
            """
            return (
                _const.RED_TARGET_NUMBER if color == "red" else
                _const.ORANGE_TARGET_NUMBER if color == "orange" else
                _const.YELLOW_TARGET_NUMBER if color == "yellow" else
                _const.GREEN_TARGET_NUMBER if color == "green" else
                _const.CYAN_TARGET_NUMBER if color == "cyan" else
                _const.BLUE_TARGET_NUMBER if color == "blue" else
                _const.MAGENTA_TARGET_NUMBER if color == "magenta" else
                _const.WHITE_TARGET_NUMBER)
        return Pattern((self.width, self.height), (((x, y), (
            "Target", __map_number(
                shape.Block.get_target_color()), shape.size)) for
                y, line in enumerate(self._shapes) for
                x, shape in enumerate(line) if shape))

    # ---- Property ----
    @property
    def width(self):
        u"""幅取得。
        """
        return len(self._shapes[0])

    @property
    def height(self):
        u"""高さ取得。
        """
        return len(self._shapes)

    @property
    def size(self):
        u"""サイズ取得。
        """
        return self.width, self.height


class Rotatable(Pattern):
    u"""回転パターン。
    """
    __slots__ = "__angle", "__form", "__pruning", "__rotations"
    __I_TETRO_FORM = [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
    __O_TETRO_FORM = [
        [1, 1],
        [1, 1]]
    __T_TETRO_FORM = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0]]
    __L_TETRO_FORM = [
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0]]
    __J_TETRO_FORM = [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0]]
    __S_TETRO_FORM = [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0]]
    __Z_TETRO_FORM = [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]]

    def __init__(self, size, pruning, params):
        u"""コンストラクタ。
        """
        super(Rotatable, self).__init__(size, params)
        self.__pruning = pruning
        self.__rotations = self.__get_rotations()
        self.__angle = _const.A0
        self.__form = ""

    def __get_rotations(self):
        u"""全回転パターン取得。
        """
        def __get_rotation():
                u"""回転後テーブル取得。
                """
                def __get_copy():
                    u"""テーブルコピー取得。
                    """
                    result = self._get_empty((
                        len(self._shapes[0]), len(self._shapes)))
                    for y, line in enumerate(shapes):
                        for x, square in enumerate(line):
                            if isinstance(square, _Shape):
                                result[y][x] = square.copy
                    return result
                return [list(elm) for elm in zip(*__get_copy()[::-1])]

        def __get_exists(shapes):
            u"""シェイプが存在するか否かの判定用マスクを取得。
            """
            w, h = self.width, self.height
            mask = self._get_empty((w, h))
            for y in range(h):
                for x in range(w):
                    if shapes[y][x]:
                        mask[y][x] = 1
            return mask

        def __adjust_shapes():
            u"""ラージシェイプ回転時のズレを修正する。
            """
            mask = __get_exists(shapes)
            for y in range(len(shapes)):
                for x in range(len(shapes[0])):
                    if mask[y][x] and 1 < shapes[y][x].h:
                        gap = shapes[y][x].h-1
                        shapes[y][x-gap] = shapes[y][x]
                        shapes[y][x] = None

        def __rotate_shapes():
            u"""長方形シェイプ回転。
            """
            mask = __get_exists(shapes)
            for y in range(len(shapes)):
                for x in range(len(shapes[0])):
                    shape = shapes[y][x]
                    if mask[y][x] and shape.w != shape.h:
                        shape.w, shape.h = shape.size[::-1]
        shapes = self._shapes
        rotate_pattern = {0: shapes}
        for angle in range(1, 4):
            shapes = __get_rotation()
            __adjust_shapes()
            __rotate_shapes()
            rotate_pattern[angle] = shapes
        return rotate_pattern

    def __get_shapes(self):
        u"""テーブルからシェイプを取得。
        """
        return (shape for line in self._shapes for shape in line if shape)

    def append(self, new, old, state=-1):
        u"""oldシェイプをnewにひとつだけ置き換える。
        """
        is_changed = False
        self.rotate(_const.A0)
        shapes = tuple(
            shape for shape in self.__get_shapes() if
            not shape.is_large and
            shape.type in old.split("#"))
        if shapes:
            shape = _random.choice(shapes)
            shape.type = new
            shape.state = state
            is_changed = True
        self.__rotations = self.__get_rotations()
        return is_changed

    def change(self, new, old, state=-1, is_lchange=False):
        u"""oldシェイプをnewに置き換える。
        is_lchange: largeブロックの置き換えフラグ。
        """
        is_changed = False
        self.rotate(_const.A0)
        for shape in self.__get_shapes():
            is_changeable = is_lchange or not shape.is_large
            if is_changeable and shape.type in old.split("#"):
                shape.type = new
                shape.state = state
                is_changed = True
        self.__rotations = self.__get_rotations()
        return is_changed

    def rotate(self, to_angle):
        u"""パターン回転処理。
        """
        self.__angle = to_angle & 0b11
        self._shapes = self.__rotations[self.__angle]

    # ---- Property ----
    @property
    def form(self):
        u"""フォーム取得。
        値が設定されていない場合設定して値を返す。
        """
        def __get_form():
            u"""フォーム判定用変数を取得。
            """
            def __get_bit():
                u"""0と1で表されたパターンを取得。
                """
                def __write():
                    u"""シェイプサイズに合わせて'1'を書き込む。
                    """
                    size = self._shapes[top][left].size
                    right, bottom = left+size[0], top+size[1]
                    for y in range(top, bottom):
                        for x in range(left, right):
                            mask[y][x] = 1
                mask = self._get_empty((self.width, self.height), 0)
                for top in range(self.height):
                    for left in range(self.width):
                        if self._shapes[top][left]:
                            __write()
                return mask
            shapes = __get_bit()
            rotations = [shapes]
            for _ in range(3):
                shapes = [list(elm) for elm in zip(*shapes[::-1])]
                rotations.append(shapes)
            return (
                "I" if self.__I_TETRO_FORM in rotations else
                "J" if self.__J_TETRO_FORM in rotations else
                "L" if self.__L_TETRO_FORM in rotations else
                "O" if self.__O_TETRO_FORM in rotations else
                "S" if self.__S_TETRO_FORM in rotations else
                "T" if self.__T_TETRO_FORM in rotations else
                "Z" if self.__Z_TETRO_FORM in rotations else "?")
        if self.__form == "":
            self.__form = __get_form()
        return self.__form

    @property
    def angle(self):
        u"""角度取得。
        """
        return self.__angle

    @angle.setter
    def angle(self, value):
        u"""角度設定。
        """
        self.rotate(value)

    @property
    def angles(self):
        u"""回転パターン数取得。
        """
        return len(self.__rotations)

    @property
    def pruning(self):
        u"""AI枝きり種類取得。
        """
        return self.__pruning


class Array(object):
    u"""パターン格納配列。
    """
    __slots__ = "__size", "__classes", "__appends", "_patterns", "__is_pop_cls"

    def __init__(self, length=-1):
        u"""コンストラクタ。
        """
        import collections as __collections
        self.__size = length
        self._patterns = __collections.deque()
        self._reload()

    def __len__(self):
        u"""長さ取得。
        """
        return len(self._patterns)

    def __getitem__(self, key):
        u"""パターン取得。
        """
        return self._patterns[key]

    def __setitem__(self, key, value):
        u"""パターン設定。
        """
        self._patterns[key] = value

    def __iter__(self):
        u"""イテレータ取得。
        """
        return iter(self._patterns)

    def _reload(self):
        u"""パターンの生成。
        """
    def pop(self):
        u"""先頭パターンをポップ。
        """
        return self._patterns.popleft()

    def append(self, *patterns):
        u"""パターン追加。
        設定されたサイズを超えた場合、先頭パターンがポップされる。
        """
        result = []
        for shapes in patterns:
            if shapes:
                self._patterns.append(shapes)
                if self.__size != -1 and len(self._patterns) > self.__size:
                    result.append(self.pop())
        return result

    @property
    def is_empty(self):
        u"""空判定。
        """
        return not self._patterns
