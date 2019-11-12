#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""field.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

フィールドモジュール。
"""
import random as _random
import utils.const as _const
import cells as _cells
import pattern as _pattern
import piece as __piece


class Field(__piece.Piece):
    u"""フィールド。
    """
    __slots__ = (
        "__dug", "__highest", "__is_super_drop", "__is_virtual", "__levels",
        "__skills", "__table")

    def __init__(self, pattern, is_virtual=False):
        u"""コンストラクタ。
        """
        import table as __table
        super(Field, self).__init__(pattern)
        self.__is_super_drop = False
        self.__is_virtual = is_virtual
        self.__dug = -1
        self.__skills = ""
        self.__table = __table.Table(
            (pattern.width, pattern.height), self, is_virtual)
        self.add(*pattern.get_blocks(is_virtual=self.__is_virtual))
        self.__set_state()

    def __repr__(self):
        u"""文字列表現取得。
        """
        return u"<{name}>".format(name=self.__class__.__name__)

    # ---- Add and Remove ----
    def add(self, *blocks):
        u"""ブロック追加。
        """
        for block in blocks:
            self._blocks.append(block)
            self.__table.write(block)

    def remove(self, *blocks):
        u"""ブロック削除。
        """
        for block in blocks:
            self.__table.erase(block)
        self._blocks = [block for block in self._blocks if block not in blocks]

    # ---- Completion ----
    def __calc(self, one_pieces, resorce=None):
        u"""コンプリート計算処理。
        """
        def __crack():
            u"""ブロックをクラックする。
            """
            def __get_flag():
                u"""クラックフラグ取得。
                """
                def __get_name(skill):
                    u"""スキル名取得。
                    """
                    name, _ = skill.split("#")
                    return name
                flag = 0b0
                if all(
                    block.is_invincible or block.is_blank for
                    block in one_piece
                ):
                    flag |= _const.FORCE_CRACK
                name = __get_name(_const.PHANTOM_THIEF_SKILL)
                if any(
                    block.is_key for block in one_piece
                ) or name in skills:
                    flag |= _const.UNLOCK_CRACK
                if any(
                    block.is_locked and not block.is_opened for
                    block in one_piece
                ):
                    flag |= _const.TREASURE_CRACK
                flag |= sum(_flag for skill, _flag in (
                    (_const.FIRE_EATER_SKILL, _const.FIRE_EATER_CRACK),
                    (_const.ICE_PICKER_SKILL, _const.ICE_PICKER_CRACK),
                    (_const.ACID_ERASER_SKILL, _const.ACID_ERASER_CRACK),
                    (_const.STONE_BREAKER_SKILL,  _const.STONE_BREAKER_CRACK),
                    (_const.POWER_STROKE_SKILL, _const.POWER_CRACK),
                    (_const.EXORCIST_SKILL, _const.EXORCIST_CRACK)) if
                    __get_name(skill) in skills)
                return flag
            skills = self.__skills.split("#")
            for one_piece in one_pieces:
                if resorce:
                    resorce.extract(one_piece)
                flag = __get_flag()
                for cell in one_piece:
                    cell.crack(flag)
            for block in self.__table.sorted:
                if block.is_blank and self.__is_super_drop or block.is_fragile:
                    block.crack()
        __crack()
        for block in self.__table.root:
            block.move_calc()

    def completion(self):
        u"""補完処理。
        一度目のループ処理でブロック消去。
        二度目のループでドロップダウン。
        """
        for block in self.__table.sorted:
            block.remove()
        for block in self.__table.sorted:
            block.drop_down()

    def simple_completion(self):
        u"""AI用の補完処理関数。
        """
        self.__set_state()
        one_pieces = self.__one_pieces
        if one_pieces:
            self.__calc(one_pieces)
            self.completion()
            return one_pieces+self.simple_completion()
        return one_pieces

    def sub_completion(self, resorce):
        u"""副次的な補完処理。
        """
        import material.sound as __sound
        self.__set_state()
        one_pieces = self.__one_pieces
        if one_pieces:
            deleted = len(one_pieces)
            __sound.SE.play("complete_"+(
                "3" if 4 <= deleted else
                "2" if 2 <= deleted else
                "1"))
            self.__calc(one_pieces, resorce=resorce)
            for block in self._blocks:
                block.disappear()
        return one_pieces

    # ---- Process ----
    def __get_2x2(self, point):
        u"""2x2マスのセル取得。
        """
        x, y = point
        return (
            self.__table.get_cell((x, y)),
            self.__table.get_cell((x+1, y)),
            self.__table.get_cell((x, y+1)),
            self.__table.get_cell((x+1, y+1)))

    def press(self, pressure, level):
        u"""フィールド下方にブロック列を生成する。
        """
        import operate as __operate

        def __get_dug():
            u"""穴空きパターン取得。
            """
            def __get_name(skill):
                u"""スキル名取得。
                """
                name, _ = skill.split("#")
                return name

            def __get_block():
                u"""基本プレスブロック取得。
                """
                for block, skill in (
                    ("Water", _const.WATER_PRESS_SKILL),
                    ("Chocolate", _const.CHOCOLATE_PRESS_SKILL)
                ):
                    if __get_name(skill) in skills:
                        return block
                return "Normal"
            normal, solid, adamant = ((name, 0, (1, 1)) for name in (
                __get_block(), "Solid", "Adamant"))
            type_ = (
                adamant if level == _const.ADAMANT_PRESS_LEVEL >> 1 else
                solid if level == _const.SOLID_PRESS_LEVEL >> 1 else
                normal)
            shapes = [((x, 0), type_) for x in range(self.width)]
            is_complete_assist = (
                __get_name(_const.COMPLETE_ASSIST_SKILL) in skills)
            width = len(shapes)-(1 if is_complete_assist else 0)
            if self.__dug == -1:
                self.__dug = _random.randint(0, width)
            self.__dug = _random.choice(
                range(self.__dug) +
                range(self.__dug+1, width))
            return (
                shapes[:self.__dug] +
                shapes[self.__dug+(2 if is_complete_assist else 1):])

        def __shift():
            u"""ブロック押上。
            """
            for block in self._blocks:
                block.shift(_const.UP)
            self._blocks = [
                block for
                block in self._blocks if 0 <= block.point.top]
        skills = self.__skills.split("#")
        pattern = _pattern.Pattern((self.width, 1), __get_dug())
        for _ in range(pressure):
            __shift()
            __operate.Dropping(pattern, (0, self.height-1)).stamp(self)
        self.__set_state()

    def replace(self, parameter, target):
        u"""ブロック置き換え。
        """
        changed = False
        new, old = target
        blocks = tuple(
            block for block in self._blocks if
            block.is_changeable and block.name in old)
        if blocks:
            if parameter:
                start, end = parameter
                if not (start == -1 or end == -1):
                    limit = len(blocks)
                    if end < limit:
                        blocks = _random.sample(blocks, _random.randint(
                            start, end if end < limit else limit))
                for block in blocks:
                    block.change(new)
                    block.generation(_cells.get)
                    changed = True
        return changed

    def hardening(self, turn):
        u"""ブロック硬質化処理。
        """
        def __growth():
            u"""基本ブロック巨大化。
            """
            def __replace():
                u"""ブロック4つをラージブロック1つに置き換え。
                """
                import collections as __collections
                cells = self.__get_2x2((x, y))
                if all(
                    cell.is_target(name) and cell.is_changeable for
                    cell in cells
                ):
                    self.remove(*cells)
                    Block = _cells.get(name)
                    most_common = __collections.Counter(
                        cell.state for cell in cells).most_common()
                    self.add(Block(
                        (x, y, 2, 2), most_common[0][0] | 0xF00,
                        self.__is_virtual))
                    return True
                return False
            is_grown = False
            for name in names:
                for x in range(self.width-1):
                    for y in range(self.height-1):
                        if __replace():
                            is_grown = True
            return is_grown

        def __rank_up():
            u"""基本ブロックランクアップ。
            """
            def __change(target):
                u"""ブロック変化。
                """
                is_changed = False
                new, old = target
                cell = self.__table.get_cell((x, y))
                if cell.is_target(old) and cell.is_changeable:
                    color = cell.color >> 1 if new == "Solid" else cell.color
                    if cell.change(new, color << 4 | cell.hp << 1):
                        cell.generation(_cells.get)
                        is_changed = True
                return is_changed
            is_changed = False
            normal, solid, adamant = names
            for x in range(self.width):
                for y in range(self.height):
                    if __change((adamant, solid)) or __change((solid, normal)):
                        is_changed = True
            return is_changed
        names = _const.BASIC_NAMES.split("#")
        is_rank_upped = __rank_up()
        is_grown = __growth()
        if is_grown or is_rank_upped:
            self.__set_state()
            return True
        return False

    def add_demon(self):
        u"""キングデーモン追加処理。
        """
        target_points = []
        names = (
            _const.BASIC_NAMES+"#" +
            _const.ITEM_NAMES+"#" +
            _const.SLIME_NAMES)
        for x in range(self.width-1):
            for y in range(self.height-1):
                if all(
                    cell.is_changeable and cell.is_target(names) for
                    cell in self.__get_2x2((x, y))
                ):
                    target_points.append((x, y))
        if target_points:
            x, y = _random.choice(target_points)
            self.remove(*self.__get_2x2((x, y)))
            Block = _cells.get("KingDemon")
            self.add(Block((x, y, 2, 2), 0, self.__is_virtual))
            self.__set_state()

    def turn(self):
        u"""ターン処理。
        """
        def __matango_growth():
            u"""キノコ成長処理。
            """
            for x in range(self.width-1):
                for y in range(self.height-1):
                    cells = self.__get_2x2((x, y))
                    if all(cell.is_target("Matango") for cell in cells):
                        self.remove(*cells)
                        Block = _cells.get("LargeMatango")
                        self.add(Block((x, y, 2, 2), 0, self.__is_virtual))
        for cell in self.__table.sorted:
            cell.effect()
        for cell in self.__table.sorted:
            cell.generation(_cells.get)
        __matango_growth()
        self.__set_state()
        self.__is_super_drop = False

    # ---- Detect ---
    def is_collide(self, piece):
        u"""piece衝突判定。
        """
        for block in piece.blocks:
            if block.is_collide(self):
                return True
        return False

    def is_outer(self, piece):
        u"""pieceはみ出し判定。
        """
        for block in piece.blocks:
            if (
                block.point.left < 0 or
                block.point.left+block.point.width > self.width or
                block.point.top < 0 or
                block.point.top+block.point.height > self.height
            ):
                return True
        return False

    def is_left_side(self, piece):
        u"""左側判定。
        pieceがフィールドの左側にあるか判定。
        """
        return True if piece.centerx < self.__table.centerx else False

    # ---- Setter ----
    def __set_state(self):
        u"""ブロック状態などを設定。
        空白、フィールド最高部、リンク、エッジ設定。
        """
        self.__table.set_state()
        self.__highest = min(
            block.point.top for block in self._blocks
        ) if self._blocks else self.height
        for block in self._blocks:
            block.link()
            if not self.__is_virtual:
                block.set_field_edge()

    def set_super_drop(self):
        u"""スーパードロップ状態を真に。
        """
        self.__is_super_drop = True

    # ---- Property ----
    @property
    def __one_pieces(self):
        u"""コンプリートライン取得。
        """
        name, _ = _const.COMPLETE_ASSIST_SKILL.split("#")
        length = (
            self.width-1 if name in self.__skills.split("#") else
            self.width)
        return self.__table.get_onepieces(length)

    @property
    def table(self):
        u"""表を取得。
        """
        return self.__table

    @property
    def packet(self):
        u"""攻撃行動に必要なポイント取得。
        """
        return self.width*_const.SINGLE_SCORE

    @property
    def skills(self):
        u"""スキル取得。
        """
        return self.__skills

    @skills.setter
    def skills(self, value):
        u"""スキル設定。
        """
        self.__skills = unicode(value)

    # ------ AI ------
    @property
    def parameter(self):
        u"""フィールド生成パラメータ取得。
        """
        return self.size, tuple(block.parameter for block in self._blocks)

    @property
    def virtual(self):
        u"""AI用コピー取得。
        """
        field = self.__class__(
            _pattern.Pattern(*self.parameter), is_virtual=True)
        field.skills = self.__skills
        return field

    # ------ Squares ------
    @property
    def one_eighth(self):
        u"""マス目の1/8を取得。
        """
        return self.squares >> 3

    @property
    def highest(self):
        u"""フィールド最高部取得。
        """
        return self.__highest

    # ------ Detect ------
    @property
    def is_moving(self):
        u"""ブロック移動判定。
        """
        return any(block.is_moving for block in self._blocks)

    @property
    def is_disappear(self):
        u"""ブロック消滅判定。
        """
        return any(block.is_disappear for block in self._blocks)

    @property
    def is_active(self):
        u"""ブロック動作判定。
        """
        return any(block.is_active for block in self._blocks)

    @property
    def is_super_drop(self):
        u"""スーパードロップ状態取得。
        """
        return self.__is_super_drop
