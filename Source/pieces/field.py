#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""field.py

Copyright(c)2019 Yukio Kuro
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
        "__skills", "__table", )

    def __init__(self, pattern, skills, is_virtual=False):
        u"""コンストラクタ。
        """
        import table as __table
        super(Field, self).__init__(pattern)
        self.__skills = skills
        self.__dug = -1
        self.__is_super_drop = False
        self.__table = __table.Table(
            (pattern.width, pattern.height), self, is_virtual)
        self.__is_virtual = is_virtual
        self.add(*pattern.get_blocks(is_virtual=self.__is_virtual))
        self.__set_states()

    def __repr__(self):
        u"""文字列表現取得。
        """
        return u"<{name}>".format(name=self.__class__.__name__)

    def __getitem__(self, value):
        u"""ライン取得。
        """
        return self.__table[value][:]

    def __setitem__(self, key, value):
        u"""ライン設定。
        """
        self.__table[key] = value

    def __set_states(self):
        u"""ブロック状態などを設定。
        空白、フィールド最高部、リンク、エッジ設定。
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
                vline = self.__table.get_vline(x)
                border_block = self.__table.get_topmost_block(x)
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

        def __set_adjacents():
            u"""隣接スペース設定。
            フィールド上ホールの、横方向に存在する空白を隣接スペースとする。
            """
            for y, line in enumerate(self.__table):
                for x, cell in enumerate(line):
                    if cell.is_hole:
                        for space in self.__table.get_side_space(x, y):
                            space.state = 3
        __set_holes()
        __set_adjacents()
        self.__highest = (
            min(block.height for block in self._blocks) if self._blocks else
            self.height)
        for block in self._blocks:
            block.set_link()
            if not self.__is_virtual:
                block.set_field_edge()

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
            self.__table.remove(block)
        self._blocks = [block for block in self._blocks if block not in blocks]

    def press(self, pressure, level):
        u"""フィールド下方にブロック列を生成する。
        """
        import operate as __operate

        def __dig_hole():
            u"""プレスパターンの穴を作る。
            """
            is_complete_assist = \
                _const.COMPLETE_ASSIST_SKILL_NAME in self.__skills.split("#")
            width = len(shapes)-(1 if is_complete_assist else 0)
            if self.__dug == -1:
                self.__dug = _random.randint(0, width)
            self.__dug = _random.choice(
                range(self.__dug)+range(self.__dug+1, width))
            return (
                shapes[:self.__dug] +
                shapes[self.__dug+(2 if is_complete_assist else 1):])

        def __shift():
            u"""ブロック押上。
            """
            for block in self._blocks:
                block.shift(_const.UP)
            self._blocks = [
                block for block in self._blocks if 0 <= block.point.top]
        normal, solid, adamant = (
            (name, 0, (1, 1)) for name in ("Normal", "Solid", "Adamant"))
        shapes = [((x, 0), (
            adamant if level == _const.ADAMANT_PRESS_LEVEL >> 1 else
            solid if level == _const.SOLID_PRESS_LEVEL >> 1 else normal
        )) for x in range(self.width)]
        pattern = _pattern.Pattern((self.width, 1), __dig_hole())
        for _ in range(int(pressure)):
            __shift()
            __operate.Dropping(pattern, (0, self.height-1)).stamp(self)
        self.__set_states()

    def __calc(self, one_pieces, resorce, is_super_drop):
        u"""コンプリート計算処理。
        """
        def __crack():
            u"""ブロックをクラックする。
            """
            def __get_flag():
                u"""クラックフラグ取得。
                """
                flag = 0b0
                if all(
                    block.is_invincible or
                    block.is_blank for block in _one_piece
                ):
                    flag |= _const.FORCE_CRACK
                if (
                    any(block.is_key for block in _one_piece) or
                    _const.PHANTOM_THIEF_SKILL_NAME in skills
                ):
                    flag |= _const.UNLOCK_CRACK
                if any(
                    block.is_locked and
                    not block.is_opened for block in _one_piece
                ):
                    flag |= _const.TREASURE_CRACK
                flag |= sum(_flag for name, _flag in (
                    (_const.FIRE_EATER_SKILL_NAME, _const.FIRE_EATER_CRACK),
                    (_const.ICE_PICKER_SKILL_NAME, _const.ICE_PICKER_CRACK),
                    (_const.ACID_ERASER_SKILL_NAME, _const.ACID_ERASER_CRACK),
                    (_const.STONE_BREAKER_SKILL_NAME,
                     _const.STONE_BREAKER_CRACK),
                    (_const.POWER_STROKE_SKILL_NAME, _const.POWER_CRACK),
                    (_const.EXORCIST_SKILL_NAME, _const.EXORCIST_CRACK)
                ) if name in skills)
                return flag
            skills = self.__skills.split("#")
            for one_piece in one_pieces:
                _one_piece = {block for block in one_piece}
                for func in (
                    resorce.star_plus, resorce.shard_plus, resorce.star_minus,
                    resorce.chests_plus, resorce.get_arcana
                ):
                    func(_one_piece)
                for cell in _one_piece:
                    cell.crack(__get_flag())
        __crack()
        for block in self.__table.get_all():
            if (
                block.is_blank and (self.__is_super_drop or is_super_drop) or
                block.is_fragile
            ):
                block.crack()
        for block in self.__table.get_roots():
            if block:
                block.move_calc()

    def completion(self):
        u"""補完処理。
        一度目のループ処理でブロック消去。
        二度目のループでドロップダウン。
        ※ブロック構成が変わるため、二度の__table.get_all()が必要。
        """
        for block in self.__table.get_all():
            block.remove()
        for block in self.__table.get_all():
            block.drop_down()

    def __get_onepieces(self):
        u"""コンプリートライン取得。
        """
        onepieces = self.__table.get_onepieces()
        if _const.COMPLETE_ASSIST_SKILL_NAME in self.__skills.split("#"):
            onepieces = self.__table.get_onepieces(self.width-1)
        return onepieces

    def simple_completion(self, resorce, is_super_drop):
        u"""AI用の補完処理関数。
        """
        self.__set_states()
        one_pieces = self.__get_onepieces()
        if one_pieces:
            self.__calc(one_pieces, resorce, is_super_drop)
            self.completion()
            return one_pieces+self.simple_completion(resorce, is_super_drop)
        return one_pieces

    def sub_completion(self, resorce):
        u"""副次的な補完処理。
        """
        import material.sound as __sound
        self.__set_states()
        one_pieces = self.__get_onepieces()
        if one_pieces:
            deleted = len(one_pieces)
            __sound.SE.play("Complete_"+(
                "3" if 4 <= deleted else "2" if 2 <= deleted else "1"))
            self.__calc(one_pieces, resorce, False)
            for block in self._blocks:
                block.disappear()
        return one_pieces

    def turn(self):
        u"""ブロック変化。
        """
        def __matango_growth():
            u"""キノコ成長処理。
            """
            for y in range(self.height-1):
                for x in range(self.width-1):
                    self.__table.get_cell((x, y))
                    blocks = (
                        self.__table.get_cell((x, y)),
                        self.__table.get_cell((x+1, y)),
                        self.__table.get_cell((x, y+1)),
                        self.__table.get_cell((x+1, y+1)))
                    if all(block.name == "Matango" for block in blocks):
                        self.remove(*blocks)
                        self.add(_cells.get("LargeMatango")(
                            (x, y, 2, 2), 0, self.__is_virtual))
        blocks = self.__table.get_all()
        for block in blocks:
            block.effect()
        for block in blocks:
            block.generation()
        __matango_growth()
        self.__set_states()
        self.__is_super_drop = False

    def replace(self, parameter, target):
        u"""ブロック置き換え。
        """
        changed = False
        new, old = target
        blocks = tuple(
            block for block in self._blocks if block.is_changeable and
            isinstance(block, tuple(_cells.get(name) for name in old)))
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
                    block.generation()
                    changed = True
        return changed

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

    @property
    def one_eighth(self):
        u"""マス目の1/8を取得。
        """
        return self.squares >> 3

    @property
    def highest(self):
        u"""最高部取得。
        """
        return self.__highest

    @property
    def table(self):
        u"""表を取得。
        """
        return self.__table

    @property
    def parameter(self):
        u"""フィールド生成パラメータ取得。
        """
        return self.size, tuple(block.parameter for block in self._blocks)

    @property
    def virtual(self):
        u"""AI用コピー取得。
        """
        return self.__class__(
            _pattern.Pattern(*self.parameter), self.__skills, True)

    @property
    def packet(self):
        u"""攻撃行動に必要なポイント取得。
        """
        return self.width*_const.SINGLE_SCORE

    @property
    def has_locked_chest(self):
        u"""宝箱・ミミック判定。
        """
        locked = _const.LOCKED_NAMES.split("#")
        return any(block.name in locked for block in self._blocks)

    @property
    def is_moving(self):
        u"""ブロック移動判定。
        """
        for block in self._blocks:
            if block.is_moving is True:
                return True
        return False

    @property
    def is_disappear(self):
        u"""ブロック消滅判定。
        """
        for block in self._blocks:
            if block.is_disappear is True:
                return True
        return False

    @property
    def is_active(self):
        u"""ブロック動作判定。
        """
        for block in self._blocks:
            if block.is_active:
                return True
        return False

    @property
    def is_super_drop(self):
        u"""スーパードロップ状態取得。
        """
        return self.__is_super_drop

    def set_super_drop(self):
        u"""スーパードロップ状態設定。
        """
        self.__is_super_drop = True
