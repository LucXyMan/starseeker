#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""general.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

汎用関数モジュール。
"""
__DE_BRUIJN_SEQUENCE = 0x03F566ED27179461
__DBS_TABLE = {}


# ---- Calculation ----
def get_number_of_bit(bits):
    u"""1のビット数を数える
    """
    bits = (bits & 0x55555555)+(bits >> 1 & 0x55555555)
    bits = (bits & 0x33333333)+(bits >> 2 & 0x33333333)
    bits = (bits & 0x0F0F0F0F)+(bits >> 4 & 0x0F0F0F0F)
    bits = (bits & 0x00FF00FF)+(bits >> 8 & 0x00FF00FF)
    return (bits & 0x0000FFFF)+(bits >> 16 & 0x0000FFFF)


def get_rightmost_bit(bits):
    u"""bitsの最も右端に存在するビット位置取得。
    """
    def __create_table():
        u"""__DBS_TABLEが空の場合に値を代入。
        """
        if not __DBS_TABLE:
            dbs = __DE_BRUIJN_SEQUENCE
            for i in range(64):
                __DBS_TABLE[dbs >> 58] = i
                dbs <<= 1
    __create_table()
    return __DBS_TABLE[int((long(bits & -bits)*__DE_BRUIJN_SEQUENCE) >> 58)]


# ---- Skill ----
def get_skill_names(*skills):
        u"""スキル名取得。
        """
        return reduce(lambda x, y: x+"#"+y, (
            name for name, _ in (skill.split("#") for skill in skills)))


def get_skill_description(skill):
    u"""スキル説明取得。
    """
    _, description = skill.split("#")
    return description
