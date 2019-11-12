#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""chest.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

宝箱・鍵ブロックモジュール。
"""
import random as _random
import utils.const as _const
import block as __block
import irregular as __irregular
import monster as __monster


# ---- Key ----
class Key(__block.Block):
    u"""鍵ブロック。
    """
    __UNLOCKED_STATE = 255
    _EFFECT = "yellow_light"
    _TARGET_COLOR = "orange"

    def crack(self, flag=0):
        u"""クラック処理。
        """
        if self._is_treasure_flag(flag):
            self._state = self.__UNLOCKED_STATE
            self._is_destroyed = True
        else:
            self._state += 1
            if self._MAX_HP < self._state:
                self._is_destroyed = True

    # ---- Property ----
    @property
    def _current_image(self):
        u"""現在画像取得。
        """
        return self._scaled_images[
            self._state if self._state < self._MAX_HP else self._MAX_HP]

    @property
    def _is_effect_available(self):
        u"""エフェクト使用可能判定。
        """
        return (
            super(Key, self)._is_effect_available and
            self._state == self.__UNLOCKED_STATE)

    @property
    def is_key(self):
        u"""鍵判定。
        """
        return True


class BronzeKey(Key):
    u"""銅の鍵ブロック。
    """
    _SCORE = _const.SINGLE_SCORE
    _IMAGES = "red_key"
    _SMALL_IMAGE = "?_1"
    _MAX_HP = 0


class SilverKey(Key):
    u"""銀の鍵ブロック。
    """
    _SCORE = _const.HALF_SCORE
    _IMAGES = "white_key"
    _SMALL_IMAGE = "?_8"
    _MAX_HP = 1


class GoldKey(Key):
    u"""金の鍵ブロック。
    """
    _SCORE = _const.QUARTER_SCORE
    _IMAGES = "yellow_key"
    _SMALL_IMAGE = "?_2"
    _MAX_HP = 3


# ---- Box ----
class _Box(__block.Block):
    u"""箱ブロック。
    """
    _OPENED_STATE = 255
    _EFFECT = "yellow_light#blue_light#green_light#purple_light"

    def _change_mimic(self):
        u"""ミミックに変身。
        """
        if hasattr(self, "_MIMIC"):
            self.change(self._MIMIC)

    # ---- Property ----
    @property
    def _hp(self):
        u"""HP取得。
        """
        return self._state & 0b00001111

    @property
    def _current_image(self):
        u"""現在画像取得。
        """
        return self._scaled_images[
            -1 if self.is_opened else self._MAX_HP if
            self._MAX_HP < self._hp else self._hp]

    @property
    def _is_effect_available(self):
        u"""エフェクト使用可能判定。
        """
        return super(_Box, self)._is_effect_available and self.is_opened

    @property
    def is_mimic(self):
        u"""ミミック判定。
        """
        return bool((self._state & 0b11110000) >> 4)

    @property
    def is_invincible(self):
        u"""無敵判定。
        宝箱の中身がミミックの場合に真。
        """
        return self.is_mimic

    @property
    def is_opened(self):
        u"""空箱判定。
        """
        return self._state == self._OPENED_STATE


# ---- Chest ----
class _Chest(_Box):
    u"""宝箱ブロック。
    """
    _TARGET_COLOR = "yellow"

    @property
    def treasure_rank(self):
        u"""宝ランク取得。
        """
        return self._RANK


class IronChest(_Chest):
    u"""鉄の宝箱ブロック。
    鍵なし。
    """
    _SCORE = _const.SINGLE_SCORE
    _IMAGES = "blue_chest"
    _SMALL_IMAGE = "star_0"
    _MAX_HP = 0
    _RANK = 1

    def crack(self, _flag=0):
        u"""クラック処理。
        """
        if self.is_opened:
            self._is_destroyed = True
        else:
            self._state = self._OPENED_STATE


class _Locked(_Chest):
    u"""鍵付き宝箱ブロック。
    9分の1が当たりでそれ以外がハズレ。
    """
    __MISS_RATE = 9

    def __init__(self, point, state, is_virtual):
        u"""コンストラクタ。
        """
        if state == -1:
            state = (0 if _random.randint(0, self.__MISS_RATE) else 1) << 4
        super(_Locked, self).__init__(point, state, is_virtual)

    def crack(self, flag=0):
        u"""クラック処理。
        """
        if self.is_opened:
            self._is_destroyed = True
        else:
            if self._is_unlock_flag(flag):
                self._state = self._OPENED_STATE
            else:
                self._state = self.is_mimic << 4 | self._hp+1
                if self._MAX_HP < self._hp:
                    if self.is_mimic:
                        self._change_mimic()
                    else:
                        self._is_destroyed = True

    @property
    def is_locked(self):
        u"""鍵付き宝箱・ミミックの場合に真。
        """
        return not self.is_opened


class BronzeChest(_Locked):
    u"""銅の宝箱ブロック。
    """
    _SCORE = _const.QUARTER_SCORE
    _IMAGES = "red_chest"
    _SMALL_IMAGE = "star_1"
    _MIMIC = "BronzeMimic"
    _MAX_HP = 3
    _RANK = 2


class SilverChest(_Locked):
    u"""銀の宝箱ブロック。
    """
    _SCORE = _const.HALF_SCORE
    _IMAGES = "white_chest"
    _SMALL_IMAGE = "star_8"
    _MIMIC = "SilverMimic"
    _MAX_HP = 1
    _RANK = 3


class GoldChest(_Locked):
    u"""金の宝箱ブロック。
    """
    _SCORE = _const.SINGLE_SCORE
    _IMAGES = "yellow_chest"
    _SMALL_IMAGE = "star_2"
    _MIMIC = "GoldMimic"
    _MAX_HP = 0
    _RANK = 4


class Pandora(_Box):
    u"""パンドラの箱ブロック。
    まれにマクスウェルデーモンを生成する。
    """
    __HIT_RATE = 9
    _SCORE = _const.SINGLE_SCORE
    _IMAGES = "black_chest"
    _SMALL_IMAGE = "star_9"
    _TARGET_COLOR = "red"
    _MIMIC = "PandoraMimic"
    _MAX_HP = 0
    _RANK = 5

    def __init__(self, point, state, is_virtual):
        u"""コンストラクタ。
        """
        if state == -1:
            state = (1 if _random.randint(0, self.__HIT_RATE) else 0) << 4
        super(Pandora, self).__init__(point, state, is_virtual)

    def crack(self, flag=0):
        u"""クラック処理。
        """
        if self._is_force_flag(flag):
            self._is_destroyed = True
        elif self.is_opened:
            self.change("Maxwell")
        else:
            if self.is_mimic:
                self._change_mimic()
            else:
                self._state = self._OPENED_STATE

    @property
    def is_invincible(self):
        u"""無敵判定。
        ミミックの場合か開いている場合に真。
        """
        return self.is_mimic or self.is_opened


# ---- Mimic ----
class __Mimic(__irregular.Invincible, __monster.Mover):
    u"""ミミックブロック。
    フィールド上を動いてブロックとアイテムを破壊する。
    鍵ブロックで封印できる。
    """
    _FRAME_NUM = 4
    _EFFECT = "white_fire"
    _MALIGNANCY = _const.HIGH_MALIGNANCY

    def crack(self, flag=0):
        u"""強制クラックか鍵があれば破壊できる。
        """
        if self._is_force_flag(flag) or self._is_unlock_flag(flag):
            self._is_destroyed = True

    def effect(self):
        u"""フィールドを移動しながら変化させる。
        """
        favo = self._FAVO+"#" if hasattr(self, "_FAVO") else ""
        self._move(
            favo+_const.STAR_NAMES+"#"+_const.SHARD_NAMES+"#" +
            _const.CARD_NAMES, self._FOOTPRINT)

    @property
    def is_locked(self):
        u"""鍵付き宝箱・ミミックの場合に真。
        """
        return True


class BronzeMimic(__Mimic):
    u"""銅ミミックブロック。
    """
    _IMAGES = "red_mimic"
    _FAVO = "Normal"
    _FOOTPRINT = "Acid"


class SilverMimic(__Mimic):
    u"""銀ミミックブロック。
    """
    _IMAGES = "white_mimic"
    _FAVO = "Normal#Solid"
    _FOOTPRINT = "Ice"


class GoldMimic(__Mimic):
    u"""金ミミックブロック。
    """
    _IMAGES = "yellow_mimic"
    _FAVO = _const.BASIC_NAMES
    _FOOTPRINT = "Stone"


class PandoraMimic(__Mimic):
    u"""パンドラミミックブロック。
    """
    _IMAGES = "black_mimic"
    _FAVO = _const.BASIC_NAMES
    _FOOTPRINT = "BlockEater"
