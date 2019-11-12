#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""config.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ユニット設定モジュール。
"""


def init():
    u"""パッケージ初期化。
    """
    import data as __data
    import utils.const as _const
    status = 10, 0
    __data.Player.set_collections((
        __data.Player(
            u"altair", u"##"+_const.WARRIOR_ROLE+u"##" +
            _const.ALTAIR_NAME+u"##闇の王国ダークランドの勇者#"
            u"不死身のゾンビ戦士", status, (
                u"ストーンブレーカー", u"パワーストローク",
                u"コンプアシスト", u"ソウルイート",
                u"アンチサモーニング", u"ネクロマンサー",
                u"ハーフジュピター", u"セーフティ",
                u"タフネス", u"杖装備",
                u"飛び道具装備", u"帽子装備",
                u"ローブ装備")),
        __data.Player(
            u"corvus", u"##"+_const.WARRIOR_ROLE+u"##" +
            _const.CORVUS_NAME+u"##黒の帝国ノワールの傭兵#"
            u"賞金首のサイコキラー", status, (
                u"ファイアイーター", u"アイスピッカー",
                u"パワーストローク", u"コンプアシスト",
                u"ヴァンピール", u"ロブカード",
                u"ファルコナー", u"ハーフマーズ",
                u"マイティ", u"杖装備",
                u"飛び道具装備", u"帽子装備",
                u"ローブ装備")),
        __data.Player(
            u"nova", u"##"+_const.WIZARD_ROLE+u"##" +
            _const.NOVA_NAME+u"##影の国シェイディアの魔術師#"
            u"魔法で生み出されたホムンクルス", status, (
                u"アイスピッカー", u"アシッドイレーザー",
                u"ダブルスペル", u"ソウルイート",
                u"リバースソーサリー", u"アルケミスト",
                u"ハーフメルクリー", u"セーフティ",
                u"スピードスター", u"剣装備",
                u"飛び道具装備", u"兜装備",
                u"鎧装備")),
        __data.Player(
            u"sirius", u"##"+_const.SEEKER_ROLE+u"##" +
            _const.SIRIUS_NAME+u"##ヴァイス・オーダーの怪物ハンター#"
            u"大狼に変身する人狼牧師", status, (
                u"ストーンブレーカー", u"エクソシスト",
                u"コンプアシスト", u"ピュリファイ",
                u"アンチサモーニング", u"シェパード",
                u"サンオブサン", u"セーフティ",
                u"ライフブースト", u"杖装備",
                u"重武器装備", u"兜装備",
                u"鎧装備")),
        __data.Player(
            u"castor", u"##"+_const.WIZARD_ROLE+u"##" +
            _const.CASTOR_NAME+u"##暁の塔の錬金術師#"
            u"禁呪を研究するマッド・ソーサラー", status, (
                u"ファイアイーター", u"アシッドイレーザー",
                u"エクソシスト", u"ダブルスペル",
                u"ソウルイート", u"リバースソーサリー",
                u"アルケミスト", u"ハーフヴェヌス",
                u"セーフティ", u"タフネス",
                u"剣装備", u"飛び道具装備",
                u"兜装備", u"鎧装備")),
        __data.Player(
            u"pluto", u"##"+_const.SEEKER_ROLE+u"##" +
            _const.PLUTO_NAME+u"##月下都市セレネの怪盗道化#"
            u"魂を盗むリーパー・クラウン", status, (
                u"ファイアイーター", u"アシッドイレーザー",
                u"ファントムシーフ", u"ロブカード",
                u"ソウルイート", u"リバースソーサリー",
                u"シェパード", u"ハーフサターン",
                u"スピードスター", u"杖装備",
                u"重武器装備", u"兜装備",
                u"鎧装備")),
        __data.Player(
            u"regulus", u"##"+_const.ROYAL_ROLE+u"##" +
            _const.REGULUS_NAME+u"##夜の国ナイトピアの王子#"
            u"亡国のファントム", status, (
                u"ファイアイーター", u"アイスピッカー",
                u"コンプアシスト", u"ソウルイート",
                u"リバースソーサリー", u"ネクロマンサー",
                u"ムーンチャイルド", u"セーフティ",
                u"スピードスター", u"重武器装備",
                u"飛び道具装備", u"兜装備",
                u"鎧装備")),
        __data.Player(
            u"lucifer", u"##"+_const.ROYAL_ROLE+u"##" +
            _const.LUCIFER_NAME+u"##宵星城を支配する伯爵#"
            u"魔城に棲むヴァンパイア", status, (
                u"ストーンブレーカー", u"パワーストローク",
                u"ヴァンピール", u"ソウルイート",
                u"リバースソーサリー", u"アンチサモーニング",
                u"ファルコナー", u"ハーフヴェヌス",
                u"マイティ", u"重武器装備",
                u"飛び道具装備", u"兜装備",
                u"鎧装備")),
        __data.Player(
            u"nebula", u"##"+_const.MONSTER_ROLE+u"##" +
            _const.NEBULA_NAME+u"##宵星城に眠る生物#"
            u"星空からやって来たインベーダー", (20, 10), (
                u"ストーンブレーカー", u"パワーストローク",
                u"エクソシスト", u"ヴァンピール",
                u"コンプアシスト", u"ピュリファイ",
                u"ダブルスペル", u"ソウルイート",
                u"アンチサモーニング", u"ドラゴンマスター",
                u"ムーンチャイルド", u"ダークフォース",
                u"セーフティ", u"タフネス"))))
    LOW_POWER = 350
    MID_POWER = 400
    HIGH_POWER = 450
    __data.Summon.set_collections((
        __data.Summon(
            u"seed_1", u"##"+_const.ALCHMIC_TRIBE +
            u"##フェアリーシード##妖精の花の種#",
            (10, 20), (1, 0), MID_POWER, fusions=(
                __data.Fusion(
                    u"ソーダスライム", u"herb_1", u"フェアリーハーブ##妖精の葉#",
                    (10, 45), HIGH_POWER, fusions=(__data.Fusion(
                         u"ソーダスライム", u"flower_1", u"フェアリーブルーム##妖精の花#木スター生成",
                         (15, 60), MID_POWER, skill=__data.Skill(
                             "Jupiter##"+_const.BASIC_NAMES,
                             _const.SUSTAIN_SKILL_TYPE, 0b11)),)),)),
        __data.Summon(
            u"snake_2", u"##"+_const.DRAGON_TRIBE +
            u"##ラージスネーク##からみあう大蛇#", (42, 25), (2, 0), MID_POWER),
        __data.Summon(
            u"fly_14", u"##"+_const.SKY_TRIBE +
            u"##ジャイアントフライ##巨大バエ#自身のスターをポイズンに",
            (62, 30), (3, 0), HIGH_POWER, skill=__data.Skill(
                "Poison##"+_const.STAR_NAMES, _const.SUSTAIN_SKILL_TYPE, 0b11)
            ),
        __data.Summon(
            u"herb_8", u"##"+_const.ALCHMIC_TRIBE +
            u"##スプライトレント##精霊が住む植物#キノコ攻撃",
            (10, 45), (4, 0), LOW_POWER, skill=__data.Skill(
                _const.MATANGO_EFFECT, _const.ATTACK_SKILL_TYPE),
            fusions=(__data.Fusion(
                u"ウィルオウィスプ", u"flower_13", u"サンブロッサム##太陽の花#生命の欠片生成",
                (5, 60), MID_POWER, skill=__data.Skill(
                    "Life##"+_const.BASIC_NAMES,
                    _const.SUSTAIN_SKILL_TYPE, 0b111)),)),
        __data.Summon(
            u"bat_5", u"##"+_const.SKY_TRIBE +
            u"##キャンドルバット##火遊び好きのコウモリ#マグマ攻撃",
            (25, 5), (1, 1), LOW_POWER, skill=__data.Skill(
                "Magma##"+_const.BASIC_NAMES, _const.ATTACK_SKILL_TYPE),
            fusions=(__data.Fusion(
                u"ジャイアントフライ", u"fly_5", u"ファイアフライ##燃え盛る虫#火スター生成",
                (53, 20), MID_POWER, skill=__data.Skill(
                    _const.MARS_EFFECT, _const.SUSTAIN_SKILL_TYPE, 0b11)),)),
        __data.Summon(
            u"rat_5", u"##"+_const.UNDEAD_TRIBE +
            u"##レッドスケルトン##血塗られしドクロ#",
            (15, 31), (2, 1), MID_POWER),
        __data.Summon(
            u"slime_5", u"##"+_const.ALCHMIC_TRIBE +
            u"##マグマゼリー##意思を持ったマグマ#マグマ生成",
            (30, 40), (3, 1), HIGH_POWER, skill=__data.Skill(
                _const.MAGMA_EFFECT, _const.SUSTAIN_SKILL_TYPE, 0b11)),
        __data.Summon(
            u"crow_5", u"##"+_const.SKY_TRIBE +
            u"##ダークフェニックス##漆黒の不死鳥#凍結・炎上防止",
            (19, 54), (4, 1), LOW_POWER, skill=__data.Skill(
                "Ice#Magma", _const.DEFENCE_SKILL_TYPE)),
        __data.Summon(
            u"rat_7", u"##"+_const.UNDEAD_TRIBE +
            u"##ボーンラット##骨ネズミ#",
            (12, 17), (1, 2), MID_POWER, fusions=(__data.Fusion(
                u"ラージスネーク", u"snake_7", u"ヒュドラゾンビ##不死身の多頭竜#ポイズン攻撃",
                (40, 30), MID_POWER, skill=__data.Skill(
                    _const.POISON_EFFECT, _const.ATTACK_SKILL_TYPE)),)),
        __data.Summon(
            u"slime_3", u"##"+_const.ALCHMIC_TRIBE +
            u"##ポイズンドロップ##猛毒スライム#ポイズン攻撃",
            (13, 35), (2, 2), LOW_POWER, skill=__data.Skill(
                _const.POISON_EFFECT, _const.ATTACK_SKILL_TYPE),
            fusions=(__data.Fusion(
                u"アシッドスライム", u"slime_15", u"レギアバブル##スライムの王様#自身のブロックをスライムに",
                (5, 65), MID_POWER, skill=__data.Skill(
                    _const.SLIME_EFFECT, _const.SUSTAIN_SKILL_TYPE, 0b11)),)),
        __data.Summon(
            u"cat_13", u"##"+_const.UNDEAD_TRIBE +
            u"##ゴーストキャット##幽霊になった猫#土スター生成",
            (42, 22), (3, 2), LOW_POWER, skill=__data.Skill(
                _const.SATURN_EFFECT, _const.SUSTAIN_SKILL_TYPE, 0b11)),
        __data.Summon(
            u"snake_11", u"##"+_const.DRAGON_TRIBE +
            u"##ヤマタオロチ##漆黒の大蛇#ストーン攻撃",
            (65, 31), (4, 2), LOW_POWER, skill=__data.Skill(
                _const.STONE_EFFECT, _const.ATTACK_SKILL_TYPE)),
        __data.Summon(
            u"slime_8", u"##"+_const.ALCHMIC_TRIBE +
            u"##アシッドスライム##酸性スライム#アシッド攻撃",
            (11, 30), (1, 3), LOW_POWER, skill=__data.Skill(
                _const.ACID_EFFECT, _const.ATTACK_SKILL_TYPE)),
        __data.Summon(
            u"crow_13", u"##"+_const.SKY_TRIBE +
            u"##スターバード##星空の渡り鳥#速さの欠片生成",
            (11, 35), (2, 3), LOW_POWER, skill=__data.Skill(
                _const.SPEED_EFFECT, _const.SUSTAIN_SKILL_TYPE, 0b111)),
        __data.Summon(
            u"rat_3", u"##"+_const.UNDEAD_TRIBE +
            u"##ゴールデンクラウン##王様のドクロ#",
            (25, 30), (3, 3), MID_POWER, fusions=(__data.Fusion(
                u"ゴーストキャット", u"cat_12", u"ゴールドレオ##黄金の獅子像#悪霊を金スターに",
                (31, 36), MID_POWER, skill=__data.Skill(
                    "Venus##"+_const.DEMON_NAMES+"#"+_const.GHOST_NAMES,
                    _const.SUSTAIN_SKILL_TYPE, 0b0)),)),
        __data.Summon(
            u"fly_12", u"##"+_const.SKY_TRIBE +
            u"##ライトニングフライ##光るハエ#酸・毒防止",
            (11, 49), (4, 3), LOW_POWER, skill=__data.Skill(
                "Acid#Poison", _const.DEFENCE_SKILL_TYPE)),
        __data.Summon(
            u"slime_10", u"##"+_const.ALCHMIC_TRIBE +
            u"##ソーダスライム##苛性ソーダ生命体#",
            (11, 20), (1, 4), MID_POWER, fusions=(
                __data.Fusion(
                    u"ブラックリッチ", u"slime_9", u"ダークマター##闇の世界の物質#月スター生成",
                    (10, 50), MID_POWER, skill=__data.Skill(
                        _const.MOON_EFFECT, _const.SUSTAIN_SKILL_TYPE, 0b11)),
            )),
        __data.Summon(
            u"slime_6", u"##"+_const.ALCHMIC_TRIBE +
            u"##フリーズジェル##液体窒素スライム#アイス生成",
            (30, 33), (2, 4), HIGH_POWER, skill=__data.Skill(
                _const.ICE_EFFECT, _const.SUSTAIN_SKILL_TYPE, 0b11)),
        __data.Summon(
            u"fish_13", u"##"+_const.BEAST_TRIBE +
            u"##マジックフィッシュ##魔法の魚#ウォーター生成",
            (10, 27), (3, 4), LOW_POWER, skill=__data.Skill(
                "Water##"+_const.BASIC_NAMES, _const.SUSTAIN_SKILL_TYPE, 0b11)
            ),
        __data.Summon(
            u"fish_11", u"##"+_const.BEAST_TRIBE +
            u"##プチリヴァイアサン##小さな怪物#アイス攻撃",
            (63, 24), (4, 4), LOW_POWER, skill=__data.Skill(
                "Ice##"+_const.BASIC_NAMES, _const.ATTACK_SKILL_TYPE)),
        __data.Summon(
            u"crow_7", u"##"+_const.SKY_TRIBE +
            u"##ナイトクロウ##夜空を写したカラス#カードを月スターに",
            (15, 26), (1, 5), LOW_POWER, skill=__data.Skill(
                "Moon##"+_const.CARD_NAMES, _const.SUSTAIN_SKILL_TYPE, 0b0)),
        __data.Summon(
            u"wolf_13", u"##"+_const.BEAST_TRIBE +
            u"##ムーンファング##月に住むオオカミ#",
            (46, 22), (2, 5), MID_POWER),
        __data.Summon(
            u"rat_11", u"##"+_const.UNDEAD_TRIBE +
            u"##ブラックリッチ##魔術師のドクロ#守りの欠片生成",
            (23, 31), (3, 5), LOW_POWER, skill=__data.Skill(
                    _const.PROTECT_EFFECT, _const.SUSTAIN_SKILL_TYPE, 0b111),
            fusions=(__data.Fusion(
                u"ジャイアントフライ", u"fly_11", u"ベルゼバブ##不死身の生物兵器#力の欠片生成",
                (25, 50), MID_POWER, skill=__data.Skill(
                    _const.POWER_EFFECT, _const.SUSTAIN_SKILL_TYPE, 0b111)),)),
        __data.Summon(
            u"doragon_14", u"##"+_const.DRAGON_TRIBE +
            u"##ブラックドラゴン##黒の竜#",
            (40, 30), (4, 5), MID_POWER, fusions=(
                __data.Fusion(
                    u"マグマゼリー", u"doragon_5", u"ダークフレイムドラゴン##炎と闇の竜#マグマ攻撃",
                    (60, 40), MID_POWER, skill=__data.Skill(
                        "Magma##Normal", _const.ATTACK_SKILL_TYPE)),
                __data.Fusion(
                    u"フリーズジェル", u"doragon_6", u"シャドーアイスドレイク##氷と影の竜#アイス攻撃",
                    (60, 40), MID_POWER, skill=__data.Skill(
                        "Ice##Normal", _const.ATTACK_SKILL_TYPE)))),
        __data.Summon(
            u"rat_10", u"##"+_const.UNDEAD_TRIBE +
            u"##クリスタルスカル##水晶のドクロ#カードを太陽スターに",
            (15, 21), (1, 6), LOW_POWER, skill=__data.Skill(
                "Sun##"+_const.CARD_NAMES, _const.SUSTAIN_SKILL_TYPE, 0b0)),
        __data.Summon(
            u"bat_12", u"##"+_const.SKY_TRIBE +
            u"##ウィルオウィスプ##光の生命体#",
            (31, 20), (2, 6), MID_POWER, fusions=(
                __data.Fusion(
                    u"ムーンファング", u"wolf_10", u"イクリプスウルフ##光と闇の狼#ストーン攻撃",
                    (53, 30), MID_POWER, skill=__data.Skill(
                        _const.STONE_EFFECT, _const.ATTACK_SKILL_TYPE)),)),
        __data.Summon(
            u"fish_12", u"##"+_const.BEAST_TRIBE +
            u"##エンゼルフィッシュ##天使の魚#ウォーターを水スターに",
            (15, 28), (3, 6), LOW_POWER, skill=__data.Skill(
                "Mercury##Water", _const.SUSTAIN_SKILL_TYPE, 0b0)),
        __data.Summon(
            u"crow_12", u"##"+_const.SKY_TRIBE +
            u"##シリウスレイヴン##白いワタリガラス#太陽スター生成",
            (22, 45), (4, 6), LOW_POWER, skill=__data.Skill(
                _const.SUN_EFFECT, _const.SUSTAIN_SKILL_TYPE, 0b11)),
        __data.Summon(
            u"fish_0", u"##"+_const.BEAST_TRIBE +
            u"##プチバハムート##小さな世界魚#マクスウェルデーモン召喚",
            (1, 65), (5, 6), LOW_POWER, skill=__data.Skill(
                "Maxwell##"+_const.BASIC_NAMES,
                _const.SUSTAIN_SKILL_TYPE, 0b1111))))
