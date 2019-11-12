#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""config.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

パターンコンフィグモジュール。
"""
import pattern as __pattern


def init():
    u"""モジュールの初期化。
    使用するパラメータの作成。
    """
    import utils.const as __const
    global __basics, __levels
    x1 = "Normal", 0, (1, 1)
    x2 = "Normal", 0, (2, 2)
    x3 = "Normal", 0, (3, 3)
    x4 = "Normal", 0, (4, 4)
    all_t = (((3, 3), __const.QUARTER_PRUNING, (
        ((1, 0), x1), ((0, 1), x1), ((1, 1), x1), ((2, 1), x1))),)*7
    __basics = (
        ((4, 4), __const.HALF_PRUNING, (
            ((0, 1), x1), ((1, 1), x1), ((2, 1), x1), ((3, 1), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((0, 0), x1), ((0, 1), x1), ((1, 1), x1), ((2, 1), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((2, 0), x1), ((0, 1), x1), ((1, 1), x1), ((2, 1), x1))),
        ((2, 2), __const.SINGLE_PRUNING, (
            ((0, 0), x1), ((1, 0), x1), ((0, 1), x1), ((1, 1), x1))),
        ((3, 3), __const.HALF_PRUNING, (
            ((1, 0), x1), ((2, 0), x1), ((0, 1), x1), ((1, 1), x1))),
        ((3, 3), __const.HALF_PRUNING, (
            ((0, 0), x1), ((1, 0), x1), ((1, 1), x1), ((2, 1), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((1, 0), x1), ((0, 1), x1), ((1, 1), x1), ((2, 1), x1))))
    __basics = all_t if __const.PIECE_TEST == "T_SPIN_TEST" else __basics
    __levels = (
        ((3, 3), __const.SINGLE_PRUNING, (((1, 1), x1),)),
        ((3, 3), __const.HALF_PRUNING, (((1, 1), x1), ((2, 1), x1))),
        ((3, 3), __const.HALF_PRUNING, (
            ((0, 1), x1), ((1, 1), x1), ((2, 1), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((1, 0), x1), ((1, 1), x1), ((2, 1), x1))),
        ((2, 2), __const.SINGLE_PRUNING, (((0, 0), x2),)),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((0, 0), x1), ((1, 0), x1), ((1, 1), x1), ((2, 1), x1),
            ((2, 2), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((0, 0), x1), ((1, 0), x1), ((0, 1), x1), ((1, 1), x1),
            ((2, 1), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((0, 1), x1), ((0, 2), x1), ((1, 2), x1), ((2, 2), x1),
            ((3, 2), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((0, 0), x1), ((0, 1), x1), ((1, 1), x1), ((2, 1), x1),
            ((1, 2), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((2, 0), x1), ((1, 0), x1), ((0, 1), x1), ((1, 1), x1),
            ((2, 1), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((3, 1), x1), ((0, 2), x1), ((1, 2), x1), ((2, 2), x1),
            ((3, 2), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((2, 0), x1), ((0, 1), x1), ((1, 1), x1), ((2, 1), x1),
            ((1, 2), x1))),
        ((3, 3), __const.HALF_PRUNING, (
            ((0, 0), x1), ((0, 1), x1), ((1, 1), x1), ((2, 1), x1),
            ((2, 2), x1))),
        ((3, 3), __const.HALF_PRUNING, (
            ((2, 0), x1), ((0, 1), x1), ((1, 1), x1), ((2, 1), x1),
            ((0, 2), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((1, 0), x1), ((1, 1), x1), ((1, 2), x1), ((0, 2), x1),
            ((2, 2), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((2, 0), x1), ((0, 1), x1), ((1, 1), x1), ((2, 1), x1),
            ((0, 0), x1))),
        ((3, 3), __const.SINGLE_PRUNING, (
            ((1, 0), x1), ((0, 1), x1), ((1, 1), x1), ((2, 1), x1),
            ((1, 2), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((1, 0), x1), ((0, 1), x1), ((1, 1), x1), ((2, 1), x1),
            ((0, 2), x1), ((2, 2), x1))),
        ((4, 4), __const.HALF_PRUNING, (
            ((1, 0), x1), ((2, 0), x1), ((1, 1), x1), ((2, 1), x1),
            ((1, 2), x1), ((2, 2), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((0, 2), x1), ((3, 2), x1), ((1, 1), x1), ((2, 1), x1),
            ((1, 2), x1), ((2, 2), x1))),
        ((4, 4), __const.HALF_PRUNING, (
            ((0, 1), x1), ((3, 2), x1), ((1, 1), x1), ((2, 1), x1),
            ((1, 2), x1), ((2, 2), x1))),
        ((4, 4), __const.HALF_PRUNING, (
            ((0, 2), x1), ((3, 1), x1), ((1, 1), x1), ((2, 1), x1),
            ((1, 2), x1), ((2, 2), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((0, 0), x1), ((2, 0), x1), ((0, 1), x1), ((1, 1), x1),
            ((2, 1), x1), ((3, 1), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((2, 0), x1), ((1, 1), x1), ((2, 1), x1), ((0, 2), x1),
            ((1, 2), x1), ((2, 2), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((0, 0), x1), ((2, 0), x1), ((0, 1), x1), ((2, 1), x1),
            ((0, 2), x1), ((1, 2), x1), ((2, 2), x1))),
        ((3, 3), __const.HALF_PRUNING, (
            ((0, 0), x1), ((2, 0), x1), ((0, 1), x1), ((2, 1), x1),
            ((0, 2), x1), ((1, 1), x1), ((2, 2), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((0, 0), x1), ((0, 1), x1), ((1, 1), x1), ((2, 1), x1),
            ((0, 2), x1), ((1, 2), x1), ((2, 2), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((2, 0), x1), ((0, 1), x1), ((1, 1), x1), ((2, 1), x1),
            ((0, 2), x1), ((1, 2), x1), ((2, 2), x1))),
        ((3, 3), __const.QUARTER_PRUNING, (
            ((0, 0), x1), ((1, 0), x1), ((2, 0), x1), ((0, 1), x1),
            ((1, 1), x1), ((2, 1), x1), ((0, 2), x1), ((2, 2), x1))),
        ((3, 3), __const.SINGLE_PRUNING, (
            ((0, 0), x1), ((1, 0), x1), ((2, 0), x1), ((0, 1), x1),
            ((2, 1), x1), ((0, 2), x1), ((1, 2), x1), ((2, 2), x1))),
        ((4, 4), __const.HALF_PRUNING, (
            ((0, 1), x1), ((1, 1), x1), ((2, 1), x1), ((3, 1), x1),
            ((0, 2), x1), ((1, 2), x1), ((2, 2), x1), ((3, 2), x1))),
        ((3, 3), __const.SINGLE_PRUNING, (
            ((0, 0), x3),)),
        ((3, 3), __const.SINGLE_PRUNING, (
            ((0, 0), x1), ((1, 0), x1), ((2, 0), x1), ((0, 1), x1),
            ((1, 1), x1), ((2, 1), x1), ((0, 2), x1), ((1, 2), x1),
            ((2, 2), x1))),
        ((4, 4), __const.HALF_PRUNING, (
            ((2, 0), x1), ((3, 0), x1), ((1, 1), x1), ((2, 1), x1),
            ((3, 1), x1), ((0, 2), x1), ((1, 2), x1), ((2, 2), x1),
            ((0, 3), x1), ((1, 3), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((3, 0), x1), ((2, 1), x1), ((3, 1), x1), ((1, 2), x1),
            ((2, 2), x1), ((3, 2), x1), ((0, 3), x1), ((1, 3), x1),
            ((2, 3), x1), ((3, 3), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((3, 0), x1), ((1, 1), x1), ((2, 1), x1), ((3, 1), x1),
            ((1, 2), x1), ((2, 2), x1), ((3, 2), x1), ((0, 3), x1),
            ((1, 3), x1), ((2, 3), x1), ((3, 3), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((3, 0), x1), ((2, 0), x1), ((0, 1), x1), ((1, 1), x1),
            ((2, 1), x1), ((3, 1), x1), ((0, 2), x1), ((2, 2), x1),
            ((0, 3), x1), ((1, 3), x1), ((2, 3), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((0, 0), x1), ((2, 0), x1), ((0, 1), x1), ((1, 1), x1),
            ((2, 1), x1), ((3, 1), x1), ((0, 2), x1), ((2, 2), x1),
            ((0, 3), x1), ((1, 3), x1), ((2, 3), x1), ((3, 3), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((1, 0), x1), ((2, 0), x1), ((1, 1), x1), ((2, 1), x1),
            ((0, 2), x1), ((1, 2), x1), ((2, 2), x1), ((3, 2), x1),
            ((0, 3), x1), ((1, 3), x1), ((2, 3), x1), ((3, 3), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((0, 0), x1), ((3, 0), x1), ((0, 1), x1), ((3, 1), x1),
            ((0, 2), x1), ((1, 2), x1), ((2, 2), x1), ((3, 2), x1),
            ((0, 3), x1), ((1, 3), x1), ((2, 3), x1), ((3, 3), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((0, 0), x1), ((1, 0), x1), ((0, 1), x1), ((1, 1), x1),
            ((0, 2), x1), ((1, 2), x1), ((2, 2), x1), ((3, 2), x1),
            ((0, 3), x1), ((1, 3), x1), ((2, 3), x1), ((3, 3), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((0, 0), x2), ((0, 2), x2), ((2, 2), x2))),
        ((4, 4), __const.SINGLE_PRUNING, (
            ((1, 0), x1), ((2, 0), x1), ((0, 1), x1), ((1, 1), x1),
            ((2, 1), x1), ((3, 1), x1), ((0, 2), x1), ((1, 2), x1),
            ((2, 2), x1), ((3, 2), x1), ((1, 3), x1), ((2, 3), x1))),
        ((4, 4), __const.SINGLE_PRUNING, (
            ((0, 0), x1), ((1, 0), x1), ((3, 0), x1), ((1, 1), x1),
            ((2, 1), x1), ((3, 1), x1), ((0, 2), x1), ((1, 2), x1),
            ((2, 2), x1), ((0, 3), x1), ((2, 3), x1), ((3, 3), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((0, 0), x1), ((2, 0), x1), ((0, 1), x3), ((3, 1), x1),
            ((3, 3), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((0, 0), x1), ((1, 0), x1), ((2, 0), x2), ((0, 1), x1),
            ((0, 2), x1), ((3, 2), x1), ((0, 3), x1), ((1, 3), x1),
            ((2, 3), x1), ((3, 3), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((0, 0), x2), ((2, 0), x1), ((2, 1), x1), ((3, 1), x1),
            ((0, 2), x1), ((2, 2), x2), ((0, 3), x1), ((1, 3), x1))),
        ((4, 4), __const.HALF_PRUNING, (
            ((0, 0), x2), ((2, 0), x1), ((3, 0), x1), ((3, 1), x1),
            ((0, 2), x1), ((2, 2), x2), ((0, 3), x1), ((1, 3), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((0, 0), x2), ((2, 0), x2), ((2, 2), x2), ((0, 2), x1),
            ((0, 3), x1), ((1, 3), x1))),
        ((4, 4), __const.QUARTER_PRUNING, (
            ((0, 0), x2), ((0, 2), x2), ((2, 2), x2), ((2, 0), x1),
            ((2, 1), x1), ((3, 1), x1))),
        ((4, 4), __const.SINGLE_PRUNING, (((0, 0), x4),)),
        ((4, 4), __const.SINGLE_PRUNING, (
            ((0, 0), x2), ((2, 0), x2), ((0, 2), x2), ((2, 2), x2))),
        ((4, 4), __const.SINGLE_PRUNING, (
            ((0, 0), x1), ((1, 0), x1), ((2, 0), x1), ((3, 0), x1),
            ((0, 1), x1), ((1, 1), x1), ((2, 1), x1), ((3, 1), x1),
            ((0, 2), x1), ((1, 2), x1), ((2, 2), x1), ((3, 2), x1),
            ((0, 3), x1), ((1, 3), x1), ((2, 3), x1), ((3, 3), x1))))


def get_basics():
    u"""基本パターン取得。
    """
    return [__pattern.Rotatable(*basic) for basic in __basics]


def get_total():
    u"""レベルピースの総数を取得。
    """
    return len(__levels)


def get_levels(start, end):
    u"""レベルに応じたパターン取得。
    """
    return [__pattern.Rotatable(*__levels[i]) for i in range(start, end)]
