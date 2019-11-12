#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""counter.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

フレームカウンタモジュール。
"""
__counter = None


def init():
    u"""モジュール初期化。
    """
    global __counter
    __counter = __Counter(4, 6, 8, 16)


def forward():
    u"""カウントを進める。
    """
    return __counter.forward()


def get_frame(number):
    u"""フレーム取得。
    """
    return __counter.get_frame(number)


class __Counter(object):
    u"""フレームカウンタ。
    スプライトのフレームを同期する。
    """
    __slots__ = "__dict", "__frame", "__lcm"

    def __init__(self, *numbers):
        u"""コンストラクタ。
        """
        def _get_lcm(*numbers):
            u"""numbersの最小公倍数取得。
            """
            def __get_lcm(a, b):
                u"""a,bの最小公倍数取得。
                """
                import fractions as __fractions
                return a*b/__fractions.gcd(a, b)
            lcm = __get_lcm(numbers[0], numbers[1])
            for number in numbers[2:]:
                lcm = __get_lcm(number, lcm)
            return lcm
        self.__dict = {}
        self.__frame = 0
        self.__lcm = numbers[0] if len(numbers) == 1 else _get_lcm(*numbers)
        for num in numbers:
            self.__dict[num] = reduce(lambda x, y: x+y, (
                (i,)*(self.__lcm/num) for i in range(num)))

    def forward(self):
        u"""カウントを進める。
        """
        value = self.__frame+1
        self.__frame = value if value < self.__lcm else 0

    def get_frame(self, number):
        u"""フレーム取得。
        """
        return self.__dict[number][self.__frame]
