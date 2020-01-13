#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""equip.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

装備モジュール。
"""
import inventories as _inventories


class Equip(object):
    u"""装備データ。
    """
    __slots__ = (
        "_ability", "__keys", "__image_number", "__seals",  "__sp",
        "__string", "__value")
    _CORRECTION = 1
    __collections = ()

    @classmethod
    def get_collections(cls):
        u"""コレクション取得。
        """
        return Equip.__collections[:]

    @classmethod
    def set_collections(cls, value):
        u"""コレクション設定。
        """
        Equip.__collections = tuple(value)

    @classmethod
    def get_collection(cls, key):
        u"""コレクション要素取得。
        """
        return Equip.__collections[key]

    @classmethod
    def get_by_name(cls, *names):
        u"""装備名による番号取得。
        """
        result = []
        for name in names:
            for equip in Equip.get_collections():
                if name == equip.name:
                    break
            else:
                raise ValueError("Name not found.")
            result.append(equip.number)
        return tuple(result)

    def __init__(
        self, image_number, string, sp, correction,
        ability=None, keys=(), seals=()
    ):
        u"""コンストラクタ。
        __image_number: 画像番号。
        __string: 種類:名前:メイン概要:サブ概要。
        __sp: 必要SP。
        __value: 能力値。
        __keys: キーアイテム。
        __seals: 必要フラグ or 必要クリアレベル。
        _ability: 特殊能力。
        """
        self.__image_number = image_number
        self.__string = string
        self.__sp = sp
        self.__value = int(self.__sp*self._CORRECTION*correction)
        self.__keys = keys
        self.__seals = seals
        self._ability = ability if ability else Ability()

    def __repr__(self):
        u"""文字列表現取得。
        """
        equip = u"Weapon", u"Head", u"Body", u"Accessory", u"Empty"
        return u"<{name}: {type_}, sp={sp}>".format(
            name=self.name, type_=equip[self.type], sp=self.__sp)

    # ---- Effect ----
    def get_enchant(self, lv):
        u"""武器効果取得。
        """
        return ()

    def get_persistence(self, turn):
        u"""頭防具効果取得。
        """
        return ()

    def is_prevention(self, target):
        u"""ブロック変化防止判定。
        """
        return False

    # ---- Property ----
    @property
    def notice(self):
        u"""情報取得。
        """
        able, cnsm = (
            (u"取得", u"消費") if _inventories.is_buyable(self) else
            (u"不可", u"必要"))
        require_key = self.rank-sum(
            1 for key in self.keys if _inventories.Item.has(key-1))
        has_text = (
            u"{name}/{param}:{value}#{desc}/{sub_desc}#"
            u"決定キーで装備/リムーブキーで解除"
        ).format(
            name=self.name, param=u"ATK" if self.is_weapon else u"DEF",
            value=self.value, desc=self.desc, sub_desc=self.sub_desc)
        require = (
            u"キーアイテムがあと{require_key}つ必要".
            format(require_key=require_key))
        buy = u"#決定キーで購入" if _inventories.is_buyable(self) else u""
        content = (
            u"{category}が入っている/{able}:{sp}SP{cnsm}{buy}".format(
                category=self.category, able=able, sp=self.sp,
                cnsm=cnsm, buy=buy))
        not_has_text = (
            u"封印されている" if self.is_sealed else
            require if require_key else content)
        return (
            has_text if _inventories.Item.has(self.number-1) else
            not_has_text)

    @property
    def number(self):
        u"""番号取得。
        """
        return Equip.__collections.index(self)

    @property
    def image_number(self):
        u"""画像番号取得。
        """
        return self.__image_number

    @property
    def icon(self):
        u"""画像番号からアイコン取得。
        """
        import material as __material
        return __material.icon.get(self.__image_number)

    @property
    def category(self):
        u"""種類の取得。
        """
        category, _, _, _ = self.__string.split("#")
        return category

    @property
    def name(self):
        u"""名前の取得。
        """
        _, name, _, _ = self.__string.split("#")
        return name

    @property
    def desc(self):
        u"""アイテム説明の取得。
        """
        _, _, desc, _ = self.__string.split("#")
        return desc

    @property
    def sub_desc(self):
        u"""能力説明を取得。
        """
        _, _, _, sub_desc = self.__string.split("#")
        return sub_desc if sub_desc else u"特殊能力なし"

    @property
    def sp(self):
        u"""必要SP取得。
        """
        return self.__sp

    @property
    def value(self):
        u"""能力値取得。
        """
        return self.__value

    @property
    def keys(self):
        u"""キーアイテム番号取得。
        """
        return self.get_by_name(*self.__keys)

    @property
    def rank(self):
        u"""ランク取得。
        キーアイテム数で決定される。
        """
        return len(self.__keys)

    @property
    def type(self):
        u"""アイテム種類番号を返す。
        0: 武器。1: 頭防具。2: 体防具。3: 装飾品。4: それ以外。
        """
        return (
            0 if self.is_weapon else 1 if self.is_head else
            2 if self.is_body else 3 if self.is_accessory else 4)

    # ------ Ability ------
    @property
    def spell(self):
        u"""装飾効果取得。
        """
        return ()

    @property
    def skills(self):
        u"""スキル取得。
        """
        _, skills = self._ability.string.split("###")
        return skills

    # ------ Detection ------
    @property
    def is_sealed(self):
        u"""封印判定。
        """
        def __is_fulfill(seal):
            u"""条件判定。
            """
            if seal == -1:
                return not _inventories.General.is_cleared_endless()
            elif seal == -2:
                return not _inventories.Item.is_completion()
            elif seal == -3:
                return not _inventories.Item.is_crown_completion()
            elif seal == -4:
                return not _inventories.Card.is_completion()
            else:
                return not _inventories.Level.has(seal)
        return any(__is_fulfill(seal) for seal in self.__seals)

    @property
    def is_locked(self):
        u"""ロックされている場合に真。
        """
        return any(not _inventories.Item.has(key-1) for key in self.keys)

    @property
    def is_weapon(self):
        u"""武器判定。
        """
        return False

    @property
    def is_armor(self):
        u"""防具判定。
        """
        return False

    @property
    def is_head(self):
        u"""頭防具判定。
        """
        return False

    @property
    def is_body(self):
        u"""体防具判定。
        """
        return False

    @property
    def is_accessory(self):
        u"""装飾品判定。
        """
        return False


class Armor(Equip):
    u"""防具データ。
    """
    __slots__ = ()

    @property
    def is_armor(self):
        u"""防具判定。
        """
        return True


class Ability(object):
    u"""装備能力データ。
    """
    __slots__ = "__interval", "__is_single", "__string",

    def __init__(self,  string="###", interval=0b0, is_single=False):
        u"""コンストラクタ。
        """
        self.__string = string
        self.__interval = interval
        self.__is_single = is_single

    @property
    def string(self):
        u"""文字列取得。
        """
        return self.__string

    @property
    def interval(self):
        u"""エフェクト間隔。
        """
        return self.__interval

    @property
    def is_single(self):
        u"""対象が単一かどうかの判定。
        """
        return self.__is_single


def get_chest(lock, rank):
    u"""宝箱取得。
    """
    rank_texts = u"", u"ブロンズ", u"シルバー", u"ゴールド", u"プラチナ"
    icon_num = 0x800, 0x700
    icon_colors = 0x9, 0x6, 0x2, 0x1, 0x8
    return Equip(
        icon_num[lock]+icon_colors[rank], u"宝箱#{rank}チェスト#{lock}#".format(
            rank=rank_texts[rank], lock=u"鍵がかかっている" if bool(lock) else
            u"アイテム入りの箱"), 0, 0)
