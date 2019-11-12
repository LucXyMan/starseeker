#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""searcher.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

コマンド探索モジュール。
"""
import Queue as _Queue
import pieces as _pieces
import utils.const as _const
if _const.IS_MULTIPROCESSING:
    import multiprocessing as __multiprocessing
    _PPType = __multiprocessing.Process
    _PPQueue = __multiprocessing.JoinableQueue
else:
    import threading as __threading
    _PPType = __threading.Thread
    _PPQueue = _Queue.Queue


class Searcher(_PPType):
    u"""コマンド探索。
    ピースの目的地を設定する。
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

    @classmethod
    def get_queue(cls):
        u"""AIが使用するキューを取得。
        """
        return _PPQueue()

    def __init__(self, in_, out, drop_pos):
        u"""コンストラクタ。
        """
        super(Searcher, self).__init__()
        self.__in = in_
        self.__out = out
        self.__drop_pos = _pieces.State(drop_pos)
        self.__is_drive = True
        self.__is_stop = False

    def run(self):
        u"""AIの起動。
        """
        import time as __time
        import command as __command

        def __tactics():
            u"""カード使用コマンドを決定。
            """
            import armament.collectible as __collectible

            def __delete():
                u"""カードの削除コマンドを設定。
                """
                cmds = (
                    _const.USE5_COMMAND, _const.USE6_COMMAND,
                    _const.USE7_COMMAND, _const.USE8_COMMAND)
                if _const.PURIFY_SKILL_NAME in prm_s.skills.split("#"):
                    for cmd, card in zip(cmds, hand):
                        if card.type == _const.JOKER_TYPE:
                            hand.remove(card)
                            return [__command.Simple(cmd)]
                if prm_s.is_full_group:
                    for cmd, card in zip(cmds, hand):
                        if card.type == _const.SUMMON_TYPE:
                            hand.remove(card)
                            return [__command.Simple(cmd)]
                if _const.SOUL_EAT_SKILL_NAME in prm_s.skills.split("#"):
                    for cmd, card in zip(cmds, hand):
                        if card.type in (
                            _const.SUMMON_TYPE, _const.SORCERY_TYPE
                        ):
                            hand.remove(card)
                            return [__command.Simple(cmd)]
                return []
            result = []
            if prm_s.is_sorcery_usable:
                hand = [__collectible.get(i) for i in prm_s.hand]
                for _ in range(
                    2 if _const.DOUBLE_SPELL_SKILL_NAME in
                    prm_s.skills.split("#") else 1
                ):
                    for cmd, item in zip((
                        _const.USE1_COMMAND, _const.USE2_COMMAND,
                        _const.USE3_COMMAND, _const.USE4_COMMAND), hand
                    ):
                        is_used = False
                        piled = None if prm_s.pile == -1 else item.adapt(
                            __collectible.get(prm_s.pile))
                        if (
                            item.type == _const.SUMMON_TYPE and
                            item.is_usable(prm_s, prm_o)
                        ):
                            is_used = True
                        elif (
                            item.type == _const.SORCERY_TYPE and
                            (piled if piled else item).is_usable(
                                prm_s, prm_o)
                        ):
                            if item.name == u"エクスチェンジ":
                                item_state_self = prm_s.hold_item_state
                                item_state_other = prm_o.hold_item_state
                                prm_s.hold_item_state = item_state_other
                                prm_o.hold_item_state = item_state_self
                            is_used = True
                        elif (
                            item.type == _const.JOKER_TYPE and
                            _const.PURIFY_SKILL_NAME not in
                            prm_s.skills.split("#")
                        ):
                            is_used = True
                        if is_used:
                            result.append(__command.Simple(cmd))
                            hand.remove(item)
                            break
                    result.extend(__delete())
            return result

        def __search():
            u"""探索処理。
            """
            import marker as __marker

            def __point_calc():
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
                    return (
                        max(__topmost_block_line(), target.bottom),
                        field.table.width-1,
                        field.table.height+target.height-1,
                        -(target.width-1))

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
                    def __get_smoothness():
                        u"""フィールドの”表面”のなめらかさを取得する。
                        なめらかさは、フィールド各列と隣接する列との、一番上のブロック差の合計。
                        フィールドのセルの数からマイナスする負の数。
                        """
                        width = _field.table.width
                        surface = map(
                            lambda block: _field.height-1 if
                            block is None else block.point.top, tuple(
                                _field.table.get_topmost_block(col) for
                                col in range(width)))
                        return (
                            surface[0]-surface[1]+surface[-1]-surface[-2] +
                            sum(abs(surface[col]-surface[col+1]) for
                                col in range(1, width-2)))

                    def __get_blocks_above_hole(x):
                        u"""ホールの上に存在するブロック数を取得。
                        """
                        lowest_space = _field.table.get_lowest_space(x)
                        lowest_space_height = (
                            lowest_space.point.top if lowest_space else 0)
                        lowest_hole = _field.table.get_lowest_hole(x)
                        return (
                            lowest_hole.point.top-lowest_space_height if
                            lowest_hole else 0)

                    def __get_unlock():
                        u"""解除される宝箱・ミミック数取得。
                        """
                        return sum(1 for line in _field if (any(
                            block.name in _const.LOCKED_NAMES.split("#") for
                            block in line) and any(
                            block.name in _const.KEY_NAMES.split("#") for
                            block in line)))

                    def __get_field_heap():
                        u"""フィールドの積み重ねを取得。
                        """
                        result = 0
                        width = _field.table.width
                        for col in range(width):
                            block = _field.table.get_topmost_block(col)
                            if block:
                                result += _field.height-block.point.top
                        return result/width
                    _field = field.virtual
                    squares = _field.squares
                    depths = tuple(block.point.y for block in target.blocks)
                    point.max_depth = max(depths) << self.__MAX_DEPTH_WEIGHT
                    point.min_depth = min(depths) << self.__MIN_DEPTH_WEIGHT
                    point.avg_depth = sum(depths)/len(
                        depths) << self.__AVG_DEPTH_WEIGHT
                    point.goal_distance = abs(
                        target.state.left-self.__drop_pos.left
                    )+abs(
                        target.state.top-self.__drop_pos.top
                    ) << self.__GOAL_DISTANCE_WEIGHT
                    target.stamp(_field)
                    point .unlock = __get_unlock() << self.__UNLOCK_WEIGHT
                    point.completions = len(_field.simple_completion(
                        prm_s.resorce.copy, point.is_t_spin_chance)
                    ) << __get_field_heap()
                    _field.turn()
                    point.hole_prevention = squares-sum(
                        1 for cell in _field.table.get_below_cells() if
                        cell.is_hole
                    ) << self.__HOLE_PREVENTION_WEIGHT
                    point.smoothness = (
                        squares-__get_smoothness()) << self.__SMOOTHNESS_WEIGHT
                    point.block_above_of_holes = (squares-sum(
                        __get_blocks_above_hole(x) for
                        x in range(_field.table.width))
                    ) << self.__BLOCKS_ABOVE_OF_HOLES_WEIGHT
                    point.adjasent_spaces = sum(
                        sum(1 for cell in line if cell.is_adjacent) for
                        line in _field.table) << self.__ADJACENT_SPACES_WEIGHT
                    point.malignancy = (squares << 2)-sum(
                        block.get_malignancy() for
                        block in _field.blocks) << self.__MALIGNANCY_WEIGHT
                points = []
                for is_hold, target in enumerate(
                    (piece,) if prm_s.is_hold_captured else (piece, hold)
                ):
                    top, right, bottom, left = __get_search_area()
                    for angle in range(target.angles):
                        if (
                            target.pruning == _const.SINGLE_PRUNING and
                            angle in (_const.A90, _const.A180, _const.A270)
                        ):
                            continue
                        elif (
                            target.pruning == _const.HALF_PRUNING and
                            angle in (_const.A180, _const.A270)
                        ):
                            continue
                        for y in range(top, bottom):
                            for x in range(left, right):
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
                                        target.is_three_corner(field))
                                    __set_point()
                                    points.append(point)
                return points
            field = _pieces.Field(
                _pieces.Pattern(*prm_s.field), prm_s.skills, is_virtual=True)
            piece = _pieces.Dropping(
                _pieces.Rotatable(*prm_s.piece), is_virtual=True).virtual
            piece.topleft = prm_s.piece_pos
            goal = piece.state
            hold_command = __command.Simple(_const.HOLD_COMMAND)
            if prm_s.hold:
                hold = _pieces.Dropping(_pieces.Rotatable(*prm_s.hold)).virtual
                points = __point_calc()
                if not self.__is_stop:
                    while points:
                        max_point = max(points)
                        points.remove(max_point)
                        target = hold if max_point.is_hold else piece
                        target.state = max_point.state
                        marker = __marker.Marker(field, target, goal)
                        marker.out = self.__out
                        result = marker.marking()
                        if result:
                            if max_point.is_hold:
                                result = [hold_command]+result
                            return result
                return [__command.Simple(_const.UP_COMMAND)]
            else:
                return [hold_command]
        wait_time = 1./_const.FRAME_RATE
        while self.__is_drive:
            __time.sleep(wait_time)
            if not self.__in.empty():
                cmd, args = self.__in.get_nowait()
                if cmd == "search":
                    prm_s, prm_o = args
                    tactics = __tactics()
                    cmds = tactics if tactics else __search()
                    if cmds or (not cmds and self.__is_stop):
                        self.__out.put_nowait(("search", (cmds,)))
                        self.__out.task_done()
                        self.__is_stop = False
                elif cmd == "terminate":
                    self.__is_drive = False
