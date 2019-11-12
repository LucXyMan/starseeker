#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""interface.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

インターフェースモジュール。
"""
import inventory as _inventory
import utils.const as _const


def init():
    u"""モジュール初期化。
    """
    _Interface()


class _Interface(object):
    u"""インベントリインターフェース。
    """
    __slot__ = ()

    def __init__(self):
        u"""設定データをロード。
        """
        import armament.collectible as __collectible
        import armament.equip as __equip
        import armament.units as __units
        import armament.skill as __skill
        _Interface._collections = __collectible.get_all()
        _Interface._equips = __equip.get_all()
        _Interface._skills = __skill.get_all()
        _Interface._players = __units.get_player_all()


class Time(_Interface):
    u"""時間管理インターフェース。
    """
    __slot__ = ()
    __LIMIT = 359999

    @classmethod
    def get(cls):
        u"""ゲーム内経過時間取得。
        """
        return _inventory.Inventory.get_time()

    @classmethod
    def forward(cls):
        u"""ゲーム内経過時間を進める。
        """
        time = _inventory.Inventory.get_time()+1
        _inventory.Inventory.set_time(
            cls.__LIMIT if cls.__LIMIT < time else time)


class SP(_Interface):
    u"""SP管理インターフェース。
    """
    __slot__ = ()
    LIMIT = 9999

    @classmethod
    def get(cls):
        u"""現在SP取得。
        """
        return (
            cls.LIMIT if _const.IS_SP_UNLIMITED else
            _inventory.Inventory.get_sp())

    @classmethod
    def set(cls, value):
        u"""現在SP設定。
        """
        _inventory.Inventory.set_sp(
            0 if value < 0 else cls.LIMIT if cls.LIMIT < value else value)

    @classmethod
    def add(cls, value):
        u"""SP追加処理。
        """
        cls.set(cls.get()+value)

    @classmethod
    def is_buyable(cls, item):
        u"""アイテム購入可能判定。
        """
        return item.sp <= SP.get()

    @classmethod
    def buy_item(cls, item):
        u"""アイテム購入処理。
        """
        import material.sound as __sound
        if cls.is_buyable(item):
            __sound.SE.play("Get")
            SP.set(_inventory.Inventory.get_sp()-item.sp)
            Items.on(item.number-1)
            return True
        __sound.SE.play("Error")
        return False

    @classmethod
    def buy_card(cls, slot, got):
        u"""カード購入処理。
        """
        consume = Cards.get_consume(got)
        sp = SP.get()
        if consume <= sp:
            SP.set(sp-consume)
            size = _inventory.Inventory.get_cards().size
            value = Cards.get(slot)+1
            Cards.set(slot, value if value < size else size)
            return True
        return False


class Utils(_Interface):
    u"""汎用パラメータ管理インターフェース。
    """
    __slot__ = ()

    @classmethod
    def get_value(cls):
        u"""数値を取得。
        """
        return sum(_inventory.Inventory.get_utils().raw)

    @classmethod
    def get_player(cls):
        u"""現在プレイヤー取得。
        """
        return _inventory.Inventory.get_utils().get(0)

    @classmethod
    def set_player(cls, value):
        u"""現在プレイヤー設定。
        """
        _inventory.Inventory.get_utils().set(0, (
            0 if value < 0 else value if value < _const.PLAYER_NUMBER-1 else
            _const.PLAYER_NUMBER-1))

    @classmethod
    def get_learnable(cls):
        u"""プレイヤーが取得可能なスキル番号取得。
        """
        return cls._players[cls.get_player()].learnable

    @classmethod
    def get_endless(cls):
        u"""エンドレス進行状態取得。
        """
        return _inventory.Inventory.get_utils().get(1)

    @classmethod
    def set_endless(cls, value):
        u"""エンドレス進行状態取得。
        """
        _inventory.Inventory.get_utils().set(1, (
            0 if value < 0 else value if value < _const.ENDLESS_LIMIT else
            _const.ENDLESS_LIMIT))

    @classmethod
    def get_speed(cls):
        u"""移動速度取得。
        """
        return _inventory.Inventory.get_utils().get(2)

    @classmethod
    def set_speed(cls, value):
        u"""移動速度設定。
        """
        _inventory.Inventory.get_utils().set(2, int(value))


class Level(_Interface):
    u"""レベル管理インターフェース。
    """
    __slot__ = ()

    @classmethod
    def get_value(cls):
        u"""数値を取得。
        """
        return sum(_inventory.Inventory.get_level().raw)

    @classmethod
    def has(cls, slot):
        u"""位置slotのクリア状態取得。
        """
        return _inventory.Inventory.get_level().has(slot)

    @classmethod
    def on(cls, slot):
        u"""位置slotのクリア状態設定。
        """
        _inventory.Inventory.get_level().on(slot)

    @classmethod
    def get_wins(cls):
        u"""デュエルモード勝利数数取得。
        """
        return _inventory.Inventory.get_level().bits


class Items(_Interface):
    u"""アイテム管理インターフェース。
    """
    __slot__ = ()

    @classmethod
    def get_value(cls):
        u"""数値を取得。
        """
        return sum(_inventory.Inventory.get_items().raw)

    @classmethod
    def has(cls, slot):
        u"""位置slotのアイテム状態を取得。
        """
        return _inventory.Inventory.get_items().has(slot)

    @classmethod
    def on(cls, slot):
        u"""slotのアイテム状態を設定。
        """
        _inventory.Inventory.get_items().on(slot)


class Cards(_Interface):
    u"""カード管理インターフェース。
    """
    __slot__ = ()
    __PRICE = 40

    @classmethod
    def get_value(cls):
        u"""数値を取得。
        """
        return sum(_inventory.Inventory.get_cards().raw)

    @classmethod
    def get(cls, slot):
        u"""位置slotのカード状態取得。
        """
        return _inventory.Inventory.get_cards().get(slot)

    @classmethod
    def set(cls, slot, value):
        u"""位置slotのカード状態設定。
        """
        _inventory.Inventory.get_cards().set(slot, value)

    @classmethod
    def get_consume(cls, got):
        u"""カード取得に必要なSPを取得。
        """
        if 0 < got:
            value = cls.__PRICE << got-1
            return 0 if value < 0 else SP.LIMIT if SP.LIMIT < value else value
        return 0


class Equip(_Interface):
    u"""装備管理インターフェース。
    """
    __slot__ = ()

    @classmethod
    def get_value(cls):
        u"""数値を取得。
        """
        return sum(_inventory.Inventory.get_equip().raw)

    @classmethod
    def get(cls, slot):
        u"""現在プレイヤー装備取得。
        slot: 装備種類。武器・兜・鎧・装飾。
        """
        equip = _inventory.Inventory.get_equip()
        return equip.get(
            Utils.get_player()*len(equip)/_const.PLAYER_NUMBER+slot)

    @classmethod
    def get_all(cls):
        u"""装備状態取得。
        """
        return tuple(cls.get(slot) for slot in range(
            0, len(_inventory.Inventory.get_equip())/_const.PLAYER_NUMBER))

    @classmethod
    def set(cls, slot, value):
        u"""プレイヤーの装備設定。
        slot: 装備種類。
        value: 設定する値。
        """
        equip = _inventory.Inventory.get_equip()
        equip.set(
            Utils.get_player()*len(equip)/_const.PLAYER_NUMBER+slot, value)


class Skill(_Interface):
    u"""スキル管理インターフェース。
    """
    __slot__ = ()

    @classmethod
    def get_value(cls):
        u"""数値を取得。
        """
        return sum(_inventory.Inventory.get_skill().raw)

    @classmethod
    def has(cls, slot):
        u"""位置slotのスキル状態を取得。
        """
        skill = _inventory.Inventory.get_skill()
        return skill.has(
            Utils.get_player()*len(skill)/_const.PLAYER_NUMBER+slot)

    @classmethod
    def __get_all(cls):
        u"""全スキル状態取得。
        """
        return tuple(cls.has(slot) for slot in range(
            len(_inventory.Inventory.get_skill())/_const.PLAYER_NUMBER))

    @classmethod
    def get_equiped(cls):
        u"""装備状態のスキル番号取得。
        """
        return tuple(number for number, has in zip(
            cls._players[Utils.get_player()].learnable,
            cls.__get_all()) if has)

    @classmethod
    def get_used_slot(cls):
        u"""使用済みスキルスロット数取得。
        """
        return sum(
           cls._skills[number].slot for number, state in zip(
               cls._players[Utils.get_player()].learnable,
               cls.__get_all()) if state)

    @classmethod
    def get_limit(cls):
        u"""最大スキルスロット取得。
        """
        return _inventory.Inventory.get_skill().slot/_const.PLAYER_NUMBER

    @classmethod
    def on(cls, slot):
        u"""位置slotのスキル状態on。
        """
        skill = _inventory.Inventory.get_skill()
        skill.on(Utils.get_player()*len(skill)/_const.PLAYER_NUMBER+slot)

    @classmethod
    def off(cls, slot):
        u"""位置slotのスキル状態off。
        """
        skill = _inventory.Inventory.get_skill()
        skill.off(Utils.get_player()*len(skill)/_const.PLAYER_NUMBER+slot)
        for slot in range(
            _inventory.Inventory.get_equip().slot/_const.PLAYER_NUMBER
        ):
            if not cls.is_item_equippable(cls._equips[Equip.get(slot)]):
                Equip.set(slot, 0)

    @classmethod
    def add_equippable(cls, skills):
        u"""スキルによる可用装備追加。
            """
        categorys = {
            _const.SWORD_EQUIP_SKILL_NAME: _const.SWORD_CATEGORY,
            _const.WAND_EQUIP_SKILL_NAME: _const.WAND_CATEGORY,
            _const.HEAVY_EQUIP_SKILL_NAME: _const.HEAVY_CATEGORY,
            _const.MISSILE_EQUIP_SKILL_NAME: _const.MISSILE_CATEGORY,
            _const.HAT_EQUIP_SKILL_NAME: _const.HAT_CATEGORY,
            _const.HELMET_EQUIP_SKILL_NAME: _const.HELMET_CATEGORY,
            _const.ROBE_EQUIP_SKILL_NAME: _const.ROBE_CATEGORY,
            _const.ARMOR_EQUIP_SKILL_NAME: _const.ARMOR_CATEGORY}
        return tuple(categorys[name] for name in (
            name for name in (skill.name for skill in skills) if
            name in categorys.keys()))

    @classmethod
    def is_item_equippable(cls, equip):
        u"""equipを装備可能な場合に真。
        """
        return (
            equip.category in cls._players[Utils.get_player()].equippable +
            cls.add_equippable((cls._skills[i] for i in cls.get_equiped())))


class Deck(_Interface):
    u"""デッキ管理インターフェース。
    """
    __slot__ = ()

    @classmethod
    def get_value(cls):
        u"""数値を取得。
        """
        return sum(_inventory.Inventory.get_deck().raw)

    @classmethod
    def get(cls, slot):
        u"""デッキカード取得。
        """
        deck = _inventory.Inventory.get_deck()
        return deck.get(Utils.get_player()*len(deck)/_const.PLAYER_NUMBER+slot)

    @classmethod
    def set(cls, slot, value):
        u"""デッキカード設定。
        """
        deck = _inventory.Inventory.get_deck()
        return deck.set(
            Utils.get_player()*len(deck)/_const.PLAYER_NUMBER+slot, value)

    @classmethod
    def get_all(cls):
        u"""デッキ取得。
        """
        deck = _inventory.Inventory.get_deck()
        rng = len(deck)/_const.PLAYER_NUMBER
        start = Utils.get_player()*rng
        return reduce(lambda x, y: x+y, (
            (i % rng,)*deck.get(i) for i in range(start, start+rng)))

    @classmethod
    def get_number(cls):
        u"""デッキカード枚数取得。
        """
        return sum(cls.get(i) for i in range(
            len(_inventory.Inventory.get_deck())/_const.PLAYER_NUMBER))
