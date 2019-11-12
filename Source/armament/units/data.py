#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""data.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ユニットデータモジュール。
"""
import pygame.transform as _transform
import armament.collectible as __collectible
import material.unit as _unit
import utils.const as _const


class __Unit(__collectible.Collectible):
    u"""ユニットデータ。
    """
    __slots__ = "_images", "__str", "_tribe", "__vit"
    __VIT_LIMIT = 100

    def __init__(self, string, parametar):
        u"""コンストラクタ。
        text: 画像##種類##種族##名前##概要。
        """
        self._type, self._tribe, self._name, self._description = \
            string.split("##")
        self.__str, vit = parametar
        limit = self.__VIT_LIMIT
        self.__vit = limit if limit < vit else vit

    @property
    def tribe(self):
        u"""種族取得。
        """
        return self._tribe

    @property
    def str(self):
        u"""ユニットの力を取得。
        """
        return self.__str

    @property
    def vit(self):
        u"""ユニットの硬さを取得。
        """
        return self.__vit

    @property
    def icons(self):
        u"""裏表無カードアイコン取得。
        """
        import material.icon as __icon
        return __icon.get(2, 0, 1), __icon.get(5, 0, 1), __icon.get(0, 0, 0),


class Player(__Unit):
    u"""プレイヤーデータ。
    """
    __slots__ = "__learnable",

    @classmethod
    def get_collections(cls):
        u"""コレクション取得。
        """
        return Player.__collections[:]

    @classmethod
    def set_collections(cls, value):
        u"""コレクション設定。
        """
        Player.__collections = tuple(value)

    @classmethod
    def get_collection(cls, key):
        u"""コレクション要素取得。
        """
        return Player.__collections[key]

    def __init__(self, image, string, parametar, learnable):
        u"""コンストラクタ。
        """
        import armament.skill as __skill
        type_, tribe, name, description = string.split("##")
        super(Player, self).__init__(
            (type_ if type_ else u"プレイヤー") +
            "##"+tribe+"##"+name+"##"+description, parametar)
        basic, another = _unit.get(image)
        self._images = (
            basic, _transform.flip(basic, True, False),
            another, _transform.flip(another, True, False))
        self.__learnable = __skill.get_by_name(*learnable)

    def __repr__(self):
        u"""文字列表現取得。
        """
        return unicode(u"<{name}: {type}, 職業:{role}>".format(
            name=self._name, type=self._type, role=self._tribe))

    def get_image(self, is_right, is_another):
        u"""画像取得。
        """
        return self._images[is_right+(is_another << 1)]

    @property
    def info(self):
        u"""情報取得。
        """
        return self.name+u"/"+self._description

    @property
    def learnable(self):
        u"""習得可能スキル取得。
        """
        return self.__learnable

    @property
    def equippable(self):
        u"""装備可能カテゴリ取得。
        """
        tribe = self._tribe
        if tribe == _const.WARRIOR_ROLE:
            return (
                _const.SWORD_CATEGORY, _const.HEAVY_CATEGORY,
                _const.HELMET_CATEGORY,
                _const.CLOTHES_CATEGORY, _const.ARMOR_CATEGORY,
                _const.RING_CATEGORY)
        elif tribe == _const.WIZARD_ROLE:
            return (
                _const.WAND_CATEGORY, _const.HEAVY_CATEGORY,
                _const.HAT_CATEGORY,
                _const.CLOTHES_CATEGORY, _const.ROBE_CATEGORY,
                _const.RING_CATEGORY)
        elif tribe == _const.SEEKER_ROLE:
            return (
                _const.SWORD_CATEGORY, _const.MISSILE_CATEGORY,
                _const.HAT_CATEGORY,
                _const.CLOTHES_CATEGORY, _const.ROBE_CATEGORY,
                _const.RING_CATEGORY)
        elif tribe == _const.ROYAL_ROLE:
            return (
                _const.SWORD_CATEGORY, _const.WAND_CATEGORY,
                _const.HAT_CATEGORY,
                _const.CLOTHES_CATEGORY, _const.ROBE_CATEGORY,
                _const.RING_CATEGORY)
        elif tribe == _const.MONSTER_ROLE:
            return (
                _const.SWORD_CATEGORY, _const.WAND_CATEGORY,
                _const.HEAVY_CATEGORY, _const.MISSILE_CATEGORY,
                _const.HAT_CATEGORY, _const.HELMET_CATEGORY,
                _const.CLOTHES_CATEGORY, _const.ROBE_CATEGORY,
                _const.ARMOR_CATEGORY, _const.RING_CATEGORY)
        else:
            raise ValueError("No Role.")


class Summon(__Unit):
    u"""召喚データ。
    """
    __slots__ = "__fusions", "__life", "__rank", "__skill"
    __STR_STAIR = 10
    __VIT_STAIR = 5

    @classmethod
    def get_collections(cls):
        u"""コレクション取得。
        """
        return Summon.__collections[:]

    @classmethod
    def set_collections(cls, value):
        u"""コレクション設定。
        """
        Summon.__collections = tuple(value)

    @classmethod
    def get_collection(cls, key):
        u"""コレクション要素取得。
        """
        return Summon.__collections[key]

    def __init__(
        self, image, string, parametar, cost, power, skill=None, fusions=()
    ):
        u"""コンストラクタ。
        """
        def __get_power(power, rank):
            u"""基本パワー取得。
            """
            return __get_power(power, rank-1)+(
                power >> rank-1) if 0 < rank-1 else power

        def __get_cost(param, stair):
            u"""パラメータコスト取得。
            """
            div, mod = divmod(param, stair)
            return reduce(
                lambda x, y: x+y, (i*stair for i in range(1, div+1))
            )+(div+1)*mod if 0 < div else mod
        type_, tribe, name, description = string.split("##")
        super(Summon, self).__init__(
            (type_ if type_ else _const.SUMMON_TYPE) +
            "##"+tribe+"##"+name+"##"+description, parametar)
        left = _unit.get(image)
        self._images = left, _transform.flip(left, True, False)
        self._rank, self._star = cost
        self.__life = __get_power(power, self._rank)-(
            __get_cost(self.str, self.__STR_STAIR) +
            __get_cost(self.vit, self.__VIT_STAIR))
        if self.__life <= 0:
            raise ValueError(u"{creature} Is LIFE:0.".format(creature=self))
        self.__skill = skill
        self.__fusions = tuple((fusion.recepter,  self.__class__(
            fusion.image, fusion.get_text(self._tribe), fusion.parameter,
            (self._rank+1, self._star), fusion.power, fusion.skill,
            fusion.fusions)) for fusion in fusions)

    def __repr__(self):
        u"""文字列表現取得。
        """
        return unicode(u"<{name}: {type}, {tribe}族, {elm}属性>".format(
            name=self._name, type=self._type, tribe=self._tribe,
            elm=_const.ELEMENTAL_TYPES[self._star]))

    def get_image(self, is_right):
        u"""画像取得。
        """
        return self._images[is_right]

    def is_usable(self, parameters, rival, skills=()):
        u"""使用できるかどうか判定する。
        """
        return (super(Summon, self).is_usable(parameters, rival) and (
            not parameters.is_full_group or self._name in parameters.recepters)
        )

    @property
    def info(self):
        u"""情報取得。
        サモンカードを取得している場合に、情報文字列を返す。
        """
        import inventory as __inventory
        param_text = u"#"+u"ライフ:{life}/攻撃:{str}/防御:{vit}".format(
                life=self.__life, str=self.str, vit=self.vit)
        fusion = tuple(recepter for recepter, _ in self.__fusions)
        fusion_text = u"#" + reduce(
            lambda x, y: x+u"・"+y, fusion)+u"と融合" if any(fusion) else u""
        desc, sub_desc = self._description.split("#")
        sub_desc = sub_desc if sub_desc else u"特殊能力無し"
        info_text = (
            u"{name}/ランク{rank}/{elm}属性/{tribe}{param}#{desc}/{sub_desc}"
            u"{fusion}".format(
                name=self._name, rank=self._rank,
                elm=(u"木", u"火", u"土", u"金", u"水", u"月", u"太陽")[self._star],
                tribe=self._tribe, param=param_text, fusion=fusion_text,
                desc=desc, sub_desc=sub_desc))
        return info_text if __inventory.Cards.get(self.number) else u""

    @property
    def rank(self):
        u"""ランク取得。
        """
        return self._rank

    @property
    def star(self):
        u"""スター属性取得。
        """
        return self._star

    @property
    def life(self):
        u"""ライフ取得。
        """
        return self.__life

    @property
    def recepters(self):
        u"""受容可能クリーチャー名取得。
        """
        return tuple(recepter for recepter, _ in self.__fusions)

    def adapt(self, target):
        u"""融合可能な場合に融合後クリーチャーを返す。
        そうでない場合Noneを返す。
        """
        for fusion in self.__fusions:
            recepter, creature = fusion
            if recepter == target.name:
                return creature
        return None

    @property
    def skill(self):
        u"""スキル情報取得。
        """
        return self.__skill


class Skill(object):
    u"""クリーチャースキルデータ。
    """
    __slots__ = "__is_single", "__sustain", "__target", "__type"

    def __init__(self, target="", type_="", sustain=0b0, is_single=False):
        u"""コンストラクタ。
        target: ターゲット文字列。new##old1#old2#... or prevent1#prevent2#...
        """
        self.__target = target
        self.__type = type_
        self.__sustain = sustain
        self.__is_single = is_single

    @property
    def target(self):
        u"""アビリティ対象取得。
        """
        return self.__target

    @property
    def type(self):
        u"""アビリティ種類取得。
        Attack: 相手フィールド変化。
        Defense: 自フィールド変化防止。
        Sustain: 自フィールド持続変化。
        """
        return self.__type

    @property
    def sustain(self):
        u"""持続効果間隔取得。
        """
        return self.__sustain

    @property
    def is_single(self):
        u"""攻撃アビリティ対象取得。
        """
        return self.__is_single


class Fusion(object):
    u"""融合データ。
    """
    __slots__ = (
        "__fusions", "__image", "__parameter", "__power", "__recepter",
        "__skill", "__string")

    def __init__(
            self, recepter, image, string, parametar, power,
            skill=None, fusions=()
    ):
        u"""コンストラクタ。
        """
        self.__recepter = recepter
        self.__image = image
        self.__string = string
        self.__parameter = parametar
        self.__power = power
        self.__skill = skill
        self.__fusions = fusions

    def get_text(self, tribe):
        u"""クリーチャー文字列取得。
        """
        return _const.FUSIONED_TYPE+"##"+tribe+"##"+self.__string

    @property
    def image(self):
        u"""画像文字列取得。
        """
        return self.__image

    @property
    def fusions(self):
        u"""融合データ取得。
        """
        return self.__fusions

    @property
    def skill(self):
        u"""スキルデータ取得。
        """
        return self.__skill

    @property
    def recepter(self):
        u"""融合対象名取得。
        """
        return self.__recepter

    @property
    def parameter(self):
        u"""パラメータ取得。
        """
        return self.__parameter

    @property
    def power(self):
        u"""パワー取得。
        """
        return self.__power
