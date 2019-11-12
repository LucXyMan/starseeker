#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""data.py

Copyright (c) 2019 Yukio Kuro
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
        string: 画像##種類##種族##名前##概要。
        """
        self._type, self._tribe, self._name, self._description = \
            string.split("##")
        self.__str, vit = parametar
        self.__vit = self.__VIT_LIMIT if self.__VIT_LIMIT < vit else vit

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
        return __icon.get(0x201), __icon.get(0x501), __icon.get(0x000)


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

    def __init__(self, string, parametar, learnable):
        u"""コンストラクタ。
        """
        import armament.skill as __skill
        image, tribe, name, description = string.split("##")
        basic, another = _unit.get(image)
        super(Player, self).__init__(
            u"プレイヤー##"+tribe+u"##"+name+u"##"+description, parametar)
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
    __slots__ = "__ability", "__fusions", "__life", "__rank"
    __STR_COST = 10
    __VIT_COST = 5

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
        self, string, parametar, cost, power,
        ability=None, fusions=()
    ):
        u"""コンストラクタ。
        """
        def __get_power(power, rank):
            u"""基本パワー取得。
            """
            return __get_power(power, rank-1)+(
                power >> rank-1) if 0 < rank-1 else power

        def __get_cost(param, cost):
            u"""パラメータコスト取得。
            """
            div, mod = divmod(param, cost)
            return reduce(
                lambda x, y: x+y, (i*cost for i in range(1, div+1))
            )+(div+1)*mod if 0 < div else mod
        type_, image, tribe, name, description = string.split("##")
        left = _unit.get(image)
        self._images = left, _transform.flip(left, True, False)
        super(Summon, self).__init__(
            (type_ if type_ else _const.SUMMON_ARCANUM) +
            "##"+tribe+"##"+name+"##" + description, parametar)
        self._rank, self._star = cost
        self.__life = __get_power(power, self._rank)-(
            __get_cost(self.str, self.__STR_COST) +
            __get_cost(self.vit, self.__VIT_COST))
        if self.__life <= 0:
            raise ValueError(u"{creature} Is LIFE:0.".format(creature=self))
        self.__ability = ability
        self.__fusions = tuple((fusion.recepter,  self.__class__(
            fusion.get_string(self._tribe), fusion.parameter,
            (self._rank+1, self._star), fusion.power, fusion.ability,
            fusion.fusions)) for fusion in fusions)

    def __repr__(self):
        u"""文字列表現取得。
        """
        return unicode(u"<{name}: {type}, {tribe}族, {elm}属性>".format(
            name=self._name, type=self._type, tribe=self._tribe,
            elm=_const.STAR_TYPES[self._star]))

    def get_image(self, is_right):
        u"""画像取得。
        """
        return self._images[is_right]

    def is_usable(self, params, skills=()):
        u"""使用できるかどうか判定する。
        """
        return (super(Summon, self).is_usable((params[0], params[1])) and (
            not params[0].is_full_group or self._name in params[0].recepters))

    @property
    def info(self):
        u"""情報取得。
        サモンカードを取得している場合に、情報文字列を返す。
        """
        import inventories as __inventories
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
        return info_text if __inventories.Card.get(self.number) else u""

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
    def ability(self):
        u"""アビリティ情報取得。
        """
        return self.__ability


class Ability(object):
    u"""クリーチャーアビリティデータ。
    """
    __slots__ = "__interval", "__is_single", "__target", "__type"

    def __init__(self, string, interval=0b0, is_single=False):
        u"""コンストラクタ。
        """
        self.__type,  self.__target = string.split("###")
        self.__interval = int(interval)
        self.__is_single = bool(is_single)

    @property
    def type(self):
        u"""アビリティ種類取得。
        Enchant: 相手フィールド変化。
        Persistence: 自フィールド持続変化。
        Prevention: 自フィールド変化防止。
        Append: スキル追加。
        """
        return self.__type

    @property
    def is_single(self):
        u"""エンチャント対象取得。
        """
        return self.__is_single

    @property
    def interval(self):
        u"""持続効果間隔取得。
        """
        return self.__interval

    @property
    def enchant(self):
        u"""エンチャント取得。
        """
        return self.__target if self.__type == _const.ENCHANT_ABILITY else ""

    @property
    def persistence(self):
        u"""持続効果取得。
        """
        return self.__target if self.__type == \
            _const.PERSISTENCE_ABILITY else ""

    @property
    def prevention(self):
        u"""防止効果取得。
        """
        return self.__target if self.__type == \
            _const.PREVENTION_ABILITY else ""

    @property
    def skills(self):
        u"""スキル取得。
        """
        return reduce(
            lambda x, y: x+"#"+y, self.__target.split("##")
        ) if self.__type == _const.ADDITION_ABILITY else ""


class Fusion(object):
    u"""融合データ。
    """
    __slots__ = (
        "__fusions", "__image", "__parameter", "__power", "__recepter",
        "__ability", "__string")

    def __init__(
        self, string, parametar, power,
        ability=None, fusions=()
    ):
        u"""コンストラクタ。
        """
        self.__string = string
        self.__parameter = parametar
        self.__power = power
        self.__ability = ability
        self.__fusions = fusions

    def get_string(self, tribe):
        u"""文字列取得。
        """
        _, image, name, description = self.__string.split("##")
        return (
            _const.FUSIONED_ARCANUM+"##"+image+"##" +
            tribe+"##"+name+"##"+description)

    @property
    def recepter(self):
        u"""融合対象名取得。
        """
        recepter, _, _, _ = self.__string.split("##")
        return recepter

    @property
    def fusions(self):
        u"""融合データ取得。
        """
        return self.__fusions

    @property
    def ability(self):
        u"""アビリティデータ取得。
        """
        return self.__ability

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
