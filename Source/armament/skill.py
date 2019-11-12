#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""skill.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

スキルデータモジュール。
"""
import inventory as _inventory
import utils.const as _const
_IMPOSSIBLE_CATEGORY = u"取得不可"
_UNACQUIRED_CATEGORY = u"未取得"
_ACQUIRED_CATEGORY = u"取得"
_ACTION_CATEGORY = u"アクション"
_SORCERY_CATEGORY = u"ソーサリー"
_STAR_CATEGORY = u"スター"
_SPECIAL_CATEGORY = u"スペシャル"


class _Skill(object):
    u"""スキルデータ。
    """
    __slots__ = "__levels",  "__slot", "__string"
    __SKILL_OFFSET = 3

    @classmethod
    def get_collections(cls):
        u"""コレクション取得。
        """
        return _Skill.__collections[_Skill.__SKILL_OFFSET:]

    @classmethod
    def set_collections(cls, value):
        u"""コレクション設定。
        """
        _Skill.__collections = tuple(value)

    @classmethod
    def get_collection(cls, key):
        u"""コレクション要素取得。
        """
        return _Skill.__collections[_Skill.__SKILL_OFFSET+key]

    @classmethod
    def get_by_name(cls, *names):
        u"""スキル名による番号取得。
        """
        result = []
        for name in names:
            for skill in _Skill.get_collections():
                if name == skill.name:
                    break
            else:
                raise ValueError("Name not found.")
            result.append(skill.number)
        return tuple(result)

    def __init__(self, string, slot, levels):
        u"""コンストラクタ。
        __string: スキル種類と名前を合わせた文字列。
        __slot: スキルを装備する時の消費コスト。
        __levels: このスキルを覚えるのに必要なレベル。
        """
        self.__string = string
        if _const.NAME_LIMIT < len(self.name):
            raise ValueError(u"name too long")
        self.__slot = slot
        self.__levels = levels

    def __repr__(self):
        u"""文字列表現取得。
        """
        return (
            u"<{name}: {category}, number={number}, slot={slot}>").format(
                name=self.name, category=self.category, number=self.number,
                slot=self.slot)

    def get_info(self):
        u"""情報の取得。
        """
        return u"{name}/SLOT:{slot}#{desc}{end}".format(
            name=self.name, slot=self.__slot, desc=self.desc,
            end=u"#決定キーで装備・解除" if self.is_equippable else u""
        ) if self.is_equippable else u"{name}/取得まで★:{levels}必要".format(
            name=self.name, levels=self.__levels-_inventory.Level.get_wins())

    @property
    def number(self):
        u"""番号取得。
        """
        return _Skill.__collections[_Skill.__SKILL_OFFSET:].index(self)

    @property
    def icon(self):
        u"""アイコン取得。
        """
        import material.icon as __icon
        return (
            __icon.get(0, 0, 0) if self.category == _IMPOSSIBLE_CATEGORY else
            __icon.get(1, 0, (
                6 if self.category == _ACTION_CATEGORY else
                4 if self.category == _SORCERY_CATEGORY else
                5 if self.category == _STAR_CATEGORY else
                3 if self.category == _SPECIAL_CATEGORY else
                8 if self.category == _UNACQUIRED_CATEGORY else 2)))

    @property
    def category(self):
        u"""カテゴリ取得。
        """
        category, _, _ = self.__string.split("#")
        return category

    @property
    def name(self):
        u"""名前取得。
        """
        _, name, _ = self.__string.split("#")
        return name

    @property
    def desc(self):
        u"""概要取得。
        """
        _, _, desc = self.__string.split("#")
        return desc

    @property
    def slot(self):
        u"""消費スロット取得。
        """
        return self.__slot

    @property
    def levels(self):
        u"""必要レベル取得。
        """
        return self.__levels

    @property
    def is_equippable(self):
        u"""装備可能判定。
        """
        return self.__levels <= _inventory.Level.get_wins()


def init():
    u"""スキルリスト作成。
    """
    _Skill.set_collections((
        _Skill(_IMPOSSIBLE_CATEGORY+u"##覚えられない", 0, 0),
        _Skill(_UNACQUIRED_CATEGORY+u"#未取得#覚えていない", 0, 0),
        _Skill(_ACQUIRED_CATEGORY+u"#取得#覚えている", 0, 0),
        _Skill(
            _ACTION_CATEGORY+u"#"+_const.FIRE_EATER_SKILL_NAME +
            u"#マグマを破壊する", 1, 9),
        _Skill(
            _ACTION_CATEGORY+u"#"+_const.ICE_PICKER_SKILL_NAME +
            u"#アイスを破壊する", 1, 9),
        _Skill(
            _ACTION_CATEGORY+u"#"+_const.ACID_ERASER_SKILL_NAME +
            u"#アシッドを破壊する", 1, 9),
        _Skill(
            _ACTION_CATEGORY+u"#"+_const.STONE_BREAKER_SKILL_NAME +
            u"#ストーンを破壊する", 1, 20),
        _Skill(
            _ACTION_CATEGORY+u"#"+_const.POWER_STROKE_SKILL_NAME +
            u"#硬いブロックを一撃で破壊する", 3, 19),
        _Skill(
            _ACTION_CATEGORY+u"#"+_const.EXORCIST_SKILL_NAME +
            u"#デーモン・ゴーストを除去する", 2, 19),
        _Skill(
            _ACTION_CATEGORY+u"#"+_const.PHANTOM_THIEF_SKILL_NAME +
            u"#宝箱をカギ無しで開ける", 4, 29),
        _Skill(
            _ACTION_CATEGORY+u"#"+_const.VAMPIRE_SKILL_NAME +
            u"#直接攻撃で相手のスターを吸収する", 6, 20),
        _Skill(
            _ACTION_CATEGORY+u"#"+_const.ROB_CARD_SKILL_NAME +
            u"#直接攻撃で相手のカードを強奪する", 3, 20),
        _Skill(
            _ACTION_CATEGORY+u"#"+_const.COMPLETE_ASSIST_SKILL_NAME +
            u"#ライン補完に必要なブロック-1",
            8, 31),
        _Skill(
            _SORCERY_CATEGORY+u"#"+_const.PURIFY_SKILL_NAME +
            u"#ジョーカーを削除できる", 5, 30),
        _Skill(
            _SORCERY_CATEGORY+u"#"+_const.DOUBLE_SPELL_SKILL_NAME +
            u"#連続でサモン・ソーサリーを使用できる", 1, 10),
        _Skill(
            _SORCERY_CATEGORY+u"#"+_const.SOUL_EAT_SKILL_NAME +
            u"#カード削除時にスター増加", 7, 29),
        _Skill(
            _SORCERY_CATEGORY+u"#"+_const.REVERSE_SORCERY_SKILL_NAME +
            u"#ソーサリー効果逆転", 2, 10),
        _Skill(
            _SORCERY_CATEGORY+u"#"+_const.ANTI_SUMMONING_SKILL_NAME +
            u"#シールドカードに召喚封印効果追加", 4, 28),
        _Skill(
            _STAR_CATEGORY+u"#"+_const.SHEPHERD_SKILL_NAME +
            u"#"+_const.BEAST_TRIBE+u"クリーチャーコスト減少", 2, 11),
        _Skill(
            _STAR_CATEGORY+u"#"+_const.FALCONER_SKILL_NAME +
            u"#"+_const.SKY_TRIBE+u"クリーチャーコスト減少", 2, 12),
        _Skill(
            _STAR_CATEGORY+u"#"+_const.ALCHMIST_SKILL_NAME +
            u"#"+_const.ALCHMIC_TRIBE+u"クリーチャーコスト減少", 2, 13),
        _Skill(
            _STAR_CATEGORY+u"#"+_const.NECROMANCER_SKILL_NAME +
            u"#"+_const.UNDEAD_TRIBE+u"クリーチャーコスト減少", 2, 14),
        _Skill(
            _STAR_CATEGORY+u"#"+_const.DRAGON_MASTER_SKILL_NAME+u"#" +
            _const.DRAGON_TRIBE+u"クリーチャーコスト減少/敵専用", 0, 0),
        _Skill(
            _STAR_CATEGORY+u"#"+_const.HALF_JUPITER_SKILL_NAME +
            u"#木スターコスト減少", 3, 21),
        _Skill(
            _STAR_CATEGORY+u"#"+_const.HALF_MARS_SKILL_NAME +
            u"#火スターコスト減少", 3, 22),
        _Skill(
            _STAR_CATEGORY+u"#"+_const.HALF_SATURN_SKILL_NAME +
            u"#土スターコスト減少", 3, 23),
        _Skill(
            _STAR_CATEGORY+u"#"+_const.HALF_VENUS_SKILL_NAME +
            u"#金スターコスト減少", 3, 24),
        _Skill(
            _STAR_CATEGORY+u"#"+_const.HALF_MERCURY_SKILL_NAME +
            u"#水スターコスト減少", 3, 25),
        _Skill(
            _STAR_CATEGORY+u"#"+_const.MOON_CHILD_SKILL_NAME +
            u"#月スターコスト減少", 3, 26),
        _Skill(
            _STAR_CATEGORY+u"#"+_const.SON_OF_SUN_SKILL_NAME +
            u"#太陽スターコスト減少", 3, 27),
        _Skill(
            _STAR_CATEGORY+u"#"+_const.DARK_FORCE_SKILL_NAME +
            u"#初期月スター追加+ブラックドラゴン追加/敵専用", 0, 0),
        _Skill(
            _SPECIAL_CATEGORY+u"#"+_const.SAFETY_SKILL_NAME +
            u"#スター減少効果防止", 2, 9),
        _Skill(
            _SPECIAL_CATEGORY+u"#"+_const.LIFE_BOOST_SKILL_NAME +
            u"#生命の欠片効果倍増", 3, 15),
        _Skill(
            _SPECIAL_CATEGORY+u"#"+_const.MIGHTY_SKILL_NAME +
            u"#力の欠片効果倍増", 3, 16),
        _Skill(
            _SPECIAL_CATEGORY+u"#"+_const.TOUGHNESS_SKILL_NAME +
            u"#守りの欠片効果倍増", 3, 17),
        _Skill(
            _SPECIAL_CATEGORY+u"#"+_const.SPEEDSTER_SKILL_NAME +
            u"#速さの欠片効果倍増", 3, 18),
        _Skill(
            _SPECIAL_CATEGORY+u"#"+_const.SWORD_EQUIP_SKILL_NAME +
            u"#"+_const.SWORD_CATEGORY+u"装備可能", 1, 1),
        _Skill(
            _SPECIAL_CATEGORY+u"#"+_const.WAND_EQUIP_SKILL_NAME +
            u"#"+_const.WAND_CATEGORY+u"装備可能", 1, 2),
        _Skill(
            _SPECIAL_CATEGORY+u"#"+_const.HEAVY_EQUIP_SKILL_NAME +
            u"#"+_const.HEAVY_CATEGORY+u"装備可能", 1, 3),
        _Skill(
            _SPECIAL_CATEGORY+u"#"+_const.MISSILE_EQUIP_SKILL_NAME +
            u"#"+_const.MISSILE_CATEGORY+u"装備可能", 1, 4),
        _Skill(
            _SPECIAL_CATEGORY+u"#"+_const.HAT_EQUIP_SKILL_NAME +
            u"#"+_const.HAT_CATEGORY+u"装備可能", 1, 5),
        _Skill(
            _SPECIAL_CATEGORY+u"#"+_const.HELMET_EQUIP_SKILL_NAME +
            u"#"+_const.HELMET_CATEGORY+u"装備可能", 1, 6),
        _Skill(
            _SPECIAL_CATEGORY+u"#"+_const.ARMOR_EQUIP_SKILL_NAME +
            u"#"+_const.ARMOR_CATEGORY+u"装備可能", 1, 7),
        _Skill(
            _SPECIAL_CATEGORY+u"#"+_const.ROBE_EQUIP_SKILL_NAME +
            u"#"+_const.ROBE_CATEGORY+u"装備可能", 1, 8)))
    if _const.IS_OUTPUT:
        for i, skill in enumerate(_Skill.get_collections()):
            print str(i)+":", unicode(skill)


get = _Skill.get_collection
get_all = _Skill.get_collections
get_by_name = _Skill.get_by_name
