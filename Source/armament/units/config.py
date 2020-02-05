#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""config.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ユニット設定モジュール。
"""


def init():
    u"""パッケージ初期化。
    """
    import data as __data
    import utils.const as _const
    VERY_LOW_POWER = 300
    LOW_POWER = 350
    MID_POWER = 400
    HIGH_POWER = 450
    status = 10, 5

    def __set_player():
        u"""プレイヤー設定。
        """
        __data.Player.set_collections((
            __data.Player(
                u"altair##"+_const.WARRIOR_ROLE+u"##"+_const.ALTAIR_NAME +
                u"##闇の王国ダークランドの勇者#不死身のゾンビ戦士", status, (
                    u"ストーンブレーカー", u"パワーストローク",
                    u"コンプアシスト", u"ソウルイート",
                    u"アンチサモーニング", u"ポイズンサモン",
                    u"ネクロマンサー", u"ハーフジュピター",
                    u"セーフティ", u"タリスマン",
                    u"マイティ", u"タフネス",
                    u"杖装備", u"飛び道具装備",
                    u"帽子装備", u"ローブ装備")),
            __data.Player(
                u"corvus##"+_const.WARRIOR_ROLE+u"##"+_const.CORVUS_NAME +
                u"##黒の帝国ノワールの傭兵#賞金首のサイコキラー", status, (
                    u"ファイアイーター", u"アイスピッカー",
                    u"パワーストローク", u"コンプアシスト",
                    u"ロブカード", u"アンチサモーニング",
                    u"ポイズンサモン", u"ファルコナー",
                    u"ハーフマーズ", u"ヴァンピール",
                    u"マイティ", u"スピードスター",
                    u"杖装備", u"飛び道具装備",
                    u"帽子装備", u"ローブ装備")),
            __data.Player(
                u"nova##"+_const.WIZARD_ROLE+u"##"+_const.NOVA_NAME +
                u"##影の国シェイディアの魔術師#魔法で生み出されたホムンクルス", status, (
                    u"アイスピッカー", u"アシッドイレーザー",
                    u"ウォータープレス", u"ダブルスペル",
                    u"ソウルイート", u"リバースソーサリー",
                    u"アルケミスト", u"ハーフメルクリー",
                    u"コンバートリソース", u"セーフティ",
                    u"ショートターン", u"スピードスター",
                    u"剣装備", u"飛び道具装備",
                    u"兜装備", u"鎧装備")),
            __data.Player(
                u"sirius##"+_const.SEEKER_ROLE+u"##"+_const.SIRIUS_NAME +
                u"##ヴァイス・オーダーの怪物ハンター#大狼に変身する人狼牧師", status, (
                    u"ストーンブレーカー", u"エクソシスト",
                    u"コンプアシスト", u"ピュリファイ",
                    u"アンチサモーニング", u"シェパード",
                    u"ファルコナー", u"サンオブサン",
                    u"セーフティ", u"タリスマン",
                    u"ショートターン", u"ライフブースト",
                    u"杖装備", u"重武器装備",
                    u"兜装備", u"鎧装備")),
            __data.Player(
                u"castor##"+_const.WIZARD_ROLE+u"##"+_const.CASTOR_NAME +
                u"##暁の塔の錬金術師#禁呪を研究するマッド・ソーサラー", status, (
                    u"ファイアイーター", u"アシッドイレーザー",
                    u"エクソシスト", u"ダブルスペル",
                    u"ソウルイート", u"リバースソーサリー",
                    u"アルケミスト", u"ドラゴンマスター",
                    u"コンバートリソース", u"セーフティ",
                    u"ショートターン", u"タフネス",
                    u"剣装備", u"飛び道具装備",
                    u"兜装備", u"鎧装備")),
            __data.Player(
                u"pluto##"+_const.SEEKER_ROLE+u"##"+_const.PLUTO_NAME +
                u"##月下都市セレネの怪盗道化#魂を盗むリーパー・クラウン", status, (
                    u"ファイアイーター", u"アシッドイレーザー",
                    u"ファントムシーフ", u"チョコレートプレス",
                    u"ダブルスペル", u"ロブカード",
                    u"ソウルイート", u"リバースソーサリー",
                    u"シェパード", u"ネクロマンサー",
                    u"ハーフサターン", u"スピードスター",
                    u"杖装備", u"重武器装備",
                    u"兜装備", u"鎧装備")),
            __data.Player(
                u"regulus##"+_const.ROYAL_ROLE+u"##"+_const.REGULUS_NAME +
                u"##夜の国ナイトピアの王子#亡国のファントム", status, (
                    u"ファイアイーター", u"アイスピッカー",
                    u"コンプアシスト", u"ソウルイート",
                    u"リバースソーサリー", u"ポイズンサモン",
                    u"ネクロマンサー", u"ムーンチャイルド",
                    u"コンバートリソース", u"セーフティ",
                    u"ショートターン", u"スピードスター",
                    u"重武器装備", u"飛び道具装備",
                    u"兜装備", u"鎧装備")),
            __data.Player(
                u"lucifer##"+_const.ROYAL_ROLE+u"##"+_const.LUCIFER_NAME +
                u"##宵星城を支配する伯爵#魔城に棲むヴァンパイア", status, (
                    u"ストーンブレーカー", u"パワーストローク",
                    u"コンプアシスト", u"ソウルイート",
                    u"リバースソーサリー", u"アンチサモーニング",
                    u"ポイズンサモン", u"ファルコナー",
                    u"ドラゴンマスター", u"ヴァンピール",
                    u"ハーフヴェヌス", u"マイティ",
                    u"重武器装備", u"飛び道具装備",
                    u"兜装備", u"鎧装備")),
            __data.Player(
                u"nebula##"+_const.MONSTER_ROLE+u"##"+_const.NEBULA_NAME +
                u"##宵星城に眠る生物#星空からやって来たインベーダー", (20, 10), (
                    u"ストーンブレーカー", u"パワーストローク",
                    u"エクソシスト", u"コンプアシスト",
                    u"ダブルスペル",  u"ソウルイート",
                    u"アンチサモーニング", u"フォースジョーカー",
                    u"ドラゴンマスター", u"ムーンチャイルド",
                    u"ヴァンピール", u"セーフティ",
                    u"タフネス"))))

    def __set_summon():
        u"""サモン設定。
        """
        import utils.general as __general
        __data.Summon.set_collections((
            __data.Summon(
                u"##seed_1##"+_const.ALCHMIC_TRIBE +
                u"##フェアリーシード##"
                u"妖精の種#",
                (10, 20), (1, 0), MID_POWER, receptors=(__data.Receptor(
                    u"ソーダスライム##herb_1##フェアリーハーブ##"
                    u"妖精の葉#木スター生成",
                    (10, 45), MID_POWER, ability=__data.Ability(
                        _const.PERSISTENCE_ABILITY+"###Jupiter##" +
                        _const.BASIC_NAMES, 0b11), receptors=(__data.Receptor(
                            u"ソーダスライム##flower_1##フェアリーブルーム##"
                            u"妖精の花#"+__general.get_skill_description(
                                _const.HALF_JUPITER_SKILL),
                            (15, 60), MID_POWER, ability=__data.Ability(
                                _const.ADDITION_ABILITY+"###" +
                                __general.get_skill_names(
                                    _const.HALF_JUPITER_SKILL))),)),)),
            __data.Summon(
                u"##snake_2##"+_const.DRAGON_TRIBE +
                u"##ラージスネーク##"
                u"からみあう大蛇#" +
                __general.get_skill_description(_const.ACID_ERASER_SKILL),
                (42, 25), (2, 0), LOW_POWER, ability=__data.Ability(
                    _const.ADDITION_ABILITY+"###" +
                    __general.get_skill_names(_const.ACID_ERASER_SKILL))),
            __data.Summon(
                u"##spider_8##"+_const.BEAST_TRIBE +
                u"##ヒュージスパイダー##"
                u"巨大グモ#ポイズン攻撃",
                (48, 20), (2, 0), LOW_POWER, ability=__data.Ability(
                    _const.ENCHANT_ABILITY+"###"+_const.POISON_CHANGE)),
            __data.Summon(
                u"##fly_14##"+_const.SKY_TRIBE +
                u"##ジャイアントフライ##"
                u"巨大バエ#自身のスターを破壊",
                (62, 30), (3, 0), HIGH_POWER, ability=__data.Ability(
                    _const.PERSISTENCE_ABILITY+"###Ruined##" +
                    _const.STAR_NAMES, 0b11)),
            __data.Summon(
                u"##herb_8##"+_const.ALCHMIC_TRIBE +
                u"##スプライトレント##"
                u"精霊が住む植物#キノコ攻撃",
                (10, 45), (4, 0), LOW_POWER, ability=__data.Ability(
                    _const.ENCHANT_ABILITY+"###"+_const.MATANGO_CHANGE
                ), receptors=(__data.Receptor(
                    u"ウィルオウィスプ##flower_13##サンブロッサム##"
                    u"太陽の花#生命の欠片生成",
                    (5, 60), MID_POWER, ability=__data.Ability(
                        _const.PERSISTENCE_ABILITY+"###Life##" +
                        _const.BASIC_NAMES, 0b111)),)),
            __data.Summon(
                u"##bat_5##"+_const.SKY_TRIBE +
                u"##キャンドルバット##"
                u"火遊び好きのコウモリ#マグマ攻撃",
                (25, 5), (1, 1), LOW_POWER, ability=__data.Ability(
                    _const.ENCHANT_ABILITY+"###Magma##"+_const.BASIC_NAMES
                ), receptors=(__data.Receptor(
                    u"ジャイアントフライ##fly_5##ファイアフライ##"
                    u"燃え盛る虫#火スター生成",
                    (53, 20), MID_POWER, ability=__data.Ability(
                        _const.PERSISTENCE_ABILITY+"###" +
                        _const.MARS_CHANGE, 0b11)),)),
            __data.Summon(
                u"##elemental_14##"+_const.ALCHMIC_TRIBE +
                u"##ファイアルビー##"
                u"焔の生命体#" +
                __general.get_skill_description(_const.FIRE_EATER_SKILL),
                (39, 11), (2, 1), LOW_POWER, ability=__data.Ability(
                    _const.ADDITION_ABILITY+"###" +
                    __general.get_skill_names(_const.FIRE_EATER_SKILL))),
            __data.Summon(
                u"##slime_5##"+_const.ALCHMIC_TRIBE +
                u"##マグマゼリー##"
                u"意思を持ったマグマ#マグマ生成",
                (30, 40), (3, 1), HIGH_POWER, ability=__data.Ability(
                    _const.PERSISTENCE_ABILITY+"###" +
                    _const.MAGMA_CHANGE, 0b11)),
            __data.Summon(
                u"##bat_4##"+_const.SKY_TRIBE +
                u"##セントエルモ##"
                u"青い炎の生物#"+__general.get_skill_description(
                    _const.HALF_MARS_SKILL),
                (12, 55), (3, 1), LOW_POWER, ability=__data.Ability(
                    _const.ADDITION_ABILITY+"###" +
                    __general.get_skill_names(_const.HALF_MARS_SKILL))),
            __data.Summon(
                u"##crow_5##"+_const.SKY_TRIBE +
                u"##ダークフェニックス##"
                u"漆黒の不死鳥#"+__general.get_skill_description(
                    _const.COMPLETE_ASSIST_SKILL),
                (19, 54), (4, 1), VERY_LOW_POWER, ability=__data.Ability(
                    _const.ADDITION_ABILITY+"###" +
                    __general.get_skill_names(_const.COMPLETE_ASSIST_SKILL))),
            __data.Summon(
                u"##rat_7##"+_const.UNDEAD_TRIBE +
                u"##ボーンラット##"
                u"骨ネズミ#スター変化無効化",
                (12, 37), (1, 2), HIGH_POWER, ability=__data.Ability(
                    _const.PREVENTION_ABILITY+"###"+_const.STAR_NAMES)),
            __data.Summon(
                u"##elemental_1##"+_const.ALCHMIC_TRIBE +
                u"##アースアメジスト##"
                u"毒性生命体#ポイズン攻撃",
                (13, 35), (2, 2), LOW_POWER, ability=__data.Ability(
                    _const.ENCHANT_ABILITY+"###"+_const.POISON_CHANGE
                ), receptors=(__data.Receptor(
                    u"アシッドスライム##slime_4##レギアバブル##"
                    u"スライムの王様#スライム生成",
                    (5, 65), MID_POWER, ability=__data.Ability(
                        _const.PERSISTENCE_ABILITY+"###" +
                        _const.SLIME_CHANGE, 0b11)),)),
            __data.Summon(
                u"##mole_9##"+_const.BEAST_TRIBE +
                u"##ゼブラモール##"
                u"しましまモグラ#"+__general.get_skill_description(
                    _const.POWER_STROKE_SKILL),
                (40, 21), (2, 2), LOW_POWER, ability=__data.Ability(
                    _const.ADDITION_ABILITY+"###" +
                    __general.get_skill_names(_const.POWER_STROKE_SKILL))),
            __data.Summon(
                u"##cat_13##"+_const.UNDEAD_TRIBE +
                u"##ゴーストキャット##"
                u"幽霊になった猫#土スター生成",
                (22, 45), (3, 2), LOW_POWER, ability=__data.Ability(
                    _const.PERSISTENCE_ABILITY+"###" +
                    _const.SATURN_CHANGE, 0b11)),
            __data.Summon(
                u"##snake_11##"+_const.DRAGON_TRIBE +
                u"##ヤマタオロチ##"
                u"漆黒の大蛇#毒霊召喚",
                (35, 31), (4, 2), VERY_LOW_POWER, ability=__data.Ability(
                    _const.ENCHANT_ABILITY+"###PoisonGhost##" +
                    _const.BASIC_NAMES,
                    is_single=True)),
            __data.Summon(
                u"##slime_8##"+_const.ALCHMIC_TRIBE +
                u"##アシッドスライム##"
                u"酸性スライム#アシッド攻撃",
                (11, 30), (1, 3), LOW_POWER, ability=__data.Ability(
                    _const.ENCHANT_ABILITY+"###"+_const.ACID_CHANGE)),
            __data.Summon(
                u"##rat_3##"+_const.UNDEAD_TRIBE +
                u"##ゴールデンクラウン##"
                u"王様のドクロ#"+__general.get_skill_description(
                    _const.HALF_VENUS_SKILL),
                (25, 30), (2, 3), LOW_POWER, ability=__data.Ability(
                    _const.ADDITION_ABILITY+"###" +
                    __general.get_skill_names(_const.HALF_VENUS_SKILL)),
                receptors=(__data.Receptor(
                    u"ゴーストキャット##cat_12##ゴールドレオ##"
                    u"黄金の獅子像#"+__general.get_skill_description(
                        _const.ANTI_SUMMONING_SKILL),
                    (21, 36), LOW_POWER, ability=__data.Ability(
                        _const.ADDITION_ABILITY+"###" +
                        __general.get_skill_names(
                            _const.ANTI_SUMMONING_SKILL))),)),
            __data.Summon(
                u"##spider_3##"+_const.BEAST_TRIBE +
                u"##ゴールドクラブ##"
                u"黄金のカニ#",
                (5, 80), (3, 3), MID_POWER,),
            __data.Summon(
                u"##cat_15##"+_const.BEAST_TRIBE +
                u"##ドロボーキャット##"
                u"どろぼう猫#" +
                __general.get_skill_description(_const.ROB_CARD_SKILL),
                (22, 35), (3, 3), VERY_LOW_POWER, ability=__data.Ability(
                    _const.ADDITION_ABILITY+"###" +
                    __general.get_skill_names(_const.ROB_CARD_SKILL))),
            __data.Summon(
                u"##fly_8##"+_const.SKY_TRIBE +
                u"##ライトニングフライ##"
                u"幸運の金バエ#"+__general.get_skill_description(
                    _const.PHANTOM_THIEF_SKILL),
                (11, 49), (4, 3), LOW_POWER, ability=__data.Ability(
                        _const.PERSISTENCE_ABILITY+"###LuckUp##" +
                        _const.BASIC_NAMES, 0b111)),
            __data.Summon(
                u"##slime_10##"+_const.ALCHMIC_TRIBE +
                u"##ソーダスライム##"
                u"苛性ソーダ生命体#",
                (11, 20), (1, 4), MID_POWER, receptors=(__data.Receptor(
                    u"ダークロウラー##slime_9##ダークマター##"
                    u"闇の世界の物質#"+__general.get_skill_description(
                        _const.MOON_CHILD_SKILL),
                    (10, 50), MID_POWER, ability=__data.Ability(
                        _const.ADDITION_ABILITY+"###" +
                        __general.get_skill_description(
                            _const.MOON_CHILD_SKILL))),)),
            __data.Summon(
                u"##elemental_6##"+_const.ALCHMIC_TRIBE +
                u"##アイスサファイア##"
                u"氷結生命体#" +
                __general.get_skill_description(_const.ICE_PICKER_SKILL),
                (30, 33), (2, 4), LOW_POWER, ability=__data.Ability(
                    _const.ADDITION_ABILITY+"###" +
                    __general.get_skill_names(_const.ICE_PICKER_SKILL))),
            __data.Summon(
                u"##fish_13##"+_const.BEAST_TRIBE +
                u"##マジックフィッシュ##"
                u"魔法の魚#ウォーター生成",
                (10, 27), (3, 4), LOW_POWER, ability=__data.Ability(
                    _const.PERSISTENCE_ABILITY+"###Water##" +
                    _const.BASIC_NAMES, 0b11)),
            __data.Summon(
                u"##snake_4##"+_const.DRAGON_TRIBE +
                u"##プチリヴァイアサン##"
                u"小さな怪物#アイス攻撃",
                (50, 27), (3, 4), LOW_POWER, ability=__data.Ability(
                    _const.ENCHANT_ABILITY+"###"+_const.ICE_CHANGE)),
            __data.Summon(
                u"##fish_0##"+_const.BEAST_TRIBE +
                u"##プチバハムート##"
                u"小さな世界魚#"+__general.get_skill_description(
                    _const.SHORT_TURN_SKILL),
                (12, 60), (4, 4), LOW_POWER, ability=__data.Ability(
                    _const.ADDITION_ABILITY+"###" +
                    __general.get_skill_names(_const.SHORT_TURN_SKILL))),
            __data.Summon(
                u"##crow_7##"+_const.SKY_TRIBE +
                u"##ナイトクロウ##"
                u"夜空を写したカラス#カードを月スターに",
                (15, 26), (1, 5), LOW_POWER, ability=__data.Ability(
                    _const.PERSISTENCE_ABILITY+"###Moon##" +
                    _const.CARD_NAMES, 0b0)),
            __data.Summon(
                u"##wolf_13##"+_const.BEAST_TRIBE +
                u"##ムーンファング##"
                u"月に住むオオカミ#",
                (41, 22), (2, 5), MID_POWER, receptors=(__data.Receptor(
                    u"ウィルオウィスプ##wolf_10##イクリプスウルフ##"
                    u"光と闇の狼#ストーン攻撃",
                    (53, 30), MID_POWER, ability=__data.Ability(
                        _const.ENCHANT_ABILITY+"###"+_const.STONE_CHANGE)),)),
            __data.Summon(
                u"##baku_9##"+_const.BEAST_TRIBE +
                u"##ソウルイーター##"
                u"魂を食べる生物#"+__general.get_skill_description(
                    _const.SOUL_EAT_SKILL),
                (11, 52), (3, 5), VERY_LOW_POWER, ability=__data.Ability(
                    _const.ADDITION_ABILITY+"###" +
                    __general.get_skill_names(_const.SOUL_EAT_SKILL))),
            __data.Summon(
                u"##mole_11##"+_const.BEAST_TRIBE +
                u"##ダークロウラー##"
                u"闇を這う生物#月スター生成",
                (13, 61), (3, 5), LOW_POWER, ability=__data.Ability(
                    _const.PERSISTENCE_ABILITY+"###" +
                    _const.MOON_CHANGE, 0b11)),
            __data.Summon(
                u"##dragon_10##"+_const.DRAGON_TRIBE +
                u"##ブラックドラゴン##"
                u"黒の竜#",
                (40, 30), (4, 5), MID_POWER, receptors=(__data.Receptor(
                    u"ファイアルビー##dragon_0##ダークフレイムドラゴン##"
                    u"炎と闇の竜#マグマ攻撃",
                    (80, 20), MID_POWER, ability=__data.Ability(
                        _const.ENCHANT_ABILITY+"###"+_const.MAGMA_CHANGE)
                    ), __data.Receptor(
                    u"アイスサファイア##dragon_4##シャドーアイスドレイク##"
                    u"氷と影の竜#水スター生成",
                    (40, 60), MID_POWER, ability=__data.Ability(
                        _const.PERSISTENCE_ABILITY+"###" +
                        _const.MERCURY_CHANGE, 0b11)))),
            __data.Summon(
                u"##rat_10##"+_const.UNDEAD_TRIBE +
                u"##クリスタルスカル##"
                u"水晶のドクロ#カードを太陽スターに",
                (15, 21), (1, 6), LOW_POWER, ability=__data.Ability(
                    _const.PERSISTENCE_ABILITY+"###Sun##" +
                    _const.CARD_NAMES, 0b0)),
            __data.Summon(
                u"##bat_12##"+_const.SKY_TRIBE +
                u"##ウィルオウィスプ##"
                u"光の生命体#"+__general.get_skill_description(
                    _const.STONE_BREAKER_SKILL),
                (31, 20), (2, 6), LOW_POWER, ability=__data.Ability(
                    _const.ADDITION_ABILITY+"###" +
                    __general.get_skill_names(_const.STONE_BREAKER_SKILL))),
            __data.Summon(
                u"##baku_12##"+_const.BEAST_TRIBE +
                u"##ホシクイ##"
                u"星を食べる生物#"+__general.get_skill_description(
                    _const.VAMPIRE_SKILL),
                (40, 20), (3, 6), LOW_POWER, ability=__data.Ability(
                    _const.ADDITION_ABILITY+"###" +
                    __general.get_skill_names(_const.VAMPIRE_SKILL))),
            __data.Summon(
                u"##fish_12##"+_const.BEAST_TRIBE +
                u"##エンゼルフィッシュ##"
                u"天使の魚#ウォーターを水スターに",
                (15, 48), (3, 6), LOW_POWER, ability=__data.Ability(
                    _const.PERSISTENCE_ABILITY+"###Mercury##Water", 0b0)),
            __data.Summon(
                u"##crow_12##"+_const.SKY_TRIBE +
                u"##シリウスレイヴン##"
                u"白いワタリガラス#太陽スター生成",
                (20, 55), (4, 6), LOW_POWER, ability=__data.Ability(
                    _const.PERSISTENCE_ABILITY+"###" +
                    _const.SUN_CHANGE, 0b11))))
    __set_player()
    __set_summon()
