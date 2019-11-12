#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""__main__.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

メインモジュール。
"""
import pygame as __pygame


def __main():
    u"""メイン関数。
    """
    import armament as __armament
    import game as __game
    import input as __input
    import inventory as __inventory
    import material as __material
    import pieces as __pieces
    import sprites as __sprites
    import utils as __utils
    __pygame.init()
    __material.init()
    __utils.init()
    __sprites.init()
    __pieces.init()
    __armament.init()
    __inventory.init()
    __input.init()
    __game.init()
    __game.Game().loop()


if __name__ == "__main__":
    __main()
    __pygame.quit()
