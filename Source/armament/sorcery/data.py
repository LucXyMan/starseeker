#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""data.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

魔術データモジュール。
"""
import armament.collectible as __collectible
import effect as _effect
import utils.const as _const


class Sorcery(__collectible.Collectible):
    u"""魔術データ。
    """
    __slots__ = "_is_agrsv", "__magic_reaction"

    @classmethod
    def get_collections(cls):
        u"""コレクション取得。
        """
        return Sorcery.__collections[:]

    @classmethod
    def set_collections(cls, value):
        u"""コレクション設定。
        """
        Sorcery.__collections = tuple(value)

    @classmethod
    def get_collection(cls, key):
        u"""コレクション要素取得。
        """
        return Sorcery.__collections[key]

    def __init__(self, text, cost, is_agrsv, pile=None):
        u"""コンストラクタ。
        pile: 変化後魔術#反応魔術。
        """
        type_, self._name, self._description = text.split("##")
        self._type = type_ if type_ else _const.SORCERY_TYPE
        self._rank, self._star = cost
        self._is_agrsv = is_agrsv
        if pile:
            self.__magic_reaction = pile.recepter,  pile.Sorcery(
                pile.text, cost, *pile.args, **pile.kw)
        else:
            self.__magic_reaction = ()

    def __repr__(self):
        u"""文字列表現取得。
        """
        return unicode(u"<{name}: {type}, {elm}属性>".format(
            name=self._name, type=self._type,
            elm=_const.ELEMENTAL_TYPES[self._star]))

    def is_usable(self, prm_s, prm_o):
        u"""使用できるかどうか判定する。
        prm_s: 自身のパラメータ。
        prm_o: 相手のパラメータ。
        """
        return (
            _const.PURIFY_SKILL_NAME not in prm_s.skills.split("#") if
            self._type == _const.JOKER_TYPE else True) if (
                super(Sorcery, self).is_usable(prm_s, prm_o) and
            self._type != _const.SHIELD_TYPE) else False

    def adapt(self, target):
        u"""パイル可能な場合、パイル後魔術を返す。そうでない場合Noneを返す。
        """
        if self.__magic_reaction:
            recepter, sorcery = self.__magic_reaction
            if recepter == target.name:
                return sorcery
        return None

    @property
    def is_agrsv(self):
        u"""攻勢属性取得。
        """
        return self._is_agrsv

    @property
    def info(self):
        u"""情報の取得。
        """
        import inventory as __inventory
        star = [u"木", u"火", u"土", u"金", u"水", u"月", u"太陽"][self._star]
        elm_text = (
            u"/ランク{rank}/{star}属性".format(rank=self._rank, star=star) if
            self._type == _const.SORCERY_TYPE else
            u"/{star}シールド".format(star=star))
        return (
            u"{name}{elm}#{description}{pile}" .format(
                name=self._name, elm=elm_text, description=self._description,
                pile=u"#"+self.recepter+u"に反応" if self.recepter else u"")
        ) if __inventory.Cards.get(self.number) else u""

    @property
    def icons(self):
        u"""裏表無カードアイコン取得。
        """
        import material.icon as __icon
        color = 5 if self._type == _const.SORCERY_TYPE else 3
        return (
            __icon.get(2, 0, color), __icon.get(5, 0, color),
            __icon.get(0, 0, 0))

    @property
    def recepter(self):
        u"""魔法反応対象名取得。
        """
        if self.__magic_reaction:
            recepter, _ = self.__magic_reaction
            return recepter
        return ""


class Forming(Sorcery):
    u"""ブロックチェンジ魔術データ。
    """
    __slots__ = "__is_strictly", "__power", "__target"

    def __init__(
        self, text, cost, is_agrsv, power, target,
        is_strictly=False, magic_reaction=None
    ):
        u"""コンストラクタ。
        """
        super(Forming, self).__init__(text, cost, is_agrsv, magic_reaction)
        self.__power = power
        self.__target = target
        self.__is_strictly = is_strictly

    def is_usable(self, prm_s, prm_o):
        u"""使用できるかどうか判定する。
        """
        is_agrsv = (
            not self._is_agrsv if _const.REVERSE_SORCERY_SKILL_NAME in
            prm_s.skills.split("#") else self._is_agrsv)
        target = prm_o if is_agrsv else prm_s
        _, field = target.field
        _, old = self.__target.split("##")
        if self.__is_strictly:
            is_useable = bool(sum((tuple(
                name for name, _, _ in (block for _, block in field)
            ).count(block_name)) for block_name in old.split("#")))
        else:
            is_useable = target.field_one_eighth < sum((tuple(
                name for name, _, _ in (block for _, block in field)
            ).count(block_name)) for block_name in old.split("#"))
        return super(Forming, self).is_usable(prm_s, prm_o) and is_useable

    def get_effects(self, _is_exsit):
        u"""魔術効果取得。
        """
        power = self._rank*self.__power
        param = (
            (-1, -1) if self.__power == -1 else
            (1, 1) if self.__power == 0 else (power, power+1))
        return _effect.Forming(self.__target, param),


class Frozen(Forming):
    u"""凍結魔術データ。
    """
    __slots__ = "__is_all",

    def __init__(
        self, text, cost, is_agrsv, is_all, power, target,
        is_strictly=False, magic_reaction=None
    ):
        u"""コンストラクタ。
        """
        super(Frozen, self).__init__(
            text, cost, is_agrsv, power, target, is_strictly, magic_reaction)
        self.__is_all = is_all

    def is_usable(self, prm_s, prm_o):
        u"""使用できるかどうか判定する。
        """
        is_agrsv = (
            not self._is_agrsv if _const.REVERSE_SORCERY_SKILL_NAME in
            prm_s.skills.split("#") else self._is_agrsv)
        target = prm_o if is_agrsv else prm_s
        return (
            Sorcery.is_usable(self, prm_s, prm_o) and
            target.has_health if target.is_group_exsit else
            super(Frozen, self).is_usable(prm_s, prm_o))

    def get_effects(self, is_exsit):
        u"""魔術効果を取得。
        """
        return (
            (_effect.Frozen(self.__is_all),) if is_exsit else
            super(Frozen, self).get_effects(is_exsit))


class Poison(Forming):
    u"""毒魔術データ。
    """
    __slots__ = "__is_all",

    def __init__(
        self, text, cost, is_agrsv, is_all, power, target,
        is_strictly=False, magic_reaction=None
    ):
        u"""コンストラクタ。
        """
        super(Poison, self).__init__(
            text, cost, is_agrsv, power, target, is_strictly, magic_reaction)
        self.__is_all = is_all

    def is_usable(self, prm_s, prm_o):
        u"""使用できるかどうか判定する。
        アンデッド以外の健康なクリーチャーが存在する場合使用する。
        """
        has_reverse_magic = (
            _const.REVERSE_SORCERY_SKILL_NAME in prm_s.skills.split("#"))
        is_agrsv = not self._is_agrsv if has_reverse_magic else self._is_agrsv
        target = prm_o if is_agrsv else prm_s
        has_target_creature = (
            target.has_health if has_reverse_magic else target.has_normal)
        return (
            Sorcery.is_usable(self, prm_s, prm_o) and
            has_target_creature if target.is_group_exsit else
            super(Poison, self).is_usable(prm_s, prm_o))

    def get_effects(self, is_exsit):
        u"""魔術効果を取得。
        """
        return (
            (_effect.Poison(self.__is_all),) if is_exsit else
            super(Poison, self).get_effects(is_exsit))


class Recovery(Sorcery):
    u"""回復魔術データ。
    """
    __slots__ = "__is_all", "__rate",

    def __init__(
        self, text, cost, is_agrsv, is_all, rate, magic_reaction=None
    ):
        u"""コンストラクタ。
        """
        super(Recovery, self).__init__(text, cost, is_agrsv, magic_reaction)
        self.__is_all = is_all
        self.__rate = rate

    def is_usable(self, prm_s, prm_o):
        u"""使用できるかどうか判定する。
        """
        is_agrsv = (
            not self._is_agrsv if _const.REVERSE_SORCERY_SKILL_NAME in
            prm_s.skills.split("#") else self._is_agrsv)
        return (
            super(Recovery, self).is_usable(prm_s, prm_o) and
            (prm_o if is_agrsv else prm_s).has_damaged)

    def get_effects(self, _is_exsit):
        u"""回復効果を取得。
        """
        return _effect.Recovery(self.__rate, self.__is_all),


class Delete(Sorcery):
    u"""カード削除魔術データ。
    """
    __slots__ = "__is_all",

    def __init__(self, text, cost, is_agrsv, is_all, magic_reaction=None):
        u"""コンストラクタ。
        """
        super(Delete, self).__init__(text, cost, is_agrsv, magic_reaction)
        self.__is_all = is_all

    def is_usable(self, prm_s, prm_o):
        u"""使用できるかどうか判定する。
        """
        is_agrsv = (
            not self._is_agrsv if _const.REVERSE_SORCERY_SKILL_NAME in
            prm_s.skills.split("#") else self._is_agrsv)
        return (
            super(Delete, self).is_usable(prm_s, prm_o) and
            (prm_o if is_agrsv else prm_s).hand)

    def get_effects(self, _is_exsit):
        u"""魔術効果を取得。
        """
        return _effect.Delete(self.__is_all),


class Critical(Sorcery):
    u"""即死魔術データ。
    """
    __slots__ = "__is_all", "__is_force"

    def __init__(
        self, text, cost, is_agrsv, is_all, is_force, magic_reaction=None
    ):
        u"""コンストラクタ。
        """
        super(Critical, self).__init__(text, cost, is_agrsv, magic_reaction)
        self.__is_all = is_all
        self.__is_force = is_force

    def is_usable(self, prm_s, prm_o):
        u"""使用できるかどうか判定する。
        """
        is_agrsv = (
            not self._is_agrsv if _const.REVERSE_SORCERY_SKILL_NAME in
            prm_s.skills.split("#") else self._is_agrsv)
        return (
            super(Critical, self).is_usable(prm_s, prm_o) and
            (prm_o if is_agrsv else prm_s).has_normal)

    def get_effects(self, _is_exsit):
        u"""魔術効果を取得。
        """
        return _effect.Critical(self.__is_all, self.__is_force),


class Star(Sorcery):
    u"""スター変化魔術データ。
    """
    __slots__ = "__add", "__target"

    def __init__(self, text, cost, is_agrsv, add, magic_reaction=None):
        u"""コンストラクタ。
        """
        super(Star, self).__init__(text, cost, is_agrsv, magic_reaction)
        self.__target, self.__add = add

    def get_effects(self, _is_exsit):
        u"""魔術効果を取得。
        """
        return _effect.Star(self.__target, self.__add),


class Hold(Sorcery):
    u"""ホールド変化魔術データ。
    """
    __slots__ = "__is_single", "__target"

    def __init__(
        self, text, cost, is_agrsv, is_single, target, magic_reaction=None
    ):
        u"""コンストラクタ。
        """
        super(Hold, self).__init__(text, cost, is_agrsv, magic_reaction)
        self.__is_single = is_single
        self.__target = target

    def get_effects(self, _is_exsit):
        u"""魔術効果を取得。
        """
        return _effect.Hold(self.__is_single, self.__target),


class Unlock(Hold):
    u"""アンロック魔術データ。
    ホールド魔術データに判定を追加。
    """
    __slots__ = ()

    def is_usable(self, prm_s, prm_o):
        u"""使用できるかどうか判定する。
        """
        return (
            super(Unlock, self).is_usable(prm_s, prm_o) and
            (prm_s.hold_item_state & 0b0011) == 0b0011 and
            prm_s.has_locked_chest)


class Exchange(Sorcery):
    u"""ホールドピース変化魔術データ。
    """
    __slots__ = ()

    def __init__(self, text, cost, is_agrsv, magic_reaction=None):
        u"""コンストラクタ。
        """
        super(Exchange, self).__init__(text, cost, is_agrsv, magic_reaction)

    def is_usable(self, prm_s, prm_o):
        u"""使用できるかどうか判定する。
        """
        is_exist = (
            prm_s.hold_item_state & 0b0001 and
            prm_o.hold_item_state & 0b0001)
        is_use = 2 < (
            (not bool(prm_s.hold_item_state & 0b0100)) +
            bool(prm_s.hold_item_state & 0b1000) +
            bool(prm_o.hold_item_state & 0b0100) +
            (not bool(prm_o.hold_item_state & 0b1000))) if is_exist else False
        return super(Exchange, self).is_usable(prm_s, prm_o) and is_use

    def get_effects(self, _is_exsit):
        u"""魔術効果を取得。
        """
        return _effect.Exchange(False),


class Equip(Sorcery):
    u"""装備破壊魔術データ。
    """
    __slots__ = "__target",

    def __init__(self, text, cost, is_agrsv, target, magic_reaction=None):
        u"""コンストラクタ。
        """
        self.__target = int(target)
        super(Equip, self).__init__(text, cost, is_agrsv, magic_reaction)

    def is_usable(self, prm_s, prm_o):
        u"""使用できるかどうか判定する。
        """
        is_agrsv = (
            not self._is_agrsv if _const.REVERSE_SORCERY_SKILL_NAME in
            prm_s.skills.split("#") else self._is_agrsv)
        equip_broken_state = (
            prm_o if is_agrsv else prm_s).equip_broken_state
        is_use = bool((equip_broken_state ^ self.__target) & self.__target)
        return super(Equip, self).is_usable(prm_s, prm_o) and is_use

    def get_effects(self, _is_exsit):
        u"""魔術効果を取得。
        """
        return _effect.Equip(self.__target),


class MagicReaction(object):
    u"""魔法反応データ。
    """
    __slots__ = "_Sorcery", "__args", "__kw", "__recepter", "__text"

    def __init__(self, recepter, Sorcery, text, *args, **kw):
        u"""コンストラクタ。
        """
        self.__recepter = recepter
        self._Sorcery = Sorcery
        self.__text = text
        self.__args = args
        self.__kw = kw

    @property
    def recepter(self):
        u"""魔法反応対象名取得。
        """
        return self.__recepter

    @property
    def Sorcery(self):
        u"""魔術データクラス取得。
        """
        return self._Sorcery

    @property
    def text(self):
        u"""テキスト取得。
        """
        return _const.PILED_TYPE+"##"+self.__text

    @property
    def args(self):
        u"""引数取得。
        """
        return self.__args

    @property
    def kw(self):
        u"""キーワード引数取得。
        """
        return self.__kw


get = Sorcery.get_collection
get_all = Sorcery.get_collections
