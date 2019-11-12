#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""iamge.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

画像エフェクトモジュール。
"""
import effect as __effect


class Image(__effect.Effect):
    u"""画像エフェクト。
    """
    def __init__(self, pos, source, vector=(0, 0), groups=None):
        u"""コンストラクタ。
        """
        self._images = self._generate(source.split("#"), vector)
        super(Image, self).__init__(pos, groups)

    def _get_images(self, sources):
        u"""エフェクト元画像取得。
        """
        import random as __random
        import material.effect as __meffect
        return __meffect.get(sources[__random.randint(0, len(sources)-1)])

    def _generate(self, sources, vector):
        u"""エフェクト画像の生成。
        """
        import utils.const as __const
        for image in self._get_images(sources):
            for _ in range(__const.FRAME_DELAY):
                yield image, vector


class __Complex(object):
    u"""複合エフェクト。
    """
    @property
    def is_dead(self):
        u"""全エフェクト停止時に真。
        """
        return all(effect.is_dead for effect in self._effects)

    @property
    def is_live(self):
        u"""エフェクト起動時に真。
        """
        return any(effect.is_live for effect in self._effects)
