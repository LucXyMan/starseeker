#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""body.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

体防具設定モジュール。
"""


def get():
    u"""体防具取得。
    """
    import equip as __equip
    import utils.const as __const
    import utils.general as __general

    class __Body(__equip.Armor):
        u"""体防具データ。
        """
        __slots__ = ()
        _CORRECTION = 0.5

        def is_prevention(self, change):
            u"""ブロック変化防止判定。
            """
            prevent, _ = self._ability.string.split("###")
            return change in prevent.split("#")

        @property
        def is_body(self):
            u"""体防具判定。
            """
            return True
    return (
        __Body(
            0xB40, __const.CLOTHES_CATEGORY +
            u"#ドンキーベスト#布の服#",
            8, __const.MID_CORRECTION),
        __Body(
            0xC42, __const.CLOTHES_CATEGORY +
            u"#シープウェア#羊毛の服#",
            15, __const.MID_CORRECTION,
            keys=(u"ドンキーベスト",)),
        __Body(
            0xB48, __const.CLOTHES_CATEGORY +
            u"#ワイルドゴート#山羊毛皮の服#",
            24, __const.MID_CORRECTION,
            keys=(u"シープウェア",)),
        __Body(
            0xC46, __const.CLOTHES_CATEGORY +
            u"#キャメルウェア#砂漠の国の服#炎上防止",
            35, __const.LOW_CORRECTION,
            ability=__equip.Ability("Magma###"),
            keys=(u"ワイルドゴート",)),
        __Body(
            0xD42, __const.CLOTHES_CATEGORY +
            u"#アルパカウェア#アルパカ毛皮の服#凍結防止",
            47, __const.LOW_CORRECTION,
            ability=__equip.Ability("Ice###"),
            keys=(u"ワイルドゴート",)),
        __Body(
            0xE4D, __const.CLOTHES_CATEGORY +
            u"#ゴールデンフリース#金羊毛の服#" +
            __general.get_skill_description(__const.HALF_VENUS_SKILL),
            56, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.HALF_VENUS_SKILL)),
            keys=(u"アルパカウェア", u"キャメルウェア")),
        __Body(
            0xB45, __const.CLOTHES_CATEGORY +
            u"#サテュロスウェア#精霊の服#" +
            __general.get_skill_description(__const.SHORT_TURN_SKILL),
            61, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.SHORT_TURN_SKILL)),
            keys=(u"アルパカウェア", u"キャメルウェア")),
        __Body(
            0xE48, __const.CLOTHES_CATEGORY +
            u"#バフォメット#悪魔崇拝者の服#" +
            __general.get_skill_description(__const.NECROMANCER_SKILL),
            67, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.NECROMANCER_SKILL)),
            keys=(u"ゴールデンフリース", u"サテュロスウェア")),
        __Body(
            0xE40, __const.CLOTHES_CATEGORY +
            u"#ケリュネイア#女神の加護の服#酸・毒・石化・破壊・キノコ防止",
            73, __const.LOW_CORRECTION,
            ability=__equip.Ability("Acid#Poison#Stone#Ruined#Matango###"),
            keys=(u"ゴールデンフリース", u"サテュロスウェア")),
        __Body(
            0xF4F, __const.ROBE_CATEGORY +
            u"#サニーローブ#晴天のローブ#凍結防止",
            17, __const.LOW_CORRECTION,
            ability=__equip.Ability("Ice###")),
        __Body(
            0x057, __const.ROBE_CATEGORY +
            u"#レイニーローブ#雨のローブ#" +
            __general.get_skill_description(__const.HALF_MERCURY_SKILL),
            22, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.HALF_MERCURY_SKILL))),
        __Body(
            0xF42, __const.ROBE_CATEGORY +
            u"#クラウディローブ#雲のローブ#炎上・破壊防止",
            33, __const.LOW_CORRECTION,
            ability=__equip.Ability("Magma#Ruined###"),
            keys=(u"レイニーローブ",)),
        __Body(
            0x157, __const.ROBE_CATEGORY +
            u"#スノーローブ#雪のローブ#凍結・炎上防止",
            38, __const.LOW_CORRECTION,
            ability=__equip.Ability("Ice#Magma###"),
            keys=(u"レイニーローブ",)),
        __Body(
            0x15D, __const.ROBE_CATEGORY +
            u"#サンダーローブ#雷を帯びたローブ#凍結・石化・キノコ防止",
            41, __const.LOW_CORRECTION,
            ability=__equip.Ability("Ice#Stone#Matango###"),
            keys=(u"サニーローブ",)),
        __Body(
            0x055, __const.ROBE_CATEGORY +
            u"#ウインディローブ#風のローブ#" +
            __general.get_skill_description(__const.SPEEDSTER_SKILL),
            46, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.SPEEDSTER_SKILL)),
            keys=(u"サンダーローブ",)),
        __Body(
            0x158, __const.ROBE_CATEGORY +
            u"#ダストローブ#流砂のローブ#" +
            __general.get_skill_description(__const.HALF_SATURN_SKILL),
            54, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.HALF_SATURN_SKILL)),
            keys=(u"クラウディローブ",)),
        __Body(
            0x25A, __const.ROBE_CATEGORY +
            u"#オーロラローブ#夜の輝きのローブ#" +
            __general.get_skill_description(__const.MOON_CHILD_SKILL),
            60, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.MOON_CHILD_SKILL)),
            keys=(u"スノーローブ", u"ダストローブ")),
        __Body(
            0x257, __const.ROBE_CATEGORY +
            u"#ミラージュローブ#幻影のローブ#" +
            __general.get_skill_description(__const.WATER_PRESS_SKILL),
            63, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.WATER_PRESS_SKILL)),
            keys=(u"ウインディローブ",)),
        __Body(
            0x25B, __const.ROBE_CATEGORY +
            u"#プリズムローブ#虹のローブ#悪霊退散",
            74, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                __const.DEMON_NAMES+"#"+__const.GHOST_NAMES+"###"),
            keys=(u"オーロラローブ", u"ミラージュローブ",)),
        __Body(
            0x25E, __const.ROBE_CATEGORY +
            u"#エクリプスローブ#光と闇のローブ#様々なステータス防止",
            82, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.IRREGULAR_NAMES+"###"),
            keys=(u"プリズムローブ",)),
        __Body(
            0x351, __const.ARMOR_CATEGORY +
            u"#タートルシェル#一般的な鎧#",
            8, __const.MID_CORRECTION),
        __Body(
            0x556, __const.ARMOR_CATEGORY +
            u"#リザードメイル#革の鎧#",
            14, __const.MID_CORRECTION,
            keys=(u"タートルシェル",)),
        __Body(
            0x458, __const.ARMOR_CATEGORY +
            u"#スネークチェイン#鎖をあみ込んだ鎧#",
            26, __const.MID_CORRECTION,
            keys=(u"タートルシェル",)),
        __Body(
            0x553, __const.ARMOR_CATEGORY +
            u"#アリゲータープレート#大ワニの皮の鎧#",
            34, __const.MID_CORRECTION,
            keys=(u"リザードメイル",)),
        __Body(
            0x455, __const.ARMOR_CATEGORY +
            u"#ヒュドラチェイン#多頭竜の皮の鎧#毒防止",
            35, __const.LOW_CORRECTION,
            ability=__equip.Ability("Poison###"),
            keys=(u"スネークチェイン",)),
        __Body(
            0x858, __const.ARMOR_CATEGORY +
            u"#ディノレザー#竜の皮の鎧#炎上防止",
            44, __const.LOW_CORRECTION,
            ability=__equip.Ability("Magma###"),
            keys=(u"アリゲータープレート", u"ヒュドラチェイン")),
        __Body(
            0x554, __const.ARMOR_CATEGORY +
            u"#バシリスク#蛇王の鎧#毒・石化防止",
            49, __const.LOW_CORRECTION,
            ability=__equip.Ability("Poison#Stone###"),
            keys=(u"アリゲータープレート", u"ヒュドラチェイン")),
        __Body(
            0x955, __const.ARMOR_CATEGORY +
            u"#ワイバーン#飛竜の皮の鎧#酸・破壊防止",
            52, __const.LOW_CORRECTION,
            ability=__equip.Ability("Acid#Ruined###"),
            keys=(u"バシリスク",)),
        __Body(
            0x652, __const.ARMOR_CATEGORY +
            u"#ブラキオシェル#巨人の鎧#",
            58, __const.MID_CORRECTION,
            keys=(u"ディノレザー",)),
        __Body(
            0x55D, __const.ARMOR_CATEGORY +
            u"#ギュスタヴプレート#巨大生物の皮の鎧#" +
            __general.get_skill_description(__const.TOUGHNESS_SKILL),
            62, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.TOUGHNESS_SKILL)),
            keys=(u"アリゲータープレート",)),
        __Body(
            0xb5F, __const.ARMOR_CATEGORY +
            u"#サラマンダー#燃え盛る鎧#凍結・キノコ防止",
            64, __const.LOW_CORRECTION,
            ability=__equip.Ability("Ice#Matango###"),
            keys=(u"ディノレザー", u"ワイバーン")),
        __Body(
            0xB50, __const.ARMOR_CATEGORY +
            u"#アイスドレイク#凍てつく鎧#毒・炎上防止",
            65, __const.LOW_CORRECTION,
            ability=__equip.Ability("Poison#Magma###"),
            keys=(u"バシリスク", u"ブラキオシェル")),
        __Body(
            0xA51, __const.ARMOR_CATEGORY +
            u"#ドラゴンアーマー#竜鱗の鎧#酸・凍結・炎上防止",
            73, __const.LOW_CORRECTION,
            ability=__equip.Ability("Acid#Ice#Magma###"),
            keys=(u"サラマンダー", u"アイスドレイク")),
        __Body(
            0x454, __const.ARMOR_CATEGORY +
            u"#ラドゥーンチェイン#神話の怪物の鎧#酸・毒防止",
            77, __const.LOW_CORRECTION,
            ability=__equip.Ability("Acid#Poison###"),
            keys=(u"ヒュドラチェイン", u"バシリスク")),
        __Body(
            0x854, __const.ARMOR_CATEGORY +
            u"#タイラントレザー#暴帝の鎧#石化・炎上・破壊防止",
            81, __const.LOW_CORRECTION,
            ability=__equip.Ability("Stone#Magma#Ruined###"),
            keys=(u"ディノレザー",)),
        __Body(
            0x957, __const.ARMOR_CATEGORY +
            u"#リンドヴルム#飛竜王の皮の鎧#酸・炎上・破壊防止",
            87, __const.LOW_CORRECTION,
            ability=__equip.Ability("Acid#Magma#Ruined###"),
            keys=(u"ワイバーン",)),
        __Body(
            0x655, __const.ARMOR_CATEGORY +
            u"#ウルトラシェル#鉄人の鎧#",
            90, __const.MID_CORRECTION,
            keys=(u"ブラキオシェル",)),
        __Body(
            0xA5B, __const.ARMOR_CATEGORY +
            u"#ニーズヘッグ#呪われし鎧#" +
            __general.get_skill_description(__const.POISON_SUMMON_SKILL),
            92, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.POISON_SUMMON_SKILL)),
            keys=(u"ドラゴンアーマー", u"ラドゥーンチェイン", u"タイラントレザー")),
        __Body(
            0xA54, __const.ARMOR_CATEGORY +
            u"#ウロボロス#錬金術で作られた鎧#酸・毒・石化・破壊防止",
            95, __const.LOW_CORRECTION,
            ability=__equip.Ability("Acid#Poison#Stone#Ruined###"),
            keys=(u"ドラゴンアーマー", u"リンドヴルム", u"ウルトラシェル")),
        __Body(
            0xA5D, __const.ARMOR_CATEGORY +
            u"#ファヴニール#黄金の鎧#毒・凍結・炎上・キノコ防止",
            102, __const.LOW_CORRECTION,
            ability=__equip.Ability("Poison#Ice#Magma#Matango###"),
            keys=(u"ギュスタヴプレート", u"ニーズヘッグ", u"ウロボロス")),
        __Body(
            0x357, __const.ARMOR_CATEGORY +
            u"#アダマンタートル#不滅の金属の鎧#あらゆるステータス防止",
            118, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability(
                __const.IRREGULAR_NAMES+"#"+__const.DEMON_NAMES+"#" +
                __const.GHOST_NAMES+"###"),
            keys=(u"ファヴニール",)))
