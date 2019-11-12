#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""memoize.py

Copyright(c)2019 Yukio Kuro
This software is released under BSD license.

メモライズモジュール。
"""
__cache = {}


def __get_key(function, *args, **kw):
    u"""キャッシュキー取得。
    デフォルトで使用される。
    """
    return u"{method}##{args}##{kw}".format(
        method=u"{module}.{name}".format(
            module=function.__module__, name=function.__name__),
        args=tuple(unicode(arg) for arg in args), kw=tuple(
            u"{key}#{value}".format(key=k, value=hash(v)) for
            k, v in kw.items()))


def memoize(cache=__cache, get_key=__get_key):
    u"""関数の戻り値をキャッシュするデコレータ。
    """
    def _memoize(function):
        def __memoize(*args, **kw):
            key = get_key(function, *args, **kw)
            try:
                return cache[key]
            except KeyError:
                value = cache[key] = function(*args, **kw)
                return value
        return __memoize
    return _memoize


def clear():
    u"""キャッシュクリア。
    """
    __cache.clear()


def print_cache():
    u"""キャッシュ表示。
    """
    print len(__cache)
    for item in __cache:
        print item
