#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""special.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

特殊効果モジュール。
"""
import armament.collectible as __collectible
import utils.const as _const


class Special(__collectible.Collectible):
    u"""特殊効果。
    """
    __slots__ = ()

    @classmethod
    def get_collections(cls):
        u"""コレクション取得。
        """
        return Special.__collections[:]

    @classmethod
    def set_collections(cls, value):
        u"""コレクション設定。
        """
        Special.__collections = tuple(value)

    @classmethod
    def get_collection(cls, key):
        u"""コレクション要素取得。
        """
        return Special.__collections[key]

    def __init__(self, string, cost):
        u"""コンストラクタ。
        """
        self._type, self._name, self._description = string.split("##")
        self._rank, self._star = cost

    def __repr__(self):
        u"""文字列表現取得。
        """
        return unicode(u"<{name}: {type}, {elm}属性>".format(
            name=self._name, type=self._type,
            elm=_const.STAR_CHARS[self._star]))

    def adapt(self, target):
        u"""魔法反応可能な場合に反応後ソーサリーを返す。
        そうでない場合Noneを返す。
        """
        return None

    @property
    def notice(self):
        u"""情報取得。
        """
        import inventories as __inventories
        star = _const.STAR_CHARS[self._star]
        have_got = __inventories.Card.get(self.number)
        if self._type == _const.SUPPORT_ARCANUM:
            return u"{name}/{description}{subscript}".format(
                name=self._name, description=self._description,
                subscript=u"/"+self.subscript if self.subscript else u""
            ) if have_got else u""
        else:
            rank_and_star = (
                u"/ランク{rank}/{star}属性".format(rank=self._rank, star=star) if
                self._type == _const.SORCERY_ARCANUM else
                u"/{star}シールド".format(star=star))
            magic_reaction = (
                u"#{recepter}に反応".format(recepter=self.recepter) if
                self.recepter else u"")
            return (
                u"{name}{rank_and_star}#{description}{magic_reaction}" .format(
                    name=self._name, rank_and_star=rank_and_star,
                    description=self._description,
                    magic_reaction=magic_reaction)) if have_got else u""

    @property
    def icons(self):
        u"""カードアイコン取得。
        """
        import material.icon as __icon
        color = (
            5 if self._type == _const.SORCERY_ARCANUM else
            7 if self._type == _const.SUPPORT_ARCANUM else
            3)
        return (
            __icon.get(0x200 | color), __icon.get(0x500 | color),
            __icon.get(0x000))


set_ = Special.set_collections
get = Special.get_collections
