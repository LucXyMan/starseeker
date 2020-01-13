#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""head.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

頭防具設定モジュール。
"""


def get():
    u"""頭防具取得。
    """
    import equip as __equip
    import utils.const as __const
    import utils.general as __general

    class __Head(__equip.Armor):
        u"""頭防具データ。
        """
        __slots__ = ()
        _CORRECTION = 0.25

        def get_persistence(self, turn):
            u"""頭防具効果取得。
            """
            change, _ = self._ability.string.split("###")
            if change:
                new, old = change.split("##")
                if turn & self._ability.interval == 0:
                    return new, old.split("#"), (1, 1)
            return ()

        @property
        def is_head(self):
            u"""頭防具判定。
            """
            return True
    return (
        __Head(
            0xD31, __const.HAT_CATEGORY +
            u"#ねずみ帽#ねずみ族の帽子#",
            5, __const.MID_CORRECTION),
        __Head(
            0xE36, __const.HAT_CATEGORY +
            u"#うり帽子#うりぼうの帽子#",
            9, __const.MID_CORRECTION,
            keys=(u"ねずみ帽",)),
        __Head(
            0xB39, __const.HAT_CATEGORY +
            u"#トラ猫フード#猫又族のフード#",
            13, __const.MID_CORRECTION,
            keys=(u"ねずみ帽",)),
        __Head(
            0xC36, __const.HAT_CATEGORY +
            u"#うさ耳帽子#うさぎ毛皮の帽子#",
            14, __const.MID_CORRECTION,
            keys=(u"ねずみ帽",)),
        __Head(
            0xF31, __const.HAT_CATEGORY +
            u"#ドッグフード#犬の毛の帽子#",
            15, __const.MID_CORRECTION,
            keys=(u"ねずみ帽",)),
        __Head(
            0x045, __const.HAT_CATEGORY +
            u"#アマガエルフード#カエル族の帽子#ポイズン浄化",
            18, __const.MID_CORRECTION,
            ability=__equip.Ability("Water##Poison###", interval=0b0),
            keys=(u"トラ猫フード",)),
        __Head(
            0xF32, __const.HAT_CATEGORY +
            u"#ウルフード#狼の毛の帽子#",
            23, __const.MID_CORRECTION,
            keys=(u"ドッグフード",)),
        __Head(
            0xB37, __const.HAT_CATEGORY +
            u"#ケットシーの帽子#猫又がかぶる帽子#",
            28, __const.MID_CORRECTION,
            keys=(u"トラ猫フード",)),
        __Head(
            0xE38, __const.HAT_CATEGORY +
            u"#エリュマントス#大イノシシの皮の帽子#土スター破壊",
            31, __const.VERY_HIGH_CORRECTION,
            ability=__equip.Ability("Ruined##Saturn###", interval=0b0),
            keys=(u"うり帽子",)),
        __Head(
            0x043, __const.HAT_CATEGORY +
            u"#ウーパーフード#ウーパー族の帽子#スライム生成",
            34, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "Slime##"+__const.BASIC_NAMES+"###", interval=0b11),
            keys=(u"アマガエルフード",)),
        __Head(
            0xF3F, __const.HAT_CATEGORY +
            u"#ヘルハウンド#燃える帽子#マグマを火スターに",
            38, __const.LOW_CORRECTION,
            ability=__equip.Ability("Mars##Magma###", interval=0b0),
            keys=(u"ウルフード",)),
        __Head(
            0xE33, __const.HAT_CATEGORY +
            u"#マタンゴピッグ#マタンゴ豚の帽子#キノコを木スターに",
            42, __const.LOW_CORRECTION,
            ability=__equip.Ability("Jupiter##Matango###", interval=0b0),
            keys=(u"エリュマントス",)),
        __Head(
            0xC3C, __const.HAT_CATEGORY +
            u"#ムーンラビット#月光の帽子#月スター生成",
            45, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.MOON_CHANGE+"###", interval=0b11),
            keys=(u"うさ耳帽子", u"ケットシーの帽子",)),
        __Head(
            0x34D, __const.HAT_CATEGORY +
            u"#グレムリンキャップ#雷を帯びた帽子#" +
            __general.get_skill_description(__const.POWER_STROKE_SKILL),
            46, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.POWER_STROKE_SKILL)),
            keys=(u"マタンゴピッグ", u"ムーンラビット")),
        __Head(
            0xD3F, __const.HAT_CATEGORY +
            u"#火ねずみの頭巾#火ねずみの皮の頭巾#火スター生成",
            48, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.MARS_CHANGE+"###", interval=0b11),
            keys=(u"ヘルハウンド",)),
        __Head(
            0x343, __const.HAT_CATEGORY +
            u"#カーバンクル#宝石で装飾された帽子#土スター生成",
            50, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                __const.SATURN_CHANGE+"###", interval=0b11),
            keys=(u"ケットシーの帽子",)),
        __Head(
            0xD38, __const.HAT_CATEGORY +
            u"#ラーテルフード#毒よけの帽子#" +
            __general.get_skill_description(__const.SAFETY_SKILL),
            56, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.SAFETY_SKILL)),
            keys=(u"グレムリンキャップ",)),
        __Head(
            0x347, __const.HAT_CATEGORY +
            u"#スピンクス#退魔の帽子#悪霊を太陽スターに",
            59, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "Sun##"+__const.DEMON_NAMES+"#"+__const.GHOST_NAMES+"###",
                interval=0b0),
            keys=(u"ムーンラビット", u"カーバンクル")),
        __Head(
            0xB34, __const.HAT_CATEGORY +
            u"#ブラックキャット#魔除けの帽子#ジョーカー消去",
            66, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability("Normal##Joker###", interval=0b0),
            keys=(u"ムーンラビット", u"カーバンクル", u"ラーテルフード")),
        __Head(
            0xD3B, __const.HAT_CATEGORY +
            u"#ラタトスク#世界樹の葉の帽子#木スター生成",
            75, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                __const.JUPITER_CHANGE+"###", interval=0b11),
            keys=(u"火ねずみの頭巾", u"スピンクス", u"ブラックキャット")),
        __Head(
            0xF3A, __const.HAT_CATEGORY +
            u"#フェンリルレザー#大狼の毛皮#力の欠片生成",
            82, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "Power##"+__const.BASIC_NAMES+"###", interval=0b111),
            keys=(u"火ねずみの頭巾",  u"ウーパーフード", u"ブラックキャット")),
        __Head(
            0x546, __const.HELMET_CATEGORY +
            u"#スタッグレザー#革製の兜#",
            9, __const.MID_CORRECTION),
        __Head(
            0x441, __const.HELMET_CATEGORY +
            u"#パプキンサレット#メッキの兜#",
            17, __const.MID_CORRECTION,
            keys=(u"スタッグレザー",)),
        __Head(
            0x445, __const.HELMET_CATEGORY +
            u"#パラワンヘルム#闘士の兜#",
            24, __const.MID_CORRECTION,
            keys=(u"パプキンサレット",)),
        __Head(
            0x642, __const.HELMET_CATEGORY +
            u"#インペリアスヘルム#帝王の兜#",
            36, __const.MID_CORRECTION,
            keys=(u"パラワンヘルム",)),
        __Head(
            0x544, __const.HELMET_CATEGORY +
            u"#レギウスヘルム#王者の兜#守りの欠片生成",
            43, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "Protect##"+__const.BASIC_NAMES+"###", interval=0b111),
            keys=(u"パラワンヘルム",)),
        __Head(
            0x64A, __const.HELMET_CATEGORY +
            u"#ドラゴンヘルム#竜の兜#太陽スター破壊",
            52, __const.VERY_HIGH_CORRECTION,
            ability=__equip.Ability("Ruined##Sun###", interval=0b0),
            keys=(u"インペリアスヘルム", u"レギウスヘルム")),
        __Head(
            0x54C, __const.HELMET_CATEGORY +
            u"#レインボーメット#虹の兜#イレギュラー浄化",
            63, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability(
                "Water##"+__const.IRREGULAR_NAMES+"###", interval=0b0),
            keys=(u"ドラゴンヘルム",)),
        __Head(
            0x547, __const.HELMET_CATEGORY +
            u"#リオテミスヘルム#妖精の兜#ミミックを金スターに",
            67, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "Venus##"+__const.MIMIC_NAMES+"###", interval=0b0),
            keys=(u"ドラゴンヘルム",)),
        __Head(
            0x44D, __const.HELMET_CATEGORY +
            u"#フォーチュンヘルム#幸運の兜#" +
            __general.get_skill_description(__const.PHANTOM_THIEF_SKILL),
            72, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.PHANTOM_THIEF_SKILL)),
            keys=(u"リオテミスヘルム",)),
        __Head(
            0x649, __const.HELMET_CATEGORY +
            u"#ギラファヘルム#麒麟の兜#" +
            __general.get_skill_description(__const.LIFE_BOOST_SKILL),
            85, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.LIFE_BOOST_SKILL)),
            keys=(u"レインボーメット", u"リオテミスヘルム",)),
        __Head(
            0x743, __const.HELMET_CATEGORY +
            u"#ビートルメット#鉄の兜#",
            16, __const.MID_CORRECTION),
        __Head(
            0x841, __const.HELMET_CATEGORY +
            u"#コーカサスヘルム#戦士の兜#",
            22, __const.MID_CORRECTION,
            keys=(u"ビートルメット",)),
        __Head(
            0x844, __const.HELMET_CATEGORY +
            u"#アトラスヘルム#巨人の兜#生命の欠片生成",
            37, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "Life##"+__const.BASIC_NAMES+"###", interval=0b111),
            keys=(u"コーカサスヘルム",)),
        __Head(
            0x846, __const.HELMET_CATEGORY +
            u"#ケンタウルスヘルム#人馬種族の兜#速さの欠片生成",
            39, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "Speed##"+__const.BASIC_NAMES+"###", interval=0b111),
            keys=(u"コーカサスヘルム",)),
        __Head(
            0x947, __const.HELMET_CATEGORY +
            u"#グラントヘルム#白亜の兜#太陽スター生成",
            45, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.SUN_CHANGE+"###", interval=0b11),
            keys=(u"アトラスヘルム", u"ケンタウルスヘルム")),
        __Head(
            0x943, __const.HELMET_CATEGORY +
            u"#ネプチューンメット#海神の兜#アイスを水スターに",
            52, __const.LOW_CORRECTION,
            ability=__equip.Ability("Mercury##Ice###", interval=0b0),
            keys=(u"アトラスヘルム", u"ケンタウルスヘルム")),
        __Head(
            0x74D, __const.HELMET_CATEGORY +
            u"#ゴールドヘルム#黄金の兜#金スター生成",
            56, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.VENUS_CHANGE+"###", interval=0b11),
            keys=(u"グラントヘルム",)),
        __Head(
            0x949, __const.HELMET_CATEGORY +
            u"#ヘラクレスヘルム#英雄の兜#",
            64, __const.MID_CORRECTION,
            keys=(u"ネプチューンメット",)),
        __Head(
            0x94C, __const.HELMET_CATEGORY +
            u"#サタンヘッド#魔王の兜#ストーンを土スターに",
            75, __const.LOW_CORRECTION,
            ability=__equip.Ability("Saturn##Stone###", interval=0b0),
            keys=(u"ネプチューンメット",)),
        __Head(
            0x84F, __const.HELMET_CATEGORY +
            u"#マルスヘルム#戦神の兜#" +
            __general.get_skill_description(__const.HALF_MARS_SKILL),
            81, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.HALF_MARS_SKILL)),
            keys=(u"ヘラクレスヘルム", u"サタンヘッド")),
        __Head(
            0xA45, __const.CROWN_CATEGORY +
            u"#スタークラウン#ゲームクリアの褒章#全アルカナコスト減少",
            1, 0,
            ability=__equip.Ability("###"+__general.get_skill_names(
                __const.HALF_JUPITER_SKILL, __const.HALF_MARS_SKILL,
                __const.HALF_SATURN_SKILL, __const.HALF_VENUS_SKILL,
                __const.HALF_MERCURY_SKILL, __const.MOON_CHILD_SKILL,
                __const.SON_OF_SUN_SKILL)),
            seals=(35,)),
        __Head(
            0xA48, __const.CROWN_CATEGORY +
            u"#エンドレスクラウン#エンドレス突破の褒章#ブロック消去強化",
            1, 0,
            ability=__equip.Ability("###"+__general.get_skill_names(
                __const.POWER_STROKE_SKILL, __const.COMPLETE_ASSIST_SKILL)),
            seals=(-1,)),
        __Head(
            0xA49, __const.CROWN_CATEGORY +
            u"#カードクラウン#カードコンプの褒章#カード操作強化",
            1, 0, ability=__equip.Ability("###"+__general.get_skill_names(
                __const.ROB_CARD_SKILL, __const.DOUBLE_SPELL_SKILL,
                __const.SOUL_EAT_SKILL)),
            seals=(-4,)),
        __Head(
            0xA46, __const.CROWN_CATEGORY +
            u"#アイテムクラウン#アイテムコンプの褒章#全ての欠片効果倍増",
            1, 0, ability=__equip.Ability("###"+__general.get_skill_names(
                __const.LIFE_BOOST_SKILL, __const.MIGHTY_SKILL,
                __const.TOUGHNESS_SKILL, __const.SPEEDSTER_SKILL)),
            seals=(-2,)),
        __Head(
            0xA4D, __const.CROWN_CATEGORY +
            u"#マスタークラウン#クラウンコンプの褒章#ジョーカー無効化",
            1, 0, ability=__equip.Ability("###"+__general.get_skill_names(
                __const.PHANTOM_THIEF_SKILL, __const.PURIFY_SKILL,
                __const.TALISMAN_SKILL)),
            seals=(-3,)))
