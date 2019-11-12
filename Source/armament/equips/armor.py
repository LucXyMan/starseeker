#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""armor.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

防具設定モジュール。
"""


def get():
    u"""防具取得。
    """
    import equip as __equip
    import utils.const as __const

    class __Armor(__equip.Equip):
        u"""防具データ。
        """
        __slots__ = ()

        @property
        def is_armor(self):
            u"""防具判定。
            """
            return True

    class __Head(__Armor):
        u"""頭防具データ。
        """
        __slots__ = ()
        _CORRECTION = 0.025

        def get_persistence(self, turn):
            u"""頭防具効果を取得。
            """
            if self._ability.target:
                new, old = self._ability.target.split("##")
                if turn & self._ability.interval == 0:
                    return new, old.split("#"), (1, 1)
            return ()

        @property
        def is_head(self):
            u"""頭防具判定。
            """
            return True

    class __Body(__Armor):
        u"""体防具データ。
        """
        __slots__ = ()
        _CORRECTION = 0.05

        def is_prevention(self, target):
            u"""ブロック変化防止の場合に真。
            """
            return target in tuple(
                self._ability.target.split("#") if self._ability else ())

        @property
        def is_body(self):
            u"""体防具判定。
            """
            return True

    class __Accessory(__Armor):
        u"""装飾品データ。
        """
        __slots__ = ()
        _CORRECTION = 0.0125

        @property
        def addition(self):
            u"""パターン変更リクエストを取得。
            """
            if self._ability.target:
                new, old = self._ability.target.split("##")
                return self._ability.is_single, new, old
            return ()

        @property
        def is_accessory(self):
            u"""装飾品判定。
            """
            return True
    return (
        __Head(
            0xE36, __const.HAT_CATEGORY +
            u"#うり帽子#うりぼうの帽子#",
            40, __const.MID_CORRECTION),
        __Head(
            0xB39, __const.HAT_CATEGORY +
            u"#トラ猫フード#猫又族のフード#",
            80, __const.MID_CORRECTION),
        __Head(
            0xC36, __const.HAT_CATEGORY +
            u"#うさ耳帽子#うさぎ毛皮の帽子#",
            110, __const.MID_CORRECTION),
        __Head(
            0xF31, __const.HAT_CATEGORY +
            u"#ドッグフード#犬の毛の帽子#",
            140, __const.MID_CORRECTION),
        __Head(
            0x045, __const.HAT_CATEGORY +
            u"#アマガエルフード#カエル族の帽子#ポイズン浄化",
            150, __const.MID_CORRECTION, ability=__equip.Ability(
                "Water##Poison", interval=0b0)),
        __Head(
            0xF32, __const.HAT_CATEGORY +
            u"#ウルフード#狼の毛の帽子#",
            190, __const.MID_CORRECTION, keys=(82,)),
        __Head(
            0xB37, __const.HAT_CATEGORY +
            u"#ケットシーの帽子#猫又がかぶる帽子#",
            210, __const.MID_CORRECTION, keys=(80,)),
        __Head(
            0xE38, __const.HAT_CATEGORY +
            u"#エリュマントス#大イノシシの皮の帽子#土スター破壊",
            230, __const.VERY_HIGH_CORRECTION, ability=__equip.Ability(
                "Ruined##Saturn", interval=0b0), keys=(79,)),
        __Head(
            0x043, __const.HAT_CATEGORY +
            u"#ウーパーフード#ウーパー族の帽子#スライム生成",
            280, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Slime##"+__const.BASIC_NAMES, interval=0b11), keys=(83,)),
        __Head(
            0xF3F, __const.HAT_CATEGORY +
            u"#ヘルハウンド#燃える帽子#マグマを火スターに",
            300, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Mars##Magma", interval=0b0), keys=(84,)),
        __Head(
            0xE33, __const.HAT_CATEGORY +
            u"#マタンゴピッグ#マタンゴ豚の帽子#キノコを木スターに",
            330, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Jupiter##Matango", interval=0b0), keys=(86,)),
        __Head(
            0xC3B, __const.HAT_CATEGORY +
            u"#ムーンラビット#月光の帽子#月スター生成",
            370, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Moon##"+__const.BASIC_NAMES, interval=0b11), keys=(81,)),
        __Head(
            0x343, __const.HAT_CATEGORY +
            u"#カーバンクル#宝石で装飾された帽子#土スター生成",
            410, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Saturn##"+__const.BASIC_NAMES, interval=0b11), keys=(90,)),
        __Head(
            0x347, __const.HAT_CATEGORY +
            u"#スピンクス#退魔の帽子#悪霊を太陽スターに",
            450, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Sun##"+__const.DEMON_NAMES+"#"+__const.GHOST_NAMES,
                interval=0b0), keys=(85,)),
        __Head(
            0xB34, __const.HAT_CATEGORY +
            u"#ブラックキャット#魔除けの帽子#ジョーカー消去",
            500, __const.VERY_LOW_CORRECTION, ability=__equip.Ability(
                "Normal##Joker", interval=0b0), keys=(91, 92)),
        __Head(
            0xF3A, __const.HAT_CATEGORY +
            u"#フェンリルレザー#大狼の毛皮#力の欠片生成",
            540, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Power##"+__const.BASIC_NAMES, interval=0b111), keys=(88,)),
        __Head(
            0x546, __const.HELMET_CATEGORY +
            u"#スタッグレザー#革製の兜#",
            50, __const.MID_CORRECTION),
        __Head(
            0x441, __const.HELMET_CATEGORY +
            u"#パプキンサレット#メッキの兜#",
            140, __const.MID_CORRECTION, keys=(95,)),
        __Head(
            0x445, __const.HELMET_CATEGORY +
            u"#パラワンヘルム#闘士の兜#",
            220, __const.MID_CORRECTION, keys=(96,)),
        __Head(
            0x54C, __const.HELMET_CATEGORY +
            u"#レインボーメット#虹の兜#イレギュラー浄化",
            330, __const.VERY_LOW_CORRECTION, ability=__equip.Ability(
                "Water##"+__const.IRREGULAR_NAMES, interval=0b0),
            keys=(83, 88, 89)),
        __Head(
            0x642, __const.HELMET_CATEGORY +
            u"#インペリアスヘルム#帝王の兜#",
            360, __const.MID_CORRECTION, keys=(97,)),
        __Head(
            0x544, __const.HELMET_CATEGORY +
            u"#レギウスヘルム#王者の兜#守りの欠片生成",
            430, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Protect##"+__const.BASIC_NAMES, interval=0b111), keys=(99,)),
        __Head(
            0x64A, __const.HELMET_CATEGORY +
            u"#ドラゴンヘルム#竜の兜#太陽スター破壊",
            460, __const.VERY_HIGH_CORRECTION, ability=__equip.Ability(
                "Ruined##Sun", interval=0b0), keys=(99, 98)),
        __Head(
            0x547, __const.HELMET_CATEGORY +
            u"#リオテミスヘルム#妖精の兜#ミミックを金スターに",
            570, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Venus##"+__const.MIMIC_NAMES, interval=0b0), keys=(101,)),
        __Head(
            0x743, __const.HELMET_CATEGORY +
            u"#ビートルメット#鉄の兜#",
            60, __const.MID_CORRECTION),
        __Head(
            0x841, __const.HELMET_CATEGORY +
            u"#コーカサスヘルム#戦士の兜#",
            120, __const.MID_CORRECTION, keys=(103,)),
        __Head(
            0x844, __const.HELMET_CATEGORY +
            u"#アトラスヘルム#巨人の兜#生命の欠片生成",
            300, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Life##"+__const.BASIC_NAMES, interval=0b111), keys=(104,)),
        __Head(
            0x846, __const.HELMET_CATEGORY +
            u"#ケンタウルスヘルム#人馬種族の兜#速さの欠片生成",
            340, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Speed##"+__const.BASIC_NAMES, interval=0b111), keys=(98,)),
        __Head(
            0x74D, __const.HELMET_CATEGORY +
            u"#ゴールドヘルム#黄金の兜#金スター生成",
            370, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Venus##"+__const.BASIC_NAMES, interval=0b11), keys=(106,)),
        __Head(
            0x943, __const.HELMET_CATEGORY +
            u"#ネプチューンメット#海神の兜#アイスを水スターに",
            410, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Mercury##Ice", interval=0b0), keys=(107,)),
        __Head(
            0x947, __const.HELMET_CATEGORY +
            u"#ヘラクレスヘルム#英雄の兜#",
            490, __const.MID_CORRECTION, keys=(108,)),
        __Head(
            0x94C, __const.HELMET_CATEGORY +
            u"#サタンヘッド#魔王の兜#ストーンを土スターに",
            580, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Saturn##Stone", interval=0b0), keys=(100, 109)),
        __Body(
            0xB40, __const.CLOTHES_CATEGORY +
            u"#ドンキーベスト#布の服#",
            40, __const.MID_CORRECTION),
        __Body(
            0xB48, __const.CLOTHES_CATEGORY +
            u"#ワイルドゴート#山羊毛皮の服#",
            70, __const.MID_CORRECTION, keys=(111,)),
        __Body(
            0xD42, __const.CLOTHES_CATEGORY +
            u"#アルパカウェア#アルパカ毛皮の服#凍結防止",
            140, __const.LOW_CORRECTION,
            ability=__equip.Ability("Ice"), keys=(112,)),
        __Body(
            0xC41, __const.CLOTHES_CATEGORY +
            u"#キャメルウェア#砂漠の国の服#マグ炎上防止",
            220, __const.LOW_CORRECTION,
            ability=__equip.Ability("Magma"), keys=(113,)),
        __Body(
            0xE4D, __const.CLOTHES_CATEGORY +
            u"#ゴールデンフリース#金羊毛の服#酸・毒・キノコ防止",
            310, __const.LOW_CORRECTION,
            ability=__equip.Ability("Acid#Poison#Matango"), keys=(114,)),
        __Body(
            0xE48, __const.CLOTHES_CATEGORY +
            u"#バフォメット#悪魔崇拝者の服#毒・石・破壊防止",
            400, __const.LOW_CORRECTION,
            ability=__equip.Ability("Poison#Stone#Ruined"), keys=(114,)),
        __Body(
            0xE40, __const.CLOTHES_CATEGORY +
            u"#ケリュネイア#女神の加護の服#酸・毒・石・破壊・キノコ防止",
            590, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Acid#Poison#Stone#Ruined#Matango"), keys=(115, 116)),
        __Body(
            0xF4F, __const.ROBE_CATEGORY +
            u"#サニーローブ#晴天のローブ#凍結防止",
            90, __const.LOW_CORRECTION, ability=__equip.Ability("Ice")),
        __Body(
            0x057, __const.ROBE_CATEGORY +
            u"#レイニーローブ#雨のローブ#炎上防止",
            220, __const.LOW_CORRECTION, ability=__equip.Ability("Magma")),
        __Body(
            0xF42, __const.ROBE_CATEGORY +
            u"#クラウディローブ#雲のローブ#破壊防止",
            260, __const.LOW_CORRECTION,
            ability=__equip.Ability("Ruined"), keys=(119,)),
        __Body(
            0x15D, __const.ROBE_CATEGORY +
            u"#サンダーローブ#雷を帯びたローブ#キノコ防止",
            330, __const.LOW_CORRECTION,
            ability=__equip.Ability("Matango"), keys=(118,)),
        __Body(
            0x158, __const.ROBE_CATEGORY +
            u"#ダストローブ#流砂のローブ#石防止",
            400, __const.LOW_CORRECTION,
            ability=__equip.Ability("Stone"), keys=(120,)),
        __Body(
            0x25B, __const.ROBE_CATEGORY +
            u"#プリズムローブ#虹のローブ#悪霊退散",
            490, __const.LOW_CORRECTION, ability=__equip.Ability(
                __const.DEMON_NAMES+"#"+__const.GHOST_NAMES), keys=(121, 122)),
        __Body(
            0x25E, __const.ROBE_CATEGORY +
            u"#エクリプスローブ#光と闇のローブ#様々なステータス防止",
            550, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.IRREGULAR_NAMES), keys=(123,)),
        __Body(
            0x351, __const.ARMOR_CATEGORY +
            u"#タートルシェル#一般的な鎧#",
            80, __const.MID_CORRECTION),
        __Body(
            0x556, __const.ARMOR_CATEGORY +
            u"#リザードメイル#革の鎧#",
            110, __const.MID_CORRECTION, keys=(125,)),
        __Body(
            0x458, __const.ARMOR_CATEGORY +
            u"#スネークチェイン#鎖をあみ込んだ鎧#",
            160, __const.MID_CORRECTION, keys=(126,)),
        __Body(
            0x553, __const.ARMOR_CATEGORY +
            u"#アリゲータープレート#大ワニの皮の鎧#",
            200, __const.MID_CORRECTION, keys=(126,)),
        __Body(
            0x858, __const.ARMOR_CATEGORY +
            u"#ディノレザー#竜の皮の鎧#炎上防止",
            240, __const.LOW_CORRECTION,
            ability=__equip.Ability("Magma"), keys=(128,)),
        __Body(
            0x955, __const.ARMOR_CATEGORY +
            u"#ワイバーン#飛竜の皮の鎧#破壊防止",
            290, __const.LOW_CORRECTION,
            ability=__equip.Ability("Ruined"), keys=(129,)),
        __Body(
            0x455, __const.ARMOR_CATEGORY +
            u"#ヒュドラチェイン#多頭竜の皮の鎧#毒防止",
            330, __const.LOW_CORRECTION,
            ability=__equip.Ability("Poison"), keys=(127,)),
        __Body(
            0x554, __const.ARMOR_CATEGORY +
            u"#バシリスク#蛇王の鎧#石防止",
            370, __const.LOW_CORRECTION,
            ability=__equip.Ability("Stone"), keys=(131,)),
        __Body(
            0x652, __const.ARMOR_CATEGORY +
            u"#ブラキオシェル#巨人の鎧#",
            410, __const.MID_CORRECTION, keys=(129,)),
        __Body(
            0xb5F, __const.ARMOR_CATEGORY +
            u"#サラマンダー#燃え盛る鎧#凍結・キノコ防止",
            440, __const.LOW_CORRECTION,
            ability=__equip.Ability("Ice#Matango"), keys=(132,)),
        __Body(
            0xB50, __const.ARMOR_CATEGORY +
            u"#アイスドレイク#凍てつく鎧#毒・炎上防止",
            450, __const.LOW_CORRECTION,
            ability=__equip.Ability("Poison#Magma"), keys=(132,)),
        __Body(
            0xA51, __const.ARMOR_CATEGORY +
            u"#ドラゴンアーマー#竜鱗の鎧#酸・炎上防止",
            500, __const.LOW_CORRECTION, ability=__equip.Ability("Acid#Magma"),
            keys=(133,)),
        __Body(
            0x454, __const.ARMOR_CATEGORY +
            u"#ラドゥーンチェイン#神話の怪物の鎧#酸・毒防止",
            570, __const.LOW_CORRECTION,
            ability=__equip.Ability("Acid#Poison"), keys=(131,)),
        __Body(
            0x854, __const.ARMOR_CATEGORY +
            u"#タイラントレザー#暴帝の鎧#石・炎上防止",
            610, __const.LOW_CORRECTION,
            ability=__equip.Ability("Stone#Magma"), keys=(129, 131)),
        __Body(
            0x957, __const.ARMOR_CATEGORY +
            u"#リンドヴルム#飛竜王の皮の鎧#炎上・破壊防止",
            670, __const.LOW_CORRECTION,
            ability=__equip.Ability("Magma#Ruined"), keys=(130,)),
        __Body(
            0x655, __const.ARMOR_CATEGORY +
            u"#ウルトラシェル#鉄人の鎧#",
            700, __const.MID_CORRECTION, keys=(133,)),
        __Body(
            0xA54, __const.ARMOR_CATEGORY +
            u"#ウロボロス#錬金術で作られた鎧#酸・毒・石・破壊防止",
            750, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Acid#Poison#Stone#Ruined"), keys=(116, 136)),
        __Body(
            0xA5D, __const.ARMOR_CATEGORY +
            u"#ファヴニール#黄金の鎧#毒・凍結・炎上・キノコ防止",
            820, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Poison#Ice#Magma#Matango"), keys=(134, 135, 136)),
        __Body(
            0x357, __const.ARMOR_CATEGORY +
            u"#アダマンタートル#不滅の金属の鎧#あらゆるステータス防止",
            900, __const.VERY_LOW_CORRECTION, ability=__equip.Ability(
                __const.IRREGULAR_NAMES+"#"+__const.DEMON_NAMES+"#" +
                __const.GHOST_NAMES), keys=(117, 124, 142)),
        __Accessory(
            0xC5F, __const.RING_CATEGORY +
            u"#ボリードリング#火球の指輪#マグマ生成",
            250, __const.HIGH_CORRECTION, ability=__equip.Ability(
                "Magma##"+__const.BASIC_NAMES, is_single=True), keys=(88,)),
        __Accessory(
            0xD50, __const.RING_CATEGORY +
            u"#クライオリング#氷の指輪#アイス生成",
            250, __const.HIGH_CORRECTION, ability=__equip.Ability(
                "Ice##"+__const.BASIC_NAMES, is_single=True), keys=(108,)),
        __Accessory(
            0xF5E, __const.RING_CATEGORY +
            u"#ヒドラリング#毒の指輪#ポイズン生成",
            250, __const.HIGH_CORRECTION, ability=__equip.Ability(
                "Poison##"+__const.BASIC_NAMES, is_single=True), keys=(83,)),
        __Accessory(
            0xE55, __const.RING_CATEGORY +
            u"#デメテルリング#豊穣の指輪#キノコ生成",
            250, __const.HIGH_CORRECTION, ability=__equip.Ability(
                "Matango##"+__const.BASIC_NAMES, is_single=True), keys=(89,)),
        __Accessory(
            0xE5C, __const.RING_CATEGORY +
            u"#エキドナリング#召喚師の指輪#イーター召喚",
            250, __const.HIGH_CORRECTION, ability=__equip.Ability(
                __const.BLOCK_EATER_EFFECT, is_single=True), keys=(92,)),
        __Accessory(
            0xC5B, __const.RING_CATEGORY +
            u"#ユーピテルリング#天空の指輪#木スター生成",
            500, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Jupiter##"+__const.BASIC_NAMES, is_single=True), keys=(147,)),
        __Accessory(
            0xD5F, __const.RING_CATEGORY +
            u"#プロミネンスリング#炎の指輪#火スター生成",
            500, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Mars##"+__const.BASIC_NAMES, is_single=True), keys=(144,)),
        __Accessory(
            0xF52, __const.RING_CATEGORY +
            u"#テラリング#大地の指輪#土スター生成",
            500, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Saturn##"+__const.BASIC_NAMES, is_single=True), keys=(146,)),
        __Accessory(
            0xE5D, __const.RING_CATEGORY +
            u"#ミダスリング#黄金の指輪#金スター生成",
            500, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Venus##"+__const.BASIC_NAMES, is_single=True), keys=(148,)),
        __Accessory(
            0xF53, __const.RING_CATEGORY +
            u"#ネプチューンリング#海神の指輪#水スター生成",
            500, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Mercury##"+__const.BASIC_NAMES, is_single=True), keys=(145,)),
        __Accessory(
            0xE58, __const.RING_CATEGORY +
            u"#ブラックホールリング#暗黒の指輪#月スター生成",
            1000, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Moon##"+__const.BASIC_NAMES, is_single=True),
            keys=(150, 151, 152)),
        __Accessory(
            0xC50, __const.RING_CATEGORY +
            u"#ダイヤモンドリング#光の指輪#太陽スター生成",
            1000, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Sun##"+__const.BASIC_NAMES, is_single=True),
            keys=(149, 152, 153)),
        __Accessory(
            0xC5D, __const.RING_CATEGORY +
            u"#ミルキーリング#天の川の指輪#生命の欠片生成",
            2000, __const.VERY_LOW_CORRECTION, ability=__equip.Ability(
                __const.LIFE_EFFECT, is_single=True), keys=(154, 155)),
        __Accessory(
            0xE5F, __const.RING_CATEGORY +
            u"#クエーサーリング#力を秘めた指輪#力の欠片生成",
            2000, __const.VERY_LOW_CORRECTION, ability=__equip.Ability(
                __const.POWER_EFFECT, is_single=True), keys=(154, 155)),
        __Accessory(
            0xF56, __const.RING_CATEGORY +
            u"#プラネタリング#惑星の指輪#守りの欠片生成",
            2000, __const.VERY_LOW_CORRECTION, ability=__equip.Ability(
                __const.PROTECT_EFFECT, is_single=True), keys=(154, 155)),
        __Accessory(
            0xD5B, __const.RING_CATEGORY +
            u"#コメットリング#彗星の指輪#速さの欠片生成",
            2000, __const.VERY_LOW_CORRECTION, ability=__equip.Ability(
                __const.SPEED_EFFECT, is_single=True), keys=(154, 155)),
        __Accessory(
            0xE5A, __const.RING_CATEGORY +
            u"#グランドクロスリング#無限の指輪#マクスウェルデーモン召喚",
            9990, 0, ability=__equip.Ability(
                "Maxwell##"+__const.BASIC_NAMES, is_single=True),
            keys=(156, 157, 158, 159)))
