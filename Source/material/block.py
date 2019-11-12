#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""block.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ブロック画像加工モジュール。
"""


def init(container):
    u"""モジュールの初期化。
    """
    import pygame as __pygame
    import utils.image as __image
    global __cells

    def __target_proc():
        u"""ターゲット画像作成。
        """
        def __edge_proc(type_):
            u"""ブロックエッジ画像加工。
            """
            def __create_base_edge():
                u"""基本ブロックエッジ画像作成。
                """
                fill = __pygame.Surface((16, 16))
                for name, adjust in (
                    ("top_edge", (0, 1)), ("right_edge", (-1, 0)),
                    ("bottom_edge", (0, -1)), ("left_edge", (1, 0)),
                    ("topright_edge", (-1, 1)), ("bottomright_edge", (-1, -1)),
                    ("bottomleft_edge", (1, -1)), ("topleft_edge", (1, 1))
                ):
                    __cells[type_+"_"+name] = ()
                    for frame in __cells[type_+"_"+"target"]:
                        copy = __image.copy(frame)
                        copy.blit(fill, adjust)
                        copy.set_colorkey(__pygame.Color("0x000000"))
                        __cells[type_+"_"+name] += copy,

            def __create_multi_edge():
                u"""複合ブロックエッジ画像作成。
                """
                for name, keys in (
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
                    __cells[type_+"_"+name] = ()
                    for edges in zip(
                        *(__cells[type_+"_"+key] for key in keys)
                    ):
                        surf = __pygame.Surface((16, 16))
                        for edge in edges:
                            surf.blit(edge, (0, 0))
                            surf.set_colorkey(__pygame.Color("0x000000"))
                        __cells[type_+"_"+name] += surf,
            __create_base_edge()
            __create_multi_edge()
        source = __image.load(container.get("target.png"))
        for i, name in enumerate((
            "white_target", "red_target", "yellow_target", "green_target",
            "magenta_target", "orange_target", "blue_target"
        )):
            __cells[name] = tuple(__image.segment(__image.get_other_color(
                source, i, 8), (4, 1)))
        for color in (
            "white", "red", "yellow", "green", "magenta", "orange", "blue"
        ):
            __edge_proc(color)

    def __basic_proc():
        u"""基本ブロック画像加工。
        """
        source = __image.load(container.get("basic.png"))
        images = [
            __image.segment(__image.get_other_color(source, i, 8), (4, 1)) for
            i in range(16)]
        __cells["normal"] = tuple(reduce(
            lambda x, y: x+y, tuple(e[0:1] for e in images[::2])))
        __cells["solid"] = tuple(reduce(
            lambda x, y: x+y, tuple(e[::2] for e in images[1:8:2])))
        __cells["adamant"] = tuple(reduce(
            lambda x, y: x+y, images[9:16:2]))

    def __star_proc():
        u"""スター画像加工。
        """
        source = __image.load(container.get("star.png"))
        for i, name in enumerate(
            ("mars", "jupiter", "mercury", "venus", "saturn", "sun", "moon")
        ):
            __cells[name] = tuple(__image.segment(
                __image.get_other_color(source, i), (4, 3)))

    def __daemon_proc():
        u"""精霊ブロック画像加工。
        """
        source = __image.load(container.get("daemon.png"))
        images = tuple(__image.get_other_color(source, i) for i in range(8))
        __cells["gargoyle"] = tuple(__image.segment(images[3], (4, 2))[0:1])
        for name, image in zip(
            ("ice_ghost", "poison_ghost", "fire_ghost"), images[:3]
        ):
            __cells[name] = tuple(__image.segment(image, (4, 2))[4:8])
        for name, image in zip(
            ("maxwell", "eater", "arch_demon", "demon"), images[4:]
        ):
            __cells[name] = tuple(__image.segment(image, (4, 2))[0:4])

    def __slime_proc():
        u"""スライム・きのこ画像加工。
        """
        source = __image.load(container.get("slime.png"))
        for i, name, in enumerate((
            "slime", "large_matango", "tired", "matango"
        )):
            images = __image.segment(
                __image.get_other_color(source, i), (4, 2))
            if i in (1, 3):
                __cells[name] = images[4:]
            elif i in (2,):
                __cells[name] = tuple(images[3:4])
            else:
                __cells[name] = tuple(images[1:2]+images[:3])

    def __nature_proc():
        u"""水系画像加工。
        """
        source = __image.load(container.get("nature.png"))
        for i, name in enumerate((
            "magma", "ice", "", "Corrosion", "acid", "poison", "water"
        )):
            if name:
                if i == 1:
                    __cells[name] = tuple(__image.segment(
                        __image.get_other_color(source, i), (4, 2))[4:])
                else:
                    __cells[name] = tuple(__image.segment(
                        __image.get_other_color(source, i), (4, 2))[:4])

    def __stone_proc():
        u"""石化画像加工。
        """
        source = __image.load(container.get("stone.png"))
        for i, name in enumerate(("chocolate", "stone")):
            __cells[name] = tuple(__image.segment(
                __image.get_other_color(source, i, 8), (4, 4)))

    def __other_proc():
        u"""その他画像加工。
        """
        source = __image.load(container.get("other.png"))
        for i, name in enumerate(("rip", "ruin")):
            __cells[name] = __image.segment(
                __image.get_other_color(source, i), (4, 2))[i],

    def __shards_proc():
        u"""力の欠片の画像加工。
        """
        source = __image.load(container.get("shards.png"))
        for i, name in enumerate((
            "speed_shards", "power_shards", "protect_shards", "life_shards"
        )):
            __cells[name] = tuple(__image.segment(__image.get_other_color(
                source, i), (4, 2))[4:])

    def __next_proc():
        u"""ネクスト表示で使用する画像加工。
        """
        source = __image.load(container.get("small.png"))
        for i in range(10):
            images = __image.segment(__image.get_other_color(
                source, i, 8), (4, 2), (8, 8))
            for j, name in enumerate((
                "square", "circle", "diamond", "star", "rect", "!", "?"
            )):
                __cells[name+"_"+str(i)] = images[j]

    def __icon_proc():
        u"""アイコン画像を使用するブロック画像加工。
        """
        import icon as _icon
        import string as __string
        for name, color, ky_rng, chst_rng in (
            ("black", 8, 0, 0), ("yellow", 1, 3, 0), ("white", 2, 1, 1),
            ("red", 6, 0, 3), ("blue", 9, 0, 0), ("green", 5, 0, 0),
            ("purple", 3, 0, 0)
        ):
            icon = _icon.get(6, 0, color)
            __cells[name+"_key"] = tuple([
                __string.get_subscript(icon, str(i)) for
                i in range(ky_rng, 0, -1)]+[icon])
            icon = _icon.get(7, 0, color)
            __cells[name+"_chest"] = tuple([
                __string.get_subscript(icon, str(i)) for
                i in range(chst_rng, 0, -1)]+[icon, _icon.get(8, 0, color)])
            __cells[name+"_mimic"] = tuple([
                _icon.get(i, 0, color) for i in (7, 9, 10, 9)])
            __cells[name+"_card"] = tuple([
                _icon.get(i, 0, color) for i in range(2, 6)]+[
                    __pygame.transform.flip(
                        _icon.get(i, 0, color), True, False) for
                    i in range(4, 2, -1)])
    __cells = {}
    surf = __pygame.Surface((16, 16))
    __image.set_colorkey(surf, "0x000000")
    __cells["dummy"] = surf,
    for func in (
        __target_proc, __basic_proc, __star_proc, __daemon_proc,
        __slime_proc, __nature_proc, __stone_proc, __other_proc,
        __shards_proc, __next_proc, __icon_proc,
    ):
        func()


def get(key):
    u"""ブロック画像取得。
    """
    return __cells[key]
