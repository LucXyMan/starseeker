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
    __slots__ = "_images", "_image_name", "__str", "_tribe", "__vit"

    def __init__(self, string, parametar):
        u"""コンストラクタ。
        string: 種類##種族##名前##概要。
        """
        self._type, self._tribe, self._name, self._description = (
            string.split("##"))
        self.__str, self.__vit = parametar

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
        self._image_name, tribe, name, description = string.split("##")
        basic, another = _unit.get(self._image_name)
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

    # ---- Property ----
    @property
    def image_type(self):
        u"""画像種類取得。
        """
        return self._image_name

    @property
    def notice(self):
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
                _const.HELMET_CATEGORY, _const.CROWN_CATEGORY,
                _const.CLOTHES_CATEGORY, _const.ARMOR_CATEGORY,
                _const.RING_CATEGORY)
        elif tribe == _const.WIZARD_ROLE:
            return (
                _const.WAND_CATEGORY, _const.HEAVY_CATEGORY,
                _const.HAT_CATEGORY, _const.CROWN_CATEGORY,
                _const.CLOTHES_CATEGORY, _const.ROBE_CATEGORY,
                _const.RING_CATEGORY)
        elif tribe == _const.SEEKER_ROLE:
            return (
                _const.SWORD_CATEGORY, _const.MISSILE_CATEGORY,
                _const.HAT_CATEGORY, _const.CROWN_CATEGORY,
                _const.CLOTHES_CATEGORY, _const.ROBE_CATEGORY,
                _const.RING_CATEGORY)
        elif tribe == _const.ROYAL_ROLE:
            return (
                _const.SWORD_CATEGORY, _const.WAND_CATEGORY,
                _const.HAT_CATEGORY, _const.CROWN_CATEGORY,
                _const.CLOTHES_CATEGORY, _const.ROBE_CATEGORY,
                _const.RING_CATEGORY)
        elif tribe == _const.MONSTER_ROLE:
            return (
                _const.SWORD_CATEGORY, _const.WAND_CATEGORY,
                _const.HEAVY_CATEGORY, _const.MISSILE_CATEGORY,
                _const.HAT_CATEGORY, _const.HELMET_CATEGORY,
                _const.CROWN_CATEGORY,
                _const.CLOTHES_CATEGORY, _const.ROBE_CATEGORY,
                _const.ARMOR_CATEGORY,
                _const.RING_CATEGORY)
        else:
            raise ValueError("No Role.")


class Summon(__Unit):
    u"""召喚データ。
    """
    __slots__ = "__ability", "__image", "__life", "__rank", "__receptors"
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
        ability=None, receptors=()
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
        type_, self._image_name, tribe, name, description = string.split("##")
        left = _unit.get(self._image_name)
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
        self.__receptors = receptors

    def __repr__(self):
        u"""文字列表現取得。
        """
        return unicode(u"<{name}: {type}, {tribe}族, {elm}属性>".format(
            name=self._name, type=self._type, tribe=self._tribe,
            elm=_const.STAR_CHARS[self._star]))

    def get_image(self, is_right):
        u"""画像取得。
        """
        return self._images[is_right]

    def is_available(self, params, skills=()):
        u"""使用できるかどうか判定する。
        """
        return (super(Summon, self).is_available((params[0], params[1])) and (
            not params[0].is_full_group or self._name in params[0].donors))

    # ---- Property ----
    @property
    def image_type(self):
        u"""画像種類取得。
        """
        type_, _ = self._image_name.split("_")
        return type_

    @property
    def notice(self):
        u"""情報取得。
        サモンカードを取得している場合に、情報文字列を返す。
        """
        import inventories as __inventories
        param_text = u"#"+u"ライフ:{life}/攻撃:{str}/防御:{vit}".format(
            life=self.__life, str=self.str, vit=self.vit)
        donor = tuple(receptors.donor for receptors in self.__receptors)
        fusion_text = u"#" + reduce(
            lambda x, y: x+u"・"+y, donor)+u"と融合" if donor else u""
        desc, sub_desc = self._description.split("#")
        sub_desc = sub_desc if sub_desc else u"特殊能力無し"
        notice = (
            u"{name}/ランク{rank}/{elm}属性/{tribe}{param}#{desc}/{sub_desc}"
            u"{fusion}".format(
                name=self._name, rank=self._rank,
                elm=_const.STAR_CHARS[self._star],
                tribe=self._tribe, param=param_text, fusion=fusion_text,
                desc=desc, sub_desc=sub_desc))
        return notice if __inventories.Card.get(self.number) else u""

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
    def donors(self):
        u"""受容可能クリーチャー名取得。
        """
        return tuple(recepter.donor for recepter in self.__receptors)

    def adapt(self, target):
        u"""融合可能な場合に融合後クリーチャーを返す。
        そうでない場合Noneを返す。
        """
        for receptor in self.__receptors:
            if receptor.donor == target.name:
                return receptor.get_summon(self)
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

    # ---- Property ----
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
        return (
            self.__target if self.__type == _const.PERSISTENCE_ABILITY else "")

    @property
    def prevention(self):
        u"""防止効果取得。
        """
        return (
            self.__target if self.__type == _const.PREVENTION_ABILITY else "")

    @property
    def skills(self):
        u"""スキル取得。
        """
        return reduce(
            lambda x, y: x+"#"+y, self.__target.split("##")
        ) if self.__type == _const.ADDITION_ABILITY else ""


class Receptor(object):
    u"""融合データ。
    """
    __slots__ = (
        "__ability", "__parameter", "__power", "__receptors", "__string")

    def __init__(
        self, string, parametar, power,
        ability=None, receptors=()
    ):
        u"""コンストラクタ。
        """
        self.__string = string
        self.__parameter = parametar
        self.__power = power
        self.__ability = ability
        self.__receptors = receptors

    def get_summon(self, summon):
        u"""召喚データ取得。
        """
        def __get_string(tribe):
            u"""文字列取得。
            """
            _, image, name, description = self.__string.split("##")
            return (
                _const.FUSIONED_ARCANUM+"##" +
                image+"##"+tribe+"##"+name+"##"+description)
        level = summon.rank+1, summon.star
        return Summon(
            __get_string(summon.tribe), self.__parameter, level,
            self.__power, self.__ability, self.__receptors)

    @property
    def donor(self):
        u"""取り込むクリーチャー名取得。
        """
        donor, _, _, _ = self.__string.split("##")
        return donor
