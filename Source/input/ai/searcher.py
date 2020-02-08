#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""searcher.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

コマンド探索モジュール。
"""
import pieces as _pieces
import utils.const as _const
if _const.IS_MULTIPROCESSING:
    import multiprocessing as __multiprocessing
    __PPType = __multiprocessing.Process
    _PPQueue = __multiprocessing.JoinableQueue
else:
    import threading as __threading
    import Queue as __Queue
    __PPType = __threading.Thread
    _PPQueue = __Queue.Queue


class Searcher(__PPType):
    u"""コマンドを作成する。
    アルカナの使用、ピースのルートを設定。
    """
    __MAX_DEPTH_WEIGHT = 0
    __MIN_DEPTH_WEIGHT = 0
    __AVG_DEPTH_WEIGHT = 0
    __HOLE_PREVENTION_WEIGHT = 3
    __SMOOTHNESS_WEIGHT = 1
    __BLOCKS_ABOVE_OF_HOLES_WEIGHT = 1
    __ADJACENT_SPACES_WEIGHT = 0
    __GOAL_DISTANCE_WEIGHT = 0
    __MALIGNANCY_WEIGHT = 1
    __UNLOCK_WEIGHT = 5

    def __init__(self, drop_point):
        u"""コンストラクタ。
        """
        import armament.collectible as __collectible
        super(Searcher, self).__init__()
        self.__in = _PPQueue()
        self.__out = _PPQueue()
        self.__drop_point = _pieces.State(drop_point)
        self.__is_drive = True
        self.__is_stop = False
        self.__collectible = __collectible.get_all()

    def run(self):
        u"""AIの起動。
        """
        import time as __time
        import command as __command

        def __get_tactics():
            u"""カード使用コマンドを決定。
            """
            def __get_deletion():
                u"""カードの削除コマンドを設定。
                """
                for cmd, card in zip((
                    _const.USE5_COMMAND, _const.USE6_COMMAND,
                    _const.USE7_COMMAND, _const.USE8_COMMAND
                ), arcana):
                    if (
                        card.type == _const.JOKER_ARCANUM and
                        prm_self.has_purify or
                        card.type == _const.SUMMON_ARCANUM and
                        (prm_self.is_full_group or prm_self.has_soul_eat)
                    ):
                        return [__command.Simple(cmd)]
                return []
            if prm_self.is_arcana_available:
                arcana = [self.__collectible[i] for i in prm_self.hand]
                for cmd, arcanum in zip((
                    _const.USE1_COMMAND, _const.USE2_COMMAND,
                    _const.USE3_COMMAND, _const.USE4_COMMAND
                ), arcana):
                    if arcanum.type == _const.JOKER_ARCANUM:
                        weight = _const.NUMBER_OF_STAR*prm_self.jokers
                        if prm_self.has_reverse_sorcery or (
                            prm_self.resource.total <= weight
                        ) and not prm_self.has_purify:
                            return [__command.Simple(cmd)]
                    elif (
                        arcanum.type == _const.SUMMON_ARCANUM and
                        arcanum.is_available((prm_self, prm_other))
                    ):
                        return [__command.Simple(cmd)]
                    elif arcanum.type == _const.SORCERY_ARCANUM:
                        altered = arcanum.adapt(
                            None if prm_self.catalyst == -1 else
                            self.__collectible[prm_self.catalyst])
                        sorcery = altered if altered else arcanum
                        if sorcery.is_available((prm_self, prm_other)):
                            return [__command.Simple(cmd)]
                deletion = __get_deletion()
                if deletion:
                    return deletion
            return []

        def __search():
            u"""探索処理。
            """
            import marker as __marker

            def __calculate():
                u"""ピースポイント計算。
                """
                import point as __point

                def __get_search_area():
                    u"""検索範囲取得。
                    return: top, right, bottom, left.
                    """
                    def __topmost_block_line():
                        u"""フィールドの最も高いブロック行番号を取得。
                        """
                        height = field.table.height
                        for y in range(height):
                            if any(
                                cell.is_block for
                                cell in field.table.get_line(y)
                            ):
                                return y
                        return height
                    top = max(__topmost_block_line(), target.bottom)
                    right = field.table.width-1
                    bottom = field.table.height+target.height-1
                    left = -(target.width-1)
                    return top, right, bottom, left

                def __is_landingable():
                    u"""ピース設置可能判定。
                    """
                    old_state = target.state
                    if (
                        not field.is_outer(target) and
                        not field.is_collide(target) and
                        not target.move(field, _const.DOWN)
                    ):
                        return True
                    else:
                        target.state = old_state
                        return False

                def __set_point():
                    u"""得点設定。
                    """
                    def __get_roughness():
                        u"""フィールドの粗さを取得する。
                        """
                        width = virtual.table.width
                        surface = map(
                            lambda block: virtual.height-1 if
                            block is None else block.point.top, tuple(
                                virtual.table.get_topmost_block(col) for
                                col in range(width)))
                        return (
                            surface[0]-surface[1]+surface[-1]-surface[-2]+sum(
                                abs(surface[col]-surface[col+1]) for
                                col in range(1, width-2)))

                    def __get_closures(x):
                        u"""ホールの上に存在するブロック数を取得。
                        """
                        lowest_space = virtual.table.get_lowest_space(x)
                        lowest_space_height = (
                            lowest_space.point.top if
                            lowest_space else 0)
                        lowest_hole = virtual.table.get_lowest_hole(x)
                        return (
                            lowest_hole.point.top-lowest_space_height if
                            lowest_hole else 0)

                    def __get_unlock(field):
                        u"""アンロック可能点数取得。
                        """
                        def __has_pair(line):
                            u"""ライン上に鍵と宝箱のペアが存在する場合に真。
                            """
                            return any(
                                cell.is_locked for cell in line) and any(
                                cell.name in _const.KEY_NAMES.split("#") for
                                cell in line)
                        lines = (
                            field.table.get_line(y) for
                            y in range(field.table.height))
                        return sum(__has_pair(line) for line in lines)

                    def __get_stack():
                        u"""フィールドの積み重ねを取得。
                        """
                        result = 0
                        width = virtual.table.width
                        for col in range(width):
                            block = virtual.table.get_topmost_block(col)
                            if block:
                                result += virtual.height-block.point.top
                        return result/width
                    virtual = field.virtual
                    squares = virtual.squares
                    depths = tuple(block.point.y for block in target.blocks)
                    point.max_depth = max(depths) << self.__MAX_DEPTH_WEIGHT
                    point.min_depth = min(depths) << self.__MIN_DEPTH_WEIGHT
                    point.avg_depth = (
                        sum(depths)/len(depths) << self.__AVG_DEPTH_WEIGHT)
                    point.goal_distance = abs(
                        target.state.left-self.__drop_point.left
                    )+abs(
                        target.state.top-self.__drop_point.top
                    ) << self.__GOAL_DISTANCE_WEIGHT
                    target.stamp(virtual)
                    point .unlock = (
                        __get_unlock(virtual) << self.__UNLOCK_WEIGHT)
                    if point.is_t_spin:
                        virtual.set_super_drop()
                    point.completions = len(
                        virtual.simple_complete()
                    ) << __get_stack()
                    virtual.turn()
                    point.hole_prevention = squares-sum(
                        1 for cell in virtual.table.below if cell.is_hole
                    ) << self.__HOLE_PREVENTION_WEIGHT
                    point.smoothness = (
                        squares-__get_roughness() << self.__SMOOTHNESS_WEIGHT)
                    point.block_above_of_holes = squares-sum(
                        __get_closures(x) for
                        x in range(virtual.table.width)
                    ) << self.__BLOCKS_ABOVE_OF_HOLES_WEIGHT
                    point.adjasent_spaces = sum(
                        1 for cell in virtual.table if cell.is_adjacent
                    ) << self.__ADJACENT_SPACES_WEIGHT
                    point.malignancy = (squares << 2)-sum(
                        block.get_malignancy() for block in virtual.blocks
                    ) << self.__MALIGNANCY_WEIGHT
                points = []
                for is_hold, target in enumerate(
                    (piece,) if prm_self.is_hold_captured else
                    (piece, hold)
                ):
                    top, right, bottom, left = __get_search_area()
                    for angle in range(target.angles):
                        if (
                            target.pruning == _const.SINGLE_PRUNING and
                            angle in (_const.A90, _const.A180, _const.A270)
                        ) or (
                            target.pruning == _const.HALF_PRUNING and
                            angle in (_const.A180, _const.A270)
                        ):
                            continue
                        for x in range(left, right):
                            for y in range(top, bottom):
                                if (
                                    _const.IS_MULTIPROCESSING and
                                    self.__out.empty()
                                ):
                                    self.__out.put_nowait(
                                        ("signal", ("point_calc",)))
                                    self.__out.task_done()
                                if not self.__in.empty():
                                    name, _ = self.__in.get_nowait()
                                    if name in ("stop", "terminate"):
                                        self.__is_stop = True
                                        if name == "terminate":
                                            self.__is_drive = False
                                        return []
                                target.angle = angle
                                target.bottomleft = x, y
                                if __is_landingable():
                                    point = __point.Point(
                                        target.state, is_hold, target.is_t and
                                        target.is_three_corner(field) and
                                        target.is_flexible(field))
                                    __set_point()
                                    points.append(point)
                return points
            hold_command = __command.Simple(_const.HOLD_COMMAND)
            if prm_self.hold:
                if not self.__is_stop:
                    field = _pieces.Field(
                        _pieces.Pattern(*prm_self.field), is_virtual=True)
                    field.skills = prm_self.skills
                    piece = _pieces.Falling(
                        _pieces.Rotatable(*prm_self.piece), is_virtual=True
                    ).virtual
                    hold = _pieces.Falling(
                        _pieces.Rotatable(*prm_self.hold), is_virtual=True
                    ).virtual
                    piece.topleft = prm_self.piece_pos
                    goal = piece.state
                    points = __calculate()
                    while points:
                        max_point = max(points)
                        points.remove(max_point)
                        target = hold if max_point.is_hold else piece
                        target.state = max_point.state
                        marker = __marker.Marker(field, target, goal)
                        marker.out = self.__out
                        result = marker.mark(
                            max_point.is_t_spin and max_point.completions)
                        if result:
                            if max_point.is_hold:
                                result = [hold_command]+result
                            return result
                return [__command.Simple(_const.UP_COMMAND)]
            else:
                return [hold_command]
        waiting_time = 1./_const.FRAME_RATE
        while self.__is_drive:
            __time.sleep(waiting_time)
            if not self.__in.empty():
                cmd, args = self.__in.get_nowait()
                if cmd == "search":
                    prm_self, prm_other = args
                    tactics = __get_tactics()
                    cmds = tactics if tactics else __search()
                    if cmds or (not cmds and self.__is_stop):
                        self.__out.put_nowait(("search", (cmds,)))
                        self.__out.task_done()
                        self.__is_stop = False
                elif cmd == "terminate":
                    self.__is_drive = False

    @property
    def in_out(self):
        u"""入出力キュー取得。
        return in, out.
        """
        return self.__in, self.__out
