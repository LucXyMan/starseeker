#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""inventory.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

インベントリモジュール。
"""
import os as _os
import struct as _struct
import utils.const as _const
import utils.packer as _packer


def get_config_dir():
    u"""設定ディレクトリ取得。
    """
    import sys as __sys
    userdir = _os.path.expanduser("~")
    return (
        _os.path.join(userdir, "AppData", "Local", "Star Seeker") if
        __sys.platform.startswith(("win", "cygwin")) else
        _os.path.join(userdir, ".config", "starseeker"))


def init():
    u"""モジュールの初期化。
    インベントリインスタンスを一つだけ作成。
    """
    Inventory.save_location = get_config_dir()
    Inventory()


class Inventory(object):
    u"""インベントリ。
    ゲーム内データを管理する。
    """
    __SAVE_FILE = "savedata"
    __HASH_INIT = (
        "nk\x07U<\x87L\x10\xc1\xaf\xe8\xbb-B;\xdcM\xde7"
        "\xe6\x0b\x91\xe6\xe2g\xe5\x12\xc1\xe1\xf6>\x11")
    # ---- Data Size ----
    __GENERAL_DATA_SIZE = 1
    __LEVEL_DATA_SIZE = 2
    __ENDLESS_DATA_SIZE = 1
    __ITEM_DATA_SIZE = 6
    __CARD_DATA_SIZE = 6
    __EQUIP_DATA_SIZE = _const.PLEYERS
    __SKILL_DATA_SIZE = _const.PLEYERS >> 1
    __DECK_DATA_SIZE = _const.PLEYERS*__CARD_DATA_SIZE
    # ---- Time ----
    __TIME_LIMIT = 359999
    # ---- General ----
    _DIFFICULTY_SLOT = 1
    _SPEED_SLOT = 2
    # ---- SP ----
    __CARD_PRICE = 4
    __SP_LIMIT = 999
    # ---- Deck ----
    __STARTER_DECK = 0, 0, 13, 13, 20, 20, 39, 59, 65, 72, 82, 84
    # ---- Debug ----
    __IS_CHEAT = False
    __IS_SP_UNLIMITED = False

    def __init__(self):
        u"""各パラメータの設定。
        __time: ゲーム内経過時間。
        __sp: 取得スターポイント。
        _general: 汎用パラメータ。
        _level: レベルクリア状態。
        _endless: エンドレス状態。
        _item: 取得アイテム状態。
        _card: 最大3枚の取得済カード。
        _equip: プレイヤー8人分の装備・スキル・デッキの状態。
        _skill: プレイヤー8人分のスキル状態。
        _deck: プレイヤー8人分のデッキ状態。最大3のカード枚数。
        """
        import armament.equips as _equips
        import armament.units as __units
        import armament.skill as _skill
        import bitflag as __bitflag

        def __init_starter_deck(*cards):
            u"""スターターデッキ初期化。
            """
            for card in cards:
                Inventory._card.set(card, Inventory._card.get(card)+1)
                for i in range(_const.PLEYERS):
                    number = i*len(Inventory._deck)/_const.PLEYERS+card
                    Inventory._deck.set(number, Inventory._deck.get(number)+1)
        Inventory.__time = 0
        Inventory.__sp = 100
        Inventory.__GeneralFlag = __bitflag.NibbleNumber
        Inventory._general = self.__GeneralFlag([0]*self.__GENERAL_DATA_SIZE)
        Inventory._general.set(self._DIFFICULTY_SLOT, 1)
        Inventory._general.set(self._SPEED_SLOT, 2)
        Inventory.__EndlessFlag = __bitflag.ByteNumber
        Inventory._endless = self.__EndlessFlag([0]*self.__ENDLESS_DATA_SIZE)
        Inventory.__LevelFlag = __bitflag.BitFlag
        Inventory._level = self.__LevelFlag([0]*self.__LEVEL_DATA_SIZE)
        Inventory.__ItemFlag = __bitflag.BitFlag
        Inventory._item = self.__ItemFlag([0]*self.__ITEM_DATA_SIZE)
        Inventory.__CardFlag = __bitflag.TwoBitNumber
        Inventory._card = self.__CardFlag([0]*self.__CARD_DATA_SIZE)
        Inventory.__EquipFlag = __bitflag.ByteNumber
        Inventory._equip = self.__EquipFlag([0]*self.__EQUIP_DATA_SIZE)
        Inventory.__SkillFlag = __bitflag.BitFlag
        Inventory._skill = self.__SkillFlag([0]*self.__SKILL_DATA_SIZE)
        Inventory.__DeckFlag = __bitflag.TwoBitNumber
        Inventory._deck = self.__DeckFlag([0]*self.__DECK_DATA_SIZE)
        __init_starter_deck(*self.__STARTER_DECK)
        Inventory._equips = _equips.get_all()
        Inventory._skills = _skill.get_all()
        Inventory._players = __units.get_players()

    @classmethod
    def __get_hash(cls, values):
        u"""ハッシュ値を取得。
        """
        import hashlib as __hashlib
        algorithm = __hashlib.md5(cls.__HASH_INIT)
        for value in values:
            algorithm.update(str(reduce(
                lambda x, y: "{x}:{y}".format(x=x, y=y), value)))
        return algorithm.digest()

    # ---- Save and Load ----
    @classmethod
    def save(cls, filename=__SAVE_FILE):
        u"""データを暗号化して保存。
        暗号化データはハッシュ値を記録する。
        """
        if not _os.path.exists(cls.save_location):
            _os.makedirs(cls.save_location, mode=0o775)
        _packer.pack(_os.path.join(cls.save_location, filename), (
            _struct.pack("<I", cls.__time)+_struct.pack("<I", cls.__sp) +
            _struct.pack(
                "<{}I".format(cls.__GENERAL_DATA_SIZE), *cls._general.raw) +
            _struct.pack(
                "<{}I".format(cls.__LEVEL_DATA_SIZE), *cls._level.raw) +
            _struct.pack(
                "<{}I".format(cls.__ENDLESS_DATA_SIZE), *cls._endless.raw) +
            _struct.pack(
                "<{}I".format(cls.__ITEM_DATA_SIZE), *cls._item.raw) +
            _struct.pack(
                "<{}I".format(cls.__CARD_DATA_SIZE), *cls._card.raw) +
            _struct.pack(
                "<{}I".format(cls.__EQUIP_DATA_SIZE), *cls._equip.raw) +
            _struct.pack(
                "<{}I".format(cls.__SKILL_DATA_SIZE), *cls._skill.raw) +
            _struct.pack(
                "<{}I".format(cls.__DECK_DATA_SIZE), *cls._deck.raw) +
            cls.__get_hash((
                (cls.__time,), (cls.__sp,), cls._general.raw, cls._level.raw,
                cls._endless.raw, cls._item.raw, cls._card.raw, cls._equip.raw,
                cls._skill.raw, cls._deck.raw))))

    @classmethod
    def load(cls):
        u"""ゲームデータのロード。
        暗号化したデータを復号化して各種変数に設定する。
        データが正常でない場合や改ざんされている場合、ロードを行わない。
        ロードに成功した場合、バックアップファイルの作成を行う。
        """
        def __is_correct(hash_):
            u"""ゲームデータの正当性テスト。
            データ改ざんされている場合False、正しい場合Trueを返す。
            """
            current = cls.__get_hash((
                (time,), (sp,), general.raw, level.raw,  endless.raw,
                items.raw, cards.raw, equip.raw, skill.raw, deck.raw))
            if hash_ == current:
                if _const.IS_OUTPUT:
                    print str(hash_), u"==", current, u" :Is correct."
                return True
            else:
                if _const.IS_OUTPUT:
                    print str(hash_), u"!=", current, u" :Is incorrect!"
                return False

        def __cheat_apply():
            u"""チート適用。
            """
            if cls.__IS_CHEAT:
                cls._level.on(35)
                cls._endless.set(0, 40)
                for i in range(len(cls._item)):
                    cls._item.on(i)
                for i in range(len(cls._card)):
                    cls._card.set(i, 3)
        filename = _os.path.join(cls.save_location, cls.__SAVE_FILE)
        if _os.path.exists(filename):
            decrypted = _packer.unpack(filename)
            time, = _struct.unpack("<I", decrypted.read(4))
            sp, = _struct.unpack("<I", decrypted.read(4))
            general = cls.__GeneralFlag(_struct.unpack(
                "<{}I".format(cls.__GENERAL_DATA_SIZE),
                decrypted.read(cls.__GENERAL_DATA_SIZE << 2)))
            level = cls.__LevelFlag(_struct.unpack(
                "<{}I".format(cls.__LEVEL_DATA_SIZE),
                decrypted.read(cls.__LEVEL_DATA_SIZE << 2)))
            endless = cls.__EndlessFlag(_struct.unpack(
                "<{}I".format(cls.__ENDLESS_DATA_SIZE),
                decrypted.read(cls.__ENDLESS_DATA_SIZE << 2)))
            items = cls.__ItemFlag(_struct.unpack(
                "<{}I".format(cls.__ITEM_DATA_SIZE),
                decrypted.read(cls.__ITEM_DATA_SIZE << 2)))
            cards = cls.__CardFlag(_struct.unpack(
                "<{}I".format(cls.__CARD_DATA_SIZE),
                decrypted.read(cls.__CARD_DATA_SIZE << 2)))
            equip = cls.__EquipFlag(_struct.unpack(
                "<{}I".format(cls.__EQUIP_DATA_SIZE),
                decrypted.read(cls.__EQUIP_DATA_SIZE << 2)))
            skill = cls.__SkillFlag(_struct.unpack(
                "<{}I".format(cls.__SKILL_DATA_SIZE),
                decrypted.read(cls.__SKILL_DATA_SIZE << 2)))
            deck = cls.__DeckFlag(_struct.unpack(
                "<{}I".format(cls.__DECK_DATA_SIZE),
                decrypted.read(cls.__DECK_DATA_SIZE << 2)))
            if __is_correct(decrypted.read(16)):
                cls.__time = time
                cls.__sp = sp
                cls._general = general
                cls._level = level
                cls._endless = endless
                cls._item = items
                cls._card = cards
                cls._equip = equip
                cls._skill = skill
                cls._deck = deck
                __cheat_apply()
                cls.save("backup")
                return True
        return True

    # ---- SP ----
    @classmethod
    def _get_require(cls, got):
        u"""カード取得に必要なSPを取得。
        """
        if 0 < got:
            value = cls.__CARD_PRICE << got-1
            return (
                0 if value < 0 else cls.__SP_LIMIT if
                cls.__SP_LIMIT < value else value)
        return 0

    @classmethod
    def get_sp(cls):
        u"""現在SP取得。
        """
        return cls.__SP_LIMIT if cls.__IS_SP_UNLIMITED else cls.__sp

    @classmethod
    def add_sp(cls, value):
        u"""SP追加処理。
        """
        value = cls.get_sp()+int(value)
        cls.__sp = (
            0 if value < 0 else cls.__SP_LIMIT if
            cls.__SP_LIMIT < value else value)

    @classmethod
    def is_buyable(cls, item):
        u"""アイテム購入可能判定。
        """
        return item.sp <= cls.get_sp()

    @classmethod
    def buy_item(cls, item):
        u"""アイテム購入処理。
        """
        import material.sound as __sound
        if cls.is_buyable(item):
            __sound.SE.play("get")
            cls.__sp = cls.get_sp()-item.sp
            cls._item.on(item.number-1)
            return True
        __sound.SE.play("error")
        return False

    @classmethod
    def buy_card(cls, slot, got):
        u"""カード購入処理。
        """
        require = cls._get_require(got)
        if require <= cls.get_sp():
            cls.__sp = cls.get_sp()-require
            size = cls._card.size
            value = cls._card.get(slot)+1
            cls._card.set(slot, value if value < size else size)
            return True
        return False

    # ---- Time ----
    @classmethod
    def get_time(cls):
        u"""ゲーム内経過時間取得。
        """
        return cls.__time

    @classmethod
    def forward_time(cls):
        u"""ゲーム内経過時間を進める。
        """
        time = cls.__time+1
        cls.__time = cls.__TIME_LIMIT if cls.__TIME_LIMIT < time else time
