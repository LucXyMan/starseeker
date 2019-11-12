#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""resorce.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ゲームリソースモジュール。
"""
import utils.const as _const


class Resorce(object):
    u"""ゲームリソース。
    取得スター・シャード・カードを管理。
    """
    __slots__ = "__arcana", "__equip", "__shards", "__skills", "__stars"
    __STAR_NUMBER = 7
    __SHARD_NUMBER = 4
    __ENERGY_MAX = 99*_const.STAR_ENERGY

    def __init__(self, skills, stars=None, shards=None, arcana=()):
        u"""リソース初期化。
        """
        self.__skills = skills
        self.__stars = stars if stars is not None else [0]*self.__STAR_NUMBER
        self.__shards = (
            shards if shards is not None else [0]*self.__SHARD_NUMBER)
        self.__arcana = arcana

    def init_stars(self):
        u"""スターポイント初期化。
        """
        self.__stars = [0]*self.__STAR_NUMBER

    @property
    def copy(self):
        u"""コピー取得。
        """
        return self.__class__(
            self.__skills[:], self.__stars[:],
            self.__shards[:], self.__arcana[:])

    def add_star(self, type_, add):
        u"""スター増減。
        type_が-1の場合、全スター増減。
        """
        if type_ == -1:
            for i in range(self.__STAR_NUMBER):
                value = self.__stars[i]+(add << _const.STAR_ENERGY_SHIFT)
                self.__stars[i] = (
                    0 if value < 0 else self.__ENERGY_MAX if
                    self.__ENERGY_MAX < value else value)
        else:
            value = self.__stars[type_]+(add << _const.STAR_ENERGY_SHIFT)
            self.__stars[type_] = (
                    0 if value < 0 else self.__ENERGY_MAX if
                    self.__ENERGY_MAX < value else value)

    def star_plus(self, one_piece):
        u"""ピースによるスター増加。
        """
        for block in one_piece:
            if block.star_type not in (-1, 0):
                type_ = block.star_type-1
                energy = self.__stars[type_]+(
                    _const.STAR_ENERGY << block.state)
                self.__stars[type_] = (
                    self.__ENERGY_MAX if self.__ENERGY_MAX < energy else
                    energy)

    def star_minus(self, one_piece, is_certainly=True):
        u"""毒取得によるスター減少。
        is_certainlyが真の場合、存在するスターを選んで必ず減少させる。
        """
        import random as __random
        if _const.SAFETY_SKILL_NAME not in self.__skills.split("#"):
            for block in one_piece:
                if block.star_type == -1:
                    exsit = tuple(
                        i for i, star in enumerate(self.__stars) if star)
                    if exsit:
                        number = (
                            __random.choice(exsit) if is_certainly else
                            __random.randint(0, 6))
                        energy = self.__stars[number]-_const.STAR_ENERGY
                        self.__stars[number] = 0 if energy < 0 else energy

    def shard_plus(self, one_piece):
        u"""ピースによるシャード増加。
        """
        for i, plus in enumerate(tuple(sum(
            1 for block in one_piece if block.shard_type == type_) for
            type_ in range(1, 5))
        ):
            self.__shards[i] += plus

    def shard_release(self, type_):
        u"""シャード開放。
        ユニットに設定する。
        """
        result = self.__shards[type_]
        self.__shards[type_] = 0
        return result

    def chests_plus(self, one_piece):
        u"""宝箱の中身を追加。
        """
        for i, got in enumerate(tuple(sum(
            1 for block in one_piece if block.treasure_rank == rank and
            block.is_opened) for rank in range(1, 5)), 1
        ):
            plus = i << _const.STAR_ENERGY_SHIFT
            for _ in range(got):
                self.__stars = map(
                    lambda x: x+plus if x+plus < self.__ENERGY_MAX else
                    self.__ENERGY_MAX, self.__stars)
                self.__shards = map(lambda x: x+1*i, self.__shards)

    def get_arcana(self, one_piece):
        u"""ピースからカード番号を取得。
        """
        self.__arcana += tuple(
            block.state for block in one_piece if block.is_arcanum)

    def __get_costs(self, item):
        u"""itemを使用する際のコストを取得。
        """
        def __is_creature_half():
            u"""クリーチャーのコスト半減スキル判定。
            """
            if item.type == _const.SUMMON_TYPE:
                return ((
                    item.tribe == _const.BEAST_TRIBE and
                    _const.SHEPHERD_SKILL_NAME in skills) or
                    (item.tribe == _const.SKY_TRIBE and
                     _const.FALCONER_SKILL_NAME in skills) or
                    (item.tribe == _const.ALCHMIC_TRIBE and
                     _const.ALCHMIST_SKILL_NAME in skills) or
                    (item.tribe == _const.UNDEAD_TRIBE and
                     _const.NECROMANCER_SKILL_NAME in skills) or
                    (item.tribe == _const.DRAGON_TRIBE and
                     _const.DRAGON_MASTER_SKILL_NAME in skills))
            return False

        def __is_star_half():
            u"""スターのコスト半減スキル判定。
            """
            return (
                (item.star == 0 and
                 _const.HALF_JUPITER_SKILL_NAME in skills) or
                (item.star == 1 and _const.HALF_MARS_SKILL_NAME in skills) or
                (item.star == 2 and _const.HALF_SATURN_SKILL_NAME in skills) or
                (item.star == 3 and _const.HALF_VENUS_SKILL_NAME in skills) or
                (item.star == 4 and
                 _const.HALF_MERCURY_SKILL_NAME in skills) or
                (item.star == 5 and _const.MOON_CHILD_SKILL_NAME in skills) or
                (item.star == 6 and _const.SON_OF_SUN_SKILL_NAME in skills))
        skills = self.__skills.split("#")
        return item.get_costs(
            (1 if __is_creature_half() else 0)+(1 if __is_star_half() else 0))

    def get_available(self, item):
        u"""使用可能なコストと番号を返す。
        return: コスト番号、スター種類。
        使用不能の場合0、使用可能の場合costの番号+1とスター種類を返す。
        """
        for i, cost in enumerate(self.__get_costs(item)):
            for energy, elm in zip(self.__stars, cost):
                if energy < elm:
                    break
            else:
                return i+1, cost.index(max(cost))
        return 0, item.star

    def consumption(self, target):
        u"""targetのコストを消費する。
        """
        number, _ = self.get_available(target)
        if number:
            for n, star in enumerate(self.__get_costs(target)[number - 1]):
                self.__stars[n] -= star

    def get_cards(self):
        u"""取得したカード番号を返して番号を削除。
        """
        result = self.__arcana
        self.__arcana = ()
        return result

    @property
    def stars(self):
        u"""スター取得。
        """
        return self.__stars[:]

    @stars.setter
    def stars(self, value):
        u"""スター設定。
        """
        self.__stars = value

    @property
    def shards(self):
        u"""シャード取得。
        """
        return self.__shards[:]

    @property
    def total(self):
        u"""スター合計取得。
        """
        return sum(self.__stars) >> _const.STAR_ENERGY_SHIFT
