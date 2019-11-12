#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""string.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

文字列エフェクトモジュール。
"""
import material.sound as _sound
import material.string as _string
import utils.const as _const
import utils.image as _image
import utils.layouter as _layouter
import effect as _effect


class _String(_effect.Effect):
    u"""基本文字列エフェクト。
    """
    _CHAR_SIZE = _const.EFFECT_CHAR_SIZE
    _VECTOR = 0, 0

    class _Form(object):
        u"""エフェクト生成パラメータ。
        """
        __slots__ = "__color", "__period", "__string"

        def __init__(self, string, color, period):
            u"""コンストラクタ。
            """
            self.__string = unicode(string)
            self.__color = _string.CharColor(color)
            self.__period = int(period)

        @property
        def string(self):
            u"""文字列取得。
            """
            return self.__string

        @property
        def color(self):
            u"""色取得。
            """
            return self.__color

        @property
        def period(self):
            u"""効果時間取得。
            """
            return self.__period

    def __init__(self, pos, form, groups=None):
        u"""コンストラクタ。
        """
        self._images = self._generator(form)
        super(_String, self).__init__(pos, groups)

    def _flash_generator(self, image, period):
        u"""点滅画像取得。
        """
        return (
            image if i & 0b11 == 0 else
            _image.get_clear(image) for i in range(period))

    def _get_init_params(self, form):
        u"""初期パラメータ取得。
        """
        def __get_init_images():
            u"""初期画像取得。
            """
            return (_string.get_string(
                form.string[:i], self._CHAR_SIZE, form.color) for
                i in range(1, len(form.string)+1))
        return tuple(
            [(image, (0, 0)) for image in __get_init_images()] +
            [(image, (0, 0)) for _ in range(form.period)])

    def _generator(self, form):
        u"""文字列画像ジェネレータ。
        """
        for image, vector in self._get_init_params(form):
            yield image, vector
        for image in self._flash_generator(image, form.period):
            yield image, self._VECTOR


# ---- Number ----
class _Number(_String):
    u"""戦闘数値表示。
    """
    _VECTOR = 0, 0

    def __init__(self, pos, string, groups=None):
        u"""コンストラクタ。
        """
        super(_Number, self).__init__(pos, self._Form(
            string, self._COLOR, _const.FRAME_RATE >> 1), groups)


class Damage(_Number):
    u"""ダメージ数値表示。
    """
    _COLOR = _const.RED+"#"+_const.YELLOW+"#"+_const.DARK_RED


class Recovery(_Number):
    u"""回復数値表示。
    """
    _COLOR = _const.BLUE+"#"+_const.CYAN+"#"+_const.DARK_BLUE


# ---- Activate ----
class _Activate(_String):
    u"""発動エフェクト。
    """
    def __init__(self, pos, string, color, groups):
        u"""コンストラクタ。
        """
        super(_Activate, self).__init__(pos, self._Form(
            string, color, _const.FRAME_RATE), groups)
        self._sub = []

    def eliminate(self):
        u"""自身とサブスプライトをグループから削除。
        """
        super(_Activate, self).kill()
        for sprite in self._sub:
            sprite.kill()

    def _generator(self, form):
        u"""文字列画像ジェネレータ。
        """
        class __Char(_String):
            u"""文字エフェクト。
            """
            _VECTOR = 0, -1
        import random as __random
        for image, vector in self._get_init_params(form):
            yield image, vector
        x, y = self.rect.midleft
        numbers = range(1, len(form.string)+1)
        __random.shuffle(numbers)
        for number, char in zip(numbers, form.string):
            effect = __Char((0, 0), self._Form(
                char, form.color.string, number*(form.period >> 1) >> 3))
            effect.rect.midleft = x, y
            x += effect.rect.width
            self._sub.append(effect)
        yield _image.get_clear(image), (0, 0)

    @property
    def is_dead(self):
        u"""エフェクト終了時に真。
        """
        return not self._images and all(s.is_dead for s in self._sub)


class Special(_Activate):
    u"""特殊エフェクト。
    """
    def __init__(self, pos, string, groups=None):
        u"""コンストラクタ。
        """
        color = _const.WHITE+"#"+_const.CYAN+"#"+_const.GRAY
        super(Special, self).__init__(pos, string, color, groups)


class Spell(_Activate):
    u"""呪文エフェクト。
    """
    def __init__(self, pos, item, is_reverse=False, groups=None):
        u"""コンストラクタ。
        """
        _sound.SE.play("spell_"+(
            "2" if item.type == _const.ALTERED_ARCANUM else "1"))
        colors = {
            _const.SUMMON_ARCANUM:
            (_const.YELLOW, _const.ORANGE, _const.DARK_YELLOW),
            _const.FUSIONED_ARCANUM:
            (_const.RED, _const.ORANGE, _const.DARK_RED),
            _const.SORCERY_ARCANUM:
            (_const.VIRIDIAN, _const.GREEN, _const.DARK_VIRIDIAN),
            _const.ALTERED_ARCANUM:
            (_const.BLUE, _const.CYAN, _const.DARK_BLUE),
            _const.SHIELD_ARCANUM:
            (_const.PURPLE, _const.MAGENTA, _const.DARK_MAGENTA),
            _const.JOKER_ARCANUM:
            (_const.GRAY, _const.BLUE, _const.DARK_BLUE)}
        start, end, back = colors[item.type]
        super(Spell, self).__init__(
            pos, item.name[::-1] if bool(is_reverse) else item.name,
            start+"#"+end+"#"+back, groups)


class Shred(_Activate):
    u"""削除エフェクト。
    """
    def __init__(self, pos, item, groups=None):
        u"""コンストラクタ。
        """
        color = _const.GRAY+"#"+_const.RED+"#"+_const.DARK_RED
        super(Shred, self).__init__(pos, item.name, color, groups)

    def _generator(self, form):
        u"""文字列画像ジェネレータ。
        """
        class __Cross(_String):
            u"""交差文字エフェクト。
            上下に交差する文字。
            """
            def __init__(self, pos, form, up, groups=None):
                u"""コンストラクタ。
                """
                self._images = self._generator(form, bool(up))
                _effect.Effect.__init__(self, pos, groups)

            def _generator(self, form, up):
                u"""文字列画像ジェネレータ。
                upが偶数の場合に上に、奇数で下がる。
                """
                for image, vector in self._get_init_params(form):
                    yield image, vector
                clear = _image.get_clear(image)
                for i in range(form.period):
                    yield (
                        image if i & 0b11 == 0 else clear,
                        (0, -1 if up & 0b1 == 0 else 1))
        for image, vector in self._get_init_params(form):
            yield image, vector
        _sound.SE.play("shred")
        x, y = self.rect.midleft
        for up, char in zip((
            False if i & 0b1 == 0 else
            True for i in range(len(form.string))), form.string
        ):
            effect = __Cross((0, 0), self._Form(
                char, form.color.string, form.period >> 1), up)
            effect.rect.midleft = x, y
            x += effect.rect.width
            self._sub.append(effect)
        yield _image.get_clear(image), (0, 0)


# ---- Start ----
class __Start(_String):
    u"""ゲーム開始エフェクト。
    """
    _DOT_LENGTH = 3
    _CHAR_SIZE = _const.MODE_CHAR_SIZE

    def _start_generator(self, first, last, form):
        u"""スタート文字列部分を作成する。
        """
        for i in range(self._DOT_LENGTH+1):
            string = (first + u"."*i).ljust(len(first)+self._DOT_LENGTH)
            for _ in range(form.period):
                yield _string.get_string(
                    string, self._CHAR_SIZE, form.color), (0, 0)
        for i in range(1, len(last)+1):
            yield _string.get_string(
                last[:i], self._CHAR_SIZE, form.color), (0, 0)
        for _ in range(form.period):
            image = _string.get_string(
                last, self._CHAR_SIZE, form.color)
            yield image, (0, 0)
        for image in self._flash_generator(image, form.period):
            yield image, (0, 0)


class Rival(__Start):
    u"""対戦相手名エフェクト。
    """
    __BASE_TEXT = "VS:#Start!"
    __NAMES = {
        _const.ALTAIR_NAME: "Altair", _const.CORVUS_NAME: "Corvus",
        _const.NOVA_NAME: "Nova", _const.SIRIUS_NAME: "Sirius",
        _const.CASTOR_NAME: "Castor", _const.PLUTO_NAME: "Pluto",
        _const.REGULUS_NAME: "Regulus", _const.LUCIFER_NAME: "Lucifer",
        _const.NEBULA_NAME: "Nebula"}

    def __init__(self, name, groups=None):
        u"""コンストラクタ。
        """
        color = _const.CYAN+"#"+_const.YELLOW+"#"+_const.DARK_CYAN
        super(Rival, self).__init__((0, 0), self._Form(
            self.__NAMES[name], color, _const.FRAME_RATE), groups)
        _layouter.Game.set_center(self)

    def _generator(self, form):
        u"""文字列画像ジェネレータ。
        """
        first, last = self.__BASE_TEXT.split("#")
        first += form.string
        for i in range(1, len(first)+1):
            yield (_string.get_string(
                first[:i].ljust(len(first)+self._DOT_LENGTH),
                self._CHAR_SIZE, form.color), (0, 0))
        for image in self._start_generator(first, last, form):
            yield image


class Progress(__Start):
    u"""進行状態エフェクト。
    """
    def __init__(self, value, groups=None):
        u"""コンストラクタ。
        """
        color = _const.GREEN+"#"+_const.YELLOW+"#"+_const.DARK_GREEN
        super(Progress, self).__init__((0, 0), self._Form(
            value, color, _const.FRAME_RATE), groups)
        _layouter.Game.set_center(self)

    def _generator(self, form):
        u"""文字列画像ジェネレータ。
        """
        first = "Level:"
        first += (
            form.string if int(form.string) < _const.ENDLESS_LIMIT else "??")
        for i in range(1, len(first)+1):
            yield (_string.get_string(
                first[:i].ljust(len(first)+self._DOT_LENGTH),
                self._CHAR_SIZE, form.color), (0, 0))
        for image in self._start_generator(first, "Start!", form):
            yield image


# ---- Result----
class _Result(_String):
    u"""結果エフェクト。
    """
    _CHAR_SIZE = _const.MODE_CHAR_SIZE

    def __init__(self, pos, string, color, groups=None):
        u"""コンストラクタ。
        """
        super(_Result, self).__init__(pos, self._Form(
            string, color, _const.FRAME_RATE << 1), groups)

    def _generator(self, form):
        u"""文字列画像ジェネレータ。
        """
        for image, vector in self._get_init_params(form):
            yield image, vector
        clear = _image.get_clear(image)
        for i in range(form.period >> 1):
            yield image if i & 0b11 == 0 else clear, (0, 0)


class Win(_Result):
    u"""勝利エフェクト。
    """
    def __init__(self, pos, groups=None):
        u"""コンストラクタ。
        """
        color = _const.RED+"#"+_const.YELLOW+"#"+_const.DARK_RED
        super(Win, self).__init__(pos, "Win", color, groups)


class Lose(_Result):
    u"""敗北エフェクト。
    """
    def __init__(self, pos, groups=None):
        u"""コンストラクタ。
        """
        color = _const.BLUE+"#"+_const.CYAN+"#"+_const.DARK_BLUE
        super(Lose, self).__init__(pos, "Lose", color, groups)


class Draw(_Result):
    u"""引き分けエフェクト。
    """
    def __init__(self, pos, groups=None):
        u"""コンストラクタ。
        """
        color = _const.RED+"#"+_const.BLUE+"#"+_const.DARK_MAGENTA
        super(Draw, self).__init__(pos, "Draw", color, groups)


class Bonus(_Result):
    u"""ボーナスエフェクト。
    """
    def __init__(self, pos, sp, groups=None):
        u"""コンストラクタ。
        """
        color = _const.ORANGE+"#"+_const.YELLOW+"#"+_const.DARK_ORANGE
        super(Bonus, self).__init__(
            pos, "Bonus:"+str(sp) if 0 < sp else "Not Bonus", color, groups)
