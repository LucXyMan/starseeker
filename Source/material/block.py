#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""block.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ブロック画像加工モジュール。
"""


def init(container):
    u"""モジュールの初期化。
    """
    import pygame as __pygame
    import utils.image as __image
    global __blocks

    # ---- Special ----
    def __process_target():
        u"""ターゲット画像作成。
        """
        def __process_edge(color):
            u"""ブロックエッジ画像加工。
            """
            def __create_base_edge():
                u"""基本ブロックエッジ画像作成。
                """
                surf = __pygame.Surface((16, 16))
                for name, offset in (
                    ("top_edge", (0, 1)), ("right_edge", (-1, 0)),
                    ("bottom_edge", (0, -1)), ("left_edge", (1, 0)),
                    ("topright_edge", (-1, 1)), ("bottomright_edge", (-1, -1)),
                    ("bottomleft_edge", (1, -1)), ("topleft_edge", (1, 1))
                ):
                    key = color+"_"+name
                    __blocks[key] = ()
                    for frame in __blocks[color+"_"+"target"]:
                        copy = __image.copy(frame)
                        copy.set_colorkey(__pygame.Color("0x000000"))
                        copy.blit(surf, offset)
                        __blocks[key] += copy,

            def __create_multi_edge():
                u"""複合ブロックエッジ画像作成。
                """
                for name, parts in (
                    ("leftright_edge", ("right_edge", "left_edge")),
                    ("topbottom_edge", ("top_edge", "bottom_edge")),
                    ("topbottomright_edge",
                     ("top_edge", "right_edge", "bottom_edge")),
                    ("leftrightbottom_edge",
                     ("right_edge", "bottom_edge", "left_edge")),
                    ("topbottomleft_edge",
                     ("top_edge", "bottom_edge", "left_edge")),
                    ("topleftright_edge",
                     ("top_edge", "right_edge", "left_edge"))
                ):
                    key = color+"_"+name
                    __blocks[key] = ()
                    for edges in zip(*(
                        __blocks[color+"_"+part] for part in parts
                    )):
                        surf = __pygame.Surface((16, 16))
                        surf.set_colorkey(__pygame.Color("0x000000"))
                        for edge in edges:
                            surf.blit(edge, (0, 0))
                        __blocks[key] += surf,
            __create_base_edge()
            __create_multi_edge()
        source = __image.load(container.get("target.png"))
        for i, name in enumerate((
            "white", "red", "yellow", "green",
            "magenta", "orange", "cyan", "blue"
        )):
            __blocks[name+"_target"] = __image.get_segment(
                __image.get_another_color(source, i, 8), (4, 1))
        for color in (
            "white", "red", "yellow", "green",
            "magenta", "orange", "cyan", "blue"
        ):
            __process_edge(color)

    def __process_next():
        u"""ネクスト表示で使用する画像加工。
        """
        source = __image.load(container.get("small.png"))
        for i in range(10):
            images = __image.get_segment(
                __image.get_another_color(source, i, 8), (4, 2), (8, 8))
            for j, name in enumerate((
                "square", "circle", "diamond", "star",
                "rect", "!", "?", "arrow"
            )):
                if name == "arrow":
                    image = images[j]
                    flipped = __pygame.transform.flip(image, False, True)
                    __blocks["up_"+name+"_"+str(i)] = image
                    __blocks["down_"+name+"_"+str(i)] = flipped
                else:
                    __blocks[name+"_"+str(i)] = images[j]

    # ---- Basic ----
    def __process_basic():
        u"""基本ブロック画像加工。
        """
        source = __image.load(container.get("basic.png"))
        images = [
            __image.get_segment(
                __image.get_another_color(source, i, 8), (4, 1)
            ) for i in range(16)]
        __blocks["normal"] = reduce(
            lambda x, y: x+y, (image[0:1] for image in images[::2]))
        __blocks["solid"] = reduce(
            lambda x, y: x+y, (image[::2] for image in images[1:8:2]))
        __blocks["adamant"] = reduce(lambda x, y: x+y, images[9:16:2])

    # ---- Item ----
    def __process_star():
        u"""スター画像加工。
        """
        source = __image.load(container.get("star.png"))
        for i, name in enumerate((
            "mars", "jupiter", "mercury", "venus", "saturn", "sun", "moon"
        )):
            __blocks[name] = __image.get_segment(
                __image.get_another_color(source, i), (4, 3))

    def __process_shards():
        u"""欠片画像加工。
        """
        source = __image.load(container.get("shards.png"))
        for i, name in enumerate((
            "speed_shards", "power_shards", "protect_shards", "life_shards"
        )):
            images = __image.get_segment(
                __image.get_another_color(source, i), (4, 2))
            __blocks[name] = images[4:]

    def __process_icon():
        u"""アイコン画像を使用するブロック画像加工。
        """
        import icon as _icon
        import string as __string
        for name, color, ky_rng, chst_rng in (
            ("black", 8, 0, 0), ("yellow", 1, 3, 0), ("white", 2, 1, 1),
            ("red", 6, 0, 3), ("blue", 9, 0, 0), ("green", 5, 0, 0),
            ("cyan", 7, 0, 0), ("purple", 3, 0, 0)
        ):
            icon = _icon.get(0x600 | color)
            __blocks[name+"_key"] = tuple([
                __string.get_subscript(icon, str(i)) for
                i in range(ky_rng, 0, -1)]+[icon])
            icon = _icon.get(0x700 | color)
            __blocks[name+"_chest"] = tuple([
                __string.get_subscript(icon, str(i)) for
                i in range(chst_rng, 0, -1)]+[icon, _icon.get(0x800 | color)])
            __blocks[name+"_mimic"] = tuple([
                _icon.get(i << 8 | color) for i in (7, 9, 10, 9)])
            __blocks[name+"_card"] = tuple([
                _icon.get(i << 8 | color) for i in range(2, 6)]+[
                    __pygame.transform.flip(
                        _icon.get(i << 8 | color), True, False
                    ) for i in range(4, 2, -1)])

    def __process_arrow():
        u"""矢印ブロック画像加工。
        """
        source = __image.load(container.get("arrow.png"))
        for i, name in enumerate((
            "red", "yellow", "magenta", "blue", "green"
        )):
            another_color = __image.get_another_color(source, i, 8)
            images = __image.get_segment(another_color, (4, 2))
            __blocks[name+"_up_arrow"] = images[:4]
            __blocks[name+"_down_arrow"] = images[4:]

    # ---- Monster ----
    def __process_daemon():
        u"""精霊ブロック画像加工。
        """
        source = __image.load(container.get("daemon.png"))
        images = [__image.get_another_color(source, i) for i in range(9)]
        _images = __image.get_segment(images[3], (4, 2))
        __blocks["gargoyle"] = _images[0:1]
        for name, image in zip((
            "ice_ghost", "poison_ghost", "fire_ghost"
        ), images[:3]):
            _images = __image.get_segment(image, (4, 2))
            __blocks[name] = _images[4:8]
        for name, image in zip((
            "maxwell", "eater", "arch_demon", "demon", "king_demon"
        ), images[4:]):
            _images = __image.get_segment(image, (4, 2))
            __blocks[name] = _images[0:4]

    def __process_slime():
        u"""スライム・きのこ画像加工。
        """
        source = __image.load(container.get("slime.png"))
        for i, name, in enumerate((
            "slime", "large_matango", "tired", "matango"
        )):
            images = __image.get_segment(
                __image.get_another_color(source, i), (4, 2))
            __blocks[name] = (
                images[4:] if i in (1, 3) else images[3:4] if i == 2 else
                images[1:2]+images[:3])

    # ---- Irregular ----
    def __process_nature():
        u"""水系画像加工。
        """
        source = __image.load(container.get("nature.png"))
        for i, name in enumerate((
            "magma", "ice", "", "Corrosion", "acid", "poison", "water"
        )):
            if name:
                images = __image.get_segment(
                    __image.get_another_color(source, i), (4, 2))
                __blocks[name] = images[4:] if i == 1 else images[:4]

    def __process_stone():
        u"""石化画像加工。
        """
        source = __image.load(container.get("stone.png"))
        for i, name in enumerate(("chocolate", "stone")):
            __blocks[name] = __image.get_segment(
                __image.get_another_color(source, i, 8), (4, 4))

    def __process_others():
        u"""その他画像加工。
        """
        source = __image.load(container.get("other.png"))
        for i, name in enumerate(("rip", "ruin")):
            images = __image.get_segment(
                __image.get_another_color(source, i), (4, 2))
            __blocks[name] = images[i],
    __blocks = {"dummy": (__image.get_clear(__pygame.Surface((16, 16))),)}
    for func in (
        __process_target, __process_next,
        __process_basic,
        __process_star, __process_shards, __process_icon, __process_arrow,
        __process_daemon, __process_slime,
        __process_nature, __process_stone, __process_others
    ):
        func()


def get(key):
    u"""ブロック画像取得。
    """
    return __blocks[key]
