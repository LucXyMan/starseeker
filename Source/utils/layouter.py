#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""layouter.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

レイアウトマネージャモジュール。
"""
import pygame as _pygame
import const as _const


def init():
    u"""使用するパラメータの初期化。
    """
    import screen as __screen
    _Layouter(__screen.Screen.get_base().get_rect())
    Game()
    Menu()


class _Layouter(object):
    u"""レイアウトマネージャ。
    """
    __slots__ = ()

    def __init__(self, screen):
        u"""使用するRectの設定。
        _screen: スクリーンのrect。
        _inner: スクリーンより多少小さい矩形。
        """
        _Layouter._screen = screen
        width, height = self._screen.size
        _Layouter._inner = _pygame.Rect(
            (0, 0), (width-(_const.GRID >> 2), height-(_const.GRID >> 1)))
        _Layouter._inner.center = self._screen.center

    @classmethod
    def __get_target(cls, object_):
        u"""操作対象rect取得。
        """
        return object_.rect if hasattr(object_, "rect") else object_

    @classmethod
    def _set_right(cls, object_, pos):
        u"""object_の右にposを設定。
        """
        cls.__get_target(object_).right = pos

    @classmethod
    def _set_left(cls, object_, pos):
        u"""object_の左にposを設定。
        """
        cls.__get_target(object_).left = pos

    @classmethod
    def _set_midtop(cls, object_, pos):
        u"""object_の中上にposを設定。
        """
        cls.__get_target(object_).midtop = pos

    @classmethod
    def _set_topright(cls, object_, pos):
        u"""object_の右上にposを設定。
        """
        cls.__get_target(object_).topright = pos

    @classmethod
    def _set_bottomright(cls, object_, pos):
        u"""object_の右下にposを設定。
        """
        cls.__get_target(object_).bottomright = pos

    @classmethod
    def _set_midbottom(cls, object_, pos):
        u"""object_の中下にposを設定。
        """
        cls.__get_target(object_).midbottom = pos

    @classmethod
    def _set_bottomleft(cls, object_, pos):
        u"""object_の左下にposを設定。
        """
        cls.__get_target(object_).bottomleft = pos

    @classmethod
    def _set_topleft(cls, object_, pos):
        u"""object_の左上にposを設定。
        """
        cls.__get_target(object_).topleft = pos


class Game(_Layouter):
    u"""メインゲームの配置を決定。
    """
    __slots__ = ()

    def __init__(self):
        u"""初期設定。
        __field: フィールド設定用。
        __piece: ピース設定用。
        __next: ネクスト・ホールドピース設定用。
        __panel: 左右のアイコン設定用。
        __group:  グループ設定用。
        __gauge: ゲージ設定用。
        """
        Game.__field = Game._inner.copy()
        Game.__field.width = Game.__field.width*0.96
        Game.__field.height = Game.__field.height*0.89
        Game.__field.center = Game._inner.center
        Game.__piece = Game._inner.copy()
        Game.__piece.width = Game.__piece.width*0.85
        Game.__piece.center = Game._inner.center
        Game.__next = Game._inner.copy()
        Game.__next.width = Game.__next.width*0.36
        Game.__panel = _pygame.Rect((0, 0), (0, int(Game._screen.height*0.60)))
        Game.__group = _pygame.Rect(
            (0, 0), (_const.GRID*5, int(_const.GRID*1.5)))
        Game.__gauge = _pygame.Rect((0, 0), (63, 9))

    # ---- Piece ----
    @classmethod
    def set_field(cls, window, id_):
        u"""フィールド位置設定。
        """
        if id_ == 0:
            cls._set_bottomleft(window, cls.__field.bottomleft)
        else:
            cls._set_bottomright(window, cls.__field.bottomright)

    @classmethod
    def set_next(cls, windows, id_):
        u"""ネクスト位置設定。
        """
        if id_ == 0:
            cls.__next.topleft = cls.__piece.topleft
            cls._set_midtop(windows[0], cls.__next.midtop)
            cls._set_topright(windows[1], cls.__next.topright)
        else:
            cls.__next.topright = cls.__piece.topright
            cls._set_midtop(windows[0], cls.__next.midtop)
            cls._set_topleft(windows[1], cls.__next.topleft)

    @classmethod
    def set_hold(cls, window, id_):
        u"""ホールド位置決定。
        """
        if id_ == 0:
            cls.__next.topleft = cls.__piece.topleft
            cls._set_topleft(window, cls.__next.topleft)
        else:
            cls.__next.topright = cls.__piece.topright
            cls._set_topright(window, cls.__next.topright)

    @classmethod
    def set_parent(cls, window):
        u"""親ブロック位置設定。
        """
        cls._set_midtop(window, cls._inner.midtop)

    @classmethod
    def set_minimap(cls, minimap, hold, id_):
        u"""ミニマップ位置設定。
        """
        cls._set_midbottom(minimap, hold.window.rect.midbottom)
        if id_ == 0:
            cls._set_left(minimap, cls.__field.left)
        else:
            cls._set_right(minimap, cls.__field.right)

    # ---- HUD ----
    @classmethod
    def set_stars(cls, stars, id_):
        u"""スター位置設定。
        """
        if id_ == 0:
            x = 0
            for star in stars:
                cls._set_bottomleft(star, (x, cls._screen.bottom))
                x += star.rect.width
        else:
            x = cls._screen.right
            for star in reversed(list(stars)):
                cls._set_bottomright(star, (x, cls._screen.bottom))
                x -= star.rect.width

    @classmethod
    def set_equip(cls, system, equip):
        u"""装備位置設定。
        """
        cls.__panel.centery = system.puzzle.window.rect.centery
        if system.id == 0:
            cls.__panel.left = cls._screen.left
            y = cls.__panel.top
            for item in equip:
                item.rect.topleft = cls.__panel.left, y
                y += item.rect.height
        else:
            cls.__panel.right = cls._screen.right
            y = cls.__panel.top
            for item in equip:
                item.rect.topright = cls.__panel.right, y
                y += item.rect.height

    @classmethod
    def set_hand(cls, system, is_set_rect=False):
        u"""手札位置設定。
        """
        hand = system.battle.hand
        rect = _pygame.Rect((0, 0), (0, _const.GRID << 2))
        cls.__panel.centery = system.puzzle.window.rect.centery
        y = 0
        if system.id == 0:
            cls.__panel.left = cls._screen.left
            rect.bottomleft = cls.__panel.bottomleft
            for card in hand:
                if not is_set_rect:
                    card.rect.topleft = rect.left, rect.top+y
                card.dest.topleft = rect.left, rect.top+y
                y += card.rect.height
        else:
            cls.__panel.right = cls._screen.right
            rect.bottomright = cls.__panel.bottomright
            for card in hand:
                if not is_set_rect:
                    card.rect.topright = rect.right, rect.top+y
                card.dest.topright = rect.right, rect.top+y
                y += card.rect.height

    @classmethod
    def set_piece_level(cls, string):
        u"""ピースレベル位置設定。
        """
        string.rect.midbottom = cls._screen.midbottom

    @classmethod
    def set_parameter(cls, strings, base_string, id_):
        u"""硬度・幸運位置設定。
        """
        strings = tuple(strings)
        if id_ == 0:
            strings[1].rect.midright = base_string.rect.midleft
            strings[0].rect.midright = strings[1].rect.midleft
        else:
            strings[0].rect.midleft = base_string.rect.midright
            strings[1].rect.midleft = strings[0].rect.midright

    # ---- Unit ----
    @classmethod
    def set_player(cls, player, window):
        u"""プレイヤー位置設定。
        """
        player.rect.midbottom = (
            window.rect.centerx, window.rect.centery+(window.rect.h >> 3))

    @classmethod
    def set_creature_init(cls, unit, player):
        u"""クリーチャー初期位置設定。
        """
        cls.__group.midtop = player.rect.midbottom
        unit.rect.midbottom = player.rect.midbottom

    @classmethod
    def set_creature(cls, units, player, id_):
        u"""クリーチャー位置設定。
        """
        cls.__group.midtop = player.rect.midbottom
        positions = cls.__group.midright, cls.__group.midleft
        positions = positions if id_ == 0 else positions[::-1]
        positions = positions[0], cls.__group.midbottom, positions[1]
        for i, unit, position in zip((2, 3, 1), units, positions):
            unit.dest.midbottom = position
            unit.draw_group.change_layer(unit, i)

    @classmethod
    def set_gauge(cls, gauge, unit):
        u"""ライフ・プレスゲージ位置設定。
        """
        cls.__gauge.midtop = unit.rect.midbottom
        gauge.rect.bottomright = cls.__gauge.bottomright

    @classmethod
    def set_charge_gauge(cls, gauge, unit):
        u"""チャージ・フリーズゲージ位置設定。
        """
        cls.__gauge.midtop = unit.rect.midbottom
        gauge.rect.topleft = cls.__gauge.topleft

    # ---- Center ----
    @classmethod
    def set_center(cls, sprite):
        u"""spriteを中心位置に設定。
        """
        sprite.rect.center = cls._inner.center


class Menu(_Layouter):
    u"""メニュー画面の配置を決定。
    """
    __slots__ = ()

    def __init__(self):
        u"""初期設定。
        __quarter: _innerの四分の一。
        __window: ウィンドウ設定用。
        """
        Menu.__quarter = _pygame.Rect(
            (0, 0), (self._inner.width >> 1, self._inner.height >> 1))
        _Layouter.__window = _pygame.Rect(
            (0, 0), (
                int(self._screen.width*0.92),
                int(self._screen.height*0.86)))
        _Layouter.__window.center = self._screen.center

    # ---- Title ----
    @classmethod
    def set_selector(cls, selectors):
        u"""モード選択文字列の位置を設定。
        """
        cls.__quarter.midbottom = cls._screen.midbottom
        center = len(selectors) >> 1
        center_string = selectors[center]
        if len(selectors) & 0b1 == 0:
            center_string.rect.midtop = cls.__quarter.center
        else:
            center_string.rect.center = cls.__quarter.center
        midbottom = center_string.rect.midtop
        for selector in selectors[:center][::-1]:
            selector.rect.midbottom = midbottom
            midbottom = selector.rect.midtop
        midtop = center_string.rect.midbottom
        for selector in selectors[1+center:]:
            selector.rect.midtop = midtop
            midtop = selector.rect.midbottom

    @classmethod
    def set_notice(cls, sprite):
        u"""通知位置設定。
        """
        sprite.rect.midtop = cls._screen.midtop

    @classmethod
    def set_title(cls, sprite):
        u"""タイトル位置設定。
        """
        cls.__quarter.midtop = cls._screen.midtop
        sprite.rect.center = cls.__quarter.center

    # ---- Notice ----
    @classmethod
    def set_time(cls, sprite):
        u"""時間位置設定。
        """
        sprite.rect.bottomright = cls._screen.bottomright

    @classmethod
    def set_level(cls, sprite):
        u"""レベル・サイズ・スコア位置設定。
        """
        sprite.rect.midbottom = cls._screen.midbottom

    @classmethod
    def set_option(cls, sprite):
        u"""オプション位置設定。
        """
        sprite.rect.bottomleft = cls._screen.bottomleft

    # ---- Menu ----
    @classmethod
    def set_controls(cls, windows):
        u"""操作ウィンドウ位置設定。
        """
        for i, name in enumerate(("topright", "midright", "bottomright")):
            setattr(windows[i].rect, name, getattr(cls.__window, name))

    @classmethod
    def set_player(cls, player, is_right=False):
        u"""プレイヤー表示位置設定。
        """
        adjust = _pygame.Rect((0, 0), (_const.GRID << 3, _const.GRID << 2))
        if is_right:
            adjust.bottomright = cls.__window.bottomright
        else:
            adjust.bottomleft = cls.__window.bottomleft
        player.rect.midbottom = adjust.midbottom

    @classmethod
    def set_status(cls, window, is_right=False):
        u"""現在ステータスウィンドウ位置設定。
        """
        if is_right:
            window.rect.midright = cls.__window.midright
        else:
            window.rect.midleft = cls.__window.midleft

    @classmethod
    def set_equip(cls, window, is_right=False):
        u"""現在装備ウィンドウ位置設定。
        """
        if is_right:
            window.rect.topright = cls.__window.topright
        else:
            window.rect.topleft = cls.__window.topleft

    # ---- Result ----
    @classmethod
    def set_result(cls, result, reward=None):
        u"""結果表示ウィンドウ位置設定。
        """
        rect = _pygame.Rect((0, 0), (0, _const.GRID*4))
        if reward:
            rect.center = cls._inner.center
            result.rect.midbottom = rect.midbottom
            reward.rect.midtop = rect.midtop
        else:
            result.rect.center = cls._inner.center
