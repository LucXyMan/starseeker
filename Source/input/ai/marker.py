#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""marker.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

位置マーカー作成モジュール。
"""
import utils.const as _const
import command as _command


class Marker(object):
    u"""位置マーカー作成。
    目的地までのパンくずを並べる。
    """
    __slots__ = "__field", "__goal", "__out", "__piece"

    def __init__(self, field, piece, goal):
        u"""コンストラクタ。
        """
        self.__field = field
        self.__piece = piece
        self.__goal = goal
        self.__out = None

    def mark(self, is_t_spin):
        u"""位置マーカーリスト取得。
        """
        def __mark(cmds, founds):
            u"""マーカーを置く。
            """
            def __signal():
                u"""起動シグナルを送出。
                """
                if (
                    _const.IS_MULTIPROCESSING and
                    self.__out and self.__out.empty()
                ):
                    self.__out.put_nowait(("signal", ("route_search",)))
                    self.__out.task_done()

            def __get_funcs():
                u"""使用する関数とパラメータを取得。
                """
                def __mark_move(move):
                    u"""移動時マーカーを置く。
                    """
                    __signal()
                    result = []
                    old_state = self.__piece.state
                    if self.__piece.move(self.__field, move):
                        result = __mark(
                            cmds+[_command.Breadcrumb(self.__piece.state)],
                            founds)
                        self.__piece.state = old_state
                    return result

                def __mark_rotate(clock_wise):
                    u"""回転時マーカーを置く。
                    """
                    __signal()
                    result = []
                    old_state = self.__piece.state
                    if (
                        self.__piece.test_rotate(self.__field, clock_wise) ==
                        _const.FLEXIBLE
                    ):
                        result = __mark(
                            cmds+[_command.Breadcrumb(self.__piece.state)],
                            founds)
                    self.__piece.state = old_state
                    return result
                is_prioritize_rotation = (
                    is_t_spin and self.__piece.is_three_corner(self.__field))
                if self.__field.is_left_side(self.__piece):
                    if self.__piece.top == self.__goal.top:
                        if self.__piece.left == self.__goal.left:
                            return (__mark_rotate, False),
                        else:
                            return (__mark_move, _const.RIGHT),
                    else:
                        moves = (
                            (__mark_move, _const.UP),
                            (__mark_move, _const.RIGHT),
                            (__mark_move, _const.LEFT))
                        rotates = (__mark_rotate, False), (__mark_rotate, True)
                        return (
                            rotates+moves if is_prioritize_rotation else
                            moves+rotates)
                else:
                    if self.__piece.top == self.__goal.top:
                        if self.__piece.left == self.__goal.left:
                            return (__mark_rotate, True),
                        else:
                            return (__mark_move, _const.LEFT),
                    else:
                        moves = (
                            (__mark_move, _const.UP),
                            (__mark_move, _const.LEFT),
                            (__mark_move, _const.RIGHT))
                        rotates = (__mark_rotate, True), (__mark_rotate, False)
                        return (
                            rotates+moves if is_prioritize_rotation else
                            moves+rotates)
            state = self.__piece.state
            if state == self.__goal:
                return cmds[::-1]
            if state in founds:
                return []
            else:
                founds.append(state)
            for func, param in __get_funcs():
                result = func(param)
                if result:
                    return result
            return []
        return __mark([_command.Breadcrumb(self.__piece.state)], [])

    @property
    def out(self):
        u"""出力キュー取得。
        """
        return self.__out

    @out.setter
    def out(self, value):
        u"""出力キュー設定。
        """
        self.__out = value
