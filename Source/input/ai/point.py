#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""point.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

AIポイントモジュール。
"""


class Point(object):
    u"""AI得点。
    ある位置にピースを落とした時の得点を表現する。
    """
    __slots__ = (
        "__adjasent_spaces", "__after", "__avg_depth",
        "__block_above_of_holes", "__completions", "__goal_distance",
        "__hole_prevention", "__is_t_spin", "__is_hold",
        "__malignancy", "__max_depth", "__min_depth", "__smoothness",
        "__state", "__unlock")

    def __init__(self, state, is_hold=False, is_t_spin=False):
        u"""コンストラクタ。
        """
        self.__state = state
        self.__is_hold = bool(is_hold)
        self.__is_t_spin = bool(is_t_spin)
        self.__max_depth = 0
        self.__min_depth = 0
        self.__avg_depth = 0
        self.__completions = 0
        self.__hole_prevention = 0
        self.__smoothness = 0
        self.__block_above_of_holes = 0
        self.__adjasent_spaces = 0
        self.__goal_distance = 0
        self.__malignancy = 0
        self.__unlock = 0

    def __repr__(self):
        u"""文字列表現取得。
        """
        return u"<{name}  state:{state}, points:{points}>".format(
            name=self.__class__.__name__, state=self.__state,
            points=self.total)

    def __lt__(self, other):
        u"""self < other.
        """
        return self.total < other.total

    def __le__(self, other):
        u"""self <= other.
        """
        return self.total <= other.total

    def __eq__(self, other):
        u"""self == other.
        """
        return self.total == other.total

    def __ne__(self, other):
        u"""self != other.
        """
        return self.total != other.total

    def __gt__(self, other):
        u"""self > other.
        """
        return self.total > other.total

    def __ge__(self, other):
        u"""self >= other.
        """
        return self.total >= other.total

    def add(self, other):
        u"""得点加算処理。
        """
        self.__max_depth += other.__max_depth
        self.__min_depth += other.__min_depth
        self.__avg_depth += other.__avg_depth
        self.__completions += other.__completion
        self.__hole_prevention += other.__hole_prevention
        self.__smoothness += other.__smoothness
        self.__block_above_of_holes += other.__block_above_of_holes
        self.__adjasent_spaces += other.__adjasent_spaces
        self.__goal_distance += other.__goal_distance
        self.__malignancy += other.__malignancy
        self.__unlock += other.__unlock

    @property
    def total(self):
        u"""合計点取得。
        T-Spinの時に1.5倍に。
        """
        total = sum((
            self.__max_depth, self.__min_depth, self.__avg_depth,
            self.__completions, self.__hole_prevention, self.__smoothness,
            self.__block_above_of_holes, self.__adjasent_spaces,
            self.__goal_distance, self.__malignancy, self.__unlock))
        return (
            total+(total >> 1) if self.is_t_spin and
            self.__completions else total)

    @property
    def state(self):
        u"""この点数の状態を取得。
        """
        return self.__state

    @property
    def is_hold(self):
        u"""ホールドを使用する場合に真。
        """
        return self.__is_hold

    @property
    def is_t_spin(self):
        u"""T-Spin判定取得。
        """
        return self.__is_t_spin

    @property
    def max_depth(self):
        u"""最底辺ブロック点数取得。
        """
        return self.__max_depth

    @max_depth.setter
    def max_depth(self, value):
        u"""最底辺ブロック点数設定。
        """
        self.__max_depth = int(value)

    @property
    def min_depth(self):
        u"""最高峰ブロック点数取得。
        """
        return self.__min_depth

    @min_depth.setter
    def min_depth(self, value):
        u"""最高峰ブロック点数設定。
        """
        self.__min_depth = int(value)

    @property
    def avg_depth(self):
        u"""ブロックの平均高さ点数取得。
        """
        return self.__avg_depth

    @avg_depth.setter
    def avg_depth(self, value):
        u"""ブロックの平均高さ点数設定。
        """
        self.__avg_depth = int(value)

    @property
    def completions(self):
        u"""コンプリート点数取得。
        """
        return self.__completions

    @completions.setter
    def completions(self, value):
        u"""コンプリート点数設定。
        """
        self.__completions = int(value)

    @property
    def hole_prevention(self):
        u"""ホール防止点数取得。
        """
        return self.__hole_prevention

    @hole_prevention.setter
    def hole_prevention(self, value):
        u"""ホール防止点数設定。
        """
        self.__hole_prevention = int(value)

    @property
    def smoothness(self):
        u"""フィールドの滑らかさ点数取得。
        """
        return self.__smoothness

    @smoothness.setter
    def smoothness(self, value):
        u"""フィールドの滑らかさ点数設定。
        """
        self.__smoothness = int(value)

    @property
    def block_above_of_holes(self):
        u"""ホール上のブロック点数取得。
        """
        return self.__block_above_of_holes

    @block_above_of_holes.setter
    def block_above_of_holes(self, value):
        u"""ホール上のブロック点数設定。
        """
        self.__block_above_of_holes = int(value)

    @property
    def adjasent_spaces(self):
        u"""隣接スペース点数取得。
        """
        return self.__adjasent_spaces

    @adjasent_spaces.setter
    def adjasent_spaces(self, value):
        u"""隣接スペース点数設定。
        """
        self.__adjasent_spaces = int(value)

    @property
    def goal_distance(self):
        u"""ゴールまでの距離取得。
        """
        return self.__goal_distance

    @goal_distance.setter
    def goal_distance(self, value):
        u"""ゴールまでの距離設定。
        """
        self.__goal_distance = int(value)

    @property
    def malignancy(self):
        u"""悪性度点数取得。
        """
        return self.__malignancy

    @malignancy.setter
    def malignancy(self, value):
        u"""悪性度点数設定。
        """
        self.__malignancy = int(value)

    @property
    def unlock(self):
        u"""アンロック点数取得。
        """
        return self.__unlock

    @unlock.setter
    def unlock(self, value):
        u"""アンロック点数設定。
        """
        self.__unlock = int(value)


if __name__ == '__main__':
    a = Point(None)
    a.max_depth = 10
    a.completions = 1
    b = Point(None)
    b.max_depth = 20
    b.completions = 1
    c = Point(None, is_t_spin=True)
    c.max_depth = 15
    c.completions = 1
    d = Point(None, is_t_spin=True)
    d.max_depth = 5
    d.completions = 1
    points = a, b, c, d
    print sorted(points)
    print max(points)
    print min(points)
