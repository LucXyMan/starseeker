#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""block.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ブロックモジュール。
"""
import pygame as _pygame
import cell as __cell
import material.block as _block
import utils.const as _const
import utils.counter as _counter
import utils.image as _image
import utils.memoize as _memoize


def _get_key(function, *args, **_kw):
    u"""ブロック画像キー取得。
    """
    block, = args
    return u"<{method}##{name}##{size}>".format(
        method=u"{module}.{name}".format(
            module=function.__module__, name=function.__name__),
        name=block.name, size=block.point.size)


class Block(__cell.Cell):
    u"""ブロック。
    """
    __EDGE_NAMES = {
        0b0001: "top_edge", 0b0010: "right_edge",
        0b0100: "bottom_edge", 0b1000: "left_edge",
        0b0011: "topright_edge", 0b0110: "bottomright_edge",
        0b1100: "bottomleft_edge", 0b1001: "topleft_edge",
        0b1010: "leftright_edge", 0b0101: "topbottom_edge",
        0b0111: "topbottomright_edge", 0b1110: "leftrightbottom_edge",
        0b1101: "topbottomleft_edge", 0b1011: "topleftright_edge",
        0b1111: "target"}
    __FLASH_PERIOD = _const.FRAME_DELAY << 2
    __STEP = 2
    _MALIGNANCY = _const.LOW_MALIGNANCY
    _SMALL_IMAGE = "!_1"
    _TARGET_COLOR = "red"
    _CROSS = 0b1111
    _BELOW = 0b1110

    @classmethod
    def get_base_images(cls):
        u"""基本画像取得。
        """
        return tuple(image for image in _block.get(cls._IMAGES))

    @classmethod
    def get_next_image(cls):
        u"""ネクスト表示用画像取得。
        """
        return _block.get(cls._SMALL_IMAGE)

    @classmethod
    def get_target_color(cls):
        u"""ターゲットブロック色を取得。
        """
        return cls._TARGET_COLOR

    @classmethod
    def get_minimap_color(cls):
        u"""ミニマップに書き込む際の色を取得。
        """
        if not hasattr(cls, "_minimap_color"):
            cls._minimap_color = (
                _const.RED if cls._TARGET_COLOR == "red" else
                _const.ORANGE if cls._TARGET_COLOR == "orange" else
                _const.YELLOW if cls._TARGET_COLOR == "yellow" else
                _const.GREEN if cls._TARGET_COLOR == "green" else
                _const.CYAN if cls._TARGET_COLOR == "cyan" else
                _const.BLUE if cls._TARGET_COLOR == "blue" else
                _const.MAGENTA if cls._TARGET_COLOR == "magenta" else
                _const.WHITE)
        return cls._minimap_color

    @classmethod
    def get_malignancy(cls):
        u"""悪性度取得。
        """
        return cls._MALIGNANCY

    def __init__(self, point, state, is_virtual):
        u"""コンストラクタ。
        """
        super(Block, self).__init__(point, state, is_virtual)
        self.__is_x_moving = self.__is_y_moving = False
        self.__animation = self.__window = None
        if not self._is_virtual:
            self.update()

    # ---- Effect ----
    def _affect(self, target, direction):
        u"""周囲への影響。
        """
        result = False
        new, old = target.split("##")
        for cell in self._get_around(direction):
            if cell.is_target(old) and cell.change(new):
                result = True
        return result

    def link(self):
        u"""リンク設定。
        """
    def rank_up(self):
        u"""スターランクアップ。
        """
    def paint(self, color=-1):
        u"""着色処理。
        """
    # ---- Edge ----
    def set_field_edge(self):
        u"""フィールドブロックエッジ設定。
        """
        result = []
        left, top = self._point.topleft
        w, h = self._point.size
        for y in range(h):
            line = []
            for x in range(w):
                edge = 0
                for i, cell in enumerate((
                    self._get((left+x, top+y-1)), self._get((left+x+1, top+y)),
                    self._get((left+x, top+y+1)), self._get((left+x-1, top+y))
                )):
                    if cell is None or cell.is_blank:
                        edge += 1 << i
                line.append(edge)
            result.append(line)
        self._edges = result

    def set_piece_edge(self):
        u"""ピースブロックエッジ設定。
        """
        def __is_blank(point):
            u"""位置pointの空白判定。
            """
            x, y = point
            return not any(
                _pygame.Rect(x, y, 1, 1).colliderect(block.point) for
                block in self._piece.blocks)
        result = []
        left, top = self._point.topleft
        w, h = self._point.size
        for y in range(h):
            line = []
            for x in range(w):
                edge = 0
                for i, point in enumerate((
                    (left+x, top+y-1), (left+x+1, top+y),
                    (left+x, top+y+1), (left+x-1, top+y))
                ):
                    if __is_blank(point):
                        edge += 1 << i
                line.append(edge)
            result.append(line)
        self._edges = result

    # ---- Update ----
    def _get_target_color(self):
        u"""ターゲットカラー取得。
        """
        if not hasattr(self, "_target_color"):
            self._target_color = self.get_target_color()
        return self._target_color

    def update(self):
        u"""更新処理。
        """
        def __flash():
            u"""点滅画像更新。
            """
            try:
                self.image.fill(_pygame.Color("0x000000"))
                self.image.blit(self.__animation.next(), (0, 0))
            except StopIteration:
                image, = _block.get("dummy")
                self.image.blit(image, (0, 0))
                self.__animation = None
                if self._piece:
                    self._piece.remove(self)

        def __update_image():
            u"""画像更新処理。
            """
            if hasattr(self, "image"):
                self.image.fill(_pygame.Color("0x000000"))
                self.image.blit(self._current_image, (0, 0))
            else:
                self.image = _image.copy(self._current_image)

        def __update_edge():
            u"""エッジ画像更新。
            """
            color = self._get_target_color()
            for y, line in enumerate(self._edges):
                for x, grid in enumerate(line):
                    if grid:
                        images = _block.get(color+"_"+self.__EDGE_NAMES[grid])
                        dest = x << _const.GRID_SHIFT, y << _const.GRID_SHIFT
                        self.image.blit(images[_counter.get_frame(4)], dest)

        def __update_rect():
            u"""rect更新。
            """
            if hasattr(self, "image"):
                if hasattr(self, "rect"):
                    self.rect.size = self.image.get_size()
                else:
                    self.rect = self.image.get_rect()
                    self.rect.x = self._point.x << _const.GRID_SHIFT
                    self.rect.y = self._point.y << _const.GRID_SHIFT

        def __move():
            u"""移動処理。
            """
            if self.rect and self.is_moving:
                self.rect.move_ip(
                    0, self.__STEP if self.rect.y < self._point.y <<
                    _const.GRID_SHIFT else -self.__STEP)
        if not self._is_virtual:
            if self.__animation:
                __flash()
            else:
                __update_image()
            __update_edge()
            __update_rect()
            __move()

    def disappear(self, delay=0):
        u"""消失処理。
        """
        import sprites.effects as __effects

        def __flash_generator(delay):
            u"""フラッシュ画像ジェネレータ。
            """
            import random as __random
            for _ in range(delay*(self.__FLASH_PERIOD >> 1)):
                yield self._current_image
            for i in range(self.__FLASH_PERIOD):
                if self._is_effect_available:
                    effect = __effects.Image((
                        self.rect.centerx +
                        __random.randint(-_const.GRID >> 1, _const.GRID >> 1),
                        self.rect.centery +
                        __random.randint(-_const.GRID >> 1, _const.GRID >> 1)),
                        self._EFFECT, vector=(0, -1), groups=() if
                        self.__window else None)
                    if self.__window:
                        self.__window.effects.append(effect)
                yield _image.get_colored_add(
                    self._current_image, _const.RAINBOW[i & 0b111])
        if self._is_destroyed:
            self.__animation = __flash_generator(delay)

    # ---- Getter ----
    def _get_top(self):
        u"""上セル取得。
        """
        return tuple(cell for cell in {
            self._get((x, self._point.top-1)) for x in
            range(self._point.left, self._point.right)} if cell)

    def _get_right(self):
        u"""右セル取得。
        """
        return tuple(cell for cell in {
            self._get((self._point.right, y)) for y in
            range(self._point.top, self._point.bottom)} if cell)

    def _get_bottom(self):
        u"""下セル取得。
        """
        return tuple(cell for cell in {
            self._get((x, self._point.bottom)) for x in
            range(self._point.left, self._point.right)} if cell)

    def _get_left(self):
        u"""左セル取得。
        """
        return tuple(cell for cell in {
            self._get((self._point.left-1, y)) for y in
            range(self._point.top, self._point.bottom)} if cell)

    def _get_around(self, direction):
        u"""周囲のセル取得。
        """
        return tuple(reduce(lambda x, y: x+y, (cell for i, cell in enumerate((
            self._get_top(), self._get_right(),
            self._get_bottom(), self._get_left())) if
            direction & 0b0001 << i)))

    # ---- Property ----
    @property
    @_memoize.memoize(get_key=_get_key)
    def _scaled_images(self):
        u"""サイズ調整後画像取得。
        """
        return tuple(_pygame.transform.scale(image, tuple(
            s << _const.GRID_SHIFT for s in self.point.size)) for
            image in self.get_base_images())

    @property
    def _current_image(self):
        u"""現在画像取得。
        """
        return self._scaled_images[
            _counter.get_frame(self._FRAME) if hasattr(self, "_FRAME") else 0]

    @property
    def _is_effect_available(self):
        u"""エフェクト使用可能判定。
        """
        return hasattr(self, "_EFFECT")

    @property
    def window(self):
        u"""所属先ウィンドウ取得。
        """
        return self.__window

    @window.setter
    def window(self, value):
        u"""所属先ウィンドウ設定。
        """
        self.__window = value

    @property
    def virtual(self):
        u"""仮想ブロック取得。
        AIに使用される。
        """
        return self.__class__(self._point, self._state, True)

    @property
    def parameter(self):
        u"""Shapeパラメータ取得。
        """
        return self._point.topleft, (self.name, self._state, self._point.size)

    @property
    def is_block(self):
        u"""ブロック判定。
        """
        return True

    @property
    def is_moving(self):
        u"""移動判定。
        """
        return self.rect.y != self._point.y << _const.GRID_SHIFT

    @property
    def is_disappear(self):
        u"""消滅判定。
        """
        return bool(self.__animation)

    @property
    def is_active(self):
        u"""動作判定。
        ブロックに動作がある場合に真。
        """
        return self.is_moving or self.is_disappear


class Target(Block):
    u"""ターゲット。
    """
    _IMAGES = "dummy"

    def _get_target_color(self):
        u"""ターゲットカラー取得。
        """
        if not hasattr(self, "_target_color"):
            self._target_color = (
                "red" if self._state == _const.RED_TARGET_NUMBER else
                "orange" if self._state == _const.ORANGE_TARGET_NUMBER else
                "yellow" if self._state == _const.YELLOW_TARGET_NUMBER else
                "green" if self._state == _const.GREEN_TARGET_NUMBER else
                "cyan" if self._state == _const.CYAN_TARGET_NUMBER else
                "blue" if self._state == _const.BLUE_TARGET_NUMBER else
                "magenta" if self._state == _const.MAGENTA_TARGET_NUMBER else
                "white")
        return self._target_color


class Blank(__cell.Cell):
    u"""空白。
    """
    @property
    def is_blank(self):
        u"""空白判定。
        """
        return True
