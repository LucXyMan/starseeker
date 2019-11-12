#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""table.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

セルテーブルモジュール。
"""
import cells as _cells


class Table(object):
    u"""セルテーブル。
    """
    __slots__ = "__field", "__grids", "__is_virtual"

    def __init__(self, size, field, is_virtual):
        u"""コンストラクタ。
        """
        def __get_blank():
            u"""空白表取得。
            """
            result = []
            w, h = size
            for y in range(h):
                line = []
                for x in range(w):
                        blank = _cells.block.Blank(
                            (x, y, 1, 1), 0, self.__is_virtual)
                        blank.piece = self.__field
                        line.append(blank)
                result.append(line)
            return result
        self.__field = field
        self.__is_virtual = bool(is_virtual)
        self.__grids = __get_blank()

    def __getitem__(self, key):
        u"""テーブルライン取得。
        """
        return self.__grids[key][:]

    def __repr__(self):
        u"""文字列表現取得。
        """
        return u"<{name} table:{table}>".format(
            name=self.__class__.__name__, table=self.__grids)

    def get_cell(self, point):
        u"""pointのセル取得。
        """
        x, y = point
        if x < 0 or self.width <= x or y < 0 or self.height <= y:
            raise ValueError("Invalid point.")
        return self.__grids[y][x]

    def set_cell(self, point, cell):
        u"""pointにセル設定。
        """
        x, y = point
        if x < 0 or self.width <= x or y < 0 or self.height <= y:
            raise ValueError("Invalid point.")
        self.__grids[y][x] = cell

    def __get_writing_range(self, block):
        u"""ブロックの書き込み範囲取得。
        """
        left, top = block.point.topleft
        right, bottom = block.point.bottomright
        if left < 0 or self.width < right or top < 0 or self.height < bottom:
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

    def remove(self, block):
        u"""ブロックを表から削除。
        """
        left, top, right, bottom = self.__get_writing_range(block)
        for y in range(top, bottom):
            for x in range(left, right):
                if self.__grids[y][x] is block:
                    blank = _cells.block.Blank(
                        (x, y, 1, 1), 0, self.__is_virtual)
                    blank.piece = self.__field
                    self.set_cell((x, y), blank)

    def get_line(self, y):
        u"""水平ライン取得。
        """
        return self.__grids[y][:]

    def get_vline(self, x):
        u"""垂直ライン取得。
        """
        return tuple(self.get_cell((x, y)) for y in range(self.height))

    def get_all(self):
        u"""全セル取得。
        """
        return reduce(
            lambda x, y: x+y,
            [[cell for cell in line] for line in self.__grids])

    def get_side_space(self, x, y):
        u"""横方向のスペースセル取得。
        """
        def __get_space(cells):
            u"""スペースリスト取得。
            """
            result = []
            for cell in cells:
                if cell.is_block or cell.is_hole:
                    return result
                else:
                    result.append(cell)
            return result
        return (
            __get_space(self.get_line(y)[x+1:]) +
            __get_space(self.get_line(y)[:x][::-1]))

    def get_below_cells(self):
        u"""一番上のブロック以下のセルを取得。
        """
        def __get_below_cell(x):
            u"""列xの一番上のブロックより下のセルを取得する。
            """
            vline = self.get_vline(x)
            for i, cell in enumerate(vline):
                if cell.is_block:
                    return vline[i:]
            else:
                return ()
        return reduce(
            lambda x, y: x+y, (__get_below_cell(x) for x in range(self.width)))

    def get_topmost_block(self, x):
        u"""xラインの内最も高いブロックを返す。
        """
        for cell in self.get_vline(x):
            if cell.is_block:
                return cell
        return None

    def get_lowest_space(self, x):
        u"""xラインの内最も低い空白を取得。
        """
        for cell in self.get_vline(x)[::-1]:
            if cell.is_space:
                return cell
        return None

    def get_lowest_hole(self, x):
        u"""最も低いホールを取得。
        """
        for cell in self.get_vline(x)[::-1]:
            if cell.is_hole:
                return cell
        return None

    def get_roots(self):
        u"""'根'となるブロックを返す。
        フィールドの一番下のブロック。
        """
        def __get_root(x):
            u"""xの根になるブロックを取得。
            """
            vline = self.get_vline(x)
            return max(vline, key=lambda c: c.point.top) if vline else None
        return tuple(__get_root(x) for x in range(self.width))

    def get_onepieces(self, length=-1):
        u"""補完されるラインを全て返す。
        """
        def __is_onepiece(y, length):
            u"""ライン内のブロック数がlength以上の場合Trueを返す。
            """
            return length <= len(tuple(
                cell for cell in self.get_line(y) if cell.is_block))
        return tuple(
            self.get_line(y) for y in range(self.height) if
            __is_onepiece(y, self.width if length == -1 else length))

    @property
    def width(self):
        u"""幅取得。
        """
        return len(self.__grids[0])

    @property
    def height(self):
        u"""高さ取得。
        """
        return len(self.__grids)

    @property
    def centerx(self):
        u"""横軸中心取得。
        """
        return self.width/2
