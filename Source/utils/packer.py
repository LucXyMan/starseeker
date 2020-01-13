#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-
u"""packer.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ファイル暗号化・圧縮モジュール。
"""
import io as _io
import os as _os
import struct as _struct
import zlib as __zlib
__IS_COMPRESSION = True
__INTERVAL = 256
__SHIFT = 2
_METADATA_FORMAT = "<IB"
_STORED_NUMBER_FORMAT = "<H"


# ---- Process ----
def __reverse(byte):
    u"""オクテットをビット反転。
    """
    return eval("'\\x"+hex(ord(byte) ^ 0xFF).lstrip("0x").zfill(2)+"'")


def __shift(byte, is_left):
    u"""オクテットをシフト。
    """
    value = ord(byte)
    return chr(
        (value << 1 & 0b11111111)+((value & 0b10000000) >> 7) if is_left else
        (value >> 1 & 0b11111111)+((value & 0b00000001) << 7))


# ---- Encode ----
def __integrate(directory, extensions, is_fast=False):
    u"""ファイルを暗号化して統合。
    暗号化ファイル: ファイル数(65535個まで)+メタデータ1+メタデータ2...+統合データ。
    メタデータ: ファイルサイズ(4Gまで)+名前サイズ(255文字まで)+名前文字列。
    is_fastの値によって暗号化方式を変更する。
    """
    meta = ""
    body = ""
    targets = []
    extensions = tuple(
        extension.upper() for extension in extensions.split("#"))
    for filename in _os.listdir(directory):
        _, ext = _os.path.splitext(filename)
        if ext.strip(".").upper() in extensions:
            targets.append(filename)
    targets.sort()
    meta += _struct.pack(_STORED_NUMBER_FORMAT, len(targets))
    for target in targets:
        filepath = _os.path.join(directory, target)
        meta += _struct.pack(
            _METADATA_FORMAT, _os.path.getsize(filepath), len(target))+target
        with _io.open(filepath, "rb") as infile:
            body += infile.read()
    if is_fast:
        fast_pack(directory+(".enf"), meta+body)
    else:
        pack(directory+(".enc"), meta+body)


def pack(filename, bytes_):
    u"""ファイルを個別に暗号化。
    """
    def __encode(bytes_):
        u"""エンコード関数。
        """
        result = ""
        for byte in bytes_:
            result += __shift(__reverse(byte), True)
        return result
    with _io.open(filename, "wb") as outfile:
        func = __zlib.compress if __IS_COMPRESSION else lambda x: x
        outfile.write(__encode(func(bytes_)))


def fast_pack(filename, bytes_):
    u"""ファイルを個別に暗号化。
    比較的早い、単純なもの。
    """
    with _io.open(filename, "wb") as outfile:
        read = 0
        while True:
            part = bytes_[read:read+__INTERVAL]
            if part:
                outfile.write(part[__SHIFT:]+part[:__SHIFT])
                read += __INTERVAL
            else:
                break


# ---- Decode ----
def unpack(filename):
    u"""暗号化ファイル復号化。
    """
    def __open_file():
        u"""ファイルを開く。
        """
        def __decode(bytes_):
            u"""デコード関数。
            """
            result = ""
            for byte in bytes_:
                result += __reverse(__shift(byte, False))
            return result
        with _io.open(name, "rb") as encrypted:
            func = __zlib.decompress if __IS_COMPRESSION else lambda x: x
            with _io.BytesIO(func(__decode(encrypted.read()))) as decrypted:
                return _io.BytesIO(decrypted.read())
    for name in (filename, _os.path.join("StarSeeker", filename)):
        if _os.path.exists(name):
            return __open_file()
    else:
        print "File not found."
        return None


def fast_unpack(filename):
    u"""暗号化ファイル復号化。
    比較的早い、単純なもの。
    """
    def __open_file():
        u"""ファイルを開く。
        """
        with _io.open(filename, "rb") as encrypted:
            result = ""
            while True:
                part = encrypted.read(__INTERVAL)
                part = part[-__SHIFT:]+part[:-__SHIFT]
                if part:
                    result += part
                else:
                    with _io.BytesIO(result) as decrypted:
                        return _io.BytesIO(decrypted.read())
    if _os.path.exists(filename):
        return __open_file()
    else:
        print "File not found."
        return None


class Container(object):
    u"""暗号化ファイルコンテナ。
    """
    __slots__ = "__dict",

    def __init__(self, filename):
        u"""暗号化ストレージファイルを復号化して格納。
        data_number: 格納データ数。
        size: 4GBまでの格納データサイズ。
        name_size: 1Bのデータ名サイズ。
        name: データ名。
        """
        self.__dict = {}
        stored_bytes_number = 2
        metadata_bytes_number = 5
        _, ext = _os.path.splitext(filename)
        decrypted = (
            fast_unpack if ext.upper() == ".ENF" else unpack)(filename)
        data_number, = _struct.unpack(
             _STORED_NUMBER_FORMAT, decrypted.read(stored_bytes_number))
        values = []
        for _ in range(data_number):
            size, name_size = _struct.unpack(
                _METADATA_FORMAT, decrypted.read(metadata_bytes_number))
            values.append((size, decrypted.read(name_size)))
        for value in values:
            size, name = value
            self.__dict[name] = _io.BytesIO(decrypted.read(size))

    def get(self, key):
        u"""ファイルオブジェクト取得。
        """
        return self.__dict[key]

    @property
    def keys(self):
        u"""キーの一覧を取得。
        """
        return self.__dict.keys()


if __name__ == "__main__":
    print "start."
    source_dir = _os.path.join(_os.path.dirname(__file__), "..", "material")
    __integrate(_os.path.join(source_dir, "images"), "png")
    __integrate(_os.path.join(source_dir, "bgm"), "ogg", is_fast=True)
    __integrate(_os.path.join(source_dir, "se"), "wav", is_fast=True)
    print "finish."
