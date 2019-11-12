#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""thinker.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

AIモジュール。
"""
import collections as _collections


class Thinker(object):
    u"""AI管理。
    """
    __slots__ = (
        "__ai", "__cmds", "__in", "__is_changed", "__is_thinking", "__out",
        "__debug_text", "__rival", "__system", "__time", "__waiting")
    __DEBUG = False
    __ROTATION_DECISIONS = {
        (0, 1): True, (0, 2): True,  (0, 3): False,
        (1, 2): True, (1, 3): True,  (1, 0): False,
        (2, 3): True, (2, 0): False, (2, 1): False,
        (3, 0): True, (3, 1): False, (3, 2): False}
    __TIMEOUT = 1
    __INPUT_INTERVAL = 8

    def __init__(self, system, rival):
        u"""コンストラクタ。
        """
        import ai as __ai
        self.__cmds = _collections.deque()
        self.__waiting = 0
        self.__is_changed = False
        self.__is_thinking = False
        self.__in = __ai.Searcher.get_queue()
        self.__out = __ai.Searcher.get_queue()
        self.__debug_text = u""
        self.__system = system
        self.__rival = rival
        self.__ai = __ai.Searcher(
            self.__in, self.__out, self.__system.blocks.drop_pos)
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
                self.__rival.get_parameter())))
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

        def __command_put():
            u"""コマンド出力。
            """
            def __command_analysis():
                u"""パンくずコマンド解析。
                現在位置より上のパンくずは取り除かれる。
                """
                state = self.__system.blocks.piece.state
                self.__cmds = _collections.deque([
                    cmd for cmd in self.__cmds if cmd.state != state and
                    state.top <= cmd.state.top])
                if self.__cmds:
                    cmd_state = self.__cmds[0].state
                    if state.angle != cmd_state.angle:
                        return (
                            __const.DECISION_COMMAND if
                            self.__ROTATION_DECISIONS[
                                state.angle, cmd_state.angle] else
                            __const.REMOVE_COMMAND)
                    if state.left < cmd_state.left:
                        return __const.RIGHT_COMMAND
                    if cmd_state.left < state.left:
                        return __const.LEFT_COMMAND
                return __const.DOWN_COMMAND
            if (
                self.__system.is_throwing and not self.__is_standby and
                self.__cmds
            ):
                waiting = self.__waiting+1
                input_interval = (
                    self.__INPUT_INTERVAL >> 1 if
                    self.__system.blocks.has_item else self.__INPUT_INTERVAL)
                self.__waiting = waiting if waiting < input_interval else 0
                if self.__waiting == 0:
                    return (
                        self.__cmds.popleft().queue if
                        self.__cmds[0].is_basic else __command_analysis())
                self.__time = 0
            return ""

        def __get_queue():
            u"""キュー出力取得。
            """
            import Queue as __Queue

            def __search_process():
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

            def __signal_process():
                u"""シグナル処理。
                """
                work, = result
                if work == "point_calc":
                    text = u"ポイント計算…"
                    if self.__debug_text != text:
                        self.__debug_text = text
                        if self.__DEBUG:
                            print self.__debug_text
                elif work == "route_search":
                    text = u"ルート検索…"
                    if self.__debug_text != text:
                        self.__debug_text = text
                        if self.__DEBUG:
                            print self.__debug_text
            try:
                name, result = self.__out.get_nowait()
                if name == "search":
                    __search_process()
                elif name == "signal":
                    __signal_process()
                self.__time = 0
            except __Queue.Empty:
                pass
        if self.__system.is_throwing:
            if not self.__is_standby:
                self.__time += 1
            __detect_timeout()
            command = __command_put()
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

    @property
    def __is_standby(self):
        u"""システム待機状態取得。
        """
        return (
            self.__system.blocks.field.is_active or
            self.__system.blocks.piece.is_rested or
            self.__system.is_game_over or self.__rival.is_game_over)

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
