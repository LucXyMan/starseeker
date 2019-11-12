#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""bitflag.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

ビットフラグモジュール。
"""
_WORD = 0x20


class _BitFlag(object):
    u"""ビットフラグ基礎。
    """
    __slots__ = "_array", "_i",

    def __init__(self):
        u"""コンストラクタ。
        """
        self._i = 0

    def __iter__(self):
        u"""イテレータ。
        """
        return self

    def __repr__(self):
        u"""文字列表現取得。
        """
        return self._array.__repr__()

    @property
    def raw(self):
        u"""実数値を取得。
        """
        return self._array[:]

    @property
    def bits(self):
        u"""真ビット数取得。
        """
        import utils.calc as __calc
        return sum(__calc.get_number_of_bit(bits) for bits in self._array)


class BitFlag(_BitFlag):
    u"""ビットフラグ。
    数値1個につき32個のフラグを設定できる。
    """
    __slots__ = ()

    def __init__(self, item):
        u"""整数の配列からビットフラグを作る。
        """
        super(BitFlag, self).__init__()
        self._array = list(item)

    def __len__(self):
        u"""要素数の取得。
        """
        return len(self._array)*_WORD

    def next(self):
        u"""イテレータ処理。
        """
        if len(self) <= self._i:
            self._i = 0
            raise StopIteration()
        result = self.has(self._i)
        self._i += 1
        return result

    def has(self, number):
        u"""番号numberのON/OFFを調べる。
        """
        index, number = divmod(number, _WORD)
        return bool(self._array[index] & 0x01 << number)

    def on(self, number):
        u"""番号numberのアイテムの入手フラグをON。
        """
        index, number = divmod(number, _WORD)
        self._array[index] |= 0x01 << number

    def off(self, number):
        u"""番号numberのアイテムの入手フラグをOFF。
        """
        index, number = divmod(number, _WORD)
        self._array[index] &= 0x01 << number ^ 0xFFFFFFFF

    @property
    def slot(self):
        u"""設定可能なスロット数を取得。
        """
        return len(self._array)*_WORD


class _BitNumber(_BitFlag):
    u"""ビットナンバーフラグ。
    1以上の数値を設定できる。
    """
    __slots__ = ()

    def __init__(self, item):
        u"""コンストラクタ。
        """
        super(_BitNumber, self).__init__()
        self._array = list(item)

    def __len__(self):
        u"""要素数の取得。
        """
        return len(self._array)*self._DVSN

    def next(self):
        u"""イテレータ処理。
        """
        if len(self) <= self._i:
            self._i = 0
            raise StopIteration()
        result = self.get(self._i)
        self._i += 1
        return result

    def get(self, number):
        u"""値の取得。
        """
        index, pos = divmod(number, self._DVSN)
        part = _WORD/self._DVSN
        shift = pos*part
        mask = self._SIZE
        value = self._array[index] >> shift
        value &= mask
        return value

    def set(self, number, value):
        u"""値の設定。
        """
        index, pos = divmod(number, self._DVSN)
        part = _WORD/self._DVSN
        shift = pos*part
        mask = 0xFFFFFFFF ^ self._SIZE << shift
        self._array[index] &= mask
        self._array[index] |= (
            0x00 if value < 0x00 else self._SIZE if self._SIZE < value else
            value) << shift

    @property
    def slot(self):
        u"""設定可能なスロット数を取得。
        """
        return len(self._array)*self._DVSN

    @property
    def size(self):
        u"""スロットサイズ取得。
        """
        return self._SIZE


class TwoBitNumber(_BitNumber):
    u"""ツービットフラグ。
    数値1個につき3までの値を16個設定できる。
    """
    __slots__ = ()
    _DVSN = 0x10
    _SIZE = 0x3


class NibbleNumber(_BitNumber):
    u"""ニブルフラグ。
    数値1個につき15までの値を8個設定できる。
    """
    __slots__ = ()
    _DVSN = 0x08
    _SIZE = 0x0F


class ByteNumber(_BitNumber):
    u"""バイトフラグ。
    数値１個につき255までの値を4個設定できる。
    """
    __slots__ = ()
    _DVSN = 0x04
    _SIZE = 0xFF


class WordNumber(_BitNumber):
    u"""ワードフラグ。
    数値１個につき65535までの値2個を設定できる。
    """
    __slots__ = ()
    _DVSN = 0x02
    _SIZE = 0xFFFF


if __name__ == '__main__':
    for i, item in enumerate(BitFlag((
        0xFFFFFFFF, 0xFFFFFFFF))
    ):
        print i, ":", item
    print "========"
    for i, item in enumerate(TwoBitNumber((
        0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF))
    ):
        print i, ":", item
