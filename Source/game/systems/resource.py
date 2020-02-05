#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""resource.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ゲームリソースモジュール。
"""
import random as _random
import utils.const as _const


class Resource(object):
    u"""ゲームリソース。
    取得スター・シャード・カードを管理。
    """
    __slots__ = (
        "__cards", "__deck", "__equip", "__level_ups", "__shards", "__skills",
        "__stars")
    __STAR_LIMIT = _const.STAR_ENERGY*4

    def __init__(self, deck, stars=None, shards=None, cards=()):
        u"""リソース初期化。
        """
        self.__skills = ""
        self.__deck = tuple(deck)
        default_stars = [0]*_const.NUMBER_OF_STAR
        self.__stars = list(default_stars if stars is None else stars)
        self.__shards = list([0, 0, 0, 0] if shards is None else shards)
        self.__level_ups = list([0, 0, 0, 0] if shards is None else shards)
        self.__cards = list(cards)

    def __has_skill(self, skill):
        u"""スキル判定。
        """
        import utils.general as __general
        name = __general.get_skill_names(skill)
        return name in self.__skills.split("#")

    # ---- Star ----
    def increase(self, star, add, detect=None):
        u"""スター増加。
        """
        if star != -1:
            has_skill = self.__has_skill if detect is None else detect
            if (
                self.__STAR_LIMIT <= self.__stars[star] and
                has_skill(_const.CONVERT_RESOURCE_SKILL)
            ):
                min_star = self.__stars.index(min(self.__stars))
                if self.__stars[min_star] < self.__STAR_LIMIT:
                    self.increase(min_star, add)
            else:
                energy = self.__stars[star]+add
                is_excess = self.__STAR_LIMIT < energy
                energy = self.__STAR_LIMIT if is_excess else energy
                self.__stars[star] = energy

    def decrease(self, star, sub):
        u"""スター減少。
        """
        if star != -1:
            energy = self.__stars[star]-sub
            self.__stars[star] = 0 if energy < 0 else energy

    def disappear(self, number=1):
        u"""ランダムにスター減少。
        """
        is_disappear = False
        for _ in range(number):
            exsits = [i for i, star in enumerate(self.__stars) if star]
            if exsits:
                star = _random.choice(exsits)
                self.decrease(star, _const.STAR_ENERGY)
                is_disappear = True
            else:
                break
        return is_disappear

    def vanish(self):
        u"""全てのSPを0に。
        """
        self.__stars = [0]*_const.NUMBER_OF_STAR

    # ---- Extract ----
    def extract(self, one_piece, detect=None):
        u"""ピースからアイテムを取得。
        """
        def __extract_star():
            u"""ピースによるスター増加。
            """
            for block in one_piece:
                if 0 <= block.star_type < _const.NUMBER_OF_STAR:
                    add = _const.STAR_ENERGY << block.state
                    self.increase(block.star_type, add, detect=detect)

        def __extract_shard():
            u"""ピースによるシャード増加。
            """
            for i, plus in enumerate((sum(
                1 for block in one_piece if block.shard_type == type_
            ) for type_ in range(4))):
                self.__shards[i] += plus

        def __extract_card():
            u"""ピースからカード番号取得。
            """
            self.__cards.extend(
                block.state for block in one_piece if block.is_arcanum)

        def __excavate():
            u"""宝箱の中身を追加。
            """
            for i, got in enumerate((sum(
                1 for block in one_piece if block.treasure_rank == rank and
                block.is_opened) for rank in range(4)), 1
            ):
                plus = i << _const.STAR_ENERGY_SHIFT
                for _ in range(got):
                    self.__stars = map(
                        lambda x: x+plus if x+plus < self.__STAR_LIMIT else
                        self.__STAR_LIMIT, self.__stars)
                    self.__shards = map(lambda x: x+1*i, self.__shards)
                    self.__cards.extend(_random.sample(self.__deck, i))

        def __extract_level_up():
            u"""レベルアップ取得。
            """
            for i, plus in enumerate((sum(
                1 for block in one_piece if block.level_up_type == type_
            ) for type_ in range(4))):
                self.__level_ups[i] += plus

        def __addict():
            u"""毒取得によるスター減少。
            """
            has_skill = self.__has_skill if detect is None else detect
            poisons = sum(
                1 for block in one_piece if
                block.star_type == _const.NUMBER_OF_STAR)
            if 0 < poisons and not has_skill(_const.SAFETY_SKILL):
                self.disappear(poisons)
        __extract_star()
        __extract_shard()
        __extract_level_up()
        __extract_card()
        __excavate()
        __addict()

    # ---- Release ----
    def release_shard(self, type_):
        u"""シャード開放。
        """
        result = self.__shards[type_]
        self.__shards[type_] = 0
        return result

    def release_level_up(self, type_):
        u"""レベルアップ開放。
        """
        result = self.__level_ups[type_]
        self.__level_ups[type_] = 0
        return result

    def draw(self):
        u"""カードドロー。
        """
        result = self.__cards
        self.__cards = []
        return result

    # ---- Consumption ----
    def consume(self, arcanum):
        u"""arcanumのコストを消費する。
        """
        costs, _ = self.__get_costs(arcanum)
        for cost in costs:
            star, energy = cost
            if energy <= self.__stars[star]:
                self.decrease(star, energy)

    # ---- Getter ----
    def __get_costs(self, arcanum):
        u"""arcanumを使用する際のコストを取得。
        return: costs, division.
        """
        def __is_summon_half():
            u"""サモンコスト半減スキル判定。
            """
            return arcanum.type == _const.SUMMON_ARCANUM and any(
                arcanum.tribe == tribe and self.__has_skill(skill) for
                tribe, skill in (
                    (_const.BEAST_TRIBE, _const.SHEPHERD_SKILL),
                    (_const.SKY_TRIBE, _const.FALCONER_SKILL),
                    (_const.ALCHMIC_TRIBE, _const.ALCHMIST_SKILL),
                    (_const.UNDEAD_TRIBE, _const.NECROMANCER_SKILL),
                    (_const.DRAGON_TRIBE, _const.DRAGON_MASTER_SKILL)))

        def __is_arcana_half():
            u"""アルカナコスト半減スキル判定。
            """
            return any(
                arcanum.star == star and self.__has_skill(skill) for
                star, skill in enumerate((
                    _const.HALF_JUPITER_SKILL, _const.HALF_MARS_SKILL,
                    _const.HALF_SATURN_SKILL, _const.HALF_VENUS_SKILL,
                    _const.HALF_MERCURY_SKILL, _const.MOON_CHILD_SKILL,
                    _const.SON_OF_SUN_SKILL)))
        division = __is_summon_half()+__is_arcana_half()
        return arcanum.get_costs(division), division

    def get_available_state(self, arcanum):
        u"""arcanumの使用可能状態取得。
        return: コスト順序+スター種類+コスト分割。
        """
        costs, division = self.__get_costs(arcanum)
        for i, cost in enumerate(costs, 1):
            star, energy = cost
            if energy <= self.__stars[star]:
                return i+(star << 4)+(division << 8)
        return arcanum.star << 4

    # ---- Property ----
    @property
    def copy(self):
        u"""コピー取得。
        """
        resource = self.__class__(
            self.__deck[:], stars=self.__stars[:],
            shards=self.__shards[:], cards=self.__cards[:])
        resource.skills = self.__skills
        return resource

    @property
    def stars(self):
        u"""スター取得。
        """
        return tuple(self.__stars)

    @property
    def shards(self):
        u"""シャード取得。
        """
        return tuple(self.__shards)

    @property
    def level_ups(self):
        u"""レベルアップ取得。
        """
        return tuple(self.__level_ups)

    @property
    def total(self):
        u"""スター合計取得。
        """
        return sum(self.__stars) >> _const.STAR_ENERGY_SHIFT

    @property
    def skills(self):
        u"""スキル取得。
        """
        return self.__skills

    @skills.setter
    def skills(self, value):
        u"""スキル設定。
        """
        self.__skills = unicode(value)
