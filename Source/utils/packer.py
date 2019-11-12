#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-
u"""packer.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ファイル暗号化・圧縮モジュール。
"""
import io as _io
import os as _os
import struct as _struct
import zlib as __zlib
__IS_COMPRESSION = True
_METADATA_FORMAT = "<IB"
_STORED_NUMBER_FORMAT = "<H"
__INTERVAL = 256
__SHIFT = 2
__filename = ""


def __reverse(byte):
    u"""オクテットをビット反転。
    """
    return eval("'\\x"+hex(ord(byte) ^ 0xFF).lstrip("0x").zfill(2)+"'")


def __caesar(byte, is_left):
    u"""オクテットをシフト。
    """
    value = ord(byte)
    return chr(
        (value << 1 & 0b11111111)+((value & 0b10000000) >> 7) if is_left else
        (value >> 1 & 0b11111111)+((value & 0b00000001) << 7))


def pack(filename, bytes_):
    u"""ファイルを個別に暗号化。
    """
    def __encode(bytes_):
        u"""エンコード関数。
        """
        result = ""
        for byte in bytes_:
            result += __caesar(__reverse(byte), True)
        return result
    with open(filename, "w") as outfile:
        outfile.write(__encode((
            __zlib.compress if __IS_COMPRESSION else lambda x: x)(bytes_)))


def pack_fast(filename, bytes_):
    u"""ファイルを個別に暗号化。
    比較的早い、単純なもの。
    """
    with open(filename, "w") as outfile:
        read = 0
        while True:
            part = bytes_[read:read+__INTERVAL]
            if part:
                outfile.write(part[__SHIFT:]+part[:__SHIFT])
                read += __INTERVAL
            else:
                break


def unpack(filename):
    u"""暗号化ファイル復号化。
    """
    def __decode(bytes_):
        u"""デコード関数。
        """
        result = ""
        for byte in bytes_:
            result += __reverse(__caesar(byte, False))
        return result

    def __open_file():
        u"""ファイルを開く。
        """
        with open(name) as encrypted:
            with _io.BytesIO((
                __zlib.decompress if __IS_COMPRESSION else lambda x: x
            )(__decode(encrypted.read()))) as decrypted:
                return _io.BytesIO(decrypted.read())
    for name in (filename, _os.path.join("StarSeeker", filename)):
        if _os.path.exists(name):
            return __open_file()
    else:
        print "File not found."
        return None


def unpack_fast(filename):
    u"""暗号化ファイル復号化。
    比較的早い、単純なもの。
    """
    def __open_file():
        u"""ファイルを開く。
        """
        with open(name) as encrypted:
            result = ""
            while True:
                part = encrypted.read(__INTERVAL)
                part = part[-__SHIFT:]+part[:-__SHIFT]
                if part:
                    result += part
                else:
                    with _io.BytesIO(result) as decrypted:
                        return _io.BytesIO(decrypted.read())
    for name in (filename, _os.path.join("StarSeeker", filename)):
        if _os.path.exists(name):
            return __open_file()
    else:
        print "File not found."
        return None


def __integration(directory, extensions, is_fast=False):
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
        with open(filepath, "r") as infile:
            body += infile.read()
    if is_fast:
        pack_fast(directory+(".enf"), meta+body)
    else:
        pack(directory+(".enc"), meta+body)


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
            unpack_fast if ext.upper() == ".ENF" else unpack)(filename)
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
    source_dir = _os.path.join("..", "material")
    __integration(_os.path.join(source_dir, "images"), "png")
    __integration(_os.path.join(source_dir, "bgm"), "ogg", is_fast=True)
    __integration(_os.path.join(source_dir, "se"), "wav", is_fast=True)
    print "finish."
