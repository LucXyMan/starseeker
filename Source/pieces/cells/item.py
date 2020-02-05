#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""item.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

アイテムブロックモジュール。
スター、パワーアップ、アルカナ。
"""
import block as __block
import utils.const as _const


# ---- Star ----
class __Star(__block.Block):
    u"""スターブロック。
    """
    _FRAME = 4
    _SCORE = _const.SINGLE_SCORE
    _TARGET_COLOR = "green"

    def effect(self):
        u"""他種スターにエネルギーシフト。
        全体の流れ: 五星→太陽→月→五星…
        五星の流れ: 木→火→土→金→水→木…
        """
        is_rank_up = False
        for cell in self._get_around(self._CROSS):
            if cell.is_target(self._TARGETS) and cell.rank_up():
                is_rank_up = True
        if is_rank_up:
            if self._state <= 0:
                self.change("Normal")
            self._state -= 1

    def rank_up(self):
        u"""スターランクアップ。
        """
        if self.is_changeable and self._state < 2:
            self._state += 1
            return True
        else:
            return False

    @property
    def _current_image(self):
        u"""現在画像取得。
        三段階に切り替わる。
        """
        import utils.counter as __counter
        return (self._scaled_images[
            __counter.get_frame(self._FRAME) +
            self._state*self._FRAME])

    @property
    def star_type(self):
        u"""スター種類取得。
        """
        return self._TYPE


class Jupiter(__Star):
    u"""木星スター。
    """
    _EFFECT = _const.JUPITER_EFFECT
    _IMAGES = "jupiter"
    _SMALL_IMAGE = "circle_4"
    _TARGETS = "Mars#Sun"
    _TYPE = 0


class Mars(__Star):
    u"""火星スター。
    """
    _EFFECT = _const.MARS_EFFECT
    _IMAGES = "mars"
    _SMALL_IMAGE = "circle_1"
    _TARGETS = "Saturn#Sun"
    _TYPE = 1


class Saturn(__Star):
    u"""土星スター。
    """
    _EFFECT = _const.SATURN_EFFECT
    _IMAGES = "saturn"
    _SMALL_IMAGE = "circle_7"
    _TARGETS = "Venus#Sun"
    _TYPE = 2


class Venus(__Star):
    u"""金星スター。
    """
    _EFFECT = _const.VENUS_EFFECT
    _IMAGES = "venus"
    _SMALL_IMAGE = "circle_2"
    _TARGETS = "Mercury#Sun"
    _TYPE = 3


class Mercury(__Star):
    u"""水星スター。
    """
    _EFFECT = _const.MERCURY_EFFECT
    _IMAGES = "mercury"
    _SMALL_IMAGE = "circle_6"
    _TARGETS = "Jupiter#Sun"
    _TYPE = 4


class Moon(__Star):
    u"""月スター。
    """
    _EFFECT = _const.MOON_EFFECT
    _IMAGES = "moon"
    _SMALL_IMAGE = "circle_9"
    _TARGETS = "Mars#Mercury#Jupiter#Venus#Saturn"
    _TYPE = 5


class Sun(__Star):
    u"""太陽スター。
    """
    _EFFECT = _const.SUN_EFFECT
    _IMAGES = "sun"
    _SMALL_IMAGE = "circle_8"
    _TARGETS = "Moon"
    _TYPE = 6


# ---- Shard ----
class __Shard(__block.Block):
    u"""パワーアップブロック。
    """
    _SCORE = _const.SINGLE_SCORE
    _FRAME = 4
    _TARGET_COLOR = "magenta"

    @property
    def shard_type(self):
        u"""シャードの種類。
        """
        return self._TYPE


class Life(__Shard):
    u"""生命の欠片ブロック。
    """
    _IMAGES = "life_shards"
    _SMALL_IMAGE = "diamond_2"
    _TYPE = 0


class Power(__Shard):
    u"""力の欠片ブロック。
    """
    _IMAGES = "power_shards"
    _SMALL_IMAGE = "diamond_1"
    _TYPE = 1


class Protect(__Shard):
    u"""守りの欠片ブロック。
    """
    _IMAGES = "protect_shards"
    _SMALL_IMAGE = "diamond_6"
    _TYPE = 2


class Speed(__Shard):
    u"""速さの欠片ブロック。
    """
    _IMAGES = "speed_shards"
    _SMALL_IMAGE = "diamond_4"
    _TYPE = 3


# ---- Card ----
class __Card(__block.Block):
    u"""カードブロック。
    """
    _FRAME = 6
    _SCORE = _const.SINGLE_SCORE
    _TARGET_COLOR = "cyan"

    @property
    def is_arcanum(self):
        u"""アルカナ判定。
        """
        return True


class Summon(__Card):
    u"""サモンカード。
    """
    _IMAGES = "yellow_card"
    _SMALL_IMAGE = "rect_2"


class Sorcery(__Card):
    u"""ソーサリーカード。
    """
    _IMAGES = "green_card"
    _SMALL_IMAGE = "rect_4"


class Shield(__Card):
    u"""シールドカード。
    """
    _IMAGES = "purple_card"
    _SMALL_IMAGE = "rect_7"


class Support(__Card):
    u"""サポートカード。
    """
    _IMAGES = "cyan_card"
    _SMALL_IMAGE = "rect_5"


class Joker(__Card):
    u"""ジョーカーカード。
    """
    _IMAGES = "black_card"
    _SMALL_IMAGE = "rect_9"
    _TARGET_COLOR = "red"


# ---- Level Up ----
class __LevelUp(__block.Block):
    u"""レベル変化ブロック。
    """
    _FRAME = 4
    _SCORE = _const.SINGLE_SCORE

    @property
    def level_up_type(self):
        u"""レベルアップ種類取得。
        """
        return self._TYPE


class HardnessUp(__LevelUp):
    u"""硬度アップブロック。
    """
    _TYPE = 0
    _IMAGES = "red_up_arrow"
    _SMALL_IMAGE = "up_arrow_1"


class HardnessDown(__LevelUp):
    u"""硬度ダウンブロック。
    """
    _TYPE = 1
    _IMAGES = "blue_down_arrow"
    _SMALL_IMAGE = "down_arrow_5"
    _TARGET_COLOR = "white"


class LuckUp(__LevelUp):
    u"""ラックアップブロック。
    """
    _TYPE = 2
    _IMAGES = "green_up_arrow"
    _SMALL_IMAGE = "up_arrow_4"
    _TARGET_COLOR = "white"


class LuckDown(__LevelUp):
    u"""ラックダウンブロック。
    """
    _TYPE = 3
    _IMAGES = "yellow_down_arrow"
    _SMALL_IMAGE = "down_arrow_2"
