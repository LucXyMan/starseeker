#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""unit.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

ユニットモジュール。
"""
import pygame as __pygame


class Unit(__pygame.sprite.DirtySprite):
    u"""基本ユニット。
    """
    __POWER_UP_LIMIT = 4

    def __init__(self, pos, data, packet, group=None):
        u"""コンストラクタ。
        pos: スプライトの左上の位置。
        data: ユニットデータ。
        """
        import sprites.huds as __huds
        import sprites.shadow as __shadow
        super(Unit, self).__init__(
            (self.group, self.draw_group) if group is None else group)
        self._data = data
        self._packet = packet
        self._power = 0
        self.__animation = None
        self._effect = None
        self._is_right = False
        self.__power_ups = []
        self.image = self.current_image
        self.rect = self.image.get_rect()
        self.__dest = self.image.get_rect()
        self.__dest.topleft = self.rect.topleft = pos
        __huds.Charge(self)
        __shadow.Shadow(self)
        self.update()

    def __repr__(self):
        u"""文字列表現取得。
        """
        return (
            u"<type: {type}, name: {name}, level: {level}, "
            u"direction: {direction}>").format(
            type=self.__class__.__name__, name=self._data.name,
            level=self.level, direction="Right" if self._is_right else "Left")

    # ---- Charge ----
    def _get_power_up_charge(self, score):
        u"""パワーアップ適用後のチャージ値を取得。
        """
        return (score+(score >> 2)*self.speed_level)

    def _get_score(self, onepieces):
        u"""ブロックから得点を取得。
        """
        return sum(
            block.get_score() for
            block in reduce(lambda a, b: a+b, onepieces))

    def charge(self, onepieces):
        u"""パワーチャージ。
        消去したラインの得点をチャージ。
        """
        def __strengthen(charge, lines):
            u"""消去した行数の数によってパワーチャージを強化。
            """
            return int(charge*(
                4 if 7 <= lines else 3.5 if 6 <= lines else
                3 if 5 <= lines else 2.5 if 4 <= lines else
                2 if 3 <= lines else 1.5 if 2 <= lines else 1))
        self._power += __strengthen(
            self._get_power_up_charge(self._get_score(onepieces)),
            len(onepieces))

    def release(self):
        u"""パワーチャージ解放。
        """
        power, self._power = divmod(self._power, self._packet)
        return power

    # ---- Attack and Defense ----
    def _get_attack(self, str_, level, power):
        u"""攻撃力取得。
        """
        return (str_+(str_ >> 2)*level)*power

    def defense(self, stroke):
        u"""攻撃を受け止める。
        """
        if 0 < stroke:
            vit = self._vit
            _vit = vit+(vit >> 3)*self.defense_level
            _stroke = int(stroke-stroke*_vit*0.01)
            return 0 if _stroke < 0 else _stroke
        return 0

    # ---- Power Up ----
    def __get_attack(self):
        u"""攻撃パワーアップを取得。
        """
        return tuple(
            power_up for power_up in self.__power_ups if
            power_up.is_attack)

    def __get_defense(self):
        u"""防御パワーアップを取得。
        """
        return tuple(
            power_up for power_up in self.__power_ups if
            power_up.is_defense)

    def __get_speed(self):
        u"""スピードパワーアップを取得。
        """
        return tuple(
            power_up for power_up in self.__power_ups if
            power_up.is_speed)

    def enhance(self, type_, plus):
        u"""パワーアップ追加。
        """
        class __PowerUp(object):
            u"""パワーアップ。
            ユニット性能を強化する。
            """
            __slots__ = "__count", "__type"
            __PERIOD = 16

            def __init__(self, type_):
                u"""コンストラクタ。
                __type: パワーアップ種類。0は攻撃、1は防御、2はチャージ。
                """
                self.__type = type_
                self.__count = self.__PERIOD

            def __repr__(self):
                u"""文字列表現取得。
                """
                return u"<name:{name}, type:{type}>".format(
                    name=self.__class__.__name__, type=self.__type)

            def count_down(self):
                u"""カウントを進める。
                """
                self.__count -= 1

            # ---- Property ----
            @property
            def copy(self):
                u"""パワーアップコピー。
                """
                power_up = self.__class__(self.__type)
                power_up.__count = self.__count
                return power_up

            # ------ Type ------
            @property
            def is_attack(self):
                u"""パワーアップ種類が攻撃の場合真。
                """
                return self.__type == 0

            @property
            def is_defense(self):
                u"""パワーアップ種類が防御の場合真。
                """
                return self.__type == 1

            @property
            def is_speed(self):
                u"""パワーアップ種類がチャージの場合真。
                """
                return self.__type == 2

            # ------ Count ------
            @property
            def count(self):
                u"""カウントを取得。
                """
                return self.__count

            @property
            def is_over(self):
                u"""カウントが0以下の場合に真。
                """
                return self.__count <= 0
        self.__power_ups.extend([__PowerUp(type_)]*plus)
        getters = self.__get_attack, self.__get_defense, self.__get_speed
        getter = getters[type_]
        while self.__POWER_UP_LIMIT < len(getter()):
            self.__power_ups.remove(min(getter(), key=lambda x: x.count))

    def count_down(self):
        u"""パワーアップのカウントを進める。
        カウント0のパワーアップを除去。
        """
        if self.__power_ups:
            min(self.__power_ups, key=lambda x: x.count).count_down()
            self.__power_ups = [
                power_up for power_up in self.__power_ups if
                not power_up.is_over]

    # ---- Update ----
    def _update_finish(self):
        u"""終了時更新。
        """
    def update(self):
        u"""スプライト更新。
        """
        def __update_image():
            u"""画像更新。
            """
            if self.__animation:
                try:
                    self.image = self.__animation.next()
                except StopIteration:
                    self._update_finish()
                    self.__animation = None
            else:
                self.image = self.current_image

        def __move():
            u"""移動処理。
            """
            if self.rect.left < self.__dest.left:
                self.rect.move_ip((1, 0))
            elif self.__dest.left < self.rect.left:
                self.rect.move_ip((-1, 0))
            if self.rect.top < self.__dest.top:
                self.rect.move_ip((0, 1))
            elif self.__dest.top < self.rect.top:
                self.rect.move_ip((0, -1))
        __update_image()
        __move()

    def flash(self, type_=""):
        u"""フラッシュ開始。
        """
        import flash as __flash
        self.__animation = __flash.get(self, type_)

    # ---- Property ----
    @property
    def _vit(self):
        u"""ユニットの守りを取得。
        """
        return self._data.vit

    @property
    def data(self):
        u"""ユニット情報取得。
        """
        return self._data

    @property
    def number(self):
        u"""番号取得。
        """
        return self._data.number

    @property
    def state(self):
        u"""現在の状態文字列取得。
        """
        return u"Normal"

    # ------ Sprite ------
    @property
    def is_right(self):
        u"""スプライトの右向き判定。
        """
        return self._is_right

    @is_right.setter
    def is_right(self, value):
        u"""スプライトの右向き設定。
        """
        self._is_right = bool(value)
        self.image = self.current_image

    @property
    def dest(self):
        u"""スプライトの移動先rectを取得。
        """
        return self.__dest

    @property
    def layer_of_sprite(self):
        u"""現在レイヤーを取得。
        """
        return self.draw_group.get_layer_of_sprite(self)

    # ------ Charge ------
    @property
    def power(self):
        u"""パワーを取得。
        """
        return self._power

    @power.setter
    def power(self, value):
        u"""パワーを設定。
        """
        self._power = int(value)

    @property
    def packet(self):
        u"""攻撃に必要な値を取得。
        """
        return self._packet

    # ------ Power Up ------
    @property
    def power_ups(self):
        u"""パワーアップ取得。
        """
        return tuple(power_up.copy for power_up in self.__power_ups)

    @power_ups.setter
    def power_ups(self, value):
        u"""パワーアップ設定。
        """
        self.__power_ups = list(value)

    @property
    def attack_level(self):
        u"""攻撃LVを取得。
        """
        return len(self.__get_attack())

    @property
    def defense_level(self):
        u"""防御LVを取得。
        """
        return len(self.__get_defense())

    @property
    def speed_level(self):
        u"""スピードLVを取得。
        """
        return len(self.__get_speed())

    @property
    def level(self):
        u"""パワーアップLVを取得。
        """
        return self.attack_level, self.defense_level, self.speed_level

    # ------ State ------
    @property
    def is_dead(self):
        u"""ユニットの死亡判定。
        """
        return False

    @property
    def is_frozen(self):
        u"""凍結状態かどうかの判定。
        """
        return False
