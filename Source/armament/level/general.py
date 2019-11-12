#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""general.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

汎用レベルモジュール。
"""
import random as __random
import inventory as __inventory
import utils.const as _const
__REWARD_SP = 20
__selected_2p = 0
__versus_level = 0
__deck = ()
__equips = ()


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
        return u"<プレイヤー番号:{0}, 装備番号:{1}, スキル番号:{2}, デッキ番号:{3}>".format(
            self._player[0], self._equip, self._skill, self._deck)

    @property
    def player(self):
        u"""プレイヤー番号・ランク取得。
        return: number, rank
        """
        if not hasattr(self, "_player"):
            self._player = divmod(self.number, _const.PLAYER_NUMBER+1)[::-1]
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
            return (
                skill for skill in (
                    __skill.get(learn) for
                    learn in __units.get_player(player).learnable) if
                skill.slot <= slot)
        slot = int(
            float(progress)/float(_const.ENDLESS_LIMIT) *
            float(_const.SKILL_CAPACITY))
        result = []
        choices = list(__get_skills(player))
        while 0 < slot and choices:
            skill = choices.pop(__random.randint(0, len(choices)-1))
            result.append(skill)
            slot -= skill.slot
            choices = [
                skill for skill in __get_skills(player) if skill not in result]
        return tuple(result)

    def _get_deck():
        u"""エンドレスデッキ取得。
        """
        def __get_deck():
            u"""種類とランクによってデッキ取得。
            """
            import armament.collectible as __collectible
            return (collection for collection in (
                _collection for _collection in __collectible.get_all() if
                _collection.type in (
                    _const.SUMMON_TYPE, _const.SORCERY_TYPE,
                    _const.SHIELD_TYPE)) if collection.rank <=
                    progress/(_const.ENDLESS_LIMIT >> 2)+1)
        result = []
        slot = progress/10*4+4
        _slot = slot if slot < _const.DECK_CAPACITY else _const.DECK_CAPACITY
        choices = [card for card in __get_deck()]
        limit = 3
        while 0 < _slot and choices:
            card = __random.choice(choices)
            number = __random.randint(0, limit if limit < _slot else _slot)
            result.extend((card,)*number)
            _slot -= number
            choices = [card for card in __get_deck() if card not in result]
        return result

    def _get_equip():
        u"""エンドレス装備取得。
        """
        def __get_equip(progress):
            u"""SPと種類によって装備取得。
            """
            import armament.equip as __equip
            return (
                equip for equip in (
                    equip for equip in __equip.get_all() if equip.sp <=
                    progress*__REWARD_SP
                ) if equip.category in (
                    caegory for caegory in __units.get_player(
                        player).equippable+__inventory.Skill.add_equippable(
                            skills) if caegory in _caegorys))
        result = []
        for _caegorys in (
            _const.WEAPON_CATEGORYS, _const.HEAD_CATEGORYS,
            _const.BODY_CATEGORYS, _const.ACCESSORY_CATEGORYS
        ):
            equips = tuple(
                equip for equip in __get_equip(progress) if equip.number != 0)
            result.append(__random.choice(equips).number if equips else 0)
        return tuple(result)
    global __deck, __equips
    progress = __inventory.Utils.get_endless()+1
    progress = (
        progress if progress < _const.ENDLESS_LIMIT else
        _const.ENDLESS_LIMIT)
    __inventory.Utils.set_endless(progress)
    player = __random.randint(
        0, _const.PLAYER_NUMBER-1 if progress < _const.ENDLESS_LIMIT else
        _const.PLAYER_NUMBER)
    skills = _get_skills()
    __equips = _get_equip()
    __deck = tuple(card.number for card in _get_deck())
    rank = progress/10
    return _General(
        __equips, tuple(skill.number for skill in skills), __deck,
        (player, _const.RANK_LIMIT if _const.RANK_LIMIT < rank else rank))


def get_reward():
    u"""褒賞アイテムを取得。
    """
    result = tuple(equip for equip in __equips if equip != 0)
    if result:
        return __random.choice(result)
    return 0


def get_deck():
    u"""エンドレスデッキ取得。
    """
    return __deck


def get_1p(rank):
    u"""1Pレベル取得。
    """
    return _General(
        __inventory.Equip.get_all(), __inventory.Skill.get_equiped(),
        __inventory.Deck.get_all(), (__inventory.Utils.get_player(), rank))


def get_versus_level():
    u"""ヴァーサスレベル番号取得。
    """
    return __versus_level


def set_versus_level(value):
    u"""ヴァーサスレベル番号設定。
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


def get_2p():
    u"""2Pレベル取得。
    """
    old = __inventory.Utils.get_player()
    set_player = __inventory.Utils.set_player
    set_player(get_selected_2p())
    result = _General(
        __inventory.Equip.get_all(),
        __inventory.Skill.get_equiped(),
        __inventory.Deck.get_all(),
        (__inventory.Utils.get_player(), __versus_level))
    set_player(old)
    return result
