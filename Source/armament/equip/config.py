#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""config.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

装備設定モジュール。
"""


def init():
    u"""アイテムコレクション作成。
    """
    import data as __data
    import utils.const as __const
    VERY_LOW_CORRECTION = 0.2
    LOW_CORRECTION = 0.8
    MID_CORRECTION = 1.0
    HIGH_CORRECTION = 1.2
    VERY_HIGH_CORRECTION = 1.8
    __data.Equip.set_collections((
        __data.Equip(0x000, u"空#装備なし#何もない#", 0, 0),
        __data.Weapon(
            0xE02, __const.SWORD_CATEGORY+u"#チキンナイフ#小さなナイフ#",
            10, MID_CORRECTION),
        __data.Weapon(
            0xF03, __const.SWORD_CATEGORY+u"#スパロウダガー#小さなダガー#",
            40, MID_CORRECTION, keys=(1,)),
        __data.Weapon(
            0xF0F, __const.SWORD_CATEGORY+u"#ブラッドフィンチ#血塗られたナイフ#ポイズン攻撃",
            120, LOW_CORRECTION, __data.Skill(__const.POISON_EFFECT),
            keys=(2,)),
        __data.Weapon(
            0x015, __const.SWORD_CATEGORY+u"#アエローダガー#鳥人が使うダガー#",
            150, MID_CORRECTION, keys=(3,)),
        __data.Weapon(
            0x014, __const.SWORD_CATEGORY+u"#サイレンダガー#沈黙のダガー#スター・カード破壊",
            250, LOW_CORRECTION, skill=__data.Skill(
                "Ruined##"+__const.STAR_NAMES+"#"+__const.CARD_NAMES),
            keys=(4,)),
        __data.Weapon(
            0x017, __const.SWORD_CATEGORY+u"#エンゼルフェザー#天使の羽のナイフ#",
            360, MID_CORRECTION, keys=(5,)),
        __data.Weapon(
            0x110, __const.SWORD_CATEGORY+u"#クロウソード#どこにでもある剣#",
            30, MID_CORRECTION),
        __data.Weapon(
            0x217, __const.SWORD_CATEGORY+u"#ガルブレイド#海兵のサーベル#",
            40, MID_CORRECTION, keys=(7,)),
        __data.Weapon(
            0x316, __const.SWORD_CATEGORY+u"#ルーンオウル#儀式用の剣#",
            60, MID_CORRECTION, keys=(8,)),
        __data.Weapon(
            0x511, __const.SWORD_CATEGORY+u"#アーキオエッジ#古代文明の剣#",
            100, MID_CORRECTION, keys=(9,)),
        __data.Weapon(
            0x414, __const.SWORD_CATEGORY+u"#アイスペンギー#氷の刃を持つ剣#アイス攻撃",
            120, LOW_CORRECTION, skill=__data.Skill(__const.ICE_EFFECT),
            keys=(10,)),
        __data.Weapon(
            0xB11, __const.SWORD_CATEGORY+u"#ヴァルチャーソード#傭兵が使う剣#",
            150, MID_CORRECTION, keys=(8,)),
        __data.Weapon(
            0x813, __const.SWORD_CATEGORY+u"#イーグルクレイモア#ハイランダーの剣#",
            200, MID_CORRECTION, keys=(12,)),
        __data.Weapon(
            0x712, __const.SWORD_CATEGORY+u"#ホークバスタード#騎士が使う剣#",
            230, MID_CORRECTION, keys=(13,)),
        __data.Weapon(
            0x919, __const.SWORD_CATEGORY+u"#グレートオストリッチ#巨大な刀身を持つ斬馬剣#",
            250, MID_CORRECTION, keys=(14,)),
        __data.Weapon(
            0x917, __const.SWORD_CATEGORY+u"#ディアトリマ#蛮竜族が使う剛剣#力の欠片攻撃",
            270, VERY_HIGH_CORRECTION, skill=__data.Skill(
                __const.POWER_EFFECT, is_single=True), keys=(15,)),
        __data.Weapon(
            0x51C, __const.SWORD_CATEGORY+u"#ストラス#黒い刀身を持つ魔石剣#土スター攻撃",
            290, HIGH_CORRECTION, skill=__data.Skill(
                __const.SATURN_EFFECT, is_single=True), keys=(10,)),
        __data.Weapon(
            0x31B, __const.SWORD_CATEGORY+u"#コカドリーユ#呪われし剣#ストーン攻撃",
            310, LOW_CORRECTION, skill=__data.Skill(__const.STONE_EFFECT),
            keys=(9,)),
        __data.Weapon(
            0xA16, __const.SWORD_CATEGORY+u"#カサワリフランベルク#波型の刃を持つ剣#",
            330, MID_CORRECTION, keys=(14,)),
        __data.Weapon(
            0x41F, __const.SWORD_CATEGORY+u"#フェニックス#炎の刀身を持つ不折剣#火スター攻撃",
            360, HIGH_CORRECTION, skill=__data.Skill(
                __const.MARS_EFFECT, is_single=True), keys=(17,)),
        __data.Weapon(
            0x61A, __const.SWORD_CATEGORY+u"#カラドリウス#天使に鍛えられた剣#太陽スター攻撃",
            400, HIGH_CORRECTION, skill=__data.Skill(
                __const.SUN_EFFECT, is_single=True), keys=(6, 23)),
        __data.Weapon(
            0x817, __const.SWORD_CATEGORY+u"#ロックセイバー#巨獣殺しの剣#",
            420, MID_CORRECTION, keys=(14,)),
        __data.Weapon(
            0xC11, __const.SWORD_CATEGORY+u"#フレスヴェルグ#風を呼ぶ聖剣#アイス攻撃",
            450, LOW_CORRECTION, skill=__data.Skill(__const.ICE_EFFECT),
            keys=(17,)),
        __data.Weapon(
            0xc1B, __const.SWORD_CATEGORY+u"#ヴィゾフニル#霊鳥の尾羽から作られた魔剣#マグマ攻撃",
            490, LOW_CORRECTION, skill=__data.Skill(__const.MAGMA_EFFECT),
            keys=(23,)),
        __data.Weapon(
            0xA1F, __const.SWORD_CATEGORY+u"#ガルトマーン#竜殺しの剣#",
            560, MID_CORRECTION, keys=(15,)),
        __data.Weapon(
            0xF16, __const.SWORD_CATEGORY+u"#隼#東方の戦士の剣#",
            250, MID_CORRECTION, keys=(12,)),
        __data.Weapon(
            0xE13, __const.SWORD_CATEGORY+u"#飛燕#切れ味鋭い名刀#",
            310, MID_CORRECTION, keys=(26,)),
        __data.Weapon(
            0xD14, __const.SWORD_CATEGORY+u"#大鴉#漆黒の大刀#月スター攻撃",
            400, HIGH_CORRECTION, skill=__data.Skill(
                __const.MOON_EFFECT, is_single=True), keys=(27,)),
        __data.Weapon(
            0xF17, __const.SWORD_CATEGORY+u"#天鳥船#さまよう魂を導く神刀#悪霊退散",
            520, HIGH_CORRECTION, skill=__data.Skill(
                "Normal##"+__const.DEMON_NAMES+"#"+__const.GHOST_NAMES),
            keys=(6, 28)),
        __data.Weapon(
            0xD2F, __const.WAND_CATEGORY+u"#ファイアイリス#輝く炎の杖#マグマ攻撃",
            50, LOW_CORRECTION, skill=__data.Skill(__const.MAGMA_EFFECT)),
        __data.Weapon(
            0x030, __const.WAND_CATEGORY+u"#フロストフラワー#凍てつく氷の杖#アイス攻撃",
            140, LOW_CORRECTION, skill=__data.Skill(__const.ICE_EFFECT)),
        __data.Weapon(
            0xE25, __const.WAND_CATEGORY+u"#エアヒヤシンス#西風を呼ぶ杖#速さの欠片攻撃",
            180, VERY_HIGH_CORRECTION, skill=__data.Skill(
                __const.SPEED_EFFECT, is_single=True), keys=(31,)),
        __data.Weapon(
            0xF2D, __const.WAND_CATEGORY+u"#サンダーリコリス#雷鳴の杖#",
            200, MID_CORRECTION, keys=(30,)),
        __data.Weapon(
            0x03C, __const.WAND_CATEGORY+u"#アースラフレシア#大地の杖#アシッド攻撃",
            240, LOW_CORRECTION, skill=__data.Skill(__const.ACID_EFFECT),
            keys=(33,)),
        __data.Weapon(
            0xF2F, __const.WAND_CATEGORY+u"#マンドレーク#呪術師の杖#ポイズン攻撃",
            280, LOW_CORRECTION, skill=__data.Skill(__const.POISON_EFFECT),
            keys=(32,)),
        __data.Weapon(
            0xE23, __const.WAND_CATEGORY+u"#アルラウネ#妖精の杖#生命の欠片攻撃",
            300, VERY_HIGH_CORRECTION, skill=__data.Skill(
                __const.LIFE_EFFECT, is_single=True), keys=(34,)),
        __data.Weapon(
            0x13D, __const.WAND_CATEGORY+u"#サンフラワー#太陽の杖#太陽スター攻撃",
            310, HIGH_CORRECTION, skill=__data.Skill(
                __const.SUN_EFFECT, is_single=True), keys=(34,)),
        __data.Weapon(
            0xD27, __const.WAND_CATEGORY+u"#ドライアド#精霊の杖#木スター攻撃",
            360, HIGH_CORRECTION, skill=__data.Skill(
                __const.JUPITER_EFFECT, is_single=True), keys=(36,)),
        __data.Weapon(
            0xF28, __const.WAND_CATEGORY+u"#アスフォデルス#冥王の杖#イーター攻撃",
            440, VERY_LOW_CORRECTION, skill=__data.Skill(
                __const.BLOCK_EATER_EFFECT, is_single=True),
            keys=(35, 148, 154)),
        __data.Weapon(
            0xF2B, __const.WAND_CATEGORY+u"#ユグドラシル#世界樹の杖#キノコ攻撃",
            500, LOW_CORRECTION, skill=__data.Skill(__const.MATANGO_EFFECT),
            keys=(38, 39)),
        __data.Weapon(
            0x920, __const.HEAVY_CATEGORY+u"#ヒポポタマス#木の棍棒#",
            70, MID_CORRECTION),
        __data.Weapon(
            0xA23, __const.HEAVY_CATEGORY+u"#ホースフレイル#木のフレイル#",
            110, MID_CORRECTION, keys=(41,)),
        __data.Weapon(
            0xC26, __const.HEAVY_CATEGORY+u"#エレファントハンマー#重量ハンマー#",
            160, MID_CORRECTION, keys=(41,)),
        __data.Weapon(
            0xC24, __const.HEAVY_CATEGORY+u"#ナイトメア#悪魔の戦槌#スター・欠片破壊",
            230, LOW_CORRECTION, skill=__data.Skill(
                "Ruined##"+__const.STAR_NAMES+"#"+__const.SHARD_NAMES),
            keys=(43,)),
        __data.Weapon(
            0x924, __const.HEAVY_CATEGORY+u"#カトブレパス#呪いのメイス#ストーン攻撃",
            280, LOW_CORRECTION, skill=__data.Skill(__const.STONE_EFFECT),
            keys=(44,)),
        __data.Weapon(
            0xA27, __const.HEAVY_CATEGORY+u"#ペガサスフレイル#天空のフレイル#",
            310, MID_CORRECTION, keys=(42,)),
        __data.Weapon(
            0x92C, __const.HEAVY_CATEGORY+u"#ベヒモスワンド#巨大なメイス#",
            370, MID_CORRECTION, keys=(45,)),
        __data.Weapon(
            0xC27, __const.HEAVY_CATEGORY+u"#スレイプニル#神の鉄槌#マグマ攻撃",
            490, LOW_CORRECTION, skill=__data.Skill(__const.MAGMA_EFFECT),
            keys=(46,)),
        __data.Weapon(
            0xC2D, __const.HEAVY_CATEGORY+u"#ガネーシャ#超重量ハンマー#",
            580, MID_CORRECTION, keys=(47,)),
        __data.Weapon(
            0x425, __const.HEAVY_CATEGORY+u"#ワイルドスピア#狩猟用の槍#",
            60, MID_CORRECTION),
        __data.Weapon(
            0x322, __const.HEAVY_CATEGORY+u"#レパードランス#騎士が使う槍#",
            120, MID_CORRECTION, keys=(50,)),
        __data.Weapon(
            0x429,  __const.HEAVY_CATEGORY+u"#タイガースピア#戦闘用の槍#",
            190, MID_CORRECTION, keys=(51,)),
        __data.Weapon(
            0x326, __const.HEAVY_CATEGORY+u"#レオランス#勇者の槍#",
            260, MID_CORRECTION, keys=(52,)),
        __data.Weapon(
            0x32C, __const.HEAVY_CATEGORY+u"#セリオン#漆黒の魔槍#ストーン攻撃",
            320, LOW_CORRECTION, skill=__data.Skill(__const.STONE_EFFECT),
            keys=(45, 53)),
        __data.Weapon(
            0x524, __const.HEAVY_CATEGORY+u"#キメラトライデント#魔法合金の槍#",
            430, MID_CORRECTION, keys=(54,)),
        __data.Weapon(
            0x527, __const.HEAVY_CATEGORY+u"#グリュプス#神々の槍#アイス攻撃",
            520, LOW_CORRECTION, skill=__data.Skill(__const.ICE_EFFECT),
            keys=(55,)),
        __data.Weapon(
            0x621, __const.HEAVY_CATEGORY+u"#オックスアクス#木こりの斧#",
            50, MID_CORRECTION),
        __data.Weapon(
            0x628, __const.HEAVY_CATEGORY+u"#ヌーアクス#兵隊の斧#",
            110, MID_CORRECTION, keys=(57,)),
        __data.Weapon(
            0x720, __const.HEAVY_CATEGORY+u"#バッファロー#大きな斧#",
            230, MID_CORRECTION, keys=(58,)),
        __data.Weapon(
            0x726, __const.HEAVY_CATEGORY+u"#バイソンラブリュス#戦闘用の斧#",
            260, MID_CORRECTION, keys=(59,)),
        __data.Weapon(
            0x825, __const.HEAVY_CATEGORY+u"#ミノタウロス#巨大な戦斧#守りの欠片攻撃",
            350, VERY_HIGH_CORRECTION, skill=__data.Skill(
                __const.PROTECT_EFFECT, is_single=True), keys=(43, 60)),
        __data.Weapon(
            0x724, __const.HEAVY_CATEGORY+u"#牛鬼#鬼神の斧#キー・チェスト破壊",
            550, LOW_CORRECTION, skill=__data.Skill(
                "Ruined##"+__const.KEY_NAMES+"#"+__const.CHEST_NAMES),
            keys=(61,)),
        __data.Weapon(
            0x435, __const.MISSILE_CATEGORY+u"#ハニービー#狩猟用の弓#",
            60, MID_CORRECTION),
        __data.Weapon(
            0x534, __const.MISSILE_CATEGORY+u"#ホーネット#戦闘用の剛弓#",
            170, MID_CORRECTION, keys=(63,)),
        __data.Weapon(
            0x63D, __const.MISSILE_CATEGORY+u"#クインビー#王者の弓#スライム攻撃",
            280, VERY_HIGH_CORRECTION,
            skill=__data.Skill(__const.SLIME_EFFECT), keys=(66, 71)),
        __data.Weapon(
            0x538, __const.MISSILE_CATEGORY+u"#キラービー#必殺の剛弓#",
            320, MID_CORRECTION, keys=(64,)),
        __data.Weapon(
            0x530,  __const.MISSILE_CATEGORY+u"#ベルゼビュート#魔神の弓#ポイズン攻撃",
            450, LOW_CORRECTION, skill=__data.Skill(__const.POISON_EFFECT),
            keys=(66, 70)),
        __data.Weapon(
            0x833, __const.MISSILE_CATEGORY+u"#アントボウガン#機械じかけの弓#",
            120, MID_CORRECTION),
        __data.Weapon(
            0x933, __const.MISSILE_CATEGORY+u"#タランチュラ#毒のボウガン#ポイズン攻撃",
            160, LOW_CORRECTION, skill=__data.Skill(__const.POISON_EFFECT),
            keys=(68,)),
        __data.Weapon(
            0x93F, __const.MISSILE_CATEGORY+u"#ファイアアント#炎の矢を放つボウガン#マグマ攻撃",
            200, LOW_CORRECTION, skill=__data.Skill(__const.MAGMA_EFFECT),
            keys=(69,)),
        __data.Weapon(
            0x738, __const.MISSILE_CATEGORY+u"#アギトボウガン#巨大なボウガン#",
            230, MID_CORRECTION, keys=(68,)),
        __data.Weapon(
            0x930, __const.MISSILE_CATEGORY+u"#アイスアント#氷の矢を放つボウガン#アイス攻撃",
            350, LOW_CORRECTION, skill=__data.Skill(__const.ICE_EFFECT),
            keys=(71,)),
        __data.Weapon(
            0x834, __const.MISSILE_CATEGORY+u"#アラクネーボウガン#呪いのボウガン#ストーン攻撃",
            420, LOW_CORRECTION, skill=__data.Skill(__const.STONE_EFFECT),
            keys=(70, 71)),
        __data.Weapon(
            0xA3A, __const.MISSILE_CATEGORY+u"#スティンガー#広く流通する銃#",
            100, MID_CORRECTION),
        __data.Weapon(
            0xA3F, __const.MISSILE_CATEGORY+u"#レッドクロウ#真紅の銃#マグマ攻撃",
            150, LOW_CORRECTION, skill=__data.Skill(
                "Magma##"+__const.BASIC_NAMES), keys=(74,)),
        __data.Weapon(
            0xA35, __const.MISSILE_CATEGORY+u"#ストライプバーグ#改良型の銃#",
            270, MID_CORRECTION, keys=(75,)),
        __data.Weapon(
            0xA38, __const.MISSILE_CATEGORY+u"#インペラトール#銃の皇帝と呼ばれる#",
            350, MID_CORRECTION, keys=(76,)),
        __data.Weapon(
            0xA3C, __const.MISSILE_CATEGORY+u"#スコルピウス#英雄殺しの銃#",
            560, MID_CORRECTION, keys=(77,)),
        __data.Head(
            0xE36, __const.HAT_CATEGORY+u"#うり帽子#うりぼうの帽子#",
            40, MID_CORRECTION),
        __data.Head(
            0xB39, __const.HAT_CATEGORY+u"#トラ猫フード#猫又族のフード#",
            80, MID_CORRECTION),
        __data.Head(
            0xC36, __const.HAT_CATEGORY+u"#うさ耳帽子#うさぎ毛皮の帽子#",
            110, MID_CORRECTION),
        __data.Head(
            0xF31, __const.HAT_CATEGORY+u"#ドッグフード#犬の毛の帽子#",
            140, MID_CORRECTION),
        __data.Head(
            0x045, __const.HAT_CATEGORY+u"#アマガエルフード#カエル族の帽子#ポイズン浄化",
            150, MID_CORRECTION, skill=__data.Skill(
                "Water##Poison", interval=0b0)),
        __data.Head(
            0xF32, __const.HAT_CATEGORY+u"#ウルフード#狼の毛の帽子#",
            190, MID_CORRECTION, keys=(82,)),
        __data.Head(
            0xB37, __const.HAT_CATEGORY+u"#ケットシーの帽子#猫又がかぶる帽子#",
            210, MID_CORRECTION, keys=(80,)),
        __data.Head(
            0xE38, __const.HAT_CATEGORY+u"#エリュマントス#大イノシシの皮の帽子#土スター破壊",
            230, VERY_HIGH_CORRECTION, skill=__data.Skill(
                "Ruined##Saturn", interval=0b0), keys=(79,)),
        __data.Head(
            0x043, __const.HAT_CATEGORY+u"#ウーパーフード#ウーパー族の帽子#スライム生成",
            280, LOW_CORRECTION, skill=__data.Skill(
                "Slime##"+__const.BASIC_NAMES, interval=0b11), keys=(83,)),
        __data.Head(
            0xF3F, __const.HAT_CATEGORY+u"#ヘルハウンド#燃える帽子#マグマを火スターに",
            300, LOW_CORRECTION, skill=__data.Skill(
                "Mars##Magma", interval=0b0), keys=(84,)),
        __data.Head(
            0xE33, __const.HAT_CATEGORY+u"#マタンゴピッグ#マタンゴ豚の帽子#キノコを木スターに",
            330, LOW_CORRECTION, skill=__data.Skill(
                "Jupiter##Matango", interval=0b0), keys=(86,)),
        __data.Head(
            0xC3B, __const.HAT_CATEGORY+u"#ムーンラビット#月光の帽子#月スター生成",
            370, LOW_CORRECTION, skill=__data.Skill(
                "Moon##"+__const.BASIC_NAMES, interval=0b11), keys=(81,)),
        __data.Head(
            0x343, __const.HAT_CATEGORY+u"#カーバンクル#宝石で装飾された帽子#土スター生成",
            410, LOW_CORRECTION, skill=__data.Skill(
                "Saturn##"+__const.BASIC_NAMES, interval=0b11), keys=(90,)),
        __data.Head(
            0x347, __const.HAT_CATEGORY+u"#スピンクス#退魔の帽子#悪霊を太陽スターに",
            450, LOW_CORRECTION, skill=__data.Skill(
                "Sun##"+__const.DEMON_NAMES+"#"+__const.GHOST_NAMES,
                interval=0b0), keys=(85,)),
        __data.Head(
            0xB34, __const.HAT_CATEGORY+u"#ブラックキャット#魔除けの帽子#ジョーカー消去",
            500, VERY_LOW_CORRECTION, skill=__data.Skill(
                "Normal##Joeker", interval=0b0), keys=(91, 92)),
        __data.Head(
            0xF3A, __const.HAT_CATEGORY+u"#フェンリルレザー#大狼の毛皮#力の欠片生成",
            540, LOW_CORRECTION, skill=__data.Skill(
                "Power##"+__const.BASIC_NAMES, interval=0b111), keys=(88,)),
        __data.Head(
            0x546, __const.HELMET_CATEGORY+u"#スタッグレザー#革製の兜#",
            50, MID_CORRECTION),
        __data.Head(
            0x441, __const.HELMET_CATEGORY+u"#パプキンサレット#メッキの兜#",
            140, MID_CORRECTION, keys=(95,)),
        __data.Head(
            0x445, __const.HELMET_CATEGORY+u"#パラワンヘルム#闘士の兜#",
            220, MID_CORRECTION, keys=(96,)),
        __data.Head(
            0x54C, __const.HELMET_CATEGORY+u"#レインボーメット#虹の兜#イレギュラー浄化",
            330, VERY_LOW_CORRECTION, skill=__data.Skill(
                "Water##"+__const.IRREGULAR_NAMES, interval=0b0),
            keys=(83, 88, 89)),
        __data.Head(
            0x642, __const.HELMET_CATEGORY+u"#インペリアスヘルム#帝王の兜#",
            360, MID_CORRECTION, keys=(97,)),
        __data.Head(
            0x544, __const.HELMET_CATEGORY+u"#レギウスヘルム#王者の兜#守りの欠片生成",
            430, LOW_CORRECTION, skill=__data.Skill(
                "Protect##"+__const.BASIC_NAMES, interval=0b111), keys=(99,)),
        __data.Head(
            0x64A, __const.HELMET_CATEGORY+u"#ドラゴンヘルム#竜の兜#月スター破壊",
            460, VERY_HIGH_CORRECTION, skill=__data.Skill(
                "Ruined##Moon", interval=0b0), keys=(99, 98)),
        __data.Head(
            0x547, __const.HELMET_CATEGORY+u"#リオテミスヘルム#妖精の兜#ミミックを金スターに",
            570, LOW_CORRECTION, skill=__data.Skill(
                "Venus##"+__const.MIMIC_NAMES, interval=0b0), keys=(101,)),
        __data.Head(
            0x743, __const.HELMET_CATEGORY+u"#ビートルメット#鉄の兜#",
            60, MID_CORRECTION),
        __data.Head(
            0x841, __const.HELMET_CATEGORY+u"#コーカサスヘルム#戦士の兜#",
            120, MID_CORRECTION, keys=(103,)),
        __data.Head(
            0x844, __const.HELMET_CATEGORY+u"#アトラスヘルム#巨人の兜#生命の欠片生成",
            300, LOW_CORRECTION, skill=__data.Skill(
                "Life##"+__const.BASIC_NAMES, interval=0b111), keys=(104,)),
        __data.Head(
            0x846, __const.HELMET_CATEGORY+u"#ケンタウルスヘルム#人馬種族の兜#速さの欠片生成",
            340, LOW_CORRECTION, skill=__data.Skill(
                "Speed##"+__const.BASIC_NAMES, interval=0b111), keys=(98,)),
        __data.Head(
            0x74D, __const.HELMET_CATEGORY+u"#ゴールドヘルム#黄金の兜#金スター生成",
            370, LOW_CORRECTION, skill=__data.Skill(
                "Venus##"+__const.BASIC_NAMES, interval=0b11), keys=(106,)),
        __data.Head(
            0x943, __const.HELMET_CATEGORY+u"#ネプチューンメット#海神の兜#アイスを水スターに",
            410, LOW_CORRECTION, skill=__data.Skill(
                "Mercury##Ice", interval=0b0), keys=(107,)),
        __data.Head(
            0x947, __const.HELMET_CATEGORY+u"#ヘラクレスヘルム#英雄の兜#",
            490, MID_CORRECTION, keys=(108,)),
        __data.Head(
            0x94C, __const.HELMET_CATEGORY+u"#サタンヘッド#魔王の兜#ストーンを土スターに",
            580, LOW_CORRECTION, skill=__data.Skill(
                "Saturn##Stone", interval=0b0), keys=(100, 109)),
        __data.Body(
            0xB40, __const.CLOTHES_CATEGORY+u"#ドンキーベスト#布の服#",
            40, MID_CORRECTION),
        __data.Body(
            0xB48, __const.CLOTHES_CATEGORY+u"#ワイルドゴート#山羊毛皮の服#",
            70, MID_CORRECTION, keys=(111,)),
        __data.Body(
            0xD42, __const.CLOTHES_CATEGORY+u"#アルパカウェア#アルパカ毛皮の服#凍結防止",
            140, LOW_CORRECTION, __data.Skill("Ice"), keys=(112,)),
        __data.Body(
            0xC41, __const.CLOTHES_CATEGORY+u"#キャメルウェア#砂漠の国の服#マグ炎上防止",
            220, LOW_CORRECTION, __data.Skill("Magma"), keys=(113,)),
        __data.Body(
            0xE4D, __const.CLOTHES_CATEGORY+u"#ゴールデンフリース#金羊毛の服#酸・毒・キノコ防止",
            310, LOW_CORRECTION, skill=__data.Skill("Acid#Poison#Matango"),
            keys=(114,)),
        __data.Body(
            0xE48, __const.CLOTHES_CATEGORY+u"#バフォメット#悪魔崇拝者の服#毒・石・破壊防止",
            400, LOW_CORRECTION, skill=__data.Skill("Poison#Stone#Ruined"),
            keys=(114,)),
        __data.Body(
            0xE40, __const.CLOTHES_CATEGORY+u"#ケリュネイア#女神の加護の服#酸・毒・石・破壊・キノコ防止",
            590, LOW_CORRECTION, skill=__data.Skill(
                "Acid#Poison#Stone#Ruined#Matango"), keys=(115, 116)),
        __data.Body(
            0xF4F, __const.ROBE_CATEGORY+u"#サニーローブ#晴天のローブ#凍結防止",
            90, LOW_CORRECTION, skill=__data.Skill("Ice")),
        __data.Body(
            0x057, __const.ROBE_CATEGORY+u"#レイニーローブ#雨のローブ#炎上防止",
            220, LOW_CORRECTION, skill=__data.Skill("Magma")),
        __data.Body(
            0xF42, __const.ROBE_CATEGORY+u"#クラウディローブ#雲のローブ#破壊防止",
            260, LOW_CORRECTION, skill=__data.Skill("Ruined"),
            keys=(119,)),
        __data.Body(
            0x15D, __const.ROBE_CATEGORY+u"#サンダーローブ#雷を帯びたローブ#キノコ防止",
            330, LOW_CORRECTION, skill=__data.Skill("Matango"),
            keys=(118,)),
        __data.Body(
            0x158, __const.ROBE_CATEGORY+u"#ダストローブ#流砂のローブ#石防止",
            400, LOW_CORRECTION, skill=__data.Skill("Stone"),
            keys=(120,)),
        __data.Body(
            0x25B, __const.ROBE_CATEGORY+u"#プリズムローブ#虹のローブ#悪霊退散",
            490, LOW_CORRECTION, skill=__data.Skill(
                __const.DEMON_NAMES+"#"+__const.GHOST_NAMES), keys=(121, 122)),
        __data.Body(
            0x25E, __const.ROBE_CATEGORY+u"#エクリプスローブ#光と闇のローブ#様々なステータス防止",
            550, LOW_CORRECTION, skill=__data.Skill(__const.IRREGULAR_NAMES),
            keys=(123,)),
        __data.Body(
            0x351, __const.ARMOR_CATEGORY+u"#タートルシェル#一般的な鎧#",
            80, MID_CORRECTION),
        __data.Body(
            0x556, __const.ARMOR_CATEGORY+u"#リザードメイル#革の鎧#",
            110, MID_CORRECTION, keys=(125,)),
        __data.Body(
            0x458, __const.ARMOR_CATEGORY+u"#スネークチェイン#鎖をあみ込んだ鎧#",
            160, MID_CORRECTION, keys=(126,)),
        __data.Body(
            0x553, __const.ARMOR_CATEGORY+u"#アリゲータープレート#大ワニの皮の鎧#",
            200, MID_CORRECTION, keys=(126,)),
        __data.Body(
            0x858, __const.ARMOR_CATEGORY+u"#ディノレザー#竜の皮の鎧#炎上防止",
            240, LOW_CORRECTION, skill=__data.Skill("Magma"), keys=(128,)),
        __data.Body(
            0x955, __const.ARMOR_CATEGORY+u"#ワイバーン#飛竜の皮の鎧#破壊防止",
            290, LOW_CORRECTION, skill=__data.Skill("Ruined"), keys=(129,)),
        __data.Body(
            0x455, __const.ARMOR_CATEGORY+u"#ヒュドラチェイン#多頭竜の皮の鎧#毒防止",
            330, LOW_CORRECTION, skill=__data.Skill("Poison"), keys=(127,)),
        __data.Body(
            0x554, __const.ARMOR_CATEGORY+u"#バシリスク#蛇王の鎧#石防止",
            370, LOW_CORRECTION, skill=__data.Skill("Stone"), keys=(131,)),
        __data.Body(
            0x652, __const.ARMOR_CATEGORY+u"#ブラキオシェル#巨人の鎧#",
            410, MID_CORRECTION, keys=(129,)),
        __data.Body(
            0xb5F, __const.ARMOR_CATEGORY+u"#サラマンダー#燃え盛る鎧#凍結・キノコ防止",
            440, LOW_CORRECTION, skill=__data.Skill("Ice#Matango"),
            keys=(132,)),
        __data.Body(
            0xB50, __const.ARMOR_CATEGORY+u"#アイスドレイク#凍てつく鎧#毒・炎上防止",
            450, LOW_CORRECTION, skill=__data.Skill("Poison#Magma"),
            keys=(132,)),
        __data.Body(
            0xA51, __const.ARMOR_CATEGORY+u"#ドラゴンアーマー#竜鱗の鎧#酸・炎上防止",
            500, LOW_CORRECTION, skill=__data.Skill("Acid#Magma"),
            keys=(133,)),
        __data.Body(
            0x454, __const.ARMOR_CATEGORY+u"#ラドゥーンチェイン#神話の怪物の鎧#酸・毒防止",
            570, LOW_CORRECTION, skill=__data.Skill("Acid#Poison"),
            keys=(131,)),
        __data.Body(
            0x854, __const.ARMOR_CATEGORY+u"#タイラントレザー#暴帝の鎧#石・炎上防止",
            610, LOW_CORRECTION, skill=__data.Skill("Stone#Magma"),
            keys=(129, 131)),
        __data.Body(
            0x957, __const.ARMOR_CATEGORY+u"#リンドヴルム#飛竜王の皮の鎧#炎上・破壊防止",
            670, LOW_CORRECTION, skill=__data.Skill("Magma#Ruined"),
            keys=(130,)),
        __data.Body(
            0x655, __const.ARMOR_CATEGORY+u"#ウルトラシェル#鉄人の鎧#",
            700, MID_CORRECTION, keys=(133,)),
        __data.Body(
            0xA54, __const.ARMOR_CATEGORY+u"#ウロボロス#錬金術で作られた鎧#酸・毒・石・破壊防止",
            750, LOW_CORRECTION, skill=__data.Skill(
                "Acid#Poison#Stone#Ruined"), keys=(116, 136)),
        __data.Body(
            0xA5D, __const.ARMOR_CATEGORY+u"#ファヴニール#黄金の鎧#毒・凍結・炎上・キノコ防止",
            820, LOW_CORRECTION, skill=__data.Skill(
                "Poison#Ice#Magma#Matango"), keys=(134, 135, 136)),
        __data.Body(
            0x357, __const.ARMOR_CATEGORY+u"#アダマンタートル#不滅の金属の鎧#あらゆるステータス防止",
            900, VERY_LOW_CORRECTION, skill=__data.Skill(
                __const.IRREGULAR_NAMES+"#"+__const.DEMON_NAMES+"#" +
                __const.GHOST_NAMES), keys=(117, 124, 142)),
        __data.Accessory(
            0xC5F, __const.RING_CATEGORY+u"#ボリードリング#火球の指輪#マグマ生成",
            250, HIGH_CORRECTION, skill=__data.Skill(
                "Magma##"+__const.BASIC_NAMES, is_single=True), keys=(88,)),
        __data.Accessory(
            0xD50, __const.RING_CATEGORY+u"#クライオリング#氷の指輪#アイス生成",
            250, HIGH_CORRECTION, skill=__data.Skill(
                "Ice##"+__const.BASIC_NAMES, is_single=True), keys=(108,)),
        __data.Accessory(
            0xF5E, __const.RING_CATEGORY+u"#ヒドラリング#毒の指輪#ポイズン生成",
            250, HIGH_CORRECTION, skill=__data.Skill(
                "Poison##"+__const.BASIC_NAMES, is_single=True), keys=(83,)),
        __data.Accessory(
            0xE55, __const.RING_CATEGORY+u"#デメテルリング#豊穣の指輪#キノコ生成",
            250, HIGH_CORRECTION, skill=__data.Skill(
                "Matango##"+__const.BASIC_NAMES, is_single=True), keys=(89,)),
        __data.Accessory(
            0xE5C, __const.RING_CATEGORY+u"#エキドナリング#召喚師の指輪#イーター召喚",
            250, HIGH_CORRECTION, skill=__data.Skill(
                __const.BLOCK_EATER_EFFECT, is_single=True), keys=(92,)),
        __data.Accessory(
            0xC5B, __const.RING_CATEGORY+u"#ユーピテルリング#天空の指輪#木スター生成",
            500, LOW_CORRECTION, skill=__data.Skill(
                "Jupiter##"+__const.BASIC_NAMES, is_single=True), keys=(147,)),
        __data.Accessory(
            0xD5F, __const.RING_CATEGORY+u"#プロミネンスリング#炎の指輪#火スター生成",
            500, LOW_CORRECTION, skill=__data.Skill(
                "Mars##"+__const.BASIC_NAMES, is_single=True), keys=(144,)),
        __data.Accessory(
            0xF52, __const.RING_CATEGORY+u"#テラリング#大地の指輪#土スター生成",
            500, LOW_CORRECTION, skill=__data.Skill(
                "Saturn##"+__const.BASIC_NAMES, is_single=True), keys=(146,)),
        __data.Accessory(
            0xE5D, __const.RING_CATEGORY+u"#ミダスリング#黄金の指輪#金スター生成",
            500, LOW_CORRECTION, skill=__data.Skill(
                "Venus##"+__const.BASIC_NAMES, is_single=True), keys=(148,)),
        __data.Accessory(
            0xF53, __const.RING_CATEGORY+u"#ネプチューンリング#海神の指輪#水スター生成",
            500, LOW_CORRECTION, skill=__data.Skill(
                "Mercury##"+__const.BASIC_NAMES, is_single=True), keys=(145,)),
        __data.Accessory(
            0xE58, __const.RING_CATEGORY+u"#ブラックホールリング#暗黒の指輪#月スター生成",
            1000, LOW_CORRECTION, skill=__data.Skill(
                "Moon##"+__const.BASIC_NAMES, is_single=True),
            keys=(150, 151, 152)),
        __data.Accessory(
            0xC50, __const.RING_CATEGORY+u"#ダイヤモンドリング#光の指輪#太陽スター生成",
            1000, LOW_CORRECTION, skill=__data.Skill(
                "Sun##"+__const.BASIC_NAMES, is_single=True),
            keys=(149, 152, 153)),
        __data.Accessory(
            0xC5D, __const.RING_CATEGORY+u"#ミルキーリング#天の川の指輪#生命の欠片生成",
            2000, VERY_LOW_CORRECTION, skill=__data.Skill(
                __const.LIFE_EFFECT, is_single=True),
            keys=(154, 155)),
        __data.Accessory(
            0xE5F, __const.RING_CATEGORY+u"#クエーサーリング#力を秘めた指輪#力の欠片生成",
            2000, VERY_LOW_CORRECTION, skill=__data.Skill(
                __const.POWER_EFFECT, is_single=True),
            keys=(154, 155)),
        __data.Accessory(
            0xF56, __const.RING_CATEGORY+u"#プラネタリング#惑星の指輪#守りの欠片生成",
            2000, VERY_LOW_CORRECTION, skill=__data.Skill(
                __const.PROTECT_EFFECT, is_single=True),
            keys=(154, 155)),
        __data.Accessory(
            0xD5B, __const.RING_CATEGORY+u"#コメットリング#彗星の指輪#速さの欠片生成",
            2000, VERY_LOW_CORRECTION, skill=__data.Skill(
                __const.SPEED_EFFECT, is_single=True),
            keys=(154, 155)),
        __data.Accessory(
            0xF5C, __const.RING_CATEGORY+u"#グランドクロスリング#無限の指輪#マクスウェルデーモン召喚",
            9990, 0, __data.Skill(
                "Maxwell##"+__const.BASIC_NAMES, is_single=True),
            keys=(156, 157, 158, 159))))
    if __const.IS_OUTPUT:
        for i, equip in enumerate(__data.Equip.get_collections()):
            print i, u":",  unicode(equip)
        names = []
        image_numbers = []
        for equip in __data.Equip.get_collections():
            if equip.name not in names:
                names.append(equip.name)
            else:
                raise ValueError("Duplicate Item name.")
            if equip.image_number not in image_numbers:
                image_numbers.append(equip.image_number)
            else:
                raise ValueError("Duplicate Item Icon.")
            if equip.number in equip.keys:
                print unicode(equip)
                raise ValueError("Invalid Key.")
