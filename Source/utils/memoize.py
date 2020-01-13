#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""memoize.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

メモライズモジュール。
"""
__cache = {}


def __get_key(function, *args, **kw):
    u"""デフォルトキャッシュキー取得。
    """
    return u"<{method}##{args}##{kw}".format(
        method=u"{module}.{name}>".format(
            module=function.__module__, name=function.__name__),
        args=tuple(unicode(arg) for arg in args), kw=tuple(
            u"{key}#{value}".format(key=k, value=hash(v)) for
            k, v in kw.items()))


def memoize(cache=__cache, get_key=__get_key):
    u"""メモ化デコレータ。
    """
    def _memoize(function):
        u"""デコレータ本体。
        """
        def __memoize(*args, **kw):
            u"""関数をラップ。
            """
            key = get_key(function, *args, **kw)
            try:
                return cache[key]
            except KeyError:
                cache[key] = function(*args, **kw)
                return cache[key]
        return __memoize
    return _memoize
