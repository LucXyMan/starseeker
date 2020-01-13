#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""various.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

様々な設定モジュール。
"""
import inventory as __inventory
import utils.const as _const


class General(__inventory.Inventory):
    u"""汎用パラメータ管理。
    """
    __slots__ = ()

    # ---- Detection ----
    @classmethod
    def is_cleared_endless(cls):
        u"""エンドレスクリア判定。
        """
        return _const.ENDLESS_LIMIT <= cls.get_reached_endless()

    # ---- Getter ----
    @classmethod
    def get_player(cls):
        u"""現在プレイヤー取得。
        """
        return cls._general.get(0)

    @classmethod
    def get_learnable(cls):
        u"""プレイヤーが取得可能なスキル番号取得。
        """
        return cls._players[cls.get_player()].learnable

    @classmethod
    def get_endless(cls):
        u"""エンドレス進行状態取得。
        """
        return cls._general.get(1)

    @classmethod
    def get_reached_endless(cls):
        u"""エンドレス到達地点取得。
        """
        return cls._general.get(2)

    @classmethod
    def get_speed(cls):
        u"""移動速度取得。
        """
        return cls._general.get(3)

    @classmethod
    def get_value(cls):
        u"""数値取得。
        """
        return sum(cls._general.raw)

    # ---- Setter ----
    @classmethod
    def set_player(cls, value):
        u"""現在プレイヤー設定。
        """
        cls._general.set(0, (
            0 if value < 0 else value if value < _const.PLEYERS-1 else
            _const.PLEYERS-1))

    @classmethod
    def set_endless(cls, value):
        u"""エンドレス進行状態設定。
        """
        cls._general.set(1, (
            0 if value < 0 else value if value < _const.ENDLESS_LIMIT else
            _const.ENDLESS_LIMIT))

    @classmethod
    def set_reached_endless(cls, value):
        u"""エンドレス到達地点設定。
        """
        value = (
            0 if value < 0 else value if value < _const.ENDLESS_LIMIT else
            _const.ENDLESS_LIMIT)
        if cls.get_reached_endless() < value:
            cls._general.set(2, value)

    @classmethod
    def set_speed(cls, value):
        u"""移動速度設定。
        """
        cls._general.set(3, value)


class Level(__inventory.Inventory):
    u"""レベル管理。
    """
    __slots__ = ()

    # ---- Getter ----
    @classmethod
    def has(cls, slot):
        u"""位置slotのクリア状態取得。
        """
        return cls._level.has(slot)

    @classmethod
    def get_wins(cls):
        u"""デュエルモード勝利数数取得。
        """
        return cls._level.bits

    @classmethod
    def get_value(cls):
        u"""数値を取得。
        """
        return sum(cls._level.raw)

    # ---- Setter ----
    @classmethod
    def on(cls, slot):
        u"""位置slotのクリア状態設定。
        """
        cls._level.on(slot)
