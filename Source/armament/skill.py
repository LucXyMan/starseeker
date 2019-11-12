#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""skill.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

スキルデータモジュール。
"""
import inventories as _inventories
import utils.const as _const
_IMPOSSIBLE_CATEGORY = u"取得不可"
_UNACQUIRED_CATEGORY = u"未取得"
_ACQUIRED_CATEGORY = u"取得"
_BLOCK_CATEGORY = u"ブロック"
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
            name=self.name, levels=self.__levels-_inventories.Level.get_wins())

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
            __icon.get(0x000) if self.category == _IMPOSSIBLE_CATEGORY else
            __icon.get(0x100 | (
                6 if self.category == _BLOCK_CATEGORY else
                4 if self.category == _SORCERY_CATEGORY else
                5 if self.category == _STAR_CATEGORY else
                3 if self.category == _SPECIAL_CATEGORY else
                8 if self.category == _UNACQUIRED_CATEGORY else
                2)))

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
        return self.__levels <= _inventories.Level.get_wins()


def init():
    u"""スキルリスト作成。
    """
    _Skill.set_collections((
        _Skill(_IMPOSSIBLE_CATEGORY+u"##覚えられない", 0, 0),
        _Skill(_UNACQUIRED_CATEGORY+u"#未取得#覚えていない", 0, 0),
        _Skill(_ACQUIRED_CATEGORY+u"#取得#覚えている", 0, 0),
        _Skill(_BLOCK_CATEGORY+u"#"+_const.FIRE_EATER_SKILL, 1, 9),
        _Skill(_BLOCK_CATEGORY+u"#"+_const.ICE_PICKER_SKILL, 1, 10),
        _Skill(_BLOCK_CATEGORY+u"#"+_const.ACID_ERASER_SKILL, 1, 11),
        _Skill(_BLOCK_CATEGORY+u"#"+_const.STONE_BREAKER_SKILL, 1, 12),
        _Skill(_BLOCK_CATEGORY+u"#"+_const.POWER_STROKE_SKILL, 1, 13),
        _Skill(_BLOCK_CATEGORY+u"#"+_const.EXORCIST_SKILL, 2, 14),
        _Skill(_BLOCK_CATEGORY+u"#"+_const.PHANTOM_THIEF_SKILL, 6, 32),
        _Skill(_BLOCK_CATEGORY+u"#"+_const.WATER_PRESS_SKILL, 6, 31),
        _Skill(_BLOCK_CATEGORY+u"#"+_const.CHOCOLATE_PRESS_SKILL, 5, 30),
        _Skill(_BLOCK_CATEGORY+u"#"+_const.COMPLETE_ASSIST_SKILL, 8, 36),
        _Skill(_SORCERY_CATEGORY+u"#"+_const.PURIFY_SKILL, 5, 35),
        _Skill(_SORCERY_CATEGORY+u"#"+_const.DOUBLE_SPELL_SKILL, 1, 10),
        _Skill(_SORCERY_CATEGORY+u"#"+_const.VAMPIRE_SKILL, 6, 21),
        _Skill(_SORCERY_CATEGORY+u"#"+_const.ROB_CARD_SKILL, 5, 22),
        _Skill(_SORCERY_CATEGORY+u"#"+_const.SOUL_EAT_SKILL, 7, 33),
        _Skill(_SORCERY_CATEGORY+u"#"+_const.REVERSE_SORCERY_SKILL, 2, 10),
        _Skill(_SORCERY_CATEGORY+u"#"+_const.ANTI_SUMMONING_SKILL, 5, 34),
        _Skill(_SORCERY_CATEGORY+u"#"+_const.POISON_SUMMON_SKILL, 2, 22),
        _Skill(_SORCERY_CATEGORY+u"#"+_const.FORCE_JOKER_SKILL, 0, 0),
        _Skill(_STAR_CATEGORY+u"#"+_const.SHEPHERD_SKILL, 2, 14),
        _Skill(_STAR_CATEGORY+u"#"+_const.FALCONER_SKILL, 2, 15),
        _Skill(_STAR_CATEGORY+u"#"+_const.ALCHMIST_SKILL, 2, 16),
        _Skill(_STAR_CATEGORY+u"#"+_const.NECROMANCER_SKILL, 2, 14),
        _Skill(_STAR_CATEGORY+u"#"+_const.DRAGON_MASTER_SKILL, 2, 17),
        _Skill(_STAR_CATEGORY+u"#"+_const.HALF_JUPITER_SKILL, 3, 23),
        _Skill(_STAR_CATEGORY+u"#"+_const.HALF_MARS_SKILL, 3, 24),
        _Skill(_STAR_CATEGORY+u"#"+_const.HALF_SATURN_SKILL, 3, 25),
        _Skill(_STAR_CATEGORY+u"#"+_const.HALF_VENUS_SKILL, 3, 26),
        _Skill(_STAR_CATEGORY+u"#"+_const.HALF_MERCURY_SKILL, 3, 27),
        _Skill(_STAR_CATEGORY+u"#"+_const.MOON_CHILD_SKILL, 3, 28),
        _Skill(_STAR_CATEGORY+u"#"+_const.SON_OF_SUN_SKILL, 3, 29),
        _Skill(_SPECIAL_CATEGORY+u"#"+_const.SAFETY_SKILL, 2, 9),
        _Skill(_SPECIAL_CATEGORY+u"#"+_const.TALISMAN_SKILL, 1, 10),
        _Skill(_SPECIAL_CATEGORY+u"#"+_const.SHORT_TURN_SKILL, 5, 32),
        _Skill(_SPECIAL_CATEGORY+u"#"+_const.LIFE_BOOST_SKILL, 3, 18),
        _Skill(_SPECIAL_CATEGORY+u"#"+_const.MIGHTY_SKILL, 3, 19),
        _Skill(_SPECIAL_CATEGORY+u"#"+_const.TOUGHNESS_SKILL, 3, 20),
        _Skill(_SPECIAL_CATEGORY+u"#"+_const.SPEEDSTER_SKILL, 3, 21),
        _Skill(_SPECIAL_CATEGORY+u"#"+_const.SWORD_EQUIP_SKILL, 1, 1),
        _Skill(_SPECIAL_CATEGORY+u"#"+_const.WAND_EQUIP_SKILL, 1, 2),
        _Skill(_SPECIAL_CATEGORY+u"#"+_const.HEAVY_EQUIP_SKILL, 1, 3),
        _Skill(_SPECIAL_CATEGORY+u"#"+_const.MISSILE_EQUIP_SKILL, 1, 4),
        _Skill(_SPECIAL_CATEGORY+u"#"+_const.HAT_EQUIP_SKILL, 1, 5),
        _Skill(_SPECIAL_CATEGORY+u"#"+_const.HELMET_EQUIP_SKILL, 1, 6),
        _Skill(_SPECIAL_CATEGORY+u"#"+_const.ARMOR_EQUIP_SKILL, 1, 7),
        _Skill(_SPECIAL_CATEGORY+u"#"+_const.ROBE_EQUIP_SKILL, 1, 8)))
    if _const.IS_OUTPUT:
        for i, skill in enumerate(_Skill.get_collections()):
            print str(i)+":", unicode(skill)


get = _Skill.get_collection
get_all = _Skill.get_collections
get_by_name = _Skill.get_by_name
