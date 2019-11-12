#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""config.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

特殊効果設定モジュール。
"""


def init():
    u"""モジュール初期化。
    """
    import utils.const as __const
    import catalyst as __catalyst
    import sorceries as __sorceries
    import special as __special
    import support as __support
    LOW_POWER = 4
    MID_POWER = LOW_POWER << 1
    HIGH_POWER = MID_POWER+(MID_POWER >> 1)
    VERY_HIGH_POWER = MID_POWER << 1

    def __get_name(skill):
        u"""スキル名取得。
        """
        name, _ = skill.split("#")
        return name

    def __get_description(skill):
        u"""スキル説明取得。
        """
        _, description = skill.split("#")
        return description
    __specials = (
        __sorceries.Forming(
            u"###キノコ###"
            u"相手のブロックをキノコに###" +
            __const.MATANGO_EFFECT,
            (1, 0), True, MID_POWER, catalyst=__catalyst.Catalyst(
                __sorceries.Forming,
                u"スライム####マナプール###"
                u"自身のブロック・キノコ・スライムを木スターに###"
                u"Jupiter##Matango#"+__const.BASIC_NAMES+u"#" +
                __const.SLIME_NAMES, False, HIGH_POWER)),
        __sorceries.Forming(
            u"###リフレッシュ###自身のイレギュラーを木スターに###"
            u"Jupiter##"+__const.IRREGULAR_NAMES,
            (2, 0), False, VERY_HIGH_POWER),
        __sorceries.Attract(
            u"###ブレインウォッシュ###"
            u"1/4の確率で相手のクリーチャーを引き抜く",
            (3, 0), True, hit_rate=1/4.),
        __sorceries.Break(
            u"###イバラ###"
            u"相手の兜封印",
            (4, 0), (True, 0B0010)),
        __sorceries.Forming(
            u"###マグマ###"
            u"相手のブロックをマグマに###"
            u"Magma##"+__const.BASIC_NAMES,
            (1, 1), True, MID_POWER, catalyst=__catalyst.Catalyst(
                __sorceries.Forming,
                u"サモンデーモン####インフェルノ###"
                u"相手フィールドに火霊を召喚###"
                u"FireGhost##"+__const.BASIC_NAMES, True, LOW_POWER)),
        __sorceries.Delete(
            u"###インシネレイト###"
            u"相手のカードを削除/削除分のスター減少",
            (2, 1), True, power=1),
        __sorceries.Forming(
            u"###シャーマニズム###"
            u"相手フィールドに火霊を召喚###"
            u"FireGhost##"+__const.BASIC_NAMES,
            (3, 1), True, 0),
        __sorceries.Break(
            u"###メルトアーマー###"
            u"相手の鎧封印",
            (4, 1), (True, 0B0100)),
        __sorceries.Forming(
            u"###チョコレート###"
            u"自身のブロックをチョコレートに###"
            u"Chocolate##"+__const.BASIC_NAMES,
            (1, 2), False, VERY_HIGH_POWER),
        __sorceries.Poison(
            u"###ポイズン###"
            u"相手のブロックをポイズンに/毒状態異常###" +
            __const.POISON_EFFECT,
            (2, 2), (True, False), MID_POWER),
        __sorceries.Forming(
            u"###ウィッチクラフト###"
            u"相手フィールドに毒霊を召喚###"
            u"PoisonGhost##"+__const.BASIC_NAMES,
            (3, 2), True, 0),
        __sorceries.Forming(
            u"###ストーン###"
            u"相手のブロックをストーンに###"
            u"Stone##"+__const.BASIC_NAMES,
            (4, 2), True, MID_POWER, catalyst=__catalyst.Catalyst(
                __sorceries.Critical,
                u"インシネレイト####マレフィック###"
                u"1/2の確率で相手の全クリーチャー破壊",
                (True, True), hit_rate=1/2.)),
        __sorceries.Forming(
            u"###アシッド###"
            u"相手のブロックをアシッドに###" +
            __const.ACID_EFFECT,
            (1, 3), True, MID_POWER, catalyst=__catalyst.Catalyst(
                __sorceries.Break,
                u"ポイズン####アクアレギア###"
                u"相手の兜・鎧封印",
                (True, 0B0110))),
        __sorceries.Unlock(
            u"###アンロック###"
            u"自身のホールドにキーを追加###"
            u"GoldKey##"+__const.BASIC_NAMES,
            (2, 3), (False, True)),
        __sorceries.Hardening(
            u"###ハードニング###"
            u"相手のブロックを硬化",
            (3, 3), True),
        __sorceries.Break(
            u"###アンチセイバー###"
            u"相手の武器封印",
            (4, 3), (True, 0B0001)),
        __sorceries.Freeze(
            u"###アイス###"
            u"相手のブロックをアイスに/凍結状態異常###"
            u"Ice##"+__const.BASIC_NAMES,
            (1, 4), (True, False), MID_POWER),
        __sorceries.Forming(
            u"###スライム###"
            u"自身のブロックをスライムに###"
            u"Slime##"+__const.BASIC_NAMES,
            (2, 4), False, HIGH_POWER),
        __sorceries.Forming(
            u"###ツナミ###"
            u"自身のブロックをウォーターに###"
            u"Water##"+__const.BASIC_NAMES,
            (3, 4), False, MID_POWER, catalyst=__catalyst.Catalyst(
                __sorceries.Forming,
                u"オールヒール####マリンブレス###"
                u"自身のブロック・アイス・ウォーターを水スターに###"
                u"Mercury##Ice#Water#"+__const.BASIC_NAMES, False, HIGH_POWER)
        ),
        __sorceries.Forming(
            u"###ネクロマンシー###"
            u"相手フィールドに氷霊を召喚###"
            u"IceGhost##"+__const.BASIC_NAMES,
            (4, 4), True, 0),
        __sorceries.Exchange(
            u"###エクスチェンジ###"
            u"互いのホールドを交換",
            (1, 5)),
        __sorceries.Critical(
            u"###リーパー###"
            u"1/3の確率で相手のクリーチャー破壊",
            (2, 5), (True, False), hit_rate=1/3.),
        __sorceries.Double(
            u"###ドッペルゲンガー###"
            u"相手のクリーチャーの分身を生成",
            (3, 5), True),
        __sorceries.Forming(
            u"###サモンデーモン###"
            u"相手フィールドにイーターを召喚###" +
            __const.BLOCK_EATER_EFFECT,
            (4, 5), True, 0, catalyst=__catalyst.Catalyst(
                __sorceries.Forming,
                u"アンロック####サタンズゲート###"
                u"相手フィールドにサタン召喚###"
                u"ArchDemon##"+__const.BASIC_NAMES, True, 0)),
        __sorceries.Recovery(
            u"###ヒーリング###"
            u"自身のクリーチャーを回復/状態異常除去",
            (1, 6), (False, False), 0.5),
        __sorceries.Recovery(
            u"###オールヒール###"
            u"自身の全クリーチャーを回復/状態異常除去",
            (2, 6), (False, True), 0.5),
        __sorceries.Forming(
            u"###エリミネイト###"
            u"自身の悪霊を太陽スターに###"
            u"Sun##"+__const.DEMON_NAMES+u"#"+__const.GHOST_NAMES,
            (3, 6), False, HIGH_POWER, is_strictly=True),
        __sorceries.Break(
            u"###インプリズン###"
            u"相手の装飾封印",
            (4, 6), (True, 0B1000), catalyst=__catalyst.Catalyst(
                __sorceries.Break,
                u"アンチセイバー####ディヴァイン###"
                u"相手の兜・装飾封印", (True, 0B1010))),
        __sorceries.Forming(
            __const.SHIELD_ARCANUM+u"###マツタケ###"
            u"相手のブロックをキノコに###"
            u"Matango##"+__const.BASIC_NAMES,
            (1, 0), True, HIGH_POWER),
        __sorceries.Forming(
            __const.SHIELD_ARCANUM+u"###バーサーク###"
            u"自身のブロックを力の欠片に###" +
            __const.POWER_EFFECT,
            (1, 1), False, MID_POWER),
        __sorceries.Poison(
            __const.SHIELD_ARCANUM+u"###トリカブト###"
            u"相手フィールドに毒霊を召喚/毒状態異常###" +
            u"PoisonGhost##"+__const.BASIC_NAMES,
            (1, 2), (True, True), LOW_POWER),
        __sorceries.Break(
            __const.SHIELD_ARCANUM+u"###グレイプニール###"
            u"相手の防具を封印",
            (1, 3), (True, 0B1110)),
        __sorceries.Freeze(
            __const.SHIELD_ARCANUM+u"###アブソリュートゼロ###"
            u"相手フィールドに氷霊を召喚/凍結状態異常###"
            u"IceGhost##"+__const.BASIC_NAMES,
            (1, 4), (True, True), LOW_POWER),
        __sorceries.Forming(
            __const.SHIELD_ARCANUM+u"###サバト###"
            u"相手フィールドにデーモンを召喚###"
            u"BlockDemon##"+__const.BASIC_NAMES,
            (1, 5), True, LOW_POWER),
        __sorceries.Recovery(
            __const.SHIELD_ARCANUM+u"###アブゾーブ###"
            u"自身の全クリーチャーを全回復/状態異常除去",
            (1, 6), (False, True), 1),
        __support.Enchant(
            u"ヴェノムエッジ###"
            u"ポイズン攻撃追加###" +
            __const.POISON_EFFECT),
        __support.Enchant(
            u"ラスティソード###"
            u"シャードをアシッドに###"
            u"Acid##"+__const.SHARD_NAMES),
        __support.Enchant(
            u"イーヴィルアイ###"
            u"スターをストーンに###" +
            u"Stone##"+__const.STAR_NAMES),
        __support.Enchant(
            u"フリーズスター###"
            u"スターをアイスに###"
            u"Ice##"+__const.STAR_NAMES),
        __support.Enchant(
            u"フレイムオーラ###"
            u"カードをマグマに###"
            u"Magma##"+__const.CARD_NAMES),
        __support.Enchant(
            u"ファンガス###"
            u"キノコ攻撃追加###" +
            __const.MATANGO_EFFECT),
        __support.Persistence(
            u"フォースシード###"
            u"木スター生成###" +
            __const.JUPITER_EFFECT, 0b111),
        __support.Persistence(
            u"ファイアブリンガー###"
            u"カードを火スターに###"
            u"Mars##"+__const.CARD_NAMES, 0b1),
        __support.Persistence(
            u"アースパワー###"
            u"土スター生成###" +
            __const.SATURN_EFFECT, 0b111),
        __support.Persistence(
            u"ミダスタッチ###"
            u"カードを金スターに###"
            u"Venus##"+__const.CARD_NAMES, 0b1),
        __support.Persistence(
            u"オーシャンソウル###"
            u"水スター生成###" +
            __const.MERCURY_EFFECT, 0b111),
        __support.Persistence(
            u"ネクロノミコン###"
            u"月スター生成###" +
            __const.MOON_EFFECT, 0b111),
        __support.Persistence(
            u"ホーリーグレイル###"
            u"太陽スター生成###" +
            __const.SUN_EFFECT, 0b111),
        __support.Skill(u"{name}##{description}##S##{name}".format(
            name=__get_name(__const.SOUL_EAT_SKILL),
            description=__get_description(__const.SOUL_EAT_SKILL))),
        __support.Skill(
            u"{name}##{description}##P##{name}".format(
                name=__get_name(__const.PURIFY_SKILL),
                description=__get_description(__const.PURIFY_SKILL))),
        __support.Skill(
            u"{name}##{description}##R##{name}".format(
                name=__get_name(__const.REVERSE_SORCERY_SKILL),
                description=__get_description(__const.REVERSE_SORCERY_SKILL))),
        __support.Skill(
            u"{name}##{description}##A##{name}".format(
                name=__get_name(__const.ANTI_SUMMONING_SKILL),
                description=__get_description(__const.ANTI_SUMMONING_SKILL))))
    __jokers = (
        __sorceries.Spawn(
            __const.JOKER_ARCANUM+u"###リバースサモン###"
            u"相手側にクリーチャー召喚###",
            (1, -1), True),
        __sorceries.Break(
            __const.JOKER_ARCANUM+u"###フルブレイク###"
            u"自身の装備封印",
            (1, -1), (False, 0B1111)),
        __sorceries.Delete(
            __const.JOKER_ARCANUM+u"###オールデリート###"
            u"自身の手札破棄",
            (1, -1), False, power=4),
        __sorceries.Critical(
            __const.JOKER_ARCANUM+u"###ジェノサイド###"
            u"自身の全クリーチャー破壊",
            (1, -1), (False, True), is_force=True),
        __sorceries.Hold(
            __const.JOKER_ARCANUM+u"###パンドラボックス###"
            u"自身のホールドにパンドラの箱を追加###"
            u"Pandora##"+__const.BASIC_NAMES,
            (1, -1), (False, True)),
        __sorceries.KingDemon(
            __const.JOKER_ARCANUM+u"###キングデーモン###"
            u"自身のフィールドに悪魔王召喚###"))
    __special.set_(__specials+__jokers)
