#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""hand.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

手札モジュール。
"""
import utils.const as _const
import utils.layouter as _layouter


class Hand(object):
    u"""手札管理。
    """
    __slots__ = "__cards", "__core", "__removed"

    def __init__(self, core):
        u"""コンストラクタ。
        """
        self.__core = core
        self.__cards = []
        self.__removed = []

    def __getitem__(self, key):
        u"""カード取得。
        """
        return self.__cards[key]

    def __iter__(self):
        u"""イテレータ取得。
        """
        return iter(self.__cards)

    def __len__(self):
        u"""長さ取得。
        """
        return len(self.__cards)

    def __nonzero__(self):
            u"""1枚でもカードが存在する場合に真。
            """
            return bool(self.__cards)

    # ---- Operation ----
    def draw(self, *numbers):
        u"""手札にカードを追加。
        anucana: アルカナ番号のタプル。
        """
        import card as __card
        import armament.collectible as __collectible
        for number in numbers:
            if len(self.jokers) < _const.NUMBER_OF_HAND:
                arcanum = __collectible.get(number)
                cards = {
                    _const.SUMMON_ARCANUM: __card.Summon,
                    _const.SORCERY_ARCANUM: __card.Sorcery,
                    _const.SHIELD_ARCANUM: __card.Shield,
                    _const.SUPPORT_ARCANUM: __card.Support,
                    _const.JOKER_ARCANUM: __card.Joker}
                Card = cards[arcanum.type]
                self.__cards.append(Card(self, arcanum))
                _layouter.Game.set_hand(self.__core)
                if _const.NUMBER_OF_HAND < len(self.__cards):
                    for card in self.__cards[:]:
                        if not card.arcanum.type == _const.JOKER_ARCANUM:
                            self.remove(card)
                            break
        self.__core.update()

    def shuffle(self):
        u"""カード回転処理。
        """
        if (
            1 < len(self.__cards) and
            all(not card.is_moving for card in self.__cards)
        ):
            import material.sound as __sound
            __sound.SE.play("shuffle")
            self.__cards = self.__cards[1:]+self.__cards[:1]
            _layouter.Game.set_hand(self.__core, True)

    # ---- Remove ----
    def remove(self, card):
        u"""カード削除。
        """
        card.burn()
        self.__cards.remove(card)
        self.__removed.append(card)
        self.__removed = [card for card in self.__removed if card.alive()]
        _layouter.Game.set_hand(self.__core, True)

    # ---- Detection ----
    def burn(self, skill):
        u"""スキル所持対象を焼却。
        """
        import utils.general as __general
        name = __general.get_skill_names(skill)
        for card in self.__cards:
            if name in card.arcanum.skills.split("#"):
                self.remove(card)
                return True
        return False

    # ---- Update ----
    def update(self):
        u"""カード表示設定。
        """
        for card in self.__cards:
            card.set_state(self.__core)

    # ---- Property ----
    @property
    def by_number(self):
        u"""番号による手札取得。
        """
        return tuple(card.arcanum.number for card in self.__cards)

    @property
    def skills(self):
        u"""カードスキル取得。
        """
        skills = tuple(
            card.arcanum.skills for card in self.__cards if
            card.arcanum.skills)
        return reduce(lambda x, y: x+"#"+y, skills) if skills else ""

    @property
    def jokers(self):
        u"""ジョーカー取得。
        """
        return tuple(
            card for card in self.__cards if
            card.arcanum.type == _const.JOKER_ARCANUM)

    @property
    def is_remaining(self):
        u"""カード残存判定。
        削除されたカードが残っている場合に真。
        """
        return any(card.alive() for card in self.__removed)
