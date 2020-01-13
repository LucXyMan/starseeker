#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""accessory.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

装飾設定モジュール。
"""


def get():
    u"""装飾取得。
    """
    import equip as __equip
    import utils.const as __const

    class __Accessory(__equip.Armor):
        u"""装飾データ。
        """
        __slots__ = ()
        _CORRECTION = 0.125

        @property
        def spell(self):
            u"""装飾効果取得。
            """
            change, _ = self._ability.string.split("###")
            if change:
                new, old = change.split("##")
                return self._ability.is_single, new, old
            return ()

        @property
        def is_accessory(self):
            u"""装飾品判定。
            """
            return True
    return (
        __Accessory(
            0xC5F, __const.RING_CATEGORY +
            u"#ボリードリング#火球の指輪#マグマ生成",
            50, __const.HIGH_CORRECTION,
            ability=__equip.Ability(
                __const.MAGMA_CHANGE+"###", is_single=True)),
        __Accessory(
            0xD50, __const.RING_CATEGORY +
            u"#クライオリング#氷の指輪#アイス生成",
            50, __const.HIGH_CORRECTION,
            ability=__equip.Ability(__const.ICE_CHANGE+"###", is_single=True)),
        __Accessory(
            0xF5E, __const.RING_CATEGORY +
            u"#ヒドラリング#毒の指輪#ポイズン生成",
            50, __const.HIGH_CORRECTION,
            ability=__equip.Ability(
                __const.POISON_CHANGE+"###", is_single=True)),
        __Accessory(
            0xE55, __const.RING_CATEGORY +
            u"#デメテルリング#豊穣の指輪#キノコ生成",
            50, __const.HIGH_CORRECTION,
            ability=__equip.Ability(
                __const.MATANGO_CHANGE+"###", is_single=True)),
        __Accessory(
            0xD5D, __const.RING_CATEGORY +
            u"#アシッドリング#酸性雨の指輪#アシッド生成",
            50, __const.HIGH_CORRECTION,
            ability=__equip.Ability(
                __const.ACID_CHANGE+"###", is_single=True)),
        __Accessory(
            0xC5B, __const.RING_CATEGORY +
            u"#ユーピテルリング#天空の指輪#木スター生成",
            70, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                __const.JUPITER_CHANGE+"###", is_single=True),
            keys=(u"デメテルリング",)),
        __Accessory(
            0xD5F, __const.RING_CATEGORY +
            u"#プロミネンスリング#炎の指輪#火スター生成",
            70, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                __const.MARS_CHANGE+"###", is_single=True),
            keys=(u"ボリードリング",)),
        __Accessory(
            0xF52, __const.RING_CATEGORY +
            u"#テラリング#大地の指輪#土スター生成",
            70, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                __const.SATURN_CHANGE+"###", is_single=True),
            keys=(u"ヒドラリング",)),
        __Accessory(
            0xE5D, __const.RING_CATEGORY +
            u"#ミダスリング#黄金の指輪#金スター生成",
            70, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                __const.VENUS_CHANGE+"###", is_single=True),
            keys=(u"アシッドリング",)),
        __Accessory(
            0xF53, __const.RING_CATEGORY +
            u"#ネプチューンリング#海神の指輪#水スター生成",
            70, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                __const.MERCURY_CHANGE+"###", is_single=True),
            keys=(u"クライオリング",)),
        __Accessory(
            0xE58, __const.RING_CATEGORY +
            u"#ブラックホールリング#暗黒の指輪#月スター生成",
            100, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                __const.MOON_CHANGE+"###", is_single=True),
            keys=(u"プロミネンスリング", u"テラリング")),
        __Accessory(
            0xC50, __const.RING_CATEGORY +
            u"#ダイヤモンドリング#光の指輪#太陽スター生成",
            100, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.SUN_CHANGE+"###", is_single=True),
            keys=(u"ユーピテルリング", u"ミダスリング", u"ネプチューンリング")),
        __Accessory(
            0xF57, __const.RING_CATEGORY +
            u"#パルサーリング#輝きの指輪#ジョーカー消去",
            120, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability("Normal##Joker###"),
            keys=(u"ダイヤモンドリング",)),
        __Accessory(
            0xE5C, __const.RING_CATEGORY +
            u"#エキドナリング#召喚師の指輪#イーター召喚",
            120, __const.HIGH_CORRECTION,
            ability=__equip.Ability(
                __const.BLOCK_EATER_CHANGE+"###", is_single=True),
            keys=(u"ブラックホールリング",)),
        __Accessory(
            0xE5E, __const.RING_CATEGORY +
            u"#ネメシスリング#神罰の指輪#ストーン生成",
            120, __const.VERY_HIGH_CORRECTION,
            ability=__equip.Ability(__const.STONE_CHANGE+"###"),
            keys=(u"ブラックホールリング",)),
        __Accessory(
            0xC5D, __const.RING_CATEGORY +
            u"#ミルキーリング#天の川の指輪#生命の欠片生成",
            200, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability(
                __const.LIFE_CHANGE+"###", is_single=True),
            keys=(u"ブラックホールリング", u"ダイヤモンドリング")),
        __Accessory(
            0xE5F, __const.RING_CATEGORY +
            u"#クエーサーリング#力を秘めた指輪#力の欠片生成",
            200, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability(
                __const.POWER_CHANGE+"###", is_single=True),
            keys=(u"ブラックホールリング", u"ダイヤモンドリング")),
        __Accessory(
            0xF56, __const.RING_CATEGORY +
            u"#プラネタリング#惑星の指輪#守りの欠片生成",
            200, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability(
                __const.PROTECT_CHANGE+"###", is_single=True),
            keys=(u"ブラックホールリング", u"ダイヤモンドリング")),
        __Accessory(
            0xD5B, __const.RING_CATEGORY +
            u"#コメットリング#彗星の指輪#速さの欠片生成",
            200, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability(
                __const.SPEED_CHANGE+"###", is_single=True),
            keys=(u"ブラックホールリング", u"ダイヤモンドリング")),
        __Accessory(
            0xE5A, __const.RING_CATEGORY +
            u"#グランドクロスリング#無限の指輪#マクスウェルデーモン召喚",
            999, 0,
            ability=__equip.Ability(
                "Maxwell##"+__const.BASIC_NAMES+"###", is_single=True),
            keys=(
                u"ミルキーリング", u"クエーサーリング",
                u"プラネタリング", u"コメットリング")))
