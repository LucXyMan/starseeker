#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""image.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

画像ユーティリティモジュール。
"""
import pygame as _pygame
import const as _const
import memoize as __memoize
__memoize = __memoize.memoize
__ALTITUDE = 16
__ADD_PAINT_TYPE = 1
__SUB_PAINT_TYPE = 2
__AVE_PAINT_TYPE = 3
__FILL_PAINT_TYPE = 4


class BackGround(object):
    u"""背景管理。
    """
    __slots__ = ()
    __image = None
    __switch = None

    @classmethod
    def set_image(cls, image, is_gradually=False):
        u"""imageから背景設定。
        """
        image = copy(image)
        if cls.__image:
            cls.__switch = image
            cls.__switch.set_alpha(0x00 if is_gradually else 0xFF)
        else:
            cls.__image = image
        cls.update()

    @classmethod
    def transcribe(cls, image):
        u"""imageに背景を書き込む。
        """
        if cls.__image:
            if cls.__switch:
                cls.__image.blit(cls.__switch, (0, 0))
            image.blit(cls.__image, (0, 0))

    @classmethod
    def update(cls):
        u"""更新処理。
        """
        if cls.__switch:
            alpha = cls.__switch.get_alpha()+1
            if 0xFF < alpha:
                cls.__switch.set_alpha(None)
                cls.__image = cls.__switch
                cls.__switch = None
            else:
                cls.__switch.set_alpha(alpha)


def load(filename):
    u"""画像の読み込み。
    ※二回目のロードはエラーになる。
    """
    image = _pygame.image.load(filename)
    image.set_colorkey(_pygame.Color("0x000000"))
    return image


def segment(source, division, grid=(16, 16), adjust=(0, 0)):
    u"""画像の分割処理。
    """
    def __split(source, rect):
        u"""画像の切り取り処理。
        """
        surf = _pygame.Surface(
            rect.size, 0, source.get_bitsize(), source.get_masks())
        surf.set_palette(source.get_palette())
        surf.set_colorkey(source.get_colorkey())
        surf.blit(source, (0, 0), rect)
        return surf
    return [
        __split(source, _pygame.Rect(
            grid[0]*x+adjust[0], grid[1]*y+adjust[1], grid[0], grid[1]
        )) for y in range(division[1]) for x in range(division[0])]


def copy(image):
    u"""画像のコピーを返す。
    Surface.copy()よりも軽い。
    """
    surf = _pygame.Surface(image.get_size())
    surf.blit(image, (0, 0))
    surf.set_colorkey(image.get_colorkey())
    return surf


def get_other_color(image, rotate, size=16):
    u"""imageの色違いを取得。
    rotateが0の場合、元の画像と同じになる。
    """
    import collections as __collections
    if rotate != 0:
        palette = __collections.deque(image.get_palette())
        other = image.copy()
        palette.rotate(-size*rotate)
        other.set_palette(palette)
        return other
    return image


def set_colorkey(image, colorkey):
    u"""imageのカラーキーを文字列で設定。
    """
    image.set_colorkey(_pygame.Color(colorkey))


def get_clear(image):
    u"""imageの透明画像を取得。
    """
    surf = _pygame.Surface(image.get_size())
    surf.set_colorkey((0, 0, 0))
    return surf


def __get_colored(image, color, type_):
    u"""着色画像を取得する。
    """
    def __get_add_colors(color, rgb):
        u"""色の加算処理。
        """
        red, green, blue = rgb
        red = ((color & 0xFF0000) >> 16)+red
        red = 0xFF if 0xFF < red else red
        green = ((color & 0x00FF00) >> 8)+green
        green = 0xFF if 0xFF < green else green
        blue = ((color & 0x0000FF))+blue
        blue = 0xFF if 0xFF < blue else blue
        return (red << 16)+(green << 8)+blue

    def __get_sub_colors(color, rgb):
        u"""色の減算処理。
        """
        red, green, blue = rgb
        red = ((color & 0xFF0000) >> 16)-red
        red = 0 if red < 0 else red
        green = ((color & 0x00FF00) >> 8)-green
        green = 0 if green < 0 else green
        blue = ((color & 0x0000FF))-blue
        blue = 0 if blue < 0 else blue
        return (red << 16)+(green << 8)+blue

    def __get_ave_colors(color, rgb):
        u"""色の平均化処理。
        """
        red, green, blue = rgb
        red = (((color & 0xFF0000) >> 16)+red) >> 1
        red = 0xFF if 0xFF < red else red
        green = (((color & 0x00FF00) >> 8)+green) >> 1
        green = 0xFF if 0xFF < green else green
        blue = (((color & 0x0000FF))+blue) >> 1
        blue = 0xFF if 0xFF < blue else blue
        return (red << 16)+(green << 8)+blue

    def __get_fill_colors(_color, rgb):
        u"""色の塗りつぶし処理。
        """
        return rgb
    array = _pygame.PixelArray(copy(image))
    color = int(color, 16)
    red = (color & 0xFF0000) >> 16
    green = (color & 0x00FF00) >> 8
    blue = (color & 0x0000FF)
    for x in range(len(array)):
            for y in range(len(array[0])):
                if array[x][y] != 0x000000:
                    array[x][y] = (
                        __get_add_colors if type_ == __ADD_PAINT_TYPE else
                        __get_sub_colors if type_ == __SUB_PAINT_TYPE else
                        __get_ave_colors if type_ == __AVE_PAINT_TYPE else
                        __get_fill_colors)(array[x][y], (red, green, blue))
    surf = array.make_surface()
    surf.set_colorkey(image.get_colorkey())
    return surf


def get_colored_add(image, color):
    u"""加算方式の着色画像を取得。
    """
    return __get_colored(image, color, __ADD_PAINT_TYPE)


def get_colored_sub(image, color):
    u"""減算方式の着色画像を取得。
    """
    return __get_colored(image, color, __SUB_PAINT_TYPE)


def get_colored_ave(image, color):
    u"""平均化方式の着色画像を取得。
    """
    return __get_colored(image, color, __AVE_PAINT_TYPE)


def get_colored_fill(image, color):
    u"""塗りつぶし着色画像を取得。
    """
    return __get_colored(image, color, __FILL_PAINT_TYPE)


def get_dull(image):
    u"""くすんだ画像取得。
    """
    return __get_colored(image, _const.GRAY, __AVE_PAINT_TYPE)


def get_dummy():
    u"""透明画像取得。
    """
    surf = _pygame.Surface((0, 0))
    surf.set_colorkey(_pygame.Color(0x000000))
    return surf


def get_flying(image):
    u"""飛行クリチャー画像取得。
    """
    def __get_change_size(image, size):
        u"""サイズを変更した画像を取得。
        """
        colorkey = image.get_colorkey()
        surf = _pygame.Surface(size)
        surf.blit(image, (0, 0))
        surf.set_colorkey(colorkey)
        return surf
    w, h = image.get_size()
    return __get_change_size(image, (w, h+__ALTITUDE))


def __get_gradient_color(color, length):
    u"""グラデーションカラー取得。
    """
    start, end = color
    return (
        _pygame.Color(
            int(start[0]+(i*float(end[0]-start[0])/length)),
            int(start[1]+(i*float(end[1]-start[1])/length)),
            int(start[2]+(i*float(end[2]-start[2])/length))
        ) for i in range(length))


def draw_gradient_h(surf, color, rect):
    u"""グラデーション水平画像を描く。
    """
    for i, c in enumerate(__get_gradient_color(color, abs(rect.width))):
        _pygame.draw.line(
            surf, c, (rect.x+i, rect.y), (rect.x+i, rect.height))


def draw_gradient_v(surf, color, rect):
    u"""グラデーション垂直画像を描く。
    """
    for i, c in enumerate(__get_gradient_color(color, abs(rect.height))):
        _pygame.draw.line(
            surf, c, (rect.x, rect.y+i), (rect.width, rect.y+i))


def get_gradient(size, color, vertical):
    u"""グラデーション画像取得。
    """
    width, height = size
    surf = _pygame.Surface((width, height))
    (draw_gradient_v if vertical else
     draw_gradient_h)(surf, color, surf.get_rect())
    return surf


@__memoize()
def get_checkered(col, row, pattern=0):
    u"""白黒チェック画像を取得。
    pattern==0: 格子模様。
    pattern==1: 縞模様。
    pattern==2: 比率が1:col-1のパターン。
    """
    @__memoize()
    def __get_square(size, white):
        u"""白黒の正方形を作成。
        """
        black_color = "0x101010", "0x303030", "0x505050"
        white_color = "0xB0B0B0", "0xD0D0D0", "0xF0F0F0"
        w, h = size
        surf = _pygame.Surface((w, h))
        dark, base, light = (
            (_pygame.Color(color) for color in white_color) if white else
            (_pygame.Color(color) for color in black_color))
        line = _pygame.draw.line
        surf.fill(base)
        line(surf, light, (0, 0), (w-2, 0))
        line(surf, light, (0, 0), (0, h-2))
        line(surf, dark, (w-1, 1), (w-1, h-1))
        line(surf, dark, (1, h-1), (w-1, h-1))
        return surf
    surf = _pygame.Surface((col*_const.GRID, row*_const.GRID))
    for x in range(1 if pattern == 1 else 2 if pattern == 2 else col):
        for y in range(row):
            if x & 0b1 == 0:
                square = __get_square(
                    (_const.GRID*(col if pattern == 1 else 1), _const.GRID),
                    y & 0b1 == 0)
            else:
                square = __get_square(
                    (_const.GRID*(col-1 if pattern == 2 else 1),  _const.GRID),
                    y & 0b1 != 0)
            surf.blit(square, (x*_const.GRID, y*_const.GRID))
    return surf
