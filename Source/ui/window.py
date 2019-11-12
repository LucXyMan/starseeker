#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""window.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

メニューウィンドウモジュール。
"""
import pygame as _pygame
import material.sound as _sound
import sprites as _sprites
import utils.const as _const
import utils.image as _image


class _Display(_sprites.Window):
    u"""表示ウィンドウ。
    """
    _SCROLL_SPEED = 4
    _FRAME_MUNBER = _const.FRAME_DELAY << 2

    def __init__(self, param, size, groups=None):
        u"""コンストラクタ。
        """
        import material.block as __block
        super(_Display, self).__init__(param, size, groups)
        self._items = []
        self._cursor = 0
        self._frame = 0
        self._area = self.image.get_rect()
        self._whole_image = _image.copy(self._bg)
        self._whole_rect = self._whole_image.get_rect()
        self._cursor_rect = _pygame.Rect(0, 0, _const.GRID, _const.GRID)
        self.__cursor_images = reduce(lambda x, y: x+y, (
            (image,)*_const.FRAME_DELAY for
            image in __block.get("green_target")))
        self._is_active = False
        self._is_motion = False

    def update(self):
        u"""ウィンドウの更新処理。
        """
        def __scroll():
            u"""ウィンドウのスクロール処理。
            """
            motion = False
            if self._cursor_rect.left < self._area.left:
                self._area.x -= self._SCROLL_SPEED
                motion = True
            elif self._area.right < self._cursor_rect.right:
                self._area.x += self._SCROLL_SPEED
                motion = True
            if self._cursor_rect.top < self._area.top:
                self._area.y -= self._SCROLL_SPEED
                motion = True
            elif self._area.bottom < self._cursor_rect.bottom:
                self._area.y += self._SCROLL_SPEED
                motion = True
            if self._whole_rect.bottom < self._area.bottom:
                self._area.bottom = self._whole_rect.height
            self._is_motion = motion

        def __light_up():
            u"""デコレータの処理。
            """
            self._decorate = (
                1 if self._area.top == 0 else 0,
                1 if self._area.right == self._whole_rect.right else 0,
                1 if self._area.bottom == self._whole_rect.bottom else 0,
                1 if self._area.left == 0 else 0)

        def __cursor_blit():
            u"""カーソルの書き込み。
            """
            if self._is_light:
                self._whole_image.blit(
                    self.__cursor_images[self._frame],
                    self._cursor_rect.topleft)
                if self._is_active:
                    self._frame += 1
                    if self._frame == self._FRAME_MUNBER:
                        self._frame = 0
        self._whole_image.blit(self._bg, (0, 0))
        self._item_blit()
        __scroll()
        __light_up()
        __cursor_blit()
        self.image.blit(self._whole_image, (0, 0), self._area)

    @property
    def items(self):
        u"""ウィンドウアイテム取得。
        """
        return self._items

    @property
    def is_active(self):
        u"""カーソル能動状態取得。
        """
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        u"""カーソル能動状態設定。
        """
        self._is_active = bool(value)

    @property
    def is_motion(self):
        u"""画面の動きの状態を取得。
        """
        return self._is_motion

    @property
    def is_label(self):
        u"""ラベルウィンドウの場合に真。
        """
        return False


class Icon(_Display):
    u"""アイコンウィンドウ。
    """
    def __init__(self, param, matrix, groups=None):
        u"""コンストラクタ。
        """
        x, y, w, h = param
        self._bg = _image.get_checkered(*matrix)
        super(Icon, self).__init__((x, y), _pygame.Surface((w, h)), groups)
        self.update()

    def _item_blit(self):
        u"""アイコンの更新と書き込み。
        """
        for item in self._items:
            item.update()
            self._whole_image.blit(item.image, item.rect.topleft)

    def append(self, item):
        u"""アイテムの追加。
        """
        y, x = divmod(len(self._items)*_const.GRID, self.rect.width)
        item.rect.topleft = x, y*_const.GRID
        self._items.append(item)

    @property
    def cursor(self):
        u"""カーソル位置取得。
        """
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        u"""カーソル位置設定。
        """
        if self._is_active and not self._is_motion:
            old_cursor = self._cursor
            pos = int(value)
            self._cursor = (
                self._cursor if pos < 0 or len(self._items)-1 < pos else pos)
            y, x = divmod(self._cursor*_const.GRID, self._whole_rect.width)
            self._cursor_rect.topleft = x, y*_const.GRID
            if self._cursor != old_cursor:
                _sound.SE.play("cursor_1")


class Label(_Display):
    u"""ラベルウィンドウ。
    """
    def __init__(self, param, matrix, groups=None):
        u"""コンストラクタ。
        """
        x, y, w, h = param
        col, row = matrix
        self._bg = _image.get_checkered(col, row, 2)
        super(Label, self).__init__((x, y), _pygame.Surface((w, h)), groups)
        self._items = []
        self.update()

    def _item_blit(self):
        u"""ラベルの書き込みと更新。
        """
        for label in self._items:
            label.update()
            self._whole_image.blit(label.image, label.rect.topleft)

    def append(self, item):
        u"""アイテムの追加。
        """
        item.rect.topleft = 0, len(self._items)*_const.GRID
        self._items.append(item)

    @property
    def cursor(self):
        u"""カーソル位置取得。
        """
        return self._cursor

    @cursor.setter
    def cursor(self, value):
        u"""カーソル位置設定。
        """
        if self._is_active and not self._is_motion:
            old_cursor = self._cursor
            pos = int(value)
            self._cursor = (
                self._cursor if pos < 0 or len(self._items)-1 < pos else pos)
            self._cursor_rect.topleft = 0, self._cursor*_const.GRID
            if self._cursor != old_cursor:
                _sound.SE.play("cursor_1")

    @property
    def is_label(self):
        u"""ラベルウィンドウの場合に真。
        """
        return True
