#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""hold.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ホールドピース管理モジュール。
"""
import pieces as _pieces
import utils.const as _const
import utils.layouter as _layouter


class Hold(object):
    u"""ホールドピース管理。
    """
    __slots__ = (
        "__id", "__item_state", "__is_captured", "__keep", "__piece",
        "__system", "__window")
    __GOOD_ITEM_NAMES = (
        _const.STAR_NAMES+"#"+_const.SHARD_NAMES+"#" +
        _const.KEY_NAMES+"#"+_const.CHEST_NAMES+"#Maxwell")
    __BAD_ITEM_NAMES = (
        _const.IRREGULAR_NAMES+"#"+_const.DEMON_NAMES+"#" +
        _const.GHOST_NAMES+"#Pandora#Joeker")

    def __init__(self, system):
        u"""コンストラクタ。
        self.__id: オブジェクトの位置決定に使用。
        self.__keep: ホールドピースパターンを保持。
        """
        import pygame as __pygame
        import window as __window
        self.__system = system
        self.__id = self.__system.id
        self.__piece = None
        self.__keep = _pieces.Array(length=2)
        self.__window = __window.Next(__pygame.Rect(
            (0, 0), _const.NEXT_WINDOW_SIZE))
        self.__is_captured = False
        self.__item_state = 0b0000
        self.__window.is_light = not self.__is_captured
        _layouter.Game.set_hold(self.__window, self.__id)

    def __display(self):
        u"""ピース表示。
        """
        _layouter.Game.set_hold(self.__window.rect, self.__id)
        self.__piece = _pieces.Dropping(self.__keep[0], (0, 0))
        self.__window.piece = self.__piece

    def __set_item_state(self):
        u"""パターン内部のアイテムによって値を設定。
        0b0001: ホールドブロックが存在する。
        0b0010: 基本ブロックが存在する。
        0b0100: 良性アイテムが存在する。
        0b1000: 悪性アイテムが存在する。
        """
        pattern, = self.__keep
        self.__item_state = (
            0b0001+(any(any(
                shape and shape.type in _const.BASIC_NAMES.split("#") for
                shape in line) for line in pattern) << 1) +
            (any(any(
                shape and shape.type in self.__GOOD_ITEM_NAMES.split("#") for
                shape in line) for line in pattern) << 2) +
            (any(any(
                shape and shape.type in self.__BAD_ITEM_NAMES.split("#") for
                shape in line) for line in pattern) << 3))

    def change(self, is_single, target):
        u"""ブロック変化。
        """
        if not self.__keep.is_empty:
            new, old = target.split("##")
            self.__piece.clear()
            if self.__system.battle.player.armor.is_prevents(new):
                _, _, armor_info, _ = self.__system.battle.equip_info
                armor_info.flash()
            elif not self.__system.battle.group.is_prevents(new):
                pattern, = self.__keep
                if is_single:
                    pattern.append(new, old)
                else:
                    pattern.change(new, old)
                self.__set_item_state()
            self.__display()

    def capture(self):
        u"""ピースの取得・交換。
        """
        import material.sound as __sound

        def __accessory_effect():
            u"""装飾品効果。
            """
            battle = self.__system.battle
            additional = battle.player.accessory.additional
            if additional:
                is_single, new, old = additional
                _, _, armor_info, accessory_info = battle.equip_info
                if battle.player.armor.is_prevents(new):
                    armor_info.flash()
                elif not battle.group.is_prevents(new) and (
                    self.__keep[-1].append(new, old) if is_single else
                    self.__keep[-1].change(new, old)
                ):
                    accessory_info.flash()
        if not self.__is_captured:
            blocks = self.__system.blocks
            if self.__keep.is_empty:
                blocks.piece.pattern.rotate(0)
                self.__keep.append(blocks.piece.pattern)
                __accessory_effect()
                blocks.piece.clear()
                blocks.advance()
            else:
                test = self.virtual
                test.topleft = blocks.piece.state.topleft
                if not test.is_collide(blocks.field):
                    self.__piece.clear()
                    blocks.piece.clear()
                    blocks.piece.pattern.rotate(0)
                    self.__keep.append(blocks.piece.pattern)
                    __accessory_effect()
                    blocks.piece.pattern = self.__keep.pop()
                    blocks.update_display()
            self.__set_item_state()
            __sound.SE.play("Hold")
            self.is_captured = True
            self.__display()

    def exchange(self, other):
        u"""ピース交換。
        """
        if not self.__keep.is_empty and not other.__keep.is_empty:
            self.__piece.clear()
            other.__piece.clear()
            pattern, = self.__keep
            other_pattern, = other.__keep
            self.__keep[0] = other_pattern
            other.__keep[0] = pattern
            self.__set_item_state()
            other.__set_item_state()
            self.__display()
            other.__display()

    @property
    def virtual(self):
        u"""計算用ピース取得。
        """
        if not self.__keep.is_empty:
            pattern, = self.__keep
            return _pieces.Dropping(pattern, is_virtual=True)

    @property
    def is_empty(self):
        u"""空判定。
        """
        return self.__keep.is_empty

    @property
    def is_captured(self):
        u"""キャプチャ判定。
        """
        return self.__is_captured

    @is_captured.setter
    def is_captured(self, value):
        u"""キャプチャ設定。
        ウィンドウの色付けも設定。
        """
        self.__is_captured = value
        self.__window.is_light = not self.__is_captured

    @property
    def item_state(self):
        u"""アイテム状態取得。
        """
        return self.__item_state

    @property
    def window(self):
        u"""ウィンドウ取得。
        """
        return self.__window
