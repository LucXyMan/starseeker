#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""sound.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

サウンドモジュール。
"""
import os as _os
import pygame as _pygame
import utils.packer as _packer
_volume = 1
_is_mute = False


def init():
    u"""モジュール初期化。
    """
    path = _os.path.join(_os.path.dirname(__file__))
    BGM.source = _os.path.join(path, "bgm.enf")
    BGM()
    SE.source = _os.path.join(path, "se.enf")
    SE()


class BGM(object):
    u"""BGM管理。
    """
    __slots__ = ()
    __dict = {}
    __playing = ""

    def __init__(self):
        u"""コンストラクタ。
        """
        if _pygame.mixer.get_num_channels():
            BGM.__channel = _pygame.mixer.Channel(0)
            BGM.__channel.set_endevent(_pygame.USEREVENT)
        container = _packer.Container(self.source)
        for name in (("Menu",)+tuple("LV"+str(i) for i in range(1, 5))):
            BGM.__dict[name] = tuple(
                _pygame.mixer.Sound(container.get(
                    "{name}_{part}.ogg".format(name=name, part=part))) for
                part in ("init", "loop"))

    @classmethod
    def loop(cls, events):
        u"""ループ処理。
        """
        if cls.__playing:
            for event in events:
                if event.type == cls.__channel.get_endevent():
                    cls.__channel.queue(cls.__current)

    @classmethod
    def play(cls, name):
        u"""BGM再生。
        """
        if cls.__playing:
            if name != cls.__playing:
                _pygame.mixer.stop()
            else:
                return None
        cls.__playing = name
        init, cls.__current = cls.__dict[name]
        init.play()
        cls.__channel.set_volume(0 if _is_mute else _volume)
        cls.__channel.queue(cls.__current)

    @classmethod
    def stop(cls):
        u"""BGM停止。
        """
        _pygame.mixer.stop()
        cls.__playing = ""

    @classmethod
    def pause(cls):
        u"""BGM一時停止。
        """
        cls.__channel.pause()

    @classmethod
    def unpause(cls):
        u"""BGM一時停止解除。
        """
        cls.__channel.unpause()

    @classmethod
    def volume_up(cls, value=0.1):
        u"""BGMの音量を上げる。
        """
        global _volume, _is_mute
        _volume = _volume+value if _volume+value < 1 else 1
        cls.__channel.set_volume(_volume)
        _is_mute = False

    @classmethod
    def volume_down(cls, value=0.1):
        u"""BGMの音量を下げる。
        """
        global _volume, _is_mute
        _volume = _volume-value if 0 < _volume-value else 0
        cls.__channel.set_volume(_volume)
        _is_mute = False

    @classmethod
    def mute(cls):
        u"""BGMミュート・アンミュート。
        """
        global _is_mute
        if _is_mute:
            cls.__channel.set_volume(_volume)
            _is_mute = False
        else:
            cls.__channel.set_volume(0)
            _is_mute = True


class SE(object):
    u"""効果音管理。
    """
    __slots__ = ()
    __dict = {}

    def __init__(self):
        u"""コンストラクタ。
        """
        container = _packer.Container(self.source)
        for filename in container.keys:
            name,  _ = _os.path.splitext(filename)
            SE.__dict[name] = _pygame.mixer.Sound(container.get(filename))

    @classmethod
    def play(cls, name):
        u"""SE再生。
        """
        cls.__dict[name].set_volume(0 if _is_mute else _volume)
        cls.__dict[name].play()
