#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""data.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

装備データモジュール。
"""
import inventory as _inventory


class Equip(object):
    u"""装備データ。
    """
    __slots__ = (
        "__keys", "__image_number", "__levels",  "_skill", "__sp", "__string",
        "__value")
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
            skill=None, keys=(), levels=()
    ):
        u"""コンストラクタ。
        __image_number: 画像番号。
        __string: 種類:名前:メイン概要:サブ概要。
        __sp: 必要SP。
        __value: 能力値。
        __keys: このアイテムを購入するためのアイテム番号。
        __levels: このアイテムを購入するためにクリアするレベル。
        _skill: スキル情報オブジェクト。
        """
        import utils.const as __const
        self.__image_number = image_number
        self.__string = string
        if __const.NAME_LIMIT < len(self.name):
            raise ValueError(u"name too long")
        self.__sp = sp
        self.__value = int(self.__sp*self._CORRECTION*correction)
        self.__keys = keys
        self.__levels = levels
        self._skill = skill if skill else Skill()

    def __repr__(self):
        u"""文字列表現取得。
        """
        return u"<{name}: {type_}, sp={sp}>".format(
            name=self.name, type_=(
                "Weapon", "Head", "Body", "Accessory", "Empty")[self.type],
            sp=self.__sp)

    def get_special(self, lv):
        u"""武器効果を取得。
        """
        return ()

    def get_sustain(self, turn):
        u"""頭防具効果を取得。
        """
        return ()

    def is_prevents(self, target):
        u"""ブロック変化防止の場合に真。
        """
        return False

    @property
    def is_sealed(self):
        u"""封印状態の場合に真。
        """
        return any(not _inventory.Level.has(seal) for seal in self.__levels)

    @property
    def is_locked(self):
        u"""ロックされている場合に真。
        """
        return any(not _inventory.Items.has(key-1) for key in self.__keys)

    @property
    def info(self):
        u"""情報の取得。
        """
        able, cnsm = (
            u"取得#消費" if _inventory.SP.is_buyable(self) else
            u"不可#必要").split(u"#")
        require_key = self.rank-sum(
            1 for key in self.__keys if _inventory.Items.has(key-1))
        has_text = (
            u"{name}/{param}:{value}#{desc}/{sub_desc}#決定キーで装備/リムーブキーで解除"
        ).format(
            name=self.name, param=u"ATK" if self.is_weapon else u"DEF",
            value=self.value, desc=self.desc, sub_desc=self.sub_desc)
        require = u"キーアイテムがあと{require_key}つ必要".format(require_key=require_key)
        contents = (u"{category}が入っている/{able}:{sp}S.P{cnsm}{buy}").format(
            category=self.category, able=able, sp=self.sp, cnsm=cnsm,
            buy=u"#決定キーで購入" if _inventory.SP.is_buyable(self) else u"")
        unsealed_text = require if require_key else contents
        not_has_text = u"封印されている" if self.is_sealed else unsealed_text
        return has_text if _inventory.Items.has(
            self.number-1) else not_has_text

    @property
    def number(self):
        u"""番号取得。
        """
        return Equip.__collections.index(self)

    @property
    def image_number(self):
        u"""画像番号取得
        """
        return self.__image_number

    @property
    def icon(self):
        u"""画像番号からアイコン取得。
        """
        import material as __material
        return __material.icon.get(
            (self.__image_number & 0xF00) >> 8,
            (self.__image_number & 0x0F0) >> 4, self.__image_number & 0x00F)

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
        return self.__keys

    @property
    def is_weapon(self):
        u"""武器判定。
        """
        return isinstance(self, Weapon)

    @property
    def is_armor(self):
        u"""防具判定。
        """
        return isinstance(self, _Garment)

    @property
    def is_head(self):
        u"""頭防具判定。
        """
        return isinstance(self, Head)

    @property
    def is_body(self):
        u"""体防具判定。
        """
        return isinstance(self, Body)

    @property
    def is_accessory(self):
        u"""装飾品判定。
        """
        return isinstance(self, Accessory)

    @property
    def type(self):
        u"""アイテム種類番号を返す。
        0: 武器。1: 頭防具。2: 体防具。3: 装飾品。4: それ以外。
        """
        return (
            0 if self.is_weapon else 1 if self.is_head else
            2 if self.is_body else 3 if self.is_accessory else 4)

    @property
    def rank(self):
        u"""ランク取得。
        キーアイテム数で決定される。
        """
        return len(self.__keys)

    @property
    def additional(self):
        u"""パターン変更リクエストを取得。
        """
        return ()


class Weapon(Equip):
    u"""武器データ。
    """
    __slots__ = ()
    _CORRECTION = 0.1

    def get_special(self, level):
        u"""武器効果を取得。
        """
        if level and self._skill.target:
            new, old = self._skill.target.split("##")
            return new, old.split("#"), (
                (1, 1) if self._skill.is_single else (level, level+1))
        return ()


class _Garment(Equip):
    u"""防具データ。
    """
    __slots__ = ()


class Head(_Garment):
    u"""頭防具データ。
    """
    __slots__ = ()
    _CORRECTION = 0.025

    def get_sustain(self, turn):
        u"""頭防具効果を取得。
        """
        if self._skill.target:
            new, old = self._skill.target.split("##")
            if turn & self._skill.interval == 0:
                return new, old.split("#"), (1, 1)
        return ()


class Body(_Garment):
    u"""体防具データ。
    """
    __slots__ = ()
    _CORRECTION = 0.05

    def is_prevents(self, target):
        u"""ブロック変化防止の場合に真。
        """
        return target in tuple(
            self._skill.target.split("#") if self._skill else ())


class Accessory(_Garment):
    u"""装飾品データ。
    """
    __slots__ = ()
    _CORRECTION = 0.0125

    @property
    def additional(self):
        u"""パターン変更リクエストを取得。
        """
        if self._skill.target:
            new, old = self._skill.target.split("##")
            return self._skill.is_single, new, old
        return ()


class Skill(object):
    u"""スキルデータ。
    """
    __slots__ = "__interval", "__is_single", "__target",

    def __init__(self,  target="", interval=0b0, is_single=False):
        u"""コンストラクタ。
        """
        self.__target = target
        self.__interval = interval
        self.__is_single = is_single

    @property
    def target(self):
        u"""ターゲット文字列。
        """
        return self.__target

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


if __name__ == '__main__':
    import utils.const as __const
    MID_CORRECTION = 1.0
    Equip.set_collections((
        Equip(0x000, u"空#装備なし#何もない#", 0, 0),
        Weapon(
            0xB02, __const.SWORD_CATEGORY+u"#チキンナイフ#小さなナイフ#",
            10, MID_CORRECTION)))
    print Equip.get_by_name(u"チキンナイフ")
