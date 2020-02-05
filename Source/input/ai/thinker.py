#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""thinker.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

AIモジュール。
"""
import collections as _collections


class Thinker(object):
    u"""AI管理。
    """
    __slots__ = (
        "__ai", "__cmds", "__in", "__is_changed", "__is_thinking", "__out",
        "__debug_string", "__rival_system", "__system", "__time", "__waiting")
    __DEBUG = False
    __ROTATION_DECISIONS = {
        (0, 1): True, (0, 2): True,  (0, 3): False,
        (1, 2): True, (1, 3): True,  (1, 0): False,
        (2, 3): True, (2, 0): False, (2, 1): False,
        (3, 0): True, (3, 1): False, (3, 2): False}
    __TIMEOUT = 1
    __REACTION_RATE = 6
    __IS_ADVANCED_DETECTION = False

    def __init__(self, systems):
        u"""コンストラクタ。
        """
        import searcher as __searcher
        self.__cmds = _collections.deque()
        self.__waiting = 0
        self.__is_changed = False
        self.__is_thinking = False
        self.__debug_string = u""
        self.__system, self.__rival_system = systems
        self.__ai = __searcher.Searcher(self.__system.puzzle.drop_point)
        self.__in, self.__out = self.__ai.in_out
        self.__ai.start()

    def start(self):
        u"""AI計算開始。
        """
        if (
            self.__system.is_throwing and not self.__is_standby and
            not self.__is_thinking and not self.__cmds
        ):
            self.__in.put_nowait(("search", (
                self.__system.get_parameter(True),
                self.__rival_system.get_parameter(False))))
            self.__in.task_done()
            self.__time = 0
            self.__is_thinking = True

    def terminate(self):
        u"""AIプロセス終了処理。
        """
        self.__in.put_nowait(("terminate", ()))
        self.__in.task_done()
        self.__ai.join()
        self.__is_thinking = False

    # ---- Command ----
    def output(self):
        u"""コマンド送出とキュー出力取得。
        """
        import pygame as __pygame
        import utils.const as __const

        def __detect_timeout():
            u"""タイムアウト検出。
            __timeが__TIMEOUT秒以上の時、RuntimeErrorを送出する。
            """
            if (
                __const.IS_MULTIPROCESSING and self.__TIMEOUT != -1 and
                __const.FRAME_RATE*self.__TIMEOUT <= self.__time
            ):
                self.__ai.terminate()
                __pygame.quit()
                raise RuntimeError("Process Timeout.")

        def __detect_abnormal():
            u"""異常終了検出。
            """
            if __const.IS_MULTIPROCESSING and not self.__ai.is_alive():
                self.__ai.terminate()
                __pygame.quit()
                raise RuntimeError("Process Abnormal Termination.")

        def __output_command():
            u"""コマンド出力。
            """
            def __analyse_command():
                u"""コマンド解析。
                現在位置より上のコマンドは取り除かれる。
                """
                import itertools as __itertools
                state = self.__system.puzzle.piece.state
                self.__cmds = _collections.deque([
                    cmd for cmd in self.__cmds if cmd.state != state and
                    state.top <= cmd.state.top])
                if self.__cmds:
                    cmd_state = self.__cmds[0].state
                    if state.angle != cmd_state.angle:
                        return (
                            __const.DECISION_COMMAND if
                            self.__ROTATION_DECISIONS[
                                state.angle, cmd_state.angle
                            ] else __const.REMOVE_COMMAND)
                    if state.left < cmd_state.left:
                        return __const.RIGHT_COMMAND
                    if cmd_state.left < state.left:
                        return __const.LEFT_COMMAND
                    if 0 < rush and all(
                        (cmd_state.left, cmd_state.angle) ==
                        (cmd.state.left, cmd.state.angle) for cmd in
                        __itertools.islice(self.__cmds, 1, None)
                    ):
                        return __const.UP_COMMAND
                return __const.DOWN_COMMAND
            if (
                self.__system.is_throwing and
                not self.__is_standby and self.__cmds
            ):
                field = self.__system.puzzle.field
                parent = self.__system.puzzle.parent
                self.__system.puzzle.next
                if self.__IS_ADVANCED_DETECTION:
                    has_item = parent.has_item or parent.has_level_up
                    has_bad_item = parent.has_joker or parent.has_bad_level_up
                else:
                    has_item = parent.has_item
                    has_bad_item = parent.has_joker
                has_rs = self.__system.has_skill(__const.REVERSE_SORCERY_SKILL)
                has_item = has_item or parent.has_joker and has_rs
                is_more_than_half = field.highest <= field.height >> 1
                rush = has_item+is_more_than_half-has_bad_item
                waiting = self.__waiting+1
                input_interval = (
                    self.__REACTION_RATE << 1 if rush < 0 else
                    self.__REACTION_RATE)
                self.__waiting = waiting if waiting < input_interval else 0
                if self.__waiting == 0:
                    return (
                        self.__cmds.popleft().queue if
                        self.__cmds[0].is_basic else __analyse_command())
                self.__time = 0
            return ""

        def __get_queue():
            u"""キュー出力取得。
            """
            import Queue as __Queue

            def __search():
                u"""サーチ処理。
                """
                cmds, = result
                if self.__is_changed:
                    self.__is_changed = False
                else:
                    self.__cmds = _collections.deque(cmds)
                    if self.__DEBUG:
                        print u"コマンド取得。"
                self.__time = 0
                self.__is_thinking = False

            def __signal():
                u"""シグナル処理。
                """
                work, = result
                if work == "point_calc":
                    string = u"ポイント計算…"
                    if self.__debug_string != string:
                        self.__debug_string = string
                        if self.__DEBUG:
                            print self.__debug_string
                elif work == "route_search":
                    string = u"ルート検索…"
                    if self.__debug_string != string:
                        self.__debug_string = string
                        if self.__DEBUG:
                            print self.__debug_string
            try:
                name, result = self.__out.get_nowait()
                if name == "search":
                    __search()
                elif name == "signal":
                    __signal()
                self.__time = 0
            except __Queue.Empty:
                pass
        if self.__system.is_throwing:
            if not self.__is_standby:
                self.__time += 1
            __detect_timeout()
            command = __output_command()
            if command:
                return command
            else:
                __detect_abnormal()
                __get_queue()
        return ""

    def clear(self):
        u"""コマンド消去。
        """
        self.__cmds = _collections.deque()

    # ---- Property ----
    @property
    def __is_standby(self):
        u"""システム待機状態取得。
        """
        return (
            self.__system.puzzle.field.is_active or
            self.__system.puzzle.piece.is_rested or
            self.__system.is_game_over or self.__rival_system.is_game_over)

    @property
    def is_changed(self):
        u"""フィールド変化状態取得。
        """
        return self.__is_changed

    @is_changed.setter
    def is_changed(self, value):
        u"""フィールド変化状態設定。
        """
        self.__is_changed = bool(value)
        if self.__is_changed:
            self.__in.put_nowait(("stop", ()))
