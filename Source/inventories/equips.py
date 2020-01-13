#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""equips.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

装備・スキル・デッキ設定モジュール。
"""
import inventory as __inventory
import utils.const as _const


class Equip(__inventory.Inventory):
    u"""装備管理。
    """
    __slots__ = ()

    # ---- Getter ----
    @classmethod
    def get(cls, slot):
        u"""現在プレイヤー装備取得。
        slot: 装備種類。武器・兜・鎧・装飾。
        """
        equip = cls._equip
        return equip.get(
            cls._general.get(0)*len(equip)/_const.PLEYERS+slot)

    @classmethod
    def get_all(cls):
        u"""装備状態取得。
        """
        length = len(cls._equip)/_const.PLEYERS
        return tuple(cls.get(slot) for slot in range(length))

    @classmethod
    def get_value(cls):
        u"""数値を取得。
        """
        return sum(cls._equip.raw)

    # ---- Setter ----
    @classmethod
    def set(cls, slot, value):
        u"""プレイヤーの装備設定。
        slot: 装備種類。
        value: 設定する値。
        """
        equip = cls._equip
        equip.set(
            cls._general.get(0)*len(equip)/_const.PLEYERS+slot, value)


class Skill(__inventory.Inventory):
    u"""スキル管理。
    """
    __slots__ = ()

    # ---- On Off ----
    @classmethod
    def on(cls, slot):
        u"""位置slotのスキル状態on。
        """
        skill = cls._skill
        skill.on(cls._general.get(0)*len(skill)/_const.PLEYERS+slot)

    @classmethod
    def off(cls, slot):
        u"""位置slotのスキル状態off。
        """
        skill = cls._skill
        skill.off(cls._general.get(0)*len(skill)/_const.PLEYERS+slot)
        for slot in range(cls._equip.slot/_const.PLEYERS):
            if not cls.is_item_equippable(cls._equips[Equip.get(slot)]):
                Equip.set(slot, 0)

    # ---- Equip ----
    @classmethod
    def add_equippable(cls, skills):
        u"""スキルによる可用装備追加。
        """
        import utils.general as __general
        categorys = {
            __general.get_skill_names(skill): category for skill, category in (
                (_const.SWORD_EQUIP_SKILL, _const.SWORD_CATEGORY),
                (_const.WAND_EQUIP_SKILL, _const.WAND_CATEGORY),
                (_const.HEAVY_EQUIP_SKILL, _const.HEAVY_CATEGORY),
                (_const.MISSILE_EQUIP_SKILL, _const.MISSILE_CATEGORY),
                (_const.HAT_EQUIP_SKILL, _const.HAT_CATEGORY),
                (_const.HELMET_EQUIP_SKILL, _const.HELMET_CATEGORY),
                (_const.ROBE_EQUIP_SKILL, _const.ROBE_CATEGORY),
                (_const.ARMOR_EQUIP_SKILL, _const.ARMOR_CATEGORY))}
        return tuple(categorys[name] for name in (
            name for name in (skill.name for skill in skills) if
            name in categorys.keys()))

    @classmethod
    def is_item_equippable(cls, equip):
        u"""equipを装備可能な場合に真。
        """
        return (
            equip.category in
            cls._players[cls._general.get(0)].equippable +
            cls.add_equippable((cls._skills[i] for i in cls.get_equiped())))

    # ---- Getter ----
    @classmethod
    def __get_all(cls):
        u"""全スキル状態取得。
        """
        return tuple(cls.has(slot) for slot in range(
            len(cls._skill)/_const.PLEYERS))

    @classmethod
    def has(cls, slot):
        u"""位置slotのスキル状態を取得。
        """
        skill = cls._skill
        return skill.has(
            cls._general.get(0)*len(skill)/_const.PLEYERS+slot)

    @classmethod
    def get_equiped(cls):
        u"""装備状態のスキル番号取得。
        """
        return tuple(number for number, has in zip(
            cls._players[cls._general.get(0)].learnable,
            cls.__get_all()) if has)

    @classmethod
    def get_used_slot(cls):
        u"""使用済みスキルスロット数取得。
        """
        return sum(
           cls._skills[number].slot for number, state in zip(
               cls._players[cls._general.get(0)].learnable,
               cls.__get_all()) if state)

    @classmethod
    def get_limit(cls):
        u"""最大スキルスロット取得。
        """
        return cls._skill.slot/_const.PLEYERS

    @classmethod
    def get_value(cls):
        u"""数値を取得。
        """
        return sum(cls._skill.raw)


class Deck(__inventory.Inventory):
    u"""デッキ管理。
    """
    __slots__ = ()

    # ---- Getter ----
    @classmethod
    def get(cls, slot):
        u"""デッキカード取得。
        """
        deck = cls._deck
        return deck.get(
            cls._general.get(0)*len(deck)/_const.PLEYERS+slot)

    @classmethod
    def get_all(cls):
        u"""デッキ取得。
        """
        deck = cls._deck
        rng = len(deck)/_const.PLEYERS
        start = cls._general.get(0)*rng
        return reduce(lambda x, y: x+y, (
            (i % rng,)*deck.get(i) for i in range(start, start+rng)))

    @classmethod
    def get_total(cls):
        u"""デッキカード枚数取得。
        """
        return sum(cls.get(i) for i in range(len(
            cls._deck)/_const.PLEYERS))

    @classmethod
    def get_value(cls):
        u"""数値を取得。
        """
        return sum(cls._deck.raw)

    # ---- Setter ----
    @classmethod
    def set(cls, slot, value):
        u"""デッキカード設定。
        """
        deck = cls._deck
        return deck.set(
            cls._general.get(0)*len(deck)/_const.PLEYERS+slot, value)
