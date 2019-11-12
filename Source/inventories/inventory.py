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
        "\x01\x8f\x85\xd2\xe4\x95N\x1d\xe7\xe8\x15\x99<\xb8\x0biq\x03\xe7\xbc:"
        "\xb2\xdaR\xf4\xdaJ9\xe5\xbc\xba\xe9")
    __UTILS_DATA_SIZE = 1
    __LEVEL_DATA_SIZE = 2
    __ITEMS_DATA_SIZE = 5
    __CARDS_DATA_SIZE = 5
    __EQUIP_DATA_SIZE = _const.PLEYERS
    __SKILL_DATA_SIZE = _const.PLEYERS >> 1
    __DECK_DATA_SIZE = _const.PLEYERS*__CARDS_DATA_SIZE
    __STARTER_DECK = 0, 4, 8, 16, 32, 45, 48, 52, 57, 59, 69, 76

    def __init__(self):
        u"""各パラメータの設定。
        __time: ゲーム内経過時間。
        __sp: 取得スターポイント。
        __utils: 汎用パラメータ。
        __level: レベルクリア状態。
        __items: 取得アイテム状態。
        __cards: 最大3枚の取得済カード。
        __equip: プレイヤー8人分の装備・スキル・デッキの状態。
        __skill: プレイヤー8人分のスキル状態。
        __deck: プレイヤー8人分のデッキ状態。最大3のカード枚数。
        """
        import bitflag as __bitflag

        def __init_starter_deck(*cards):
            u"""スターターデッキ初期化。
            """
            for card in cards:
                Inventory.__cards.set(card, 1)
                for i in range(_const.PLEYERS):
                    Inventory.__deck.set(
                        i*len(Inventory.__deck)/_const.PLEYERS+card, 1)
        Inventory.__time = 0
        Inventory.__sp = 100
        if not hasattr(self, "__UtilsContainer"):
            Inventory.__UtilsContainer = __bitflag.ByteNumber
        Inventory.__utils = self.__UtilsContainer([0]*self.__UTILS_DATA_SIZE)
        Inventory.__utils.set(2, 2)
        if not hasattr(self, "__LevelContainer"):
            Inventory.__LevelContainer = __bitflag.BitFlag
        Inventory.__level = self.__LevelContainer([0]*self.__LEVEL_DATA_SIZE)
        if not hasattr(self, "__ItemsContainer"):
            Inventory.__ItemsContainer = __bitflag.BitFlag
        Inventory.__items = self.__ItemsContainer([0]*self.__ITEMS_DATA_SIZE)
        if not hasattr(self, "__CardContainer"):
            Inventory.__CardContainer = __bitflag.TwoBitNumber
        Inventory.__cards = self.__CardContainer([0]*self.__CARDS_DATA_SIZE)
        if not hasattr(self, "__EquipContainer"):
            Inventory.__EquipContainer = __bitflag.ByteNumber
        Inventory.__equip = self.__EquipContainer([0]*self.__EQUIP_DATA_SIZE)
        if not hasattr(self, "__SkillContainer"):
            Inventory.__SkillContainer = __bitflag.BitFlag
        Inventory.__skill = self.__SkillContainer([0]*self.__SKILL_DATA_SIZE)
        if not hasattr(self, "__DeckContainer"):
            Inventory.__DeckContainer = __bitflag.TwoBitNumber
        Inventory.__deck = self.__DeckContainer([0]*self.__DECK_DATA_SIZE)
        __init_starter_deck(*self.__STARTER_DECK)

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
                "<{}I".format(cls.__UTILS_DATA_SIZE), *cls.__utils.raw) +
            _struct.pack(
                "<{}I".format(cls.__LEVEL_DATA_SIZE), *cls.__level.raw) +
            _struct.pack(
                "<{}I".format(cls.__ITEMS_DATA_SIZE), *cls.__items.raw) +
            _struct.pack(
                "<{}I".format(cls.__CARDS_DATA_SIZE), *cls.__cards.raw) +
            _struct.pack(
                "<{}I".format(cls.__EQUIP_DATA_SIZE), *cls.__equip.raw) +
            _struct.pack(
                "<{}I".format(cls.__SKILL_DATA_SIZE), *cls.__skill.raw) +
            _struct.pack(
                "<{}I".format(cls.__DECK_DATA_SIZE), *cls.__deck.raw) +
            cls.__get_hash((
                (cls.__time,), (cls.__sp,), cls.__utils.raw, cls.__level.raw,
                cls.__items.raw, cls.__cards.raw, cls.__equip.raw,
                cls.__skill.raw, cls.__deck.raw))))

    @classmethod
    def load(cls):
        u"""ゲームデータのロード。
        暗号化したデータを復号化して各種変数に設定する。
        データが正常でない場合や改ざんされている場合、ロードを行わない。
        ロードに成功した場合、バックアップファイルの作成を行う。
        """
        def __test_correct(hash_):
            u"""ゲームデータの正当性テスト。
            データ改ざんされている場合False、正しい場合Trueを返す。
            """
            current = cls.__get_hash((
                (time,), (sp,), utils.raw, level.raw, items.raw, cards.raw,
                equip.raw, skill.raw, deck.raw))
            if hash_ == current:
                if _const.IS_OUTPUT:
                    print str(hash_), u"==", current, u" :Is correct."
                return True
            else:
                if _const.IS_OUTPUT:
                    print str(hash_), u"!=", current, u" :Is incorrect!"
                return False
        filename = _os.path.join(cls.save_location, cls.__SAVE_FILE)
        if _os.path.exists(filename):
            decrypted = _packer.unpack(filename)
            time, = _struct.unpack("<I", decrypted.read(4))
            sp, = _struct.unpack("<I", decrypted.read(4))
            utils = cls.__UtilsContainer(_struct.unpack(
                "<{}I".format(cls.__UTILS_DATA_SIZE),
                decrypted.read(cls.__UTILS_DATA_SIZE << 2)))
            level = cls.__LevelContainer(_struct.unpack(
                "<{}I".format(cls.__LEVEL_DATA_SIZE),
                decrypted.read(cls.__LEVEL_DATA_SIZE << 2)))
            items = cls.__ItemsContainer(_struct.unpack(
                "<{}I".format(cls.__ITEMS_DATA_SIZE),
                decrypted.read(cls.__ITEMS_DATA_SIZE << 2)))
            cards = cls.__CardContainer(_struct.unpack(
                "<{}I".format(cls.__CARDS_DATA_SIZE),
                decrypted.read(cls.__CARDS_DATA_SIZE << 2)))
            equip = cls.__EquipContainer(_struct.unpack(
                "<{}I".format(cls.__EQUIP_DATA_SIZE),
                decrypted.read(cls.__EQUIP_DATA_SIZE << 2)))
            skill = cls.__SkillContainer(_struct.unpack(
                "<{}I".format(cls.__SKILL_DATA_SIZE),
                decrypted.read(cls.__SKILL_DATA_SIZE << 2)))
            deck = cls.__DeckContainer(_struct.unpack(
                "<{}I".format(cls.__DECK_DATA_SIZE),
                decrypted.read(cls.__DECK_DATA_SIZE << 2)))
            if __test_correct(decrypted.read(16)):
                cls.__time = time
                cls.__sp = sp
                cls.__utils = utils
                cls.__level = level
                cls.__items = items
                cls.__cards = cards
                cls.__equip = equip
                cls.__skill = skill
                cls.__deck = deck
                cls.save("backup")
                return True
            else:
                return False
        else:
            return True

    # ---- Getter ----
    @classmethod
    def get_time(cls):
        u"""経過時間取得。
        """
        return cls.__time

    @classmethod
    def get_sp(cls):
        u"""SP取得。
        """
        return cls.__sp

    @classmethod
    def get_utils(cls):
        u"""ユーティリティ取得。
        """
        return cls.__utils

    @classmethod
    def get_level(cls):
        u"""レベル状態取得。
        """
        return cls.__level

    @classmethod
    def get_items(cls):
        u"""アイテム状態取得。
        """
        return cls.__items

    @classmethod
    def get_cards(cls):
        u"""取得済みカード取得。
        """
        return cls.__cards

    @classmethod
    def get_equip(cls):
        u"""現在装備取得。
        """
        return cls.__equip

    @classmethod
    def get_skill(cls):
        u"""スキル取得。
        """
        return cls.__skill

    @classmethod
    def get_deck(cls):
        u"""装備カード取得。
        """
        return cls.__deck

    # ---- Setter ----
    @classmethod
    def set_time(cls, value):
        u"""経過時間設定。
        """
        cls.__time = int(value)

    @classmethod
    def set_sp(cls, value):
        u"""SP設定。
        """
        cls.__sp = int(value)
