#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""effect.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

エフェクトスプライトモジュール。
"""
import pygame as __pygame


class Effect(__pygame.sprite.DirtySprite):
    u"""エフェクトスプライト。
    """
    @classmethod
    def is_active(cls):
        u"""動作判定。
        エフェクトが一つでも存在する場合に真。
        """
        return bool(cls.group)

    def __init__(self, pos, groups):
        u"""コンストラクタ。
        """
        super(Effect, self).__init__(
            (self.group, self.draw_group) if groups is None else groups)
        self.image, _ = self._images.next()
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        u"""更新処理。
        """
        try:
            center = self.rect.center
            self.image, move = self._images.next()
            self.rect.size = self.image.get_size()
            self.rect.center = center
            self.rect.move_ip(*move)
        except StopIteration:
            self._images = None
            self.kill()

    @property
    def is_live(self):
        u"""動作判定。
        """
        return self._images

    @property
    def is_dead(self):
        u"""終了判定。
        """
        return not self._images
