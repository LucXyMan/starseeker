#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""minimap.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ミニマップモジュール。
"""
import pygame as _pygame
import utils.const as _const
import general as _general


class _Minimap(_general.Indicator):
    u"""フィールドミニマップ。
    """
    def __init__(self, param, groups=None):
        u"""サーフェスとデコレータ作成。
        """
        import sprites.decorator as __decorator
        super(_Minimap, self).__init__(groups)
        rect = _pygame.Rect(*param)
        self.image = _pygame.Surface(rect.size)
        self.image.set_colorkey(_pygame.Color("0x000000"))
        self.rect = rect
        self._decorate = 1, 1, 1, 1
        __decorator.set_decorator(self)
        self.update()

    @property
    def decorate(self):
        u"""デコレータ状態取得。
        """
        return self._decorate

    @property
    def is_light(self):
        u"""ウィンドウ発光判定。
        """
        return False


class Block(_Minimap):
    u"""ブロックミニマップ。
    """
    def write_blocks(self, fill, *blocks):
        u"""ブロックを書き込む。
        """
        rect = _pygame.draw.rect
        if fill:
            self.image.fill(self.image.get_colorkey())
        for block in blocks:
            x, y, w, h = block.point
            for _x in range(w):
                for _y in range(h):
                    if (
                        self.image.get_at((x+_x, y+_y)) !=
                        self.image.get_colorkey()
                    ):
                        rect(
                            self.image, _pygame.Color(_const.GRAY),
                            (x+_x, y+_y, 1, 1), 1)
                    else:
                        rect(
                            self.image, _pygame.Color(
                                block.get_minimap_color()),
                            (x+_x, y+_y, 1, 1), 1)


class Space(_Minimap):
    u"""空白ミニマップ。
    """
    def write_blocks(self, fill, table):
        u"""ブロックを書き込む。
        """
        if fill:
            self.image.fill(self.image.get_colorkey())
        for y, line in enumerate(table):
            for x, cell in enumerate(line):
                if cell.is_space:
                    color = "0x000000"
                elif cell.is_hole:
                    color = _const.RED
                elif cell.is_adjacent:
                    color = _const.CYAN
                else:
                    color = _const.WHITE
                _pygame.draw.rect(
                    self.image, _pygame.Color(color), (x, y, 1, 1), 1)
