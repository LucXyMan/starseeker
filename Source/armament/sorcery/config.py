#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""config.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

魔術設定モジュール。
"""


def init():
    u"""モジュール初期化。
    魔法反応の例: スライム→キノコ使用で、
    キノコがマナプールに変化する。
    """
    import utils.const as __const
    import data as __data
    global __sorcerys, __joekers
    LOW_POWER = 2
    MID_POWER = LOW_POWER << 1
    HIGH_POWER = MID_POWER+(MID_POWER >> 1)
    VERY_HIGH_POWER = MID_POWER << 2
    __sorcerys = (
        __data.Forming(
            u"##キノコ##相手のブロックをキノコに",
            (1, 0), True, MID_POWER, __const.MATANGO_EFFECT,
            magic_reaction=__data.MagicReaction(
                u"スライム", __data.Forming, u"マナプール##自身のブロック・キノコ・スライムを木スターに",
                False, HIGH_POWER, "Jupiter##Matango#"+__const.BASIC_NAMES +
                "#"+__const.SLIME_NAMES)),
        __data.Equip(
            u"##イバラ##相手の兜封印", (2, 0), True, 0B0010),
        __data.Forming(
            u"##カミカゼ##自身のカードを速さの欠片に",
            (3, 0), False, HIGH_POWER, "Speed##"+__const.CARD_NAMES,
            is_strictly=True),
        __data.Forming(
            u"##リフレッシュ##自身のイレギュラーを木スターに",
            (4, 0), False, HIGH_POWER, "Jupiter##"+__const.IRREGULAR_NAMES),
        __data.Forming(
            u"##マグマ##相手のブロックをマグマに",
            (1, 1), True, MID_POWER, "Magma##"+__const.BASIC_NAMES,
            magic_reaction=__data.MagicReaction(
                u"カミカゼ", __data.Equip, u"インフェルノ##相手の武器・装飾封印", True, 0B1001)),
        __data.Equip(
            u"##メルトアーマー##相手の鎧封印", (2, 1), True, 0B0100),
        __data.Forming(
            u"##バーニングパワー##自身のカードを力の欠片に",
            (3, 1), False, HIGH_POWER, "Power##"+__const.CARD_NAMES,
            is_strictly=True),
        __data.Forming(
            u"##シャーマニズム##相手フィールドに火霊を召喚",
            (4, 1), True, 0, "FireGhost##"+__const.BASIC_NAMES),
        __data.Forming(
            u"##チョコレート##自身のブロックをチョコレートに",
            (1, 2), False, VERY_HIGH_POWER, "Chocolate##"+__const.BASIC_NAMES),
        __data.Poison(
            u"##トキシン##相手のブロックをポイズンに/毒状態異常",
            (2, 2), True, False, MID_POWER, __const.POISON_EFFECT),
        __data.Forming(
            u"##ストーン##相手のブロックをストーンに",
            (3, 2), True, MID_POWER, "Stone##"+__const.BASIC_NAMES,
            magic_reaction=__data.MagicReaction(
                u"リーパー", __data.Critical, u"アースクエイク##相手の全クリーチャー破壊",
                True, True, False)),
        __data.Forming(
            u"##ウィッチクラフト##相手フィールドに毒霊を召喚",
            (4, 2), True, 0, "PoisonGhost##"+__const.BASIC_NAMES),
        __data.Forming(
            u"##アシッド##相手のブロックをアシッドに",
            (1, 3), True, MID_POWER, __const.ACID_EFFECT,
            magic_reaction=__data.MagicReaction(
                u"トキシン", __data.Equip, u"アクアレギア##相手の兜・鎧封印", True, 0B0110)),
        __data.Unlock(
            u"##アンロック##自身のホールドにキーを追加",
            (2, 3), False, True, "GoldKey##"+__const.BASIC_NAMES),
        __data.Forming(
            u"##プロテクト##自身のカードを守りの欠片に",
            (3, 3), False, HIGH_POWER, "Protect##"+__const.CARD_NAMES,
            is_strictly=True),
        __data.Forming(
            u"##ミダスタッチ##自身のミミックを金スターに",
            (4, 3), False, MID_POWER, "Venus##"+__const.MIMIC_NAMES,
            is_strictly=True),
        __data.Forming(
            u"##スライム##自身のブロックをスライムに",
            (1, 4), False, HIGH_POWER, "Slime##"+__const.BASIC_NAMES),
        __data.Frozen(
            u"##アイス##相手のブロックをアイスに/凍結状態異常",
            (2, 4), True, False, MID_POWER, "Ice##"+__const.BASIC_NAMES),
        __data.Forming(
            u"##ツナミ##自身のブロックをウォーターに",
            (3, 4), False, HIGH_POWER, "Water##"+__const.BASIC_NAMES,
            magic_reaction=__data.MagicReaction(
                u"ヒーリング", __data.Forming, u"マリンブレス##自身のブロック・アイス・ウォーターを水スターに",
                False, HIGH_POWER, "Mercury##Ice#Water#"+__const.BASIC_NAMES)),
        __data.Forming(
            u"##ネクロマンシー##相手フィールドに氷霊を召喚",
            (4, 4), True, 0, "IceGhost##"+__const.BASIC_NAMES),
        __data.Exchange(
            u"##エクスチェンジ##互いのホールドを交換",
            (1, 5), True),
        __data.Equip(
            u"##アンチセイバー##相手の武器封印", (2, 5), True, 0B0001),
        __data.Critical(
            u"##リーパー##相手のクリーチャー破壊",
            (3, 5), True, False, False),
        __data.Forming(
            u"##サモンデーモン##相手フィールドにイーターを召喚",
            (4, 5), True, 0, __const.BLOCK_EATER_EFFECT,
            magic_reaction=__data.MagicReaction(
                u"アンロック", __data.Forming, u"サタンズゲート##相手フィールドにサタン召喚",
                True, 0, "ArchDemon##"+__const.BASIC_NAMES)),
        __data.Recovery(
            u"##ヒーリング##自身のクリーチャーを回復/状態異常除去#アンデッドは回復しない",
            (1, 6), False, False, 0.5),
        __data.Equip(
            u"##インプリズン##相手の装飾封印", (2, 6), True, 0B1000,
            magic_reaction=__data.MagicReaction(
                u"アンチセイバー", __data.Equip, u"ディヴァイン##相手の兜・装飾封印", True, 0B1010)),
        __data.Forming(
            u"##リジェネレーション##自身のカードを生命の欠片に",
            (3, 6), False, HIGH_POWER, "Life##"+__const.CARD_NAMES,
            is_strictly=True),
        __data.Forming(
            u"##エリミネイト##自身の悪霊を太陽スターに",
            (4, 6), False, HIGH_POWER, "Sun##"+__const.DEMON_NAMES+"#" +
            __const.GHOST_NAMES, is_strictly=True),
        __data.Forming(
            __const.SHIELD_TYPE+u"##マツタケ##相手のブロックをキノコに",
            (1, 0), True, HIGH_POWER, "Matango##"+__const.BASIC_NAMES),
        __data.Forming(
            __const.SHIELD_TYPE+u"##バーサーク##自身のブロックを力の欠片に",
            (1, 1), False, HIGH_POWER, __const.POWER_EFFECT),
        __data.Poison(
            __const.SHIELD_TYPE+u"##トリカブト##相手のブロックをポイズンに/毒状態異常",
            (1, 2), True, True, HIGH_POWER, __const.POISON_EFFECT),
        __data.Equip(
            __const.SHIELD_TYPE+u"##グレイプニール##相手の防具を封印", (1, 3), True, 0B1110),
        __data.Frozen(
            __const.SHIELD_TYPE+u"##サイレント##相手のスター・カードをアイスに/凍結状態異常",
            (1, 4), True, True, HIGH_POWER, "Ice##"+__const.STAR_NAMES+"#" +
            __const.CARD_NAMES),
        __data.Forming(
            __const.SHIELD_TYPE+u"##サバト##相手フィールドにデーモンを召喚",
            (1, 5), True, MID_POWER, "BlockDemon##"+__const.BASIC_NAMES),
        __data.Recovery(
            __const.SHIELD_TYPE+u"##アブゾーブ##自身の全クリーチャーを全回復/"
            u"状態異常除去#アンデッドは回復しない", (1, 6), False, True, 1))
    __joekers = (
        __data.Equip(
            __const.JOKER_TYPE+u"##カーズ##自身の装備封印", (1, -1), False, 0B1111),
        __data.Delete(
            __const.JOKER_TYPE+u"##オールデリート##自身の手札破棄", (1, -1), False, True),
        __data.Critical(
            __const.JOKER_TYPE+u"##ジェノサイド##自身の全クリーチャー破壊",
            (1, -1), False, True, True),
        __data.Star(
            __const.JOKER_TYPE+u"##ヴァニシングスター##自身の全スター消失",
            (1, -1), False, (-1, -99)),
        __data.Hold(
            __const.JOKER_TYPE+u"##パンドラボックス##自身のホールドにパンドラの箱を追加",
            (1, -1), False, True, "Pandora##"+__const.BASIC_NAMES))
    __data.Sorcery.set_collections(__sorcerys+__joekers)
