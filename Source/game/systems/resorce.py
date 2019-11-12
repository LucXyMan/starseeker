#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""resorce.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ゲームリソースモジュール。
"""
import random as _random
import utils.const as _const


class Resorce(object):
    u"""ゲームリソース。
    取得スター・シャード・カードを管理。
    """
    __slots__ = (
        "__cards", "__deck", "__equip", "__shards", "__skills", "__stars")
    __MAX_STAR = _const.STAR_ENERGY*99
    __NUMBER_OF_SHARD = 4

    def __init__(self, deck, stars=None, shards=None, cards=()):
        u"""リソース初期化。
        """
        self.__skills = ""
        self.__deck = tuple(deck)
        self.__stars = list(
            stars if stars is not None else
            [0]*_const.NUMBER_OF_STAR)
        self.__shards = list(
            shards if shards is not None else
            [0]*self.__NUMBER_OF_SHARD)
        self.__cards = list(cards)

    # ---- Star ----
    def inc_and_dec(self, type_, add):
        u"""スター増減。
        """
        value = self.__stars[type_]+(add << _const.STAR_ENERGY_SHIFT)
        self.__stars[type_] = (
            0 if value < 0 else self.__MAX_STAR if
            self.__MAX_STAR < value else value)

    def disappear(self):
        u"""ランダムにスター減少。
        """
        exsits = [i for i, star in enumerate(self.__stars) if star]
        if exsits:
            number = _random.choice(exsits)
            energy = self.__stars[number]-_const.STAR_ENERGY
            self.__stars[number] = 0 if energy < 0 else energy
            return True
        return False

    def vanishing(self):
        u"""全てのSPを0に。
        """
        self.__stars = [0]*_const.NUMBER_OF_STAR

    # ---- Extract ----
    def extract(self, one_piece):
        u"""ピースからアイテムを取得。
        """
        def __extract_star():
            u"""ピースによるスター増加。
            """
            for block in one_piece:
                if 0 < block.star_type:
                    type_ = block.star_type-1
                    energy = self.__stars[type_]+(
                        _const.STAR_ENERGY << block.state)
                    self.__stars[type_] = (
                        self.__MAX_STAR if self.__MAX_STAR < energy else
                        energy)

        def __extract_shard():
            u"""ピースによるシャード増加。
            """
            for i, plus in enumerate(tuple(sum(
                1 for block in one_piece if block.shard_type == type_
            ) for type_ in range(1, 5))):
                self.__shards[i] += plus

        def __extract_card():
            u"""ピースからカード番号を取得。
            """
            self.__cards.extend([
                block.state for block in one_piece if
                block.is_arcanum])

        def __excavate():
            u"""宝箱の中身を追加。
            """
            for i, got in enumerate((sum(
                1 for block in one_piece if block.treasure_rank == rank and
                block.is_opened) for rank in range(1, 5)), 1
            ):
                plus = i << _const.STAR_ENERGY_SHIFT
                for _ in range(got):
                    self.__stars = map(
                        lambda x: x+plus if x+plus < self.__MAX_STAR else
                        self.__MAX_STAR, self.__stars)
                    self.__shards = map(lambda x: x+1*i, self.__shards)
                    self.__cards.extend(_random.sample(self.__deck, i))

        def __addict():
            u"""毒取得によるスター減少。
            """
            name, _ = _const.SAFETY_SKILL.split("#")
            if name not in self.__skills.split("#"):
                for block in one_piece:
                    if block.star_type == -1:
                        self.disappear()
        __extract_star()
        __extract_shard()
        __extract_card()
        __excavate()
        __addict()

    # ---- Release ----
    def release(self, type_):
        u"""シャード開放。
        """
        result = self.__shards[type_]
        self.__shards[type_] = 0
        return result

    def draw(self):
        u"""カードドロー。
        """
        result = self.__cards
        self.__cards = []
        return result

    # ---- Consumption ----
    def __get_costs(self, target):
        u"""targetを使用する際のコストを取得。
        """
        def __get_name(skill):
            u"""スキル名取得。
            """
            name, _ = skill.split("#")
            return name

        def __is_creature_half():
            u"""クリーチャーのコスト半減スキル判定。
            """
            return target.type == _const.SUMMON_ARCANUM and any(
                target.tribe == tribe and __get_name(skill) in skills for
                tribe, skill in (
                    (_const.BEAST_TRIBE, _const.SHEPHERD_SKILL),
                    (_const.SKY_TRIBE, _const.FALCONER_SKILL),
                    (_const.ALCHMIC_TRIBE, _const.ALCHMIST_SKILL),
                    (_const.UNDEAD_TRIBE, _const.NECROMANCER_SKILL),
                    (_const.DRAGON_TRIBE, _const.DRAGON_MASTER_SKILL)))

        def __is_star_half():
            u"""スターのコスト半減スキル判定。
            """
            return any(
                target.star == star and __get_name(skill) in skills for
                star, skill in enumerate((
                    _const.HALF_JUPITER_SKILL, _const.HALF_MARS_SKILL,
                    _const.HALF_SATURN_SKILL, _const.HALF_VENUS_SKILL,
                    _const.HALF_MERCURY_SKILL, _const.MOON_CHILD_SKILL,
                    _const.SON_OF_SUN_SKILL)))
        skills = self.__skills.split("#")
        return target.get_costs(__is_creature_half()+__is_star_half())

    def get_available(self, target):
        u"""使用可能なコストと番号を返す。
        return: コスト番号、スター種類。
        使用不能の場合0、使用可能の場合costの番号+1とスター種類を返す。
        """
        for i, cost in enumerate(self.__get_costs(target)):
            for energy, elm in zip(self.__stars, cost):
                if energy < elm:
                    break
            else:
                return i+1, cost.index(max(cost))
        return 0, target.star

    def consumption(self, target):
        u"""targetのコストを消費する。
        """
        number, _ = self.get_available(target)
        if number:
            for n, star in enumerate(self.__get_costs(target)[number - 1]):
                self.__stars[n] -= star

    # ---- Property ----
    @property
    def copy(self):
        u"""コピー取得。
        """
        resorce = self.__class__(
            self.__deck[:], stars=self.__stars[:],
            shards=self.__shards[:], cards=self.__cards[:])
        resorce.skills = self.__skills
        return resorce

    @property
    def stars(self):
        u"""スター取得。
        """
        return tuple(self.__stars)

    @stars.setter
    def stars(self, value):
        u"""スター設定。
        """
        self.__stars = list(value)

    @property
    def shards(self):
        u"""シャード取得。
        """
        return tuple(self.__shards)

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
