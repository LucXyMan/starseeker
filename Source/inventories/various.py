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
    __PLAYER_SLOT = 0

    # ---- Getter ----
    @classmethod
    def get_player(cls):
        u"""現在プレイヤー取得。
        """
        return cls._general.get(cls.__PLAYER_SLOT)

    @classmethod
    def get_learnable(cls):
        u"""プレイヤーが取得可能なスキル番号取得。
        """
        return cls._players[cls.get_player()].learnable

    @classmethod
    def get_difficulty(cls):
        u"""ゲーム難易度取得。
        """
        return cls._general.get(cls._DIFFICULTY_SLOT)

    @classmethod
    def get_speed(cls):
        u"""カーソル移動速度取得。
        """
        return cls._general.get(cls._SPEED_SLOT)

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
        cls._general.set(cls.__PLAYER_SLOT, (
            0 if value < 0 else value if value < _const.PLEYERS-1 else
            _const.PLEYERS-1))

    @classmethod
    def set_difficulty(cls, value):
        u"""ゲーム難易度設定。
        """
        return cls._general.set(cls._DIFFICULTY_SLOT, value)

    @classmethod
    def set_speed(cls, value):
        u"""カーソル移動速度設定。
        """
        cls._general.set(cls._SPEED_SLOT, value)


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

    # ---- Setter ----
    @classmethod
    def on(cls, slot):
        u"""位置slotのクリア状態設定。
        """
        cls._level.on(slot)


class Endless(__inventory.Inventory):
    u"""エンドレス管理。
    """
    __PROGRESS_SLOT = 0
    __REACHED_SLOT = 1

    # ---- Detection ----
    @classmethod
    def is_cleared(cls):
        u"""クリア判定。
        """
        return _const.ENDLESS_LIMIT <= cls.get_reached()

    # ---- Getter ----
    @classmethod
    def get_progress(cls):
        u"""進行状態取得。
        """
        return cls._endless.get(cls.__PROGRESS_SLOT)

    @classmethod
    def get_reached(cls):
        u"""到達地点取得。
        """
        return cls._endless.get(cls.__REACHED_SLOT)

    # ---- Setter ----
    @classmethod
    def set_progress(cls, value):
        u"""進行状態設定。
        """
        cls._endless.set(cls.__PROGRESS_SLOT, (
            0 if value < 0 else value if value < _const.ENDLESS_LIMIT else
            _const.ENDLESS_LIMIT))

    @classmethod
    def set_reached(cls, value):
        u"""到達地点設定。
        """
        value = (
            0 if value < 0 else value if value < _const.ENDLESS_LIMIT else
            _const.ENDLESS_LIMIT)
        if cls.get_reached() < value:
            cls._endless.set(cls.__REACHED_SLOT, value)
