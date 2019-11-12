#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""weapon.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

武器設定モジュール。
"""


def get():
    u"""武器取得。
    """
    import equip as __equip
    import utils.const as __const

    class __Weapon(__equip.Equip):
        u"""武器データ。
        """
        __slots__ = ()
        _CORRECTION = 0.1

        def get_enchant(self, level):
            u"""武器効果を取得。
            """
            if level and self._ability.target:
                new, old = self._ability.target.split("##")
                return new, tuple(old.split("#")), (
                    (1, 1) if self._ability.is_single else (level, level+1))
            return ()

        @property
        def is_weapon(self):
            u"""武器判定。
            """
            return True
    return (
        __Weapon(
            0xE02, __const.SWORD_CATEGORY +
            u"#チキンナイフ#小さなナイフ#",
            10, __const.MID_CORRECTION),
        __Weapon(
            0xF03, __const.SWORD_CATEGORY +
            u"#スパロウダガー#小さなダガー#",
            40, __const.MID_CORRECTION, keys=(1,)),
        __Weapon(
            0xF0F, __const.SWORD_CATEGORY +
            u"#ブラッドフィンチ#血塗られたナイフ#ポイズン攻撃",
            120, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.POISON_EFFECT), keys=(2,)),
        __Weapon(
            0x015, __const.SWORD_CATEGORY +
            u"#アエローダガー#鳥人が使うダガー#",
            150, __const.MID_CORRECTION, keys=(3,)),
        __Weapon(
            0x014, __const.SWORD_CATEGORY +
            u"#サイレンダガー#沈黙のダガー#スター・カード破壊",
            250, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Ruined##"+__const.STAR_NAMES+"#"+__const.CARD_NAMES),
            keys=(4,)),
        __Weapon(
            0x017, __const.SWORD_CATEGORY +
            u"#エンゼルフェザー#天使の羽のナイフ#",
            360, __const.MID_CORRECTION, keys=(5,)),
        __Weapon(
            0x110, __const.SWORD_CATEGORY +
            u"#クロウソード#どこにでもある剣#",
            30, __const.MID_CORRECTION),
        __Weapon(
            0x217, __const.SWORD_CATEGORY +
            u"#ガルブレイド#海兵のサーベル#",
            40, __const.MID_CORRECTION, keys=(7,)),
        __Weapon(
            0x316, __const.SWORD_CATEGORY +
            u"#ルーンオウル#儀式用の剣#",
            60, __const.MID_CORRECTION, keys=(8,)),
        __Weapon(
            0x511, __const.SWORD_CATEGORY +
            u"#アーキオエッジ#古代文明の剣#",
            100, __const.MID_CORRECTION, keys=(9,)),
        __Weapon(
            0x414, __const.SWORD_CATEGORY +
            u"#アイスペンギー#氷の刃を持つ剣#アイス攻撃",
            120, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.ICE_EFFECT), keys=(10,)),
        __Weapon(
            0xB11, __const.SWORD_CATEGORY +
            u"#ヴァルチャーソード#傭兵が使う剣#",
            150, __const.MID_CORRECTION, keys=(8,)),
        __Weapon(
            0x813, __const.SWORD_CATEGORY +
            u"#イーグルクレイモア#ハイランダーの剣#",
            200, __const.MID_CORRECTION, keys=(12,)),
        __Weapon(
            0x712, __const.SWORD_CATEGORY +
            u"#ホークバスタード#騎士が使う剣#",
            230, __const.MID_CORRECTION, keys=(13,)),
        __Weapon(
            0x919, __const.SWORD_CATEGORY +
            u"#グレートオストリッチ#巨大な刀身を持つ斬馬剣#",
            250, __const.MID_CORRECTION, keys=(14,)),
        __Weapon(
            0x917, __const.SWORD_CATEGORY +
            u"#ディアトリマ#蛮竜族が使う剛剣#力の欠片攻撃",
            270, __const.VERY_HIGH_CORRECTION, ability=__equip.Ability(
                __const.POWER_EFFECT, is_single=True), keys=(15,)),
        __Weapon(
            0x51C, __const.SWORD_CATEGORY +
            u"#ストラス#黒い刀身を持つ魔石剣#土スター攻撃",
            290, __const.HIGH_CORRECTION, ability=__equip.Ability(
                __const.SATURN_EFFECT, is_single=True), keys=(10,)),
        __Weapon(
            0x31B, __const.SWORD_CATEGORY +
            u"#コカドリーユ#呪われし剣#ストーン攻撃",
            310, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.STONE_EFFECT), keys=(9,)),
        __Weapon(
            0xA16, __const.SWORD_CATEGORY +
            u"#カサワリフランベルク#波型の刃を持つ剣#",
            330, __const.MID_CORRECTION, keys=(14,)),
        __Weapon(
            0x41F, __const.SWORD_CATEGORY +
            u"#フェニックス#炎の刀身を持つ不折剣#火スター攻撃",
            360, __const.HIGH_CORRECTION, ability=__equip.Ability(
                __const.MARS_EFFECT, is_single=True), keys=(17,)),
        __Weapon(
            0x61A, __const.SWORD_CATEGORY +
            u"#カラドリウス#天使に鍛えられた剣#太陽スター攻撃",
            400, __const.HIGH_CORRECTION, ability=__equip.Ability(
                __const.SUN_EFFECT, is_single=True), keys=(6, 23)),
        __Weapon(
            0x817, __const.SWORD_CATEGORY +
            u"#ロックセイバー#巨獣殺しの剣#",
            420, __const.MID_CORRECTION, keys=(14,)),
        __Weapon(
            0xC11, __const.SWORD_CATEGORY +
            u"#フレスヴェルグ#風を呼ぶ聖剣#アイス攻撃",
            450, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.ICE_EFFECT), keys=(17,)),
        __Weapon(
            0xc1B, __const.SWORD_CATEGORY +
            u"#ヴィゾフニル#霊鳥の尾羽から作られた魔剣#マグマ攻撃",
            490, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.MAGMA_EFFECT), keys=(23,)),
        __Weapon(
            0xA1F, __const.SWORD_CATEGORY +
            u"#ガルトマーン#竜殺しの剣#",
            560, __const.MID_CORRECTION, keys=(15,)),
        __Weapon(
            0xF16, __const.SWORD_CATEGORY +
            u"#隼#東方の戦士の剣#",
            250, __const.MID_CORRECTION, keys=(12,)),
        __Weapon(
            0xE13, __const.SWORD_CATEGORY +
            u"#飛燕#切れ味鋭い名刀#",
            310, __const.MID_CORRECTION, keys=(26,)),
        __Weapon(
            0xD14, __const.SWORD_CATEGORY +
            u"#大鴉#漆黒の大刀#月スター攻撃",
            450, __const.HIGH_CORRECTION, ability=__equip.Ability(
                __const.MOON_EFFECT, is_single=True), keys=(27,)),
        __Weapon(
            0xF17, __const.SWORD_CATEGORY +
            u"#天鳥船#さまよう魂を導く神刀#悪霊退散",
            520, __const.HIGH_CORRECTION, ability=__equip.Ability(
                "Sun##"+__const.DEMON_NAMES+"#"+__const.GHOST_NAMES),
            keys=(6, 28)),
        __Weapon(
            0xD2F, __const.WAND_CATEGORY +
            u"#ファイアイリス#輝く炎の杖#マグマ攻撃",
            50, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.MAGMA_EFFECT)),
        __Weapon(
            0x030, __const.WAND_CATEGORY +
            u"#フロストフラワー#凍てつく氷の杖#アイス攻撃",
            140, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.ICE_EFFECT)),
        __Weapon(
            0xE25, __const.WAND_CATEGORY +
            u"#エアヒヤシンス#西風を呼ぶ杖#速さの欠片攻撃",
            180, __const.VERY_HIGH_CORRECTION, ability=__equip.Ability(
                __const.SPEED_EFFECT, is_single=True), keys=(31,)),
        __Weapon(
            0xF2D, __const.WAND_CATEGORY +
            u"#サンダーリコリス#雷鳴の杖#",
            200, __const.MID_CORRECTION, keys=(30,)),
        __Weapon(
            0x03C, __const.WAND_CATEGORY +
            u"#アースラフレシア#大地の杖#アシッド攻撃",
            240, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.ACID_EFFECT), keys=(33,)),
        __Weapon(
            0xF2F, __const.WAND_CATEGORY +
            u"#マンドレーク#呪術師の杖#ポイズン攻撃",
            280, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.POISON_EFFECT), keys=(32,)),
        __Weapon(
            0xE23, __const.WAND_CATEGORY +
            u"#アルラウネ#妖精の杖#生命の欠片攻撃",
            300, __const.VERY_HIGH_CORRECTION, ability=__equip.Ability(
                __const.LIFE_EFFECT, is_single=True), keys=(34,)),
        __Weapon(
            0x13D, __const.WAND_CATEGORY +
            u"#サンフラワー#太陽の杖#太陽スター攻撃",
            310, __const.HIGH_CORRECTION, ability=__equip.Ability(
                __const.SUN_EFFECT, is_single=True), keys=(34,)),
        __Weapon(
            0xD27, __const.WAND_CATEGORY +
            u"#ドライアド#精霊の杖#木スター攻撃",
            360, __const.HIGH_CORRECTION, ability=__equip.Ability(
                __const.JUPITER_EFFECT, is_single=True), keys=(36,)),
        __Weapon(
            0xF28, __const.WAND_CATEGORY +
            u"#アスフォデルス#冥王の杖#イーター召喚",
            440, __const.VERY_LOW_CORRECTION, ability=__equip.Ability(
                __const.BLOCK_EATER_EFFECT, is_single=True),
            keys=(35, 148, 154)),
        __Weapon(
            0xF2B, __const.WAND_CATEGORY +
            u"#ユグドラシル#世界樹の杖#キノコ攻撃",
            500, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.MATANGO_EFFECT), keys=(38, 39)),
        __Weapon(
            0x920, __const.HEAVY_CATEGORY +
            u"#ヒポポタマス#木の棍棒#",
            70, __const.MID_CORRECTION),
        __Weapon(
            0xA23, __const.HEAVY_CATEGORY +
            u"#ホースフレイル#木のフレイル#",
            110, __const.MID_CORRECTION, keys=(41,)),
        __Weapon(
            0xC26, __const.HEAVY_CATEGORY +
            u"#エレファントハンマー#重量ハンマー#",
            160, __const.MID_CORRECTION, keys=(41,)),
        __Weapon(
            0xC24, __const.HEAVY_CATEGORY +
            u"#ナイトメア#悪魔の戦槌#スター・欠片破壊",
            230, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Ruined##"+__const.STAR_NAMES+"#"+__const.SHARD_NAMES),
            keys=(43,)),
        __Weapon(
            0x924, __const.HEAVY_CATEGORY +
            u"#カトブレパス#呪いのメイス#ストーン攻撃",
            280, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.STONE_EFFECT), keys=(44,)),
        __Weapon(
            0xA27, __const.HEAVY_CATEGORY +
            u"#ペガサスフレイル#天空のフレイル#",
            310, __const.MID_CORRECTION, keys=(42,)),
        __Weapon(
            0x92C, __const.HEAVY_CATEGORY +
            u"#ベヒモスワンド#巨大なメイス#",
            370, __const.MID_CORRECTION, keys=(45,)),
        __Weapon(
            0xC27, __const.HEAVY_CATEGORY +
            u"#スレイプニル#神の鉄槌#マグマ攻撃",
            490, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.MAGMA_EFFECT), keys=(46,)),
        __Weapon(
            0xC2D, __const.HEAVY_CATEGORY +
            u"#ガネーシャ#超重量ハンマー#",
            580, __const.MID_CORRECTION, keys=(47,)),
        __Weapon(
            0x425, __const.HEAVY_CATEGORY +
            u"#ワイルドスピア#狩猟用の槍#",
            60, __const.MID_CORRECTION),
        __Weapon(
            0x322, __const.HEAVY_CATEGORY +
            u"#レパードランス#騎士が使う槍#",
            120, __const.MID_CORRECTION, keys=(50,)),
        __Weapon(
            0x429,  __const.HEAVY_CATEGORY +
            u"#タイガースピア#戦闘用の槍#",
            190, __const.MID_CORRECTION, keys=(51,)),
        __Weapon(
            0x326, __const.HEAVY_CATEGORY +
            u"#レオランス#勇者の槍#",
            260, __const.MID_CORRECTION, keys=(52,)),
        __Weapon(
            0x32C, __const.HEAVY_CATEGORY +
            u"#セリオン#漆黒の魔槍#ストーン攻撃",
            320, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.STONE_EFFECT), keys=(45, 53)),
        __Weapon(
            0x524, __const.HEAVY_CATEGORY +
            u"#キメラトライデント#魔法合金の槍#",
            430, __const.MID_CORRECTION, keys=(54,)),
        __Weapon(
            0x527, __const.HEAVY_CATEGORY +
            u"#グリュプス#神々の槍#アイス攻撃",
            520, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.ICE_EFFECT), keys=(55,)),
        __Weapon(
            0x621, __const.HEAVY_CATEGORY +
            u"#オックスアクス#木こりの斧#",
            50, __const.MID_CORRECTION),
        __Weapon(
            0x628, __const.HEAVY_CATEGORY +
            u"#ヌーアクス#兵隊の斧#",
            110, __const.MID_CORRECTION, keys=(57,)),
        __Weapon(
            0x720, __const.HEAVY_CATEGORY +
            u"#バッファロー#大きな斧#",
            230, __const.MID_CORRECTION, keys=(58,)),
        __Weapon(
            0x726, __const.HEAVY_CATEGORY +
            u"#バイソンラブリュス#戦闘用の斧#",
            260, __const.MID_CORRECTION, keys=(59,)),
        __Weapon(
            0x825, __const.HEAVY_CATEGORY +
            u"#ミノタウロス#巨大な戦斧#守りの欠片攻撃",
            350, __const.VERY_HIGH_CORRECTION, ability=__equip.Ability(
                __const.PROTECT_EFFECT, is_single=True), keys=(43, 60)),
        __Weapon(
            0x724, __const.HEAVY_CATEGORY +
            u"#牛鬼#鬼神の斧#キー・チェスト破壊",
            550, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Ruined##"+__const.KEY_NAMES+"#"+__const.CHEST_NAMES),
            keys=(61,)),
        __Weapon(
            0x435, __const.MISSILE_CATEGORY +
            u"#ハニービー#狩猟用の弓#",
            60, __const.MID_CORRECTION),
        __Weapon(
            0x534, __const.MISSILE_CATEGORY +
            u"#ホーネット#戦闘用の剛弓#",
            170, __const.MID_CORRECTION, keys=(63,)),
        __Weapon(
            0x63D, __const.MISSILE_CATEGORY +
            u"#クインビー#王者の弓#スライム攻撃",
            280, __const.VERY_HIGH_CORRECTION,
            ability=__equip.Ability(__const.SLIME_EFFECT), keys=(66, 71)),
        __Weapon(
            0x538, __const.MISSILE_CATEGORY +
            u"#キラービー#必殺の剛弓#",
            320, __const.MID_CORRECTION, keys=(64,)),
        __Weapon(
            0x530,  __const.MISSILE_CATEGORY +
            u"#ベルゼビュート#魔神の弓#ポイズン攻撃",
            450, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.POISON_EFFECT), keys=(66, 70)),
        __Weapon(
            0x833, __const.MISSILE_CATEGORY +
            u"#アントボウガン#機械じかけの弓#",
            120, __const.MID_CORRECTION),
        __Weapon(
            0x933, __const.MISSILE_CATEGORY +
            u"#タランチュラ#毒のボウガン#ポイズン攻撃",
            160, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.POISON_EFFECT), keys=(68,)),
        __Weapon(
            0x93F, __const.MISSILE_CATEGORY +
            u"#ファイアアント#炎の矢を放つボウガン#マグマ攻撃",
            200, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.MAGMA_EFFECT), keys=(69,)),
        __Weapon(
            0x738, __const.MISSILE_CATEGORY +
            u"#アギトボウガン#巨大なボウガン#",
            230, __const.MID_CORRECTION, keys=(68,)),
        __Weapon(
            0x930, __const.MISSILE_CATEGORY +
            u"#アイスアント#氷の矢を放つボウガン#アイス攻撃",
            350, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.ICE_EFFECT), keys=(71,)),
        __Weapon(
            0x834, __const.MISSILE_CATEGORY +
            u"#アラクネーボウガン#呪いのボウガン#ストーン攻撃",
            420, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.STONE_EFFECT), keys=(70, 71)),
        __Weapon(
            0xA3A, __const.MISSILE_CATEGORY +
            u"#スティンガー#広く流通する銃#",
            100, __const.MID_CORRECTION),
        __Weapon(
            0xA3F, __const.MISSILE_CATEGORY +
            u"#レッドクロウ#真紅の銃#マグマ攻撃",
            150, __const.LOW_CORRECTION, ability=__equip.Ability(
                "Magma##"+__const.BASIC_NAMES), keys=(74,)),
        __Weapon(
            0xA35, __const.MISSILE_CATEGORY +
            u"#ストライプバーグ#改良型の銃#",
            270, __const.MID_CORRECTION, keys=(75,)),
        __Weapon(
            0xA38, __const.MISSILE_CATEGORY +
            u"#インペラトール#銃の皇帝と呼ばれる#",
            350, __const.MID_CORRECTION, keys=(76,)),
        __Weapon(
            0xA3C, __const.MISSILE_CATEGORY +
            u"#スコルピウス#英雄殺しの銃#",
            560, __const.MID_CORRECTION, keys=(77,)))
