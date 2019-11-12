#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""layouter.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

レイアウトマネージャモジュール。
"""
import pygame as _pygame
import const as _const


def init():
    u"""使用するパラメータの初期化。
    """
    import screen as __screen
    screen = __screen.Screen.get_base()
    Game(screen.get_rect())
    Menu(screen.get_rect())


class _Layouter(object):
    u"""レイアウトマネージャ。
    """
    def __init__(self, screen):
        u"""使用するRectの設定。
        screen: スクリーンのrect。
        inner: スクリーンより多少小さい矩形。
        inner_half: innerの四分の一。
        """
        _Layouter._screen = screen
        _Layouter._inner = _pygame.Rect(
            (0, 0), tuple(elm-(_const.GRID >> 2) for elm in self._screen.size))
        _Layouter._inner.center = self._screen.center
        _Layouter._inner_half = _pygame.Rect(
            (0, 0), (self._inner.width >> 1, self._inner.height >> 1))
        _Layouter._menu = _pygame.Rect((0, 0), (
            int(self._screen.width*0.92), int(self._screen.height*0.86)))
        _Layouter._menu.center = self._screen.center

    @classmethod
    def __get_target(cls, obj):
        u"""操作対象となるrect取得。
        """
        return obj.rect if hasattr(obj, "rect") else obj

    @classmethod
    def _set_obj_center(cls, obj, pos):
        u"""objの中心にposを設定。
        """
        cls.__get_target(obj).center = pos

    @classmethod
    def _set_obj_centery(cls, obj, pos):
        u"""objの中心y軸にposを設定。
        """
        cls.__get_target(obj).centery = pos

    @classmethod
    def _set_obj_top(cls, obj, pos):
        u"""objの上にposを設定。
        """
        cls.__get_target(obj).top = pos

    @classmethod
    def _set_obj_right(cls, obj, pos):
        u"""objの右にposを設定。
        """
        cls.__get_target(obj).right = pos

    @classmethod
    def _set_obj_left(cls, obj, pos):
        u"""objの左にposを設定。
        """
        cls.__get_target(obj).left = pos

    @classmethod
    def _set_obj_midtop(cls, obj, pos):
        u"""objの中上にposを設定。
        """
        cls.__get_target(obj).midtop = pos

    @classmethod
    def _set_obj_topright(cls, obj, pos):
        u"""objの右上にposを設定。
        """
        cls.__get_target(obj).topright = pos

    @classmethod
    def _set_obj_midright(cls, obj, pos):
        u"""objの中右にposを設定。
        """
        cls.__get_target(obj).midright = pos

    @classmethod
    def _set_obj_bottomright(cls, obj, pos):
        u"""objの右下にposを設定。
        """
        cls.__get_target(obj).bottomright = pos

    @classmethod
    def _set_obj_midbottom(cls, obj, pos):
        u"""objの中下にposを設定。
        """
        cls.__get_target(obj).midbottom = pos

    @classmethod
    def _set_obj_bottomleft(cls, obj, pos):
        u"""objの左下にposを設定。
        """
        cls.__get_target(obj).bottomleft = pos

    @classmethod
    def _set_obj_midleft(cls, obj, pos):
        u"""objの中左にposを設定。
        """
        cls.__get_target(obj).midleft = pos

    @classmethod
    def _set_obj_topleft(cls, obj, pos):
        u"""objの左上にposを設定。
        """
        cls.__get_target(obj).topleft = pos


class Game(_Layouter):
    u"""メインゲームの配置を決定。
    """
    def __init__(self, border):
        u"""初期設定。
        __field: フィールド設定用。
        __top: 画面上の方。
        __next: ネクスト・ホールドピース設定用。
        """
        _Layouter.__init__(self, border)
        Game.__field = Game._inner.copy()
        Game.__field.width = Game.__field.width*0.96
        Game.__field.height = Game.__field.height*0.89
        Game.__field.center = Game._inner.center
        Game.__top = Game._inner.copy()
        Game.__top.width = Game.__top.width*0.85
        Game.__top.center = Game._inner.center
        Game.__next = Game._inner.copy()
        Game.__next.width = Game.__next.width*0.36
        Game.__panel = _pygame.Rect((0, 0), (0, int(Game._screen.height*0.60)))
        Game.__units = _pygame.Rect(
            (0, 0), (_const.GRID*6, int(_const.GRID*1.5)))
        Game.__gauge = _pygame.Rect((0, 0), (63, 9))

    @classmethod
    def set_field(cls, obj, id_):
        u"""フィールド位置設定。
        """
        if id_ == 0:
            cls._set_obj_bottomleft(obj, cls.__field.bottomleft)
        else:
            cls._set_obj_bottomright(obj, cls.__field.bottomright)

    @classmethod
    def set_next(cls, objs, id_):
        u"""ネクスト位置設定。
        """
        if id_ == 0:
            cls.__next.topleft = cls.__top.topleft
            cls._set_obj_midtop(objs[0], cls.__next.midtop)
            cls._set_obj_topright(objs[1], cls.__next.topright)
        else:
            cls.__next.topright = cls.__top.topright
            cls._set_obj_midtop(objs[0], cls.__next.midtop)
            cls._set_obj_topleft(objs[1], cls.__next.topleft)

    @classmethod
    def set_hold(cls, obj, id_):
        u"""ホールド位置決定。
        """
        if id_ == 0:
            cls.__next.topleft = cls.__top.topleft
            cls._set_obj_topleft(obj, cls.__next.topleft)
        else:
            cls.__next.topright = cls.__top.topright
            cls._set_obj_topright(obj, cls.__next.topright)

    @classmethod
    def set_parent(cls, obj):
        u"""親ブロック位置設定。
        """
        cls._set_obj_midtop(obj.window, cls._inner.midtop)

    @classmethod
    def set_stars(cls, gauges, id_):
        u"""スター情報位置設定。
        """
        if id_ == 0:
            x = 0
            for gauge in gauges:
                cls._set_obj_bottomleft(gauge, (x, cls._screen.bottom))
                x += gauge.rect.width
        else:
            x = cls._screen.right
            for gauge in reversed(gauges):
                cls._set_obj_bottomright(gauge, (x, cls._screen.bottom))
                x -= gauge.rect.width

    @classmethod
    def set_equip(cls, infos, window, id_):
        u"""装備情報位置設定。
        """
        cls.__panel.centery = window.rect.centery
        if id_ == 0:
            cls.__panel.left = cls._screen.left
            y = cls.__panel.top
            for info in infos:
                info.rect.topleft = cls.__panel.left, y
                y += info.rect.height
        else:
            cls.__panel.right = cls._screen.right
            y = cls.__panel.top
            for info in infos:
                info.rect.topright = cls.__panel.right, y
                y += info.rect.height

    @classmethod
    def set_card(cls, cards, window, id_, set_dest=False):
        u"""カード情報位置設定。
        """
        for i, card in enumerate(cards):
            card.draw_group.change_layer(card, i)
        rect = _pygame.Rect((0, 0), (_const.GRID, _const.GRID << 2))
        cls.__panel.centery = window.rect.centery
        if id_ == 0:
            cls.__panel.left = cls._screen.left
            rect.bottomleft = cls.__panel.bottomleft
            y = 0
            for card in cards:
                if not set_dest:
                    card.rect.topleft = rect.left, rect.top+y
                card.dest.topleft = rect.left, rect.top+y
                y += card.rect.height
        else:
            cls.__panel.right = cls._screen.right
            rect.bottomright = cls.__panel.bottomright
            y = 0
            for card in cards:
                if not set_dest:
                    card.rect.topright = rect.right, rect.top+y
                card.dest.topright = rect.right, rect.top+y
                y += card.rect.height

    @classmethod
    def set_block_level(cls, chars):
        u"""ブロックレベル文字列位置設定。
        """
        chars[1].rect.midbottom = cls._screen.midbottom
        chars[0].rect.midright = chars[1].rect.midleft
        chars[2].rect.midleft = chars[1].rect.midright

    @classmethod
    def set_minimap(cls, obj, hold, id_):
        cls._set_obj_midbottom(obj, hold.window.rect.midbottom)
        if id_ == 0:
            cls._set_obj_left(obj, cls.__field.left)
        else:
            cls._set_obj_right(obj, cls.__field.right)

    @classmethod
    def set_player(cls, player, window):
        u"""プレイヤーの位置設定。
        """
        player.dest.midbottom = player.rect.midbottom = (
            window.rect.centerx, window.rect.centery+(window.rect.h >> 3))

    @classmethod
    def set_creature_layer(cls, units):
        u"""クリーチャーレイヤーグループの設定。
        """
        for i, unit in zip((2, 3, 1), units):
            unit.draw_group.change_layer(unit, i)

    @classmethod
    def set_creature_init(cls, number, units, player):
        u"""クリーチャー初期位置設定。
        """
        cls.__units.midtop = player.rect.midbottom
        unit = units[number]
        unit.rect.midbottom = player.rect.midbottom

    @classmethod
    def set_creature_dest(cls, units, player, id_):
        u"""クリーチャー位置設定。
        """
        cls.__units.midtop = player.rect.midbottom
        for i, unit in enumerate(units):
            if id_ == 0:
                if i == 0:
                    unit.dest.midbottom = cls.__units.midright
                elif i == 2:
                    unit.dest.midbottom = cls.__units.midleft
            else:
                if i == 0:
                    unit.dest.midbottom = cls.__units.midleft
                elif i == 2:
                    unit.dest.midbottom = cls.__units.midright
            if i == 1:
                unit.dest.midbottom = cls.__units.midbottom

    @classmethod
    def set_power_gauge(cls, gauge, unit):
        u"""ライフ・プレスゲージ位置設定。
        """
        cls.__gauge.midtop = unit.rect.midbottom
        gauge.rect.bottomright = cls.__gauge.bottomright

    @classmethod
    def set_charge_gauge(cls, gauge, unit):
        u"""チャージゲージ位置設定。
        """
        cls.__gauge.midtop = unit.rect.midbottom
        gauge.rect.topleft = cls.__gauge.topleft

    @classmethod
    def set_paused(cls, sprite):
        u"""一時停止表示位置設定。
        """
        sprite.rect.center = cls._inner.center


class Menu(_Layouter):
    u"""メニュー画面の配置を決定。
    """
    @classmethod
    def set_selector(cls, selectors):
        u"""モード選択文字列の位置を設定。
        """
        cls._inner_half.midbottom = cls._screen.midbottom
        center = len(selectors)/2
        center_string = selectors[center]
        if len(selectors) % 2 == 0:
            center_string.rect.midtop = cls._inner_half.center
        else:
            center_string.rect.center = cls._inner_half.center
        midbottom = center_string.rect.midtop
        for selector in selectors[:center][::-1]:
            selector.rect.midbottom = midbottom
            midbottom = selector.rect.midtop
        midtop = center_string.rect.midbottom
        for selector in selectors[1+center:]:
            selector.rect.midtop = midtop
            midtop = selector.rect.midbottom

    @classmethod
    def set_info(cls, sprite):
        u"""情報表示位置設定。
        """
        sprite.rect.midtop = cls._screen.midtop

    @classmethod
    def set_title(cls, sprite):
        u"""タイトル位置設定。
        """
        cls._inner_half.midtop = cls._screen.midtop
        sprite.rect.center = cls._inner_half.center

    @classmethod
    def set_time(cls, sprite):
        u"""時間文字列位置設定。
        """
        sprite.rect.bottomright = cls._screen.bottomright

    @classmethod
    def set_midbottom(cls, sprite):
        u"""スプライト位置を中下に設定。
        """
        sprite.rect.midbottom = cls._screen.midbottom

    @classmethod
    def set_bottomleft(cls, sprite):
        u"""スプライト位置を左下に設定。
        """
        sprite.rect.bottomleft = cls._screen.bottomleft

    @classmethod
    def set_controls(cls, windows):
        u"""操作ウィンドウ位置設定。
        """
        for i, name in enumerate(("topright", "midright", "bottomright")):
            setattr(windows[i].rect, name, getattr(cls._menu, name))

    @classmethod
    def set_player_image(cls, doppel, is_right=False):
        u"""プレイヤー表示位置設定。
        """
        adjust = _pygame.Rect((0, 0), (_const.GRID << 3, _const.GRID << 2))
        if is_right:
            adjust.bottomright = cls._menu.bottomright
        else:
            adjust.bottomleft = cls._menu.bottomleft
        doppel.rect.midbottom = adjust.midbottom

    @classmethod
    def set_result(cls, result, reward=None):
        u"""結果表示ウィンドウ位置設定。
        """
        adjust = _pygame.Rect((0, 0), (0, _const.GRID*4))
        if reward:
            adjust.center = cls._inner.center
            result.rect.midbottom = adjust.midbottom
            reward.rect.midtop = adjust.midtop
        else:
            result.rect.center = cls._inner.center

    @classmethod
    def set_status(cls, window, is_right=False):
        u"""現在ステータスウィンドウ位置設定。
        """
        if is_right:
            window.rect.midright = cls._menu.midright
        else:
            window.rect.midleft = cls._menu.midleft

    @classmethod
    def set_equip(cls, window, is_right=False):
        u"""現在装備ウィンドウ位置設定。
        """
        if is_right:
            window.rect.topright = cls._menu.topright
        else:
            window.rect.topleft = cls._menu.topleft
