#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""parameter.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

パラメータモジュール。
"""
import utils.const as _const


class Parameter(object):
    u"""パラメータ。
    AIに受け渡す各種パラメータを格納する。
    """
    __slots__ = (
        "__catalyst", "__equip_broken_state", "__field", "__field_one_eighth",
        "__hand", "__has_damaged", "__has_health", "__has_alone_chest",
        "__has_normal", "__hold", "__hold_item_state", "__is_full_group",
        "__is_group_exsit", "__is_hold_captured", "__is_sorcery_usable",
        "__jokers", "__piece", "__piece_pos", "__recepters", "__resorce",
        "__skills")

    # ---- System ----
    @property
    def resorce(self):
        u"""リソース取得。
        """
        return self.__resorce

    @resorce.setter
    def resorce(self, value):
        u"""リソース設定。
        """
        self.__resorce = value

    # ---- Skill ----
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

    @property
    def has_phantom_thief(self):
        u"""ファントムシーフスキル判定。
        """
        name, _ = _const.PHANTOM_THIEF_SKILL.split("#")
        return name in self.__skills.split("#")

    @property
    def has_soul_eat(self):
        u"""ソウルイートスキル判定。
        """
        name, _ = _const.SOUL_EAT_SKILL.split("#")
        return name in self.__skills.split("#")

    @property
    def has_reverse_sorcery(self):
        u"""魔術逆転スキル判定。
        """
        name, _ = _const.REVERSE_SORCERY_SKILL.split("#")
        return name in self.__skills.split("#")

    @property
    def has_purify(self):
        u"""ジョーカー削除スキル判定。
        """
        name, _ = _const.PURIFY_SKILL.split("#")
        return name in self.__skills.split("#")

    @property
    def has_talisman(self):
        u"""タリスマンスキル判定。
        """
        name, _ = _const.TALISMAN_SKILL.split("#")
        return name in self.__skills.split("#")

    # ---- Equip ----
    @property
    def equip_broken_state(self):
        u"""装備破壊状態取得。
        """
        return self.__equip_broken_state

    @equip_broken_state.setter
    def equip_broken_state(self, value):
        u"""装備破壊状態設定。
        """
        self.__equip_broken_state = int(value)

    # ---- Field ----
    @property
    def field(self):
        u"""フィールド取得。
        """
        return self.__field

    @field.setter
    def field(self, value):
        u"""フィールド設定。
        """
        self.__field = tuple(value)

    @property
    def field_one_eighth(self):
        u"""1/8フィールドサイズ取得。
        """
        return self.__field_one_eighth

    @field_one_eighth.setter
    def field_one_eighth(self, value):
        u"""1/8フィールドサイズ設定。
        """
        self.__field_one_eighth = int(value)

    @property
    def has_alone_chest(self):
        u"""ペア無し宝箱状態取得。
        """
        return self.__has_alone_chest

    @has_alone_chest.setter
    def has_alone_chest(self, value):
        u"""ペア無し宝箱状態設定。
        """
        self.__has_alone_chest = bool(value)

    # ---- Piece ----
    @property
    def piece(self):
        u"""ピースパラメータ取得。
        """
        return self.__piece

    @piece.setter
    def piece(self, value):
        u"""ピースパラメータ設定。
        """
        self.__piece = tuple(value)

    @property
    def piece_pos(self):
        u"""ピース位置取得。
        """
        return self.__piece_pos

    @piece_pos.setter
    def piece_pos(self, value):
        u"""ピース位置設定。
        """
        self.__piece_pos = tuple(value)

    # ---- Hold ----
    @property
    def hold(self):
        u"""ホールドパラメータ取得。
        """
        return self.__hold

    @hold.setter
    def hold(self, value):
        u"""ホールドパラメータ設定。
        """
        self.__hold = value

    @property
    def is_hold_captured(self):
        u"""ホールドキャプチャ状態取得。
        """
        return self.__is_hold_captured

    @is_hold_captured.setter
    def is_hold_captured(self, value):
        u"""ホールドキャプチャ状態設定。
        """
        self.__is_hold_captured = bool(value)

    @property
    def hold_item_state(self):
        u"""ホールドのアイテム状態取得。
        """
        return self.__hold_item_state

    @hold_item_state.setter
    def hold_item_state(self, value):
        u"""ホールドのアイテム状態設定。
        """
        self.__hold_item_state = int(value)

    # ---- Arcana ----
    @property
    def hand(self):
        u"""手札番号取得。
        """
        return self.__hand

    @hand.setter
    def hand(self, value):
        u"""手札番号設定。
        """
        self.__hand = tuple(value)

    @property
    def catalyst(self):
        u"""触媒番号取得。
        """
        return self.__catalyst

    @catalyst.setter
    def catalyst(self, value):
        u"""触媒番号設定。
        """
        self.__catalyst = value

    @property
    def jokers(self):
        u"""ジョーカー数取得。
        """
        return self.__jokers

    @jokers.setter
    def jokers(self, value):
        u"""ジョーカー数設定。
        """
        self.__jokers = int(value)

    @property
    def is_sorcery_useable(self):
        u"""魔術使用可能状態取得。
        """
        return self.__is_sorcery_usable

    @is_sorcery_useable.setter
    def is_sorcery_useable(self, value):
        u"""魔術使用可能状態設定。
        """
        self.__is_sorcery_usable = bool(value)

    # ---- Creature ----
    @property
    def has_health(self):
        u"""健康クリーチャーの有無を取得。
        """
        return self.__has_health

    @has_health.setter
    def has_health(self, value):
        u"""健康クリーチャーの有無を設定。
        """
        self.__has_health = bool(value)

    @property
    def has_normal(self):
        u"""健康かつゾンビ以外クリーチャーの有無を取得。
        """
        return self.__has_normal

    @has_normal.setter
    def has_normal(self, value):
        u"""健康かつゾンビ以外クリーチャーの有無を設定。
        """
        self.__has_normal = bool(value)

    @property
    def has_damaged(self):
        u"""HP半減かつゾンビ以外クリーチャーの有無を取得。
        """
        return self.__has_damaged

    @has_damaged.setter
    def has_damaged(self, value):
        u"""HP半減かつゾンビ以外クリーチャーの有無を設定。
        """
        self.__has_damaged = bool(value)

    @property
    def is_full_group(self):
        u"""グループ満員判定取得。
        """
        return self.__is_full_group

    @is_full_group.setter
    def is_full_group(self, value):
        u"""グループ満員判定設定。
        """
        self.__is_full_group = bool(value)

    @property
    def is_group_exsit(self):
        u"""グループが存在するかどうかの判定取得。
        """
        return self.__is_group_exsit

    @is_group_exsit.setter
    def is_group_exsit(self, value):
        u"""グループが存在するかどうかの判定設定。
        """
        self.__is_group_exsit = bool(value)

    @property
    def recepters(self):
        u"""受容可能クリーチャー名セット取得。
        """
        return self.__recepters

    @recepters.setter
    def recepters(self, value):
        u"""受容可能クリーチャー名セット設定。
        """
        self.__recepters = set(value)
