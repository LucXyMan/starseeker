#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""window.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

セルウィンドウモジュール。
"""
import pygame as _pygame
import utils.const as _const
import sprites as __sprites


class __Cell(__sprites.Window):
    u"""セルウィンドウ。
    """
    @property
    def piece(self):
        u"""監視対象のオブジェクトを返す。
        """
        return self._piece

    @piece.setter
    def piece(self, value):
        u"""監視するオブジェクトを設定。
        """
        self._piece = value


class Next(__Cell):
    u"""ネクストウィンドウ。
    """
    __GRID = _const.GRID >> 1

    def __init__(self, param):
        u"""コンストラクタ。
        """
        rect = _pygame.Rect(*param)
        surf = _pygame.Surface(rect.size)
        surf.fill(_pygame.Color("0x000000"))
        super(Next, self).__init__(rect.topleft, surf)

    @property
    def piece(self):
        u"""監視対象のオブジェクトを返す。
        """
        return self._piece

    @piece.setter
    def piece(self, value):
        u"""監視するオブジェクトを設定。
        ブロック画像の書き込みも行う。
        """
        def __write_blocks():
            u"""ブロック書き込み。
            """
            for block in self._piece.blocks:
                block.update()
                x, y, w, h = block.point
                self.image.blit(_pygame.transform.scale(
                    block.get_next_image(), (w*self.__GRID, h*self.__GRID)
                ), (x*self.__GRID, y*self.__GRID))
        self._piece = value
        self.image.fill(_pygame.Color("0x000000"))
        __write_blocks()


class Field(__Cell):
    u"""フィールドウィンドウ。
    """
    __X_GRID = _const.GRID >> 1

    def __init__(self, rect, whole=None):
        u"""コンストラクタ。
        ウィンドウの矩形rectと全体イメージサイズのwholeを引数に。
        """
        rect = _pygame.Rect(*rect)
        self.__whole_image = (
            _pygame.Surface(whole) if whole else
            _pygame.Surface(rect.size))
        self.__whole_rect = self.__whole_image.get_rect()
        surf = _pygame.Surface(rect.size)
        surf.set_colorkey(_pygame.Color("0x000000"))
        super(Field, self).__init__(rect.topleft, surf)
        self.__area = self.image.get_rect()
        self.__effects = []
        self.update()

    # ---- Update ----
    def update_area(self):
        u"""表示範囲の更新。
        """
        self.__whole_rect.left = -self._piece.left*self.__X_GRID
        self.__whole_rect.top = -self._piece.top*_const.GRID
        self.__area.topleft = (
            -self.__whole_rect.left, -self.__whole_rect.top)
        if self.__area.left < 0:
            self.__area.left = 0
        elif self.__whole_rect.w < self.__area.right:
            self.__area.right = self.__whole_rect.w
        if self.__area.top < 0:
            self.__area.top = 0
        elif self.__whole_rect.h < self.__area.bottom:
            self.__area.bottom = self.__whole_rect.h
        if 0 < self.__whole_rect.left:
            self.__whole_rect.left = 0
        elif self.__whole_rect.right < self.rect.width:
            self.__whole_rect.right = self.rect.width
        if 0 < self.__whole_rect.top:
            self.__whole_rect.top = 0
        elif self.__whole_rect.bottom < self.rect.height:
            self.__whole_rect.bottom = self.rect.height

    def update(self):
        u"""ピースの位置に合わせて表示する。
        """
        def __write_blocks():
            u"""ブロック書き込み。
            """
            for block in (
                self.__field.blocks+self._piece.blocks +
                (self.__ghost.blocks if self.__ghost else [])
            ):
                block.window = self
                block.update()
                if block.rect.colliderect(self.__area):
                    self.__whole_image.blit(block.image, block.rect.topleft)

        def __write_effects():
            u"""エフェクト書き込み。
            """
            for fx in self.__effects[:]:
                fx.update()
                if fx.rect.colliderect(self.__area):
                    self.__whole_image.blit(fx.image, fx.rect.topleft)
                if fx.is_dead:
                    self.__effects.remove(fx)

        def __update_edge():
            u"""デコレータ処理。
            """
            self._decoration = (
                (1 if self.__whole_rect.top == 0 else 0) +
                (2 if self.__whole_rect.right == self.rect.width else 0) +
                (4 if self.__whole_rect.bottom == self.rect.height else 0) +
                (8 if self.__whole_rect.left == 0 else 0))
        self.__whole_image.fill(_pygame.Color("0x000000"))
        if hasattr(self, "_piece"):
            __write_blocks()
            __write_effects()
            __update_edge()
            self.image.blit(self.__whole_image, (0, 0), self.__area)
        else:
            self._decoration = 0b0000
            self.image.blit(self.__whole_image, (0, 0))

    # ---- Property ----
    @property
    def field(self):
        u"""フィールド取得。
        """
        return self.__field

    @field.setter
    def field(self, value):
        u"""フィールド設定。
        """
        self.__field = value

    @property
    def ghost(self):
        u"""ゴーストピース取得。
        """
        return self.__ghost

    @ghost.setter
    def ghost(self, value):
        u"""ゴーストピース設定。
        """
        self.__ghost = value

    @property
    def effects(self):
        u"""エフェクトを取得。
        """
        return self.__effects

    @property
    def difference(self):
        u"""画像全体と描画領域のブロック差分を取得。
        """
        diff = self.__whole_rect.bottom-self.__area.bottom >> _const.GRID_SHIFT
        return 0 if diff < 0 else diff
