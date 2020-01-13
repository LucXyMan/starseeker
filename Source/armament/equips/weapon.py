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
    import utils.general as __general

    class __Weapon(__equip.Equip):
        u"""武器データ。
        """
        __slots__ = ()
        _CORRECTION = 1.

        def get_enchant(self, level):
            u"""武器効果取得。
            """
            change, _ = self._ability.string.split("###")
            if level and change:
                new, old = change.split("##")
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
            1, __const.MID_CORRECTION),
        __Weapon(
            0xF03, __const.SWORD_CATEGORY +
            u"#スパロウダガー#小さなダガー#",
            8, __const.MID_CORRECTION,
            keys=(u"チキンナイフ",)),
        __Weapon(
            0x015, __const.SWORD_CATEGORY +
            u"#アエローダガー#鳥人が使うダガー#",
            17, __const.MID_CORRECTION,
            keys=(u"スパロウダガー",)),
        __Weapon(
            0xE04, __const.SWORD_CATEGORY +
            u"#サイレンダガー#沈黙のダガー#スター・カード破壊",
            25, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "Ruined##"+__const.STAR_NAMES+"#"+__const.CARD_NAMES+"###"),
            keys=(u"アエローダガー",)),
        __Weapon(
            0xF0A, __const.SWORD_CATEGORY +
            u"#シュライクスティング#青白く光る短剣#",
            36, __const.MID_CORRECTION,
            keys=(u"アエローダガー",)),
        __Weapon(
            0xF0F, __const.SWORD_CATEGORY +
            u"#ブラッドフィンチ#血塗られたナイフ#" +
            __general.get_skill_description(__const.VAMPIRE_SKILL),
            44, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.VAMPIRE_SKILL)),
            keys=(u"シュライクスティング",)),
        __Weapon(
            0x014, __const.SWORD_CATEGORY +
            u"#ククールス#盗賊のダガー#" +
            __general.get_skill_description(__const.ROB_CARD_SKILL),
            56, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.ROB_CARD_SKILL)),
            keys=(u"シュライクスティング",)),
        __Weapon(
            0x017, __const.SWORD_CATEGORY +
            u"#エンゼルフェザー#天使の羽のナイフ#" +
            __general.get_skill_description(__const.FALCONER_SKILL),
            67, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.FALCONER_SKILL)),
            keys=(u"ブラッドフィンチ", u"ククールス")),
        __Weapon(
            0x110, __const.SWORD_CATEGORY +
            u"#クロウソード#どこにでもある剣#",
            3, __const.MID_CORRECTION),
        __Weapon(
            0x217, __const.SWORD_CATEGORY +
            u"#ガルブレイド#海兵のサーベル#",
            9, __const.MID_CORRECTION,
            keys=(u"クロウソード",)),
        __Weapon(
            0x316, __const.SWORD_CATEGORY +
            u"#ルーンオウル#儀式用の剣#",
            16, __const.MID_CORRECTION,
            keys=(u"クロウソード",)),
        __Weapon(
            0x511, __const.SWORD_CATEGORY +
            u"#アーキオエッジ#古代文明の剣#",
            20, __const.MID_CORRECTION,
            keys=(u"ガルブレイド",)),
        __Weapon(
            0x414, __const.SWORD_CATEGORY +
            u"#アイスペンギー#氷の刃を持つ剣#アイス攻撃",
            26, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.ICE_CHANGE+"###"),
            keys=(u"ルーンオウル",)),
        __Weapon(
            0xB11, __const.SWORD_CATEGORY +
            u"#ヴァルチャーソード#傭兵が使う剣#",
            28, __const.MID_CORRECTION,
            keys=(u"アーキオエッジ",)),
        __Weapon(
            0x813, __const.SWORD_CATEGORY +
            u"#イーグルクレイモア#ハイランダーの剣#",
            33, __const.MID_CORRECTION,
            keys=(u"ヴァルチャーソード",)),
        __Weapon(
            0x31B, __const.SWORD_CATEGORY +
            u"#コカドリーユ#呪われし剣#ストーン攻撃",
            35, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.STONE_CHANGE+"###"),
            keys=(u"ルーンオウル",)),
        __Weapon(
            0x712, __const.SWORD_CATEGORY +
            u"#ホークバスタード#騎士が使う剣#",
            37, __const.MID_CORRECTION,
            keys=(u"イーグルクレイモア",)),
        __Weapon(
            0xA16, __const.SWORD_CATEGORY +
            u"#カサワリフランベルク#波型の刃を持つ剣#",
            42, __const.MID_CORRECTION,
            keys=(u"ホークバスタード",)),
        __Weapon(
            0x919, __const.SWORD_CATEGORY +
            u"#グレートオストリッチ#巨大な刀身を持つ斬馬剣#",
            45, __const.MID_CORRECTION,
            keys=(u"ホークバスタード",)),
        __Weapon(
            0x41F, __const.SWORD_CATEGORY +
            u"#フェニックス#炎の刀身を持つ不折剣#" +
            __general.get_skill_description(__const.FIRE_EATER_SKILL),
            46, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.FIRE_EATER_SKILL),
                is_single=True),
            keys=(u"コカドリーユ",)),
        __Weapon(
            0x51C, __const.SWORD_CATEGORY +
            u"#ストラス#黒い刀身を持つ魔石剣#" +
            __general.get_skill_description(__const.REVERSE_SORCERY_SKILL),
            48, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.REVERSE_SORCERY_SKILL),
                is_single=True),
            keys=(u"アイスペンギー", u"アーキオエッジ")),
        __Weapon(
            0x917, __const.SWORD_CATEGORY +
            u"#ディアトリマ#蛮竜族が使う剛剣#力の欠片攻撃",
            50, __const.VERY_HIGH_CORRECTION,
            ability=__equip.Ability(
                __const.POWER_CHANGE+"###", is_single=True),
            keys=(u"グレートオストリッチ",)),
        __Weapon(
            0x817, __const.SWORD_CATEGORY +
            u"#ロックセイバー#巨獣殺しの剣#",
            52, __const.MID_CORRECTION,
            keys=(u"グレートオストリッチ",)),
        __Weapon(
            0xA1F, __const.SWORD_CATEGORY +
            u"#ガルトマーン#竜殺しの剣#",
            58, __const.MID_CORRECTION,
            keys=(u"カサワリフランベルク",)),
        __Weapon(
            0x61A, __const.SWORD_CATEGORY +
            u"#カラドリウス#天使に鍛えられた剣#" +
            __general.get_skill_description(__const.TALISMAN_SKILL),
            60, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.TALISMAN_SKILL),
                is_single=True),
            keys=(u"フェニックス", u"ストラス")),
        __Weapon(
            0xC11, __const.SWORD_CATEGORY +
            u"#フレスヴェルグ#風を呼ぶ聖剣#" +
            __general.get_skill_description(__const.ICE_PICKER_SKILL),
            65, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.ICE_PICKER_SKILL)),
            keys=(u"ガルトマーン", u"カラドリウス")),
        __Weapon(
            0xc1B, __const.SWORD_CATEGORY +
            u"#ヴィゾフニル#霊鳥の尾羽から作られた魔剣#マグマ攻撃",
            70, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.MAGMA_CHANGE+"###"),
            keys=(u"ガルトマーン", u"カラドリウス")),
        __Weapon(
            0x614, __const.SWORD_CATEGORY +
            u"#ジェフティ#知恵の神の剣#" +
            __general.get_skill_description(__const.ALCHMIST_SKILL),
            75, __const.LOW_CORRECTION,
            ability=__equip.Ability("###"+__general.get_skill_names(
                __const.ALCHMIST_SKILL), is_single=True),
            keys=(u"フレスヴェルグ", u"ヴィゾフニル")),
        __Weapon(
            0xF16, __const.SWORD_CATEGORY +
            u"#隼#東方の戦士の剣#",
            25, __const.MID_CORRECTION),
        __Weapon(
            0xE13, __const.SWORD_CATEGORY +
            u"#飛燕#切れ味鋭い名刀#",
            41, __const.MID_CORRECTION,
            keys=(u"隼",)),
        __Weapon(
            0xD14, __const.SWORD_CATEGORY +
            u"#大鴉#漆黒の妖刀#" +
            __general.get_skill_description(__const.SOUL_EAT_SKILL),
            55, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability("###"+__general.get_skill_names(
                __const.SOUL_EAT_SKILL), is_single=True),
            keys=(u"飛燕",)),
        __Weapon(
            0xD1F, __const.SWORD_CATEGORY +
            u"#朱雀#朱染めの大太刀#火霊召喚",
            64, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability(
                "FireGhost##"+__const.BASIC_NAMES+"###", is_single=True),
            keys=(u"飛燕",)),
        __Weapon(
            0xF17, __const.SWORD_CATEGORY +
            u"#天鳥船#さまよう魂を導く御神刀#" +
            __general.get_skill_description(__const.EXORCIST_SKILL),
            72, __const.LOW_CORRECTION,
            ability=__equip.Ability("###"+__general.get_skill_names(
                __const.EXORCIST_SKILL)),
            keys=(u"大鴉", u"朱雀")),
        __Weapon(
            0xD2F, __const.WAND_CATEGORY +
            u"#ファイアイリス#輝く炎の杖#マグマ攻撃",
            7, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.MAGMA_CHANGE+"###")),
        __Weapon(
            0x030, __const.WAND_CATEGORY +
            u"#フロストフラワー#凍てつく氷の杖#アイス攻撃",
            8, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.ICE_CHANGE+"###")),
        __Weapon(
            0xE25, __const.WAND_CATEGORY +
            u"#エアヒヤシンス#西風を呼ぶ杖#" +
            __general.get_skill_description(__const.SPEEDSTER_SKILL),
            18, __const.LOW_CORRECTION,
            ability=__equip.Ability("###"+__general.get_skill_names(
                __const.SPEEDSTER_SKILL), is_single=True),
            keys=(u"ファイアイリス",)),
        __Weapon(
            0xF2D, __const.WAND_CATEGORY +
            u"#サンダーリコリス#雷鳴の杖#" +
            __general.get_skill_description(__const.STONE_BREAKER_SKILL),
            26, __const.LOW_CORRECTION,
            ability=__equip.Ability("###"+__general.get_skill_names(
                __const.STONE_BREAKER_SKILL), is_single=True),
            keys=(u"フロストフラワー",)),
        __Weapon(
            0x03C, __const.WAND_CATEGORY +
            u"#アースラフレシア#大地の杖#アシッド攻撃",
            30, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.ACID_CHANGE+"###"),
            keys=(u"ファイアイリス", u"フロストフラワー")),
        __Weapon(
            0xF2F, __const.WAND_CATEGORY +
            u"#マンドレーク#呪術師の杖#ポイズン攻撃",
            35, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.POISON_CHANGE+"###"),
            keys=(u"アースラフレシア",)),
        __Weapon(
            0xE29, __const.WAND_CATEGORY +
            u"#アルラウネ#妖精の杖#" +
            __general.get_skill_description(__const.CONVERT_RESOURCE_SKILL),
            41, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability("###"+__general.get_skill_names(
                __const.CONVERT_RESOURCE_SKILL), is_single=True),
            keys=(u"アースラフレシア",)),
        __Weapon(
            0xD25, __const.WAND_CATEGORY +
            u"#ドライアド#精霊の杖#" +
            __general.get_skill_description(__const.HALF_JUPITER_SKILL),
            42, __const.LOW_CORRECTION,
            ability=__equip.Ability("###"+__general.get_skill_names(
                __const.HALF_JUPITER_SKILL), is_single=True),
            keys=(u"アルラウネ",)),
        __Weapon(
            0x13D, __const.WAND_CATEGORY +
            u"#サンフラワー#太陽の杖#" +
            __general.get_skill_description(__const.SON_OF_SUN_SKILL),
            45, __const.LOW_CORRECTION,
            ability=__equip.Ability("###"+__general.get_skill_names(
                __const.SON_OF_SUN_SKILL), is_single=True),
            keys=(u"アルラウネ",)),
        __Weapon(
            0x037, __const.WAND_CATEGORY +
            u"#セイントヴェロニカ#聖者の杖#" +
            __general.get_skill_description(__const.PURIFY_SKILL),
            47, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability("###"+__general.get_skill_names(
                __const.PURIFY_SKILL)),
            keys=(u"ドライアド", u"サンフラワー")),
        __Weapon(
            0xF28, __const.WAND_CATEGORY +
            u"#アスフォデルス#冥王の杖#イーター召喚",
            55, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability(
                __const.BLOCK_EATER_CHANGE+"###", is_single=True),
            keys=(u"ドライアド", u"サンフラワー")),
        __Weapon(
            0xF2B, __const.WAND_CATEGORY +
            u"#ユグドラシル#世界樹の杖#キノコ攻撃",
            67, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.MATANGO_CHANGE+"###"),
            keys=(u"セイントヴェロニカ", u"アスフォデルス")),
        __Weapon(
            0x233, __const.WAND_CATEGORY +
            u"#ヘヴンズロータス#天人の杖#" +
            __general.get_skill_description(__const.ANTI_SUMMONING_SKILL),
            75, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.ANTI_SUMMONING_SKILL)),
            keys=(u"ユグドラシル",)),
        __Weapon(
            0x920, __const.HEAVY_CATEGORY +
            u"#ヒポポタマス#木の棍棒#",
            8, __const.MID_CORRECTION),
        __Weapon(
            0xA23, __const.HEAVY_CATEGORY +
            u"#ホースフレイル#木のフレイル#",
            16, __const.MID_CORRECTION,
            keys=(u"ヒポポタマス",)),
        __Weapon(
            0xC26, __const.HEAVY_CATEGORY +
            u"#エレファントハンマー#重量ハンマー#",
            24, __const.MID_CORRECTION,
            keys=(u"ホースフレイル",)),
        __Weapon(
            0xC24, __const.HEAVY_CATEGORY +
            u"#ナイトメア#悪魔の戦槌#スター・欠片破壊",
            32, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "Ruined##"+__const.STAR_NAMES+"#"+__const.SHARD_NAMES+"###"),
            keys=(u"エレファントハンマー",)),
        __Weapon(
            0xA27, __const.HEAVY_CATEGORY +
            u"#ペガサスフレイル#天空のフレイル#",
            38, __const.MID_CORRECTION,
            keys=(u"ホースフレイル",)),
        __Weapon(
            0x924, __const.HEAVY_CATEGORY +
            u"#カトブレパス#呪いのメイス#ストーン攻撃",
            44, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.STONE_CHANGE+"###"),
            keys=(u"ナイトメア",)),
        __Weapon(
            0x92C, __const.HEAVY_CATEGORY +
            u"#ベヒモスワンド#巨大なメイス#",
            52, __const.MID_CORRECTION,
            keys=(u"カトブレパス",)),
        __Weapon(
            0xC27, __const.HEAVY_CATEGORY +
            u"#スレイプニル#神の鉄槌#マグマ攻撃",
            64, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.MAGMA_CHANGE+"###"),
            keys=(u"ペガサスフレイル",)),
        __Weapon(
            0xC2D, __const.HEAVY_CATEGORY +
            u"#ガネーシャ#超重量ハンマー#",
            71, __const.MID_CORRECTION,
            keys=(u"ベヒモスワンド", u"スレイプニル")),
        __Weapon(
            0x425, __const.HEAVY_CATEGORY +
            u"#ワイルドスピア#狩猟用の槍#",
            7, __const.MID_CORRECTION),
        __Weapon(
            0x429,  __const.HEAVY_CATEGORY +
            u"#タイガースピア#戦闘用の槍#",
            19, __const.MID_CORRECTION,
            keys=(u"ワイルドスピア",)),
        __Weapon(
            0x322, __const.HEAVY_CATEGORY +
            u"#レパードランス#騎士が使う槍#",
            25, __const.MID_CORRECTION,
            keys=(u"タイガースピア",)),
        __Weapon(
            0x326, __const.HEAVY_CATEGORY +
            u"#レオランス#勇者の槍#",
            37, __const.MID_CORRECTION,
            keys=(u"レパードランス",)),
        __Weapon(
            0x32C, __const.HEAVY_CATEGORY +
            u"#セリオン#漆黒の魔槍#ストーン攻撃",
            44, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.STONE_CHANGE+"###"),
            keys=(u"レパードランス",)),
        __Weapon(
            0x524, __const.HEAVY_CATEGORY +
            u"#キメラトライデント#魔法合金の槍#",
            53, __const.MID_CORRECTION,
            keys=(u"セリオン",)),
        __Weapon(
            0x527, __const.HEAVY_CATEGORY +
            u"#グリュプス#神々の槍#アイス攻撃",
            68, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.ICE_CHANGE+"###"),
            keys=(u"レオランス",)),
        __Weapon(
            0x621, __const.HEAVY_CATEGORY +
            u"#オックスアクス#木こりの斧#",
            7, __const.MID_CORRECTION),
        __Weapon(
            0x628, __const.HEAVY_CATEGORY +
            u"#ヌーアクス#兵隊の斧#",
            15, __const.MID_CORRECTION,
            keys=(u"オックスアクス",)),
        __Weapon(
            0x720, __const.HEAVY_CATEGORY +
            u"#バッファロー#大きな斧#",
            25, __const.MID_CORRECTION,
            keys=(u"ヌーアクス",)),
        __Weapon(
            0x726, __const.HEAVY_CATEGORY +
            u"#バイソンラブリュス#戦闘用の斧#",
            38, __const.MID_CORRECTION,
            keys=(u"バッファロー",)),
        __Weapon(
            0x825, __const.HEAVY_CATEGORY +
            u"#ミノタウロス#巨大な戦斧#守りの欠片攻撃",
            54, __const.VERY_HIGH_CORRECTION,
            ability=__equip.Ability(
                __const.PROTECT_CHANGE+"###", is_single=True),
            keys=(u"バイソンラブリュス",)),
        __Weapon(
            0x724, __const.HEAVY_CATEGORY +
            u"#牛鬼#鬼神の斧#キー・チェスト破壊",
            69, __const.LOW_CORRECTION,
            ability=__equip.Ability(
                "Ruined##"+__const.KEY_NAMES+"#"+__const.CHEST_NAMES+"###"),
            keys=(u"ミノタウロス",)),
        __Weapon(
            0x435, __const.MISSILE_CATEGORY +
            u"#ハニービー#狩猟用の弓#",
            8, __const.MID_CORRECTION),
        __Weapon(
            0x534, __const.MISSILE_CATEGORY +
            u"#ホーネット#戦闘用の剛弓#",
            17, __const.MID_CORRECTION,
            keys=(u"ハニービー",)),
        __Weapon(
            0x43A,  __const.MISSILE_CATEGORY +
            u"#モスキート#吸血弓#" +
            __general.get_skill_description(__const.VAMPIRE_SKILL),
            25, __const.VERY_LOW_CORRECTION,
            ability=__equip.Ability(
                "###"+__general.get_skill_names(__const.VAMPIRE_SKILL)),
            keys=(u"ホーネット",)),
        __Weapon(
            0x538, __const.MISSILE_CATEGORY +
            u"#キラービー#必殺の剛弓#",
            45, __const.MID_CORRECTION,
            keys=(u"ホーネット",)),
        __Weapon(
            0x530,  __const.MISSILE_CATEGORY +
            u"#ベルゼビュート#魔神の弓#ポイズン攻撃",
            66, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.POISON_CHANGE+"###"),
            keys=(u"キラービー",)),
        __Weapon(
            0x63D, __const.MISSILE_CATEGORY +
            u"#クインビー#王者の弓#スライム攻撃",
            71, __const.VERY_HIGH_CORRECTION,
            ability=__equip.Ability(__const.SLIME_CHANGE+"###"),
            keys=(u"キラービー",)),
        __Weapon(
            0x833, __const.MISSILE_CATEGORY +
            u"#アントボウガン#機械じかけの弓#",
            22, __const.MID_CORRECTION),
        __Weapon(
            0x933, __const.MISSILE_CATEGORY +
            u"#タランチュラ#毒のボウガン#ポイズン攻撃",
            36, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.POISON_CHANGE+"###"),
            keys=(u"アントボウガン",)),
        __Weapon(
            0x93F, __const.MISSILE_CATEGORY +
            u"#ファイアアント#炎の矢を放つボウガン#マグマ攻撃",
            41, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.MAGMA_CHANGE+"###"),
            keys=(u"タランチュラ",)),
        __Weapon(
            0x930, __const.MISSILE_CATEGORY +
            u"#アイスアント#氷の矢を放つボウガン#アイス攻撃",
            45, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.ICE_CHANGE+"###"),
            keys=(u"タランチュラ",)),
        __Weapon(
            0x738, __const.MISSILE_CATEGORY +
            u"#アギトボウガン#巨大なボウガン#",
            57, __const.MID_CORRECTION,
            keys=(u"アントボウガン",)),
        __Weapon(
            0x834, __const.MISSILE_CATEGORY +
            u"#アラクネーボウガン#呪いのボウガン#ストーン攻撃",
            69, __const.LOW_CORRECTION,
            ability=__equip.Ability(__const.STONE_CHANGE+"###"),
            keys=(u"ファイアアント", u"アイスアント")),
        __Weapon(
            0xA3A, __const.MISSILE_CATEGORY +
            u"#スティンガー#広く流通する銃#",
            15, __const.MID_CORRECTION),
        __Weapon(
            0xA3F, __const.MISSILE_CATEGORY +
            u"#レッドクロウ#真紅の銃#マグマ攻撃",
            23, __const.LOW_CORRECTION,
            ability=__equip.Ability("Magma##"+__const.BASIC_NAMES+"###"),
            keys=(u"スティンガー",)),
        __Weapon(
            0xA35, __const.MISSILE_CATEGORY +
            u"#ストライプバーグ#改良型の銃#",
            41, __const.MID_CORRECTION,
            keys=(u"レッドクロウ",)),
        __Weapon(
            0xA38, __const.MISSILE_CATEGORY +
            u"#インペラトール#銃の皇帝と呼ばれる#",
            62, __const.MID_CORRECTION,
            keys=(u"ストライプバーグ",)),
        __Weapon(
            0xA3C, __const.MISSILE_CATEGORY +
            u"#スコルピウス#英雄殺しの銃#",
            70, __const.MID_CORRECTION,
            keys=(u"インペラトール",)))
