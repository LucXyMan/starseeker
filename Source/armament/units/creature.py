#!/usr/bin/env python2.7
# -*- coding:UTF-8 -*-2
u"""creature.py

Copyright (c) 2019 Yukio Kuro
This software is released under BSD license.

クリーチャーモジュール。
"""
import unit as __unit
import utils.const as _const
import utils.memoize as _memoize
import utils.image as _image
import sprites.effects as _effects


class Creature(__unit.Unit):
    u"""クリーチャー。
    プレイヤーの分身。
    """
    __POISON_RATE = 0.025
    __REGENERATION_RATE = 0.0125

    class _Explosion(_effects.effect.Effect):
        u"""クリーチャー撃破エフェクト。
        """
        __STAR_NUMBER = 8
        __STAR_SPEED = 3
        __star_vectors = ()

        def __init__(self, unit, groups=None):
            u"""コンストラクタ。
            """
            def __init_params():
                u"""爆発に必要なパラメータ設定。
                """
                import math as __math
                if not Creature._Explosion.__star_vectors:
                    angle = __math.pi*2/self.__STAR_NUMBER
                    Creature._Explosion.__star_vectors = tuple((
                        round(__math.cos(i*angle)*self.__STAR_SPEED),
                        round(__math.sin(i*angle)*self.__STAR_SPEED)) for
                        i in range(self.__STAR_NUMBER))
            self.__unit = unit
            self._images = self._generate(self.__STAR_NUMBER)
            __init_params()
            super(Creature._Explosion, self).__init__((0, 0), groups)

        def _generate(self, period):
            u"""エフェクト画像生成。
            """
            class _RainbowStar(_effects.image.Image):
                u"""虹色の星型。
                クリーチャー撃破時のエフェクトに使用。
                """
                __MOVE_PERIOD = 3

                def __init__(self, pos, number, direction, groups=None):
                    u"""コンストラクタ。
                    """
                    self.__counter = 0
                    super(_RainbowStar, self).__init__(
                        pos, "comet_"+str(number & 0x07), direction, groups)

                def _generate(self, sources, direction):
                    u"""エフェクト画像生成。
                    """
                    for image in self._get_images(sources):
                        for _ in range(_const.FRAME_DELAY):
                            yield image, (
                                direction if self.__counter <
                                self.__MOVE_PERIOD else (0, 0))
                        self.__counter += 1
            for i in range(period):
                yield _image.get_dummy(), (0, 0)
                _RainbowStar(
                    self.__unit.rect.center, i,
                    Creature._Explosion.__star_vectors[i])

    def __init__(self, pos, data, packet, group=None):
        u"""コンスタラクタ。
        """
        import sprites.huds as __huds
        self.__is_destroyed = False
        self.__is_poison = False
        self.__frozen_time = 0
        self.__life = self.__max_life = data.life
        super(Creature, self).__init__(pos, data, packet, group)
        if data.tribe == _const.BEAST_TRIBE:
            self.enhance(0, 1)
        elif data.tribe == _const.ALCHMIC_TRIBE:
            self.enhance(1, 1)
        elif data.tribe == _const.SKY_TRIBE:
            self.enhance(2, 1)
        __huds.Life(self)
        __huds.Freeze(self)

    def __repr__(self):
        u"""文字列表現取得。
        """
        return (
            u"<type: {type}, name: {name}, level: {level}, "
            u"direction: {direction}, state: {state}>").format(
            type=self.__class__.__name__, name=self._data.name,
            level=self.level,
            direction="Right" if self._is_right else "Left", state=self.state)

    # ---- Charge ----
    def charge(self, onepieces):
        u"""チャージ処理。
        消去したライン得点をチャージする。
        凍結状態の場合凍結ゲージが減少する。
        """
        if self.is_frozen:
            self.frozen_time -= self._get_power_up_charge(
                self._get_score(onepieces))
        else:
            super(Creature, self).charge(onepieces)

    # ---- Attack and Defense ----
    def attack(self):
        u"""攻撃処理。
        """
        if not self.is_frozen:
            lv = self._power/self._packet
            power = self.release()
            if 0 < power:
                self.flash()
                return self._get_attack(
                    self._data.str, self.attack_level, power), lv
        return 0, 0

    def receive(self, stroke):
        u"""攻撃受け取り処理。
        """
        self.life_with_effect -= stroke
        if self.__life < 0:
            return abs(self.__life)
        return 0

    # ---- Power Up ----
    def enhance(self, type_, plus):
        u"""パワーアップ追加。
        毒状態の時にパワーアップ無効。
        """
        if not self.is_poison or self.is_undead:
            super(Creature, self).enhance(type_, plus)

    # ---- Status Effect ----
    def poisoning(self):
        u"""毒効果。
        """
        self.__is_poison = False if self.is_frozen else True

    def freezing(self):
        u"""凍結効果。
        """
        self.__frozen_time = int(0 if self.__is_poison else self._packet << 2)

    def death(self, is_force=False):
        u"""即死効果。
        不死属性の場合無効。
        """
        if is_force or not self.is_undead:
            self.__life = 0
            return True
        return False

    def poison_effect(self):
        u"""毒効果処理。
        不死属性の場合回復する。
        """
        if self.is_undead:
            recovery = self.__life+int(self.__max_life*self.__POISON_RATE)
            self.__life = (
                recovery if recovery < self.__max_life else self.__max_life)
        else:
            self.__life -= int(self.__max_life*self.__POISON_RATE)

    def regenerate(self):
        u"""回復効果処理。
        """
        if self.is_regeneratable:
            recovery = self.__life+int(
                self.__max_life*self.__REGENERATION_RATE)
            self.__life = (
                recovery if recovery < self.__max_life else self.__max_life)

    # ---- Ability ----
    def get_enchant(self, level):
        u"""エンチャント効果取得。
        """
        ability = self._data.ability
        if ability:
            enchant = ability.enchant
            if level and not self.is_frozen and enchant:
                new, old = enchant.split("##")
                rank = self._data.rank
                return new, old.split("#"), (
                    (1, 1) if ability.is_single else
                    (level*rank, level*rank+1))
        return ()

    def get_persistence(self, turn):
        u"""持続効果取得。
        """
        ability = self._data.ability
        if ability:
            persistence = ability.persistence
            if (
                not self.is_frozen and persistence and
                turn & ability.interval == 0
            ):
                new, old = persistence.split("##")
                return new, old.split("#"), (1, 1)
        return ()

    # ---- Summon ----
    def adapt(self, target):
        u"""融合可能な場合、融合後クリーチャーを返す。
        そうでない場合Noneを返す。
        """
        return self._data.adapt(target)

    def copy_parameter(self, unit):
        u"""unitのパラメータを自身にコピーする。
        """
        self.__life = unit.__life
        self.__power_ups = unit.power_ups
        self.__is_poison = unit.__is_poison
        self.__frozen_time = unit.__frozen_time
        self._power = unit._power

    # ---- Update ----
    def _update_finish(self):
        u"""終了時更新。
        """
        if self.__is_destroyed:
            self.kill()

    def add_effect(self, effect):
        u"""エフェクト追加。
        文字表示エフェクトが存在する場合にkillする。
        """
        if self._effect and not self._effect.is_dead:
            self._effect.kill()
            self._effect = None
        self._effect = effect

    def destroy(self):
        u"""撃破処理。
        """
        import material.sound as __sound
        __sound.SE.play("shockwave")
        self._Explosion(self)
        self.flash("summon")
        self.__life = 0
        self.__is_destroyed = True

    # ---- Property ----
    @property
    def name(self):
        u"""名前取得。
        """
        return self._data.name

    @property
    def recepters(self):
        u"""受容可能クリーチャー名取得。
        """
        return self._data.recepters

    @property
    def state(self):
        u"""現在状態取得。
        """
        return (
            u"Poison" if self.is_poison else
            u"Freeze" if self.is_frozen else
            u"Normal")

    # ------ Image ------
    @property
    def base_image(self):
        u"""基本画像取得。
        """
        return self._data.get_image(False)

    @property
    @_memoize.memoize()
    def current_image(self):
        u"""現在画像取得。
        """
        image = self.data.get_image(self.is_right)
        if self.is_poison:
            image = _image.get_colored_ave(image, _const.GREEN)
        elif self.is_frozen:
            image = _image.get_colored_ave(image, _const.CYAN)
        return image

    # ------ Life ------
    @property
    def max_life(self):
        u"""最大ライフ取得。
        """
        return self.__max_life

    @property
    def life(self):
        u"""現在ライフ取得。
        """
        return self.__life

    @life.setter
    def life(self, value):
        u"""現在ライフ設定。
        """
        self.__life = value

    @life.setter
    def life_with_effect(self, value):
        u"""現在ライフをエフェクト付きで設定。
        """
        def __damage_display(damage):
            u"""ダメージ表示。
            """
            self.flash("damage")
            if damage:
                self.add_effect(
                    _effects.Damage(self.rect.center, str(damage)))

        def __recovery_display(recover):
            u"""回復表示。
            """
            self.flash("recovery")
            if recover:
                self.add_effect(
                    _effects.Recovery(self.rect.center, str(recover)))
        if self.__life < value and not self.is_undead:
            old_life = self.__life
            self.__life = value if value < self.__max_life else self.__max_life
            __recovery_display(self.__life-old_life)
            self.__is_poison = False
            self.__frozen_time = 0
        elif value < self.__life:
            __damage_display(self.__life-value)
            self.__life = value

    @property
    def is_half(self):
        u"""ライフ1/2判定。
        """
        return self.__life <= self.__max_life >> 1

    @property
    def is_quarter(self):
        u"""ライフ1/4判定。
        """
        return self.__life <= self.__max_life >> 2

    @property
    def is_dead(self):
        u"""ユニット死亡判定。
        """
        return self.__life <= 0

    @property
    def is_alive(self):
        u"""ユニット生存判定。
        """
        return not self.is_dead

    @property
    def healing_priority(self):
        u"""回復優先度取得。
        """
        return float(self.__max_life)/float(self.__life)*(
            2 if self.is_poison or self.is_frozen else 1)

    # ------ Status ------
    @property
    def str(self):
        u"""クリーチャーの力。
        """
        return self._data.str

    @property
    def vit(self):
        u"""クリーチャーの生命力。
        """
        return self._vit

    @property
    def is_poison(self):
        u"""毒状態取得。
        """
        return self.__is_poison

    @property
    def frozen_time(self):
        u"""凍結時間取得。
        """
        return self.__frozen_time

    @frozen_time.setter
    def frozen_time(self, value):
        u"""凍結時間設定。
        """
        self.__frozen_time = 0 if value < 0 else int(value)

    @property
    def is_frozen(self):
        u"""凍結状態判定。
        """
        return 0 < self.__frozen_time

    @property
    def is_healths(self):
        u"""クリーチャーの健康体判定。
        """
        return not self.__is_poison and not self.is_frozen

    @property
    def is_regeneratable(self):
        u"""自己再生効果の使用可能判定。
        """
        return (
            self._data.tribe == _const.DRAGON_TRIBE and
            not self.is_poison and not self.is_frozen)

    @property
    def is_undead(self):
        u"""不死属性判定。
        """
        return self._data.tribe == _const.UNDEAD_TRIBE

    # ------ Ability ------
    @property
    def prevents(self):
        u"""防止する変化を取得。
        """
        ability = self._data.ability
        if ability:
            prevention = ability.prevention
            if not self.is_frozen and prevention:
                return prevention.split("#")
        return ()

    @property
    def skills(self):
        u"""スキル取得。
        """
        ability = self._data.ability
        return ability.skills if ability and not self.is_frozen else ""
