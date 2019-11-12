#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""level.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

レベルモジュール。
"""
import random as __random
import inventories as __inventories
import utils.const as _const
__REWARD_SP = 20
__selected_2p = 0
__versus_level = 0
__deck = ()
__equip = ()


class Level(object):
    u"""レベルデータ。
    """
    __slots__ = "_deck", "_equip", "_player", "_skill"

    def __init__(self, equip, skill, deck):
        u"""コンストラクタ。
        """
        self._equip = equip
        if 4 < len(self._equip):
            raise ValueError("Exceed the limit of equip.")
        self._skill = skill
        self._deck = deck
        if _const.DECK_CAPACITY < len(self._deck):
            raise ValueError("Exceed the limit of deck.")

    # ---- Property ----
    @property
    def player(self):
        u"""プレイヤー番号・レベル取得。
        return: number, rank
        """
        return self._player

    @property
    def equip(self):
        u"""装備の取得。
        """
        return self._equip

    @property
    def skill(self):
        u"""スキルの取得。
        """
        return self._skill

    @property
    def deck(self):
        u"""デッキの取得。
        """
        return self._deck


class _General(Level):
    u"""汎用レベルデータ。
    """
    __slots__ = ()

    def __init__(self, equip, skill, deck, player):
        u"""コンストラクタ。
        """
        self._player = player
        super(_General, self).__init__(equip, skill, deck)

    def __repr__(self):
        u"""文字列表現取得。
        """
        player, _ = self._player
        return (
            u"<プレイヤー番号:{player}, 装備番号:{equip}, "
            u"スキル番号:{skill}, デッキ番号:{deck}>".format(
                player=player, equip=self._equip,
                skill=self._skill, deck=self._deck))

    # ---- Property ----
    @property
    def player(self):
        u"""プレイヤー番号・ランク取得。
        return: number, rank
        """
        if not hasattr(self, "_player"):
            self._player = divmod(
                self.number, _const.PLEYERS+1)[::-1]
        return self._player

    @property
    def rewards(self):
        u"""特典カード取得。
        """
        return self.__rewards

    @property
    def is_playable(self):
        u"""対戦可能な場合に真。
        """
        return True


# ---- Get Level ----
def get_1p(rank):
    u"""1Pレベル取得。
    """
    return _General(
        __inventories.Equip.get_all(), __inventories.Skill.get_equiped(),
        __inventories.Deck.get_all(), (__inventories.Utils.get_player(), rank))


def get_2p():
    u"""2Pレベル取得。
    """
    old = __inventories.Utils.get_player()
    set_player = __inventories.Utils.set_player
    set_player(get_selected_2p())
    result = _General(
        __inventories.Equip.get_all(),
        __inventories.Skill.get_equiped(),
        __inventories.Deck.get_all(),
        (__inventories.Utils.get_player(), __versus_level))
    set_player(old)
    return result


def get_endless():
    u"""エンドレスレベル取得。
    呼び出しの時にエンドレス進行状況とデッキを設定する。
    """
    import armament.units as __units

    def _get_skills():
        u"""エンドレススキル取得。
        """
        def __get_skills(player):
            u"""プレイヤーとスロットによってスキル取得。
            """
            import armament.skill as __skill
            learnable = (
                __skill.get(learn) for
                learn in __units.get_player(player).learnable)
            return [
                skill for skill in learnable if
                skill.slot <= capacity and skill not in result]
        result = []
        capacity = int(
            float(progress)/float(_const.ENDLESS_LIMIT) *
            float(_const.SKILL_CAPACITY))
        skills = __get_skills(player)
        while 0 < capacity and skills:
            skill = skills.pop(__random.randint(0, len(skills)-1))
            result.append(skill)
            capacity -= skill.slot
            skills = __get_skills(player)
        return tuple(result)

    def _get_deck():
        u"""エンドレスデッキ取得。
        """
        def __get_deck():
            u"""種類とランクによってデッキ取得。
            """
            import armament.collectible as __collectible
            return tuple(
                collection for collection in __collectible.get_all() if
                collection.rank <= progress/(_const.ENDLESS_LIMIT >> 2)+1 and
                collection.type in (
                    _const.SUMMON_ARCANUM, _const.SORCERY_ARCANUM,
                    _const.SHIELD_ARCANUM, _const.SUPPORT_ARCANUM))
        result = []
        slot = progress/10*4+4
        slot = slot if slot < _const.DECK_CAPACITY else _const.DECK_CAPACITY
        deck = __get_deck()
        limit = 3
        while 0 < slot and deck:
            card = __random.choice(deck)
            number = __random.randint(0, limit if limit < slot else slot)
            result.extend((card,)*number)
            slot -= number
            deck = tuple(card for card in __get_deck() if card not in result)
        return tuple(result)

    def _get_equip():
        u"""エンドレス装備取得。
        """
        def __get_equip():
            u"""SPと種類によって装備取得。
            """
            import armament.equips as __equips
            upper = progress*__REWARD_SP
            lower = upper >> 1
            equippable = (
                __units.get_player(player).equippable +
                __inventories.Skill.add_equippable(skills))
            return tuple(
                item for item in __equips.get_all() if
                item.number != 0 and lower <= item.sp <= upper and
                item.category in equippable and item.category in categorys)
        result = []
        for categorys in (
            _const.WEAPON_CATEGORYS, _const.HEAD_CATEGORYS,
            _const.BODY_CATEGORYS, _const.ACCESSORY_CATEGORYS
        ):
            equip = __get_equip()
            result.append(__random.choice(equip).number if equip else 0)
        return tuple(result)
    global __deck, __equip
    progress = __inventories.Utils.get_endless()+1
    progress = progress if progress < _const.ENDLESS_LIMIT else \
        _const.ENDLESS_LIMIT
    __inventories.Utils.set_endless(progress)
    is_boss_battle = _const.ENDLESS_LIMIT <= progress
    player = __random.randint(
        0, _const.PLEYERS if is_boss_battle else _const.PLEYERS-1)
    skills = _get_skills()
    __equip = _get_equip()
    __deck = tuple(card.number for card in _get_deck())
    rank = progress/10
    rank_limit = 3
    return _General(
        __equip, tuple(skill.number for skill in skills), __deck,
        (player, rank_limit if rank_limit < rank else rank))


# ---- Reward ----
def get_reward():
    u"""褒賞アイテムを取得。
    """
    result = tuple(item for item in __equip if item != 0)
    if result:
        return __random.choice(result)
    return 0


def get_deck():
    u"""エンドレスデッキ取得。
    """
    return __deck


# ---- State ----
def get_versus_level():
    u"""ヴァーサスレベル状態取得。
    """
    return __versus_level


def set_versus_level(value):
    u"""ヴァーサスレベル状態設定。
    """
    global __versus_level
    __versus_level = int(value)


def get_selected_2p():
    u"""2P選択状態取得。
    """
    return __selected_2p


def set_selected_2p(value):
    u"""2P選択状態設定。
    """
    global __selected_2p
    __selected_2p = int(value)
