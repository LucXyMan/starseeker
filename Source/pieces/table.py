#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""table.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

セルテーブルモジュール。
"""
import cells.block as _block


class Table(object):
    u"""セルテーブル。
    """
    __slots__ = "__cells", "__field", "__height", "__is_virtual", "__width"

    def __init__(self, size, field, is_virtual):
        u"""コンストラクタ。
        """
        def __get_blank():
            u"""空白表取得。
            """
            result = []
            for grid in range(self.__width*self.__height):
                y, x = divmod(grid, self.__width)
                blank = _block.Blank((x, y, 1, 1), 0, self.__is_virtual)
                blank.piece = self.__field
                result.append(blank)
            return result
        self.__width, self.__height = size
        self.__field = field
        self.__is_virtual = bool(is_virtual)
        self.__cells = __get_blank()

    def __repr__(self):
        u"""文字列表現取得。
        """
        return u"<{name} table:{table}>".format(
            name=self.__class__.__name__, table=self.__cells)

    def __iter__(self):
        u"""イテレータ取得。
        """
        return iter(self.__cells)

    # ---- Write and Erase ----
    def __get_writing_range(self, block):
        u"""ブロックの書き込み範囲取得。
        """
        left, top = block.point.topleft
        right, bottom = block.point.bottomright
        if (
            left < 0 or self.__width < right or
            top < 0 or self.__height < bottom
        ):
            raise ValueError("Invalid range.")
        return left, top, right, bottom

    def write(self, block):
        u"""ブロックを表に書き込む。
        """
        left, top, right, bottom = self.__get_writing_range(block)
        for y in range(top, bottom):
            for x in range(left, right):
                block.piece = self.__field
                self.set_cell((x, y), block)

    def erase(self, block):
        u"""ブロックを表から削除。
        """
        left, top, right, bottom = self.__get_writing_range(block)
        for y in range(top, bottom):
            for x in range(left, right):
                if self.get_cell((x, y)) is block:
                    blank = _block.Blank((x, y, 1, 1), 0, self.__is_virtual)
                    blank.piece = self.__field
                    self.set_cell((x, y), blank)

    # ---- Getter ----
    def __get_vline(self, x):
        u"""垂直ライン取得。
        """
        return tuple(self.get_cell((x, y)) for y in range(self.__height))

    def get_cell(self, point):
        u"""pointのセル取得。
        """
        x, y = point
        if x < 0 or self.__width <= x or y < 0 or self.__height <= y:
            return None
        return self.__cells[x+y*self.__width]

    def get_line(self, y):
        u"""水平ライン取得。
        """
        offset = y*self.__width
        return tuple(self.__cells[offset:offset+self.__width])

    def get_topmost_block(self, x):
        u"""xラインの内最も高いブロックを返す。
        """
        for cell in self.__get_vline(x):
            if cell.is_block:
                return cell
        return None

    def get_lowest_space(self, x):
        u"""xラインの内最も低い空白を取得。
        """
        vline = self.__get_vline(x)
        for cell in vline[::-1]:
            if cell.is_space:
                return cell
        return None

    def get_lowest_hole(self, x):
        u"""最も低いホールを取得。
        """
        vline = self.__get_vline(x)
        for cell in vline[::-1]:
            if cell.is_hole:
                return cell
        return None

    def get_onepieces(self, length=-1):
        u"""補完されるラインを全て返す。
        """
        length = self.__width if length == -1 else length
        return tuple(
            tuple(sorted(set(line))) for
            line in (self.get_line(y) for y in range(self.__height)) if
            length <= sum(1 for cell in line if cell.is_block))

    # ---- Setter ----
    def set_cell(self, point, cell):
        u"""pointにセル設定。
        """
        x, y = point
        if x < 0 or self.__width <= x or y < 0 or self.__height <= y:
            raise ValueError("Invalid point.")
        self.__cells[x+y*self.__width] = cell

    def set_state(self):
        u"""空白状態設定。
        """
        def __set_holes():
            u"""フィールド上スペースとホールを設定する。
            フィールド上各列に_set_hole関数を適用。
            """
            def __set_hole(x):
                u"""列のスペースとホールを設定する。
                列の一番上のブロックより下にある空白をホール、
                それ以外の空白をスペースとする。空白のstate変数に
                スペースの場合1を、ホールの場合は2を設定する。
                列にブロックがない場合にはその列は全てスペースとなる。
                """
                vline = self.__get_vline(x)
                border_block = self.get_topmost_block(x)
                if border_block:
                    border = border_block.point.top
                    for cell in vline[:border]:
                        if cell.is_blank:
                            cell.state = 1
                    for cell in vline[border:]:
                        if cell.is_blank:
                            cell.state = 2
                else:
                    for cell in vline:
                        if cell.is_blank:
                            cell.state = 1
            for x in range(self.width):
                __set_hole(x)

        def __set_adjacent_spaces():
            u"""隣接スペース設定。
            フィールド上ホールの、横方向に存在する空白を隣接スペースとする。
            """
            def __get_side_spaces(point):
                u"""横方向のスペースセル取得。
                """
                def __get_consecutive_space(cells):
                    u"""連続するスペースセル取得。
                    """
                    result = []
                    for cell in cells:
                        if cell.is_block or cell.is_hole:
                            return result
                        else:
                            result.append(cell)
                    return result
                x, y = point
                line = self.get_line(y)
                return tuple(
                    __get_consecutive_space(line[x+1:]) +
                    __get_consecutive_space(line[:x][::-1]))
            for cell in (cell for cell in self.__cells if cell.is_hole):
                for space in __get_side_spaces(cell.point.topleft):
                    space.state = 3
        __set_holes()
        __set_adjacent_spaces()

    # ---- Property ----
    @property
    def width(self):
        u"""幅取得。
        """
        return self.__width

    @property
    def height(self):
        u"""高さ取得。
        """
        return self.__height

    @property
    def centerx(self):
        u"""横軸中心取得。
        """
        return self.__width >> 1

    @property
    def sorted(self):
        u"""ソートされたセル取得。
        """
        return tuple(sorted(set(self.__cells)))

    @property
    def below(self):
        u"""一番上のブロックより下のセルを取得。
        """
        def __get_below(x):
            u"""列xの一番上のブロックより下のセルを取得する。
            """
            vline = self.__get_vline(x)
            for i, cell in enumerate(vline):
                if cell.is_block:
                    return vline[i:]
            else:
                return ()
        return reduce(lambda x, y: x+y, (
            __get_below(x) for x in range(self.__width)))

    @property
    def root(self):
        u"""ルートセル取得。
        フィールドの一番下のセル。
        """
        def __get_root(x):
            u"""xの根になるセル取得。
            """
            vline = self.__get_vline(x)
            return max(vline, key=lambda c: c.point.top) if vline else None
        return tuple(sorted({__get_root(x) for x in range(self.__width)}))

    @property
    def has_alone_chest(self):
        u"""ペア無し宝箱判定。
        """
        def __has_alone_chest(line):
            u"""ライン上にペアの鍵が無い宝箱が存在する場合に真。
            """
            import utils.const as __const
            return any(
                cell.is_locked for cell in line) and all(
                cell.name not in __const.KEY_NAMES.split("#") for cell in line)
        lines = (self.get_line(y) for y in range(self.height))
        return any(__has_alone_chest(line) for line in lines)
