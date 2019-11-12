#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""item.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

アイテムブロックモジュール。
スター、パワーアップ、アルカナ。
"""
import utils.const as _const
import block as __block


class __Star(__block.Block):
    u"""スターブロック。
    """
    _FRAME_NUM = 4
    _SCORE = _const.SINGLE_SCORE
    _TARGET_COLOR = "green"

    def effect(self):
        u"""他種スターにエネルギーシフト。
        全体の流れ: 五星→太陽→月→五星…
        五星の流れ: 木→火→土→金→水→木…
        """
        is_rank_up = False
        for cell in self._get_surround(self._CROSS):
            if cell and cell._is_target(self._TARGETS) and cell.rank_up():
                is_rank_up = True
        if is_rank_up and 0 <= self._state:
            self._state -= 1
            if self._state == -1:
                self.change("Normal")

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
            __counter.get_frame(self._FRAME_NUM) +
            self._state*self._FRAME_NUM])

    @property
    def star_type(self):
        u"""スター種類取得。
        """
        return self._TYPE


class Jupiter(__Star):
    u"""木星スター。
    """
    _EFFECT = "blue_line"
    _IMAGES = "jupiter"
    _SMALL_IMAGE = "circle_4"
    _TARGETS = "Mars#Sun"
    _TYPE = 1


class Mars(__Star):
    u"""火星スター。
    """
    _EFFECT = "red_fire"
    _IMAGES = "mars"
    _SMALL_IMAGE = "circle_1"
    _TARGETS = "Saturn#Sun"
    _TYPE = 2


class Saturn(__Star):
    u"""土星スター。
    """
    _EFFECT = "purple_light"
    _IMAGES = "saturn"
    _SMALL_IMAGE = "circle_7"
    _TARGETS = "Venus#Sun"
    _TYPE = 3


class Venus(__Star):
    u"""金星スター。
    """
    _EFFECT = "yellow_line"
    _IMAGES = "venus"
    _SMALL_IMAGE = "circle_2"
    _TARGETS = "Mercury#Sun"
    _TYPE = 4


class Mercury(__Star):
    u"""水星スター。
    """
    _EFFECT = "blue_bubble"
    _IMAGES = "mercury"
    _SMALL_IMAGE = "circle_6"
    _TARGETS = "Jupiter#Sun"
    _TYPE = 5


class Moon(__Star):
    u"""月スター。
    """
    _EFFECT = "black_fire"
    _IMAGES = "moon"
    _SMALL_IMAGE = "circle_9"
    _TARGETS = "Mars#Mercury#Jupiter#Venus#Saturn"
    _TYPE = 6


class Sun(__Star):
    u"""太陽スター。
    """
    _EFFECT = "yellow_light"
    _IMAGES = "sun"
    _SMALL_IMAGE = "circle_8"
    _TARGETS = "Moon"
    _TYPE = 7


class __Shard(__block.Block):
    u"""パワーアップブロック。
    """
    _SCORE = _const.SINGLE_SCORE
    _FRAME_NUM = 4
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
    _TYPE = 1


class Power(__Shard):
    u"""力の欠片ブロック。
    """
    _IMAGES = "power_shards"
    _SMALL_IMAGE = "diamond_1"
    _TYPE = 2


class Protect(__Shard):
    u"""守りの欠片ブロック。
    """
    _IMAGES = "protect_shards"
    _SMALL_IMAGE = "diamond_6"
    _TYPE = 3


class Speed(__Shard):
    u"""速さの欠片ブロック。
    """
    _IMAGES = "speed_shards"
    _SMALL_IMAGE = "diamond_4"
    _TYPE = 4


class __Arcanum(__block.Block):
    u"""アルカナブロック。
    """
    _FRAME_NUM = 6
    _SCORE = _const.SINGLE_SCORE
    _TARGET_COLOR = "blue"

    @property
    def is_arcanum(self):
        u"""アルカナ判定。
        """
        return True


class Summon(__Arcanum):
    u"""召喚アルカナ。
    """
    _IMAGES = "yellow_card"
    _SMALL_IMAGE = "rect_2"


class Sorcery(__Arcanum):
    u"""魔術アルカナ。
    """
    _IMAGES = "green_card"
    _SMALL_IMAGE = "rect_4"


class Shield(__Arcanum):
    u"""シールドアルカナ。
    """
    _IMAGES = "purple_card"
    _SMALL_IMAGE = "rect_7"


class Joeker(__Arcanum):
    u"""ジョーカーアルカナ。
    """
    _IMAGES = "black_card"
    _SMALL_IMAGE = "rect_9"
    _TARGET_COLOR = "red"
